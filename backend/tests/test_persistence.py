from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import StatementError

from app.core.errors import ConflictError, ImmutableAuditError
from app.db.models import AuditEvent, Tender
from app.db.repositories import create_analysis_run, create_tender, set_run_status
from app.db.session import Database
from app.domain.policy import apply_hard_gate
from app.domain.schemas import AIAnalysisDraft, Recommendation, RunStatus, TenderCreate


async def test_audit_events_cannot_be_updated(database: Database) -> None:
    async with database.session_factory() as session:
        tender = Tender(
            title="Tender",
            source_text="Source",
            source_sha256="6d201a42f74f5e2a3aafb439a76491f25c098ccf1de4f5d541221f8c0a3f2f75",
        )
        session.add(tender)
        await session.flush()
        event = AuditEvent(
            tender_id=tender.id,
            action="REVIEW",
            actor_id="reviewer",
            reason="Initial review",
            correlation_id=str(uuid4()),
            occurred_at=datetime.now(UTC),
        )
        session.add(event)
        await session.commit()

        event.reason = "Mutated review"
        with pytest.raises((ImmutableAuditError, StatementError)):
            await session.commit()
        await session.rollback()


async def test_run_transitions_are_idempotent_and_terminal(database: Database) -> None:
    correlation_id = str(uuid4())
    async with database.session_factory() as session:
        tender = await create_tender(
            session,
            TenderCreate(title="Tender", source_text="Official source"),
            actor_id="analyst",
            correlation_id=correlation_id,
        )
        run = await create_analysis_run(
            session,
            tender_id=tender.id,
            workflow_id=f"workflow-{uuid4()}",
            requested_by="analyst",
            correlation_id=correlation_id,
        )
        await set_run_status(
            session, run.id, RunStatus.RUNNING, correlation_id=correlation_id
        )
        await set_run_status(
            session, run.id, RunStatus.RUNNING, correlation_id=correlation_id
        )
        analysis = apply_hard_gate(
            AIAnalysisDraft(
                summary="Summary",
                recommendation=Recommendation.REVIEW,
                confidence=0.5,
                cited_material_fields=[],
                requirements=[],
                missing_facts=[],
                risks=[],
            )
        )
        await set_run_status(
            session,
            run.id,
            RunStatus.SUCCEEDED,
            correlation_id=correlation_id,
            analysis=analysis,
        )
        await set_run_status(
            session,
            run.id,
            RunStatus.SUCCEEDED,
            correlation_id=correlation_id,
            analysis=analysis,
        )

        started_count = await session.scalar(
            select(func.count())
            .select_from(AuditEvent)
            .where(
                AuditEvent.analysis_run_id == run.id,
                AuditEvent.action == "ANALYSIS_STARTED",
            )
        )
        completed_count = await session.scalar(
            select(func.count())
            .select_from(AuditEvent)
            .where(
                AuditEvent.analysis_run_id == run.id,
                AuditEvent.action == "ANALYSIS_COMPLETED",
            )
        )
        assert started_count == 1
        assert completed_count == 1

        with pytest.raises(ConflictError, match="terminal"):
            await set_run_status(
                session, run.id, RunStatus.FAILED, correlation_id=correlation_id
            )
