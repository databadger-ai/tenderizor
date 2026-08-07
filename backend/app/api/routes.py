import asyncio
from collections.abc import Awaitable, Callable
from typing import Annotated
from uuid import UUID, uuid4

import structlog
from fastapi import APIRouter, Header, Request, Response, status

from app.api.dependencies import DispatcherDependency, SessionDependency
from app.core.errors import DependencyUnavailableError, PayloadTooLargeError
from app.core.logging import get_logger
from app.db.models import AnalysisRun, AuditEvent, Tender
from app.db.repositories import (
    append_correction,
    create_analysis_run,
    create_tender,
    get_analysis_run,
    get_latest_analysis_run,
    get_tender,
    list_activity,
    list_tenders,
    set_run_status,
)
from app.domain.schemas import (
    ActivityList,
    AnalysisResult,
    AnalysisRunAccepted,
    AnalysisRunCreate,
    AnalysisRunDetail,
    AuditAction,
    AuditEventView,
    CorrectionCreate,
    DependencyStatus,
    HealthResponse,
    ReadinessResponse,
    RunStatus,
    TenderCreate,
    TenderDetail,
    TenderList,
    TenderSummary,
)
from app.workflows.contracts import TenderWorkflowInput

logger = get_logger("api")
router = APIRouter()


def _tender_summary(tender: Tender, latest_run: AnalysisRun | None = None) -> TenderSummary:
    latest_analysis = (
        AnalysisResult.model_validate(latest_run.analysis)
        if latest_run is not None and latest_run.analysis is not None
        else None
    )
    return TenderSummary(
        id=tender.id,
        title=tender.title,
        buyer=tender.buyer,
        deadline=tender.deadline,
        reference_number=tender.reference_number,
        solicitation_number=tender.solicitation_number,
        source_sha256=tender.source_sha256,
        line_count=len(tender.source_text.splitlines()) or 1,
        latest_run_id=latest_run.id if latest_run is not None else None,
        latest_run_status=RunStatus(latest_run.status) if latest_run is not None else None,
        recommendation=latest_analysis.recommendation if latest_analysis is not None else None,
        gate_outcome=latest_analysis.gate_outcome if latest_analysis is not None else None,
        created_at=tender.created_at,
        updated_at=tender.updated_at,
    )


def _tender_detail(tender: Tender, latest_run: AnalysisRun | None = None) -> TenderDetail:
    return TenderDetail(
        **_tender_summary(tender, latest_run).model_dump(), source_text=tender.source_text
    )


def _run_detail(run: AnalysisRun) -> AnalysisRunDetail:
    analysis = AnalysisResult.model_validate(run.analysis) if run.analysis is not None else None
    return AnalysisRunDetail(
        run_id=run.id,
        tender_id=run.tender_id,
        workflow_id=run.workflow_id,
        status=RunStatus(run.status),
        analysis=analysis,
        error_code=run.error_code,
        created_at=run.created_at,
        updated_at=run.updated_at,
        completed_at=run.completed_at,
    )


def _audit_view(event: AuditEvent) -> AuditEventView:
    return AuditEventView(
        id=event.id,
        tender_id=event.tender_id,
        analysis_run_id=event.analysis_run_id,
        action=AuditAction(event.action),
        actor_id=event.actor_id,
        reason=event.reason,
        field_path=event.field_path,
        previous_value=event.previous_value,
        corrected_value=event.corrected_value,
        correlation_id=event.correlation_id,
        occurred_at=event.occurred_at,
    )


@router.get("/health", response_model=HealthResponse, tags=["operations"])
@router.get("/health/live", response_model=HealthResponse, tags=["operations"])
async def health(request: Request) -> HealthResponse:
    return HealthResponse(status="ok", service=request.app.state.settings.service_name)


async def _dependency_check(
    name: str, check: Callable[[], Awaitable[None]]
) -> DependencyStatus:
    try:
        await check()
        return DependencyStatus(status="ready")
    except Exception as exc:
        logger.exception(
            "readiness_check_failed",
            dependency=name,
            status="NOT_READY",
            error_class=type(exc).__name__,
        )
        return DependencyStatus(status="not_ready", error_class=type(exc).__name__)


@router.get("/ready", response_model=ReadinessResponse, tags=["operations"])
@router.get("/health/ready", response_model=ReadinessResponse, tags=["operations"])
async def readiness(request: Request, response: Response) -> ReadinessResponse:
    database, temporal = await asyncio.gather(
        _dependency_check("database", request.app.state.database.check),
        _dependency_check("temporal", request.app.state.dispatcher.check),
    )
    ready = database.status == "ready" and temporal.status == "ready"
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadinessResponse(
        status="ready" if ready else "not_ready", database=database, temporal=temporal
    )


@router.post(
    "/api/v1/tenders",
    response_model=TenderDetail,
    status_code=status.HTTP_201_CREATED,
    tags=["tenders"],
)
async def create_tender_endpoint(
    payload: TenderCreate,
    request: Request,
    session: SessionDependency,
    actor_id: Annotated[str, Header(alias="X-Actor-ID")] = "phase0-user",
) -> TenderDetail:
    if len(payload.source_text) > request.app.state.settings.max_source_text_chars:
        raise PayloadTooLargeError("source_text exceeds configured maximum")
    tender = await create_tender(
        session,
        payload,
        actor_id=actor_id,
        correlation_id=request.state.correlation_id,
    )
    structlog.contextvars.bind_contextvars(tender_id=str(tender.id), status="CREATED")
    return _tender_detail(tender)


@router.get("/api/v1/tenders", response_model=TenderList, tags=["tenders"])
async def list_tenders_endpoint(
    session: SessionDependency,
) -> TenderList:
    items, total = await list_tenders(session)
    return TenderList(
        items=[_tender_summary(tender, latest_run) for tender, latest_run in items],
        total=total,
    )


@router.get("/api/v1/tenders/{tender_id}", response_model=TenderDetail, tags=["tenders"])
async def get_tender_endpoint(
    tender_id: UUID,
    session: SessionDependency,
) -> TenderDetail:
    tender = await get_tender(session, tender_id)
    latest_run = await get_latest_analysis_run(session, tender_id)
    structlog.contextvars.bind_contextvars(tender_id=str(tender.id))
    return _tender_detail(tender, latest_run)


@router.post(
    "/api/v1/tenders/{tender_id}/analysis-runs",
    response_model=AnalysisRunAccepted,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["analysis"],
)
async def start_analysis_endpoint(
    tender_id: UUID,
    payload: AnalysisRunCreate,
    request: Request,
    session: SessionDependency,
    dispatcher: DispatcherDependency,
) -> AnalysisRunAccepted:
    workflow_id = f"tender-analysis-{uuid4()}"
    run = await create_analysis_run(
        session,
        tender_id=tender_id,
        workflow_id=workflow_id,
        requested_by=payload.requested_by,
        correlation_id=request.state.correlation_id,
    )
    structlog.contextvars.bind_contextvars(
        tender_id=str(tender_id), workflow_id=workflow_id, status=RunStatus.QUEUED.value
    )
    workflow_input = TenderWorkflowInput(
        tender_id=tender_id,
        run_id=run.id,
        workflow_id=workflow_id,
        correlation_id=request.state.correlation_id,
    )
    try:
        await dispatcher.start(workflow_input)
    except Exception as exc:
        await set_run_status(
            session,
            run.id,
            RunStatus.FAILED,
            correlation_id=request.state.correlation_id,
            error_code=type(exc).__name__,
        )
        raise DependencyUnavailableError("analysis workflow could not be started") from exc
    return AnalysisRunAccepted(
        run_id=run.id, workflow_id=workflow_id, status=RunStatus.QUEUED
    )


@router.get(
    "/api/v1/analysis-runs/{run_id}", response_model=AnalysisRunDetail, tags=["analysis"]
)
async def get_analysis_endpoint(
    run_id: UUID,
    session: SessionDependency,
) -> AnalysisRunDetail:
    run = await get_analysis_run(session, run_id)
    structlog.contextvars.bind_contextvars(
        tender_id=str(run.tender_id), workflow_id=run.workflow_id, status=run.status
    )
    return _run_detail(run)


@router.post(
    "/api/v1/tenders/{tender_id}/corrections",
    response_model=AuditEventView,
    status_code=status.HTTP_201_CREATED,
    tags=["audit"],
)
async def create_correction_endpoint(
    tender_id: UUID,
    payload: CorrectionCreate,
    request: Request,
    session: SessionDependency,
) -> AuditEventView:
    event = await append_correction(
        session, tender_id, payload, correlation_id=request.state.correlation_id
    )
    structlog.contextvars.bind_contextvars(tender_id=str(tender_id), status="APPENDED")
    return _audit_view(event)


@router.get(
    "/api/v1/tenders/{tender_id}/activity", response_model=ActivityList, tags=["audit"]
)
async def list_activity_endpoint(
    tender_id: UUID,
    session: SessionDependency,
) -> ActivityList:
    items, total = await list_activity(session, tender_id)
    structlog.contextvars.bind_contextvars(tender_id=str(tender_id))
    return ActivityList(items=[_audit_view(item) for item in items], total=total)
