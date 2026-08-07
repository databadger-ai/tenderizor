from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.errors import ImmutableAuditError
from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Tender(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tenders"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    source_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    buyer: Mapped[str | None] = mapped_column(String(500))
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reference_number: Mapped[str | None] = mapped_column(String(255))
    solicitation_number: Mapped[str | None] = mapped_column(String(255))

    analysis_runs: Mapped[list["AnalysisRun"]] = relationship(back_populates="tender")


class AnalysisRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "analysis_runs"

    tender_id: Mapped[UUID] = mapped_column(
        ForeignKey("tenders.id", ondelete="CASCADE"), index=True, nullable=False
    )
    workflow_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False)
    analysis: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    error_code: Mapped[str | None] = mapped_column(String(120))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    tender: Mapped[Tender] = relationship(back_populates="analysis_runs")


class AuditEvent(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "audit_events"

    tender_id: Mapped[UUID] = mapped_column(
        ForeignKey("tenders.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    analysis_run_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="RESTRICT"), index=True
    )
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    field_path: Mapped[str | None] = mapped_column(String(500))
    previous_value: Mapped[Any | None] = mapped_column(JSON)
    corrected_value: Mapped[Any | None] = mapped_column(JSON)
    correlation_id: Mapped[str] = mapped_column(String(255), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


@event.listens_for(AuditEvent, "before_update")
@event.listens_for(AuditEvent, "before_delete")
def prevent_audit_mutation(*_: object) -> None:
    raise ImmutableAuditError("audit events are append-only")
