from datetime import UTC, datetime
from hashlib import sha256
from typing import cast
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.db.models import AnalysisRun, AuditEvent, Tender
from app.domain.schemas import (
    AIAnalysisDraft,
    AnalysisResult,
    AuditAction,
    CorrectionCreate,
    RunStatus,
    TenderCreate,
)


def source_sha256(source_text: str) -> str:
    return sha256(source_text.encode("utf-8")).hexdigest()


async def get_tender(session: AsyncSession, tender_id: UUID) -> Tender:
    tender = await session.get(Tender, tender_id)
    if tender is None:
        raise NotFoundError("tender not found")
    if source_sha256(tender.source_text) != tender.source_sha256:
        raise ConflictError("persisted tender evidence hash mismatch")
    return tender


async def create_tender(
    session: AsyncSession, payload: TenderCreate, *, actor_id: str, correlation_id: str
) -> Tender:
    digest = source_sha256(payload.source_text)
    tender = Tender(
        title=payload.title,
        source_text=payload.source_text,
        source_sha256=digest,
        buyer=payload.buyer,
        deadline=payload.deadline,
        reference_number=payload.reference_number,
        solicitation_number=payload.solicitation_number,
    )
    session.add(tender)
    await session.flush()
    if source_sha256(tender.source_text) != tender.source_sha256:
        raise ConflictError("source evidence hash verification failed")
    session.add(
        AuditEvent(
            tender_id=tender.id,
            action=AuditAction.TENDER_CREATED.value,
            actor_id=actor_id,
            reason="Tender source evidence created",
            correlation_id=correlation_id,
            occurred_at=datetime.now(UTC),
        )
    )
    await session.commit()
    await session.refresh(tender)
    return tender


async def get_latest_analysis_run(
    session: AsyncSession, tender_id: UUID
) -> AnalysisRun | None:
    return await session.scalar(
        select(AnalysisRun)
        .where(AnalysisRun.tender_id == tender_id)
        .order_by(AnalysisRun.created_at.desc(), AnalysisRun.id.desc())
        .limit(1)
    )


async def list_tenders(
    session: AsyncSession,
) -> tuple[list[tuple[Tender, AnalysisRun | None]], int]:
    latest_run_id = (
        select(AnalysisRun.id)
        .where(AnalysisRun.tender_id == Tender.id)
        .order_by(AnalysisRun.created_at.desc(), AnalysisRun.id.desc())
        .limit(1)
        .correlate(Tender)
        .scalar_subquery()
    )
    statement = (
        select(Tender, AnalysisRun)
        .outerjoin(AnalysisRun, AnalysisRun.id == latest_run_id)
        .order_by(Tender.created_at.desc())
    )
    rows = (await session.execute(statement)).all()
    items = [(row[0], cast(AnalysisRun | None, row[1])) for row in rows]
    total = int(await session.scalar(select(func.count()).select_from(Tender)) or 0)
    return items, total


async def create_analysis_run(
    session: AsyncSession,
    *,
    tender_id: UUID,
    workflow_id: str,
    requested_by: str,
    correlation_id: str,
) -> AnalysisRun:
    await get_tender(session, tender_id)
    run = AnalysisRun(
        tender_id=tender_id,
        workflow_id=workflow_id,
        status=RunStatus.QUEUED.value,
        requested_by=requested_by,
    )
    session.add(run)
    await session.flush()
    session.add(
        AuditEvent(
            tender_id=tender_id,
            analysis_run_id=run.id,
            action=AuditAction.ANALYSIS_REQUESTED.value,
            actor_id=requested_by,
            reason="Analysis workflow requested",
            correlation_id=correlation_id,
            occurred_at=datetime.now(UTC),
        )
    )
    await session.commit()
    await session.refresh(run)
    return run


async def get_analysis_run(session: AsyncSession, run_id: UUID) -> AnalysisRun:
    run = await session.get(AnalysisRun, run_id)
    if run is None:
        raise NotFoundError("analysis run not found")
    return run


async def set_run_status(
    session: AsyncSession,
    run_id: UUID,
    status: RunStatus,
    *,
    correlation_id: str,
    analysis: AnalysisResult | None = None,
    error_code: str | None = None,
) -> AnalysisRun:
    run = await session.scalar(
        select(AnalysisRun).where(AnalysisRun.id == run_id).with_for_update()
    )
    if run is None:
        raise NotFoundError("analysis run not found")
    current = RunStatus(run.status)
    if current is status:
        return run
    if current in {RunStatus.SUCCEEDED, RunStatus.FAILED}:
        raise ConflictError("terminal analysis run cannot transition")
    allowed = {
        RunStatus.QUEUED: {RunStatus.RUNNING, RunStatus.FAILED},
        RunStatus.RUNNING: {RunStatus.SUCCEEDED, RunStatus.FAILED},
    }
    if status not in allowed[current]:
        raise ConflictError(f"invalid analysis run transition: {current.value} to {status.value}")
    run.status = status.value
    run.analysis = analysis.model_dump(mode="json") if analysis else None
    run.error_code = error_code
    action: AuditAction | None = None
    reason: str | None = None
    if status is RunStatus.RUNNING:
        action, reason = AuditAction.ANALYSIS_STARTED, "Analysis workflow started"
    elif status is RunStatus.SUCCEEDED:
        action, reason = AuditAction.ANALYSIS_COMPLETED, "Analysis workflow completed"
        run.completed_at = datetime.now(UTC)
    elif status is RunStatus.FAILED:
        action, reason = AuditAction.ANALYSIS_FAILED, "Analysis workflow failed"
        run.completed_at = datetime.now(UTC)
    if action is not None:
        session.add(
            AuditEvent(
                tender_id=run.tender_id,
                analysis_run_id=run.id,
                action=action.value,
                actor_id="system",
                reason=reason,
                correlation_id=correlation_id,
                occurred_at=datetime.now(UTC),
            )
        )
    await session.commit()
    await session.refresh(run)
    return run


async def append_correction(
    session: AsyncSession,
    tender_id: UUID,
    payload: CorrectionCreate,
    *,
    correlation_id: str,
) -> AuditEvent:
    await get_tender(session, tender_id)
    if payload.analysis_run_id is not None:
        run = await get_analysis_run(session, payload.analysis_run_id)
        if run.tender_id != tender_id:
            raise ConflictError("analysis run does not belong to tender")
    event = AuditEvent(
        tender_id=tender_id,
        analysis_run_id=payload.analysis_run_id,
        action=payload.action.value,
        actor_id=payload.actor_id,
        reason=payload.reason,
        field_path=payload.field_path,
        previous_value=payload.previous_value,
        corrected_value=payload.corrected_value,
        correlation_id=correlation_id,
        occurred_at=datetime.now(UTC),
    )
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def list_activity(session: AsyncSession, tender_id: UUID) -> tuple[list[AuditEvent], int]:
    await get_tender(session, tender_id)
    statement = (
        select(AuditEvent)
        .where(AuditEvent.tender_id == tender_id)
        .order_by(AuditEvent.occurred_at.desc(), AuditEvent.id.desc())
    )
    items = list((await session.scalars(statement)).all())
    total = int(
        await session.scalar(
            select(func.count()).select_from(AuditEvent).where(AuditEvent.tender_id == tender_id)
        )
        or 0
    )
    return items, total


def validate_citations(source_text: str, draft: AIAnalysisDraft) -> None:
    lines = source_text.splitlines() or [source_text]
    citations = [citation for field in draft.cited_material_fields for citation in field.citations]
    citations.extend(citation for item in draft.requirements for citation in item.citations)
    citations.extend(citation for item in draft.risks for citation in item.citations)
    for citation in citations:
        if citation.line_end > len(lines):
            raise ConflictError("analysis citation line is outside source evidence")
        cited_text = "\n".join(lines[citation.line_start - 1 : citation.line_end])
        if citation.quote not in cited_text:
            raise ConflictError("analysis citation quote does not match source evidence")
