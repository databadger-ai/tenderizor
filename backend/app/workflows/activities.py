from hashlib import sha256

from temporalio import activity

from app.core.errors import ConflictError
from app.db.repositories import get_analysis_run, get_tender, set_run_status, validate_citations
from app.db.session import Database
from app.domain.schemas import RunStatus
from app.workflows.contracts import (
    MarkRunningInput,
    PersistAnalysisInput,
    PersistFailureInput,
    TenderAnalysisContext,
    TenderWorkflowInput,
)


class TenderActivities:
    def __init__(self, database: Database) -> None:
        self.database = database

    @activity.defn(name="mark_analysis_running")
    async def mark_running(self, payload: MarkRunningInput) -> None:
        async with self.database.session_factory() as session:
            await set_run_status(
                session, payload.run_id, RunStatus.RUNNING, correlation_id=payload.correlation_id
            )

    @activity.defn(name="load_tender_analysis_context")
    async def load_context(self, payload: TenderWorkflowInput) -> TenderAnalysisContext:
        async with self.database.session_factory() as session:
            run = await get_analysis_run(session, payload.run_id)
            if run.tender_id != payload.tender_id or run.workflow_id != payload.workflow_id:
                raise ConflictError("workflow input does not match persisted analysis run")
            tender = await get_tender(session, payload.tender_id)
            digest = sha256(tender.source_text.encode("utf-8")).hexdigest()
            if digest != tender.source_sha256:
                raise ConflictError("persisted tender evidence hash mismatch")
            return TenderAnalysisContext(
                tender_id=tender.id,
                run_id=run.id,
                title=tender.title,
                source_text=tender.source_text,
                source_sha256=tender.source_sha256,
            )

    @activity.defn(name="persist_tender_analysis")
    async def persist_analysis(self, payload: PersistAnalysisInput) -> None:
        async with self.database.session_factory() as session:
            run = await get_analysis_run(session, payload.run_id)
            tender = await get_tender(session, run.tender_id)
            validate_citations(tender.source_text, payload.analysis)
            await set_run_status(
                session,
                run.id,
                RunStatus.SUCCEEDED,
                correlation_id=payload.correlation_id,
                analysis=payload.analysis,
            )

    @activity.defn(name="persist_tender_analysis_failure")
    async def persist_failure(self, payload: PersistFailureInput) -> None:
        async with self.database.session_factory() as session:
            await set_run_status(
                session,
                payload.run_id,
                RunStatus.FAILED,
                correlation_id=payload.correlation_id,
                error_code=payload.error_code,
            )
