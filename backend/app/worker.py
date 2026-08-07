import asyncio

from pydantic_ai.durable_exec.temporal import PydanticAIPlugin
from temporalio.client import Client
from temporalio.worker import Worker

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.db.session import Database
from app.workflows.activities import TenderActivities
from app.workflows.definition import TenderAnalysisWorkflow


async def run_worker() -> None:
    settings = get_settings()
    configure_logging(settings)
    logger = get_logger("temporal_worker")
    database = Database(settings.database_url)
    client = await Client.connect(
        settings.temporal_address,
        namespace=settings.temporal_namespace,
        plugins=[PydanticAIPlugin()],
    )
    activities = TenderActivities(database)
    logger.info(
        "worker_starting",
        status="STARTING",
        workflow_id=None,
        tender_id=None,
        correlation_id=None,
        request_id=None,
        error_class=None,
        task_queue=settings.temporal_task_queue,
    )
    try:
        async with Worker(
            client,
            task_queue=settings.temporal_task_queue,
            workflows=[TenderAnalysisWorkflow],
            activities=[
                activities.mark_running,
                activities.load_context,
                activities.persist_analysis,
                activities.persist_failure,
            ],
        ):
            await asyncio.Event().wait()
    finally:
        await database.dispose()


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
