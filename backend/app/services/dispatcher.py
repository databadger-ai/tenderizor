import asyncio
from typing import Protocol

from pydantic_ai.durable_exec.temporal import PydanticAIPlugin
from temporalio.client import Client

from app.core.config import Settings
from app.core.logging import get_logger
from app.db.repositories import get_analysis_run, get_tender, set_run_status, validate_citations
from app.db.session import Database
from app.domain.policy import apply_hard_gate
from app.domain.schemas import RunStatus
from app.services.analyzer import DeterministicFakeAnalyzer
from app.workflows.contracts import TenderWorkflowInput
from app.workflows.definition import TenderAnalysisWorkflow

logger = get_logger("dispatcher")


class AnalysisDispatcher(Protocol):
    async def start(self, payload: TenderWorkflowInput) -> None: ...

    async def check(self) -> None: ...

    async def close(self) -> None: ...


class TemporalAnalysisDispatcher:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client: Client | None = None
        self._lock = asyncio.Lock()

    async def _get_client(self) -> Client:
        if self._client is None:
            async with self._lock:
                if self._client is None:
                    self._client = await Client.connect(
                        self.settings.temporal_address,
                        namespace=self.settings.temporal_namespace,
                        plugins=[PydanticAIPlugin()],
                    )
        return self._client

    async def start(self, payload: TenderWorkflowInput) -> None:
        client = await self._get_client()
        await client.start_workflow(
            TenderAnalysisWorkflow.run,
            payload,
            id=payload.workflow_id,
            task_queue=self.settings.temporal_task_queue,
        )

    async def check(self) -> None:
        client = await self._get_client()
        await client.service_client.check_health()

    async def close(self) -> None:
        return None


class FakeAnalysisDispatcher:
    """Schedules deterministic in-process work after the HTTP command returns."""

    def __init__(self, database: Database) -> None:
        self.database = database
        self.analyzer = DeterministicFakeAnalyzer()
        self._tasks: set[asyncio.Task[None]] = set()

    async def start(self, payload: TenderWorkflowInput) -> None:
        task = asyncio.create_task(self._run(payload), name=f"fake-analysis-{payload.run_id}")
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        await asyncio.sleep(0)

    async def _run(self, payload: TenderWorkflowInput) -> None:
        try:
            async with self.database.session_factory() as session:
                await set_run_status(
                    session,
                    payload.run_id,
                    RunStatus.RUNNING,
                    correlation_id=payload.correlation_id,
                )
            await asyncio.sleep(0)
            async with self.database.session_factory() as session:
                run = await get_analysis_run(session, payload.run_id)
                tender = await get_tender(session, run.tender_id)
                draft = await self.analyzer.analyze(tender.title, tender.source_text)
                validate_citations(tender.source_text, draft)
                analysis = apply_hard_gate(draft)
                await set_run_status(
                    session,
                    run.id,
                    RunStatus.SUCCEEDED,
                    correlation_id=payload.correlation_id,
                    analysis=analysis,
                )
        except Exception as exc:
            logger.exception(
                "fake_analysis_failed",
                workflow_id=payload.workflow_id,
                tender_id=str(payload.tender_id),
                correlation_id=payload.correlation_id,
                status="FAILED",
                error_class=type(exc).__name__,
            )
            async with self.database.session_factory() as session:
                await set_run_status(
                    session,
                    payload.run_id,
                    RunStatus.FAILED,
                    correlation_id=payload.correlation_id,
                    error_code=type(exc).__name__,
                )

    async def check(self) -> None:
        return None

    async def close(self) -> None:
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
