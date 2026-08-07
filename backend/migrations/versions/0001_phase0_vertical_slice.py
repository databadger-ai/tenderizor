"""Create Phase-0 tender, analysis, and immutable audit tables.

Revision ID: 0001_phase0
Revises: None
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_phase0"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tenders",
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("source_text", sa.Text(), nullable=False),
        sa.Column("source_sha256", sa.String(length=64), nullable=False),
        sa.Column("buyer", sa.String(length=500), nullable=True),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reference_number", sa.String(length=255), nullable=True),
        sa.Column("solicitation_number", sa.String(length=255), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tenders")),
    )
    op.create_table(
        "analysis_runs",
        sa.Column("tender_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_id", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("requested_by", sa.String(length=255), nullable=False),
        sa.Column("analysis", sa.JSON(), nullable=True),
        sa.Column("error_code", sa.String(length=120), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["tender_id"],
            ["tenders.id"],
            name=op.f("fk_analysis_runs_tender_id_tenders"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_runs")),
        sa.UniqueConstraint("workflow_id", name=op.f("uq_analysis_runs_workflow_id")),
    )
    op.create_index(op.f("ix_analysis_runs_status"), "analysis_runs", ["status"], unique=False)
    op.create_index(
        op.f("ix_analysis_runs_tender_id"), "analysis_runs", ["tender_id"], unique=False
    )
    op.create_table(
        "audit_events",
        sa.Column("tender_id", sa.Uuid(), nullable=False),
        sa.Column("analysis_run_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=255), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("field_path", sa.String(length=500), nullable=True),
        sa.Column("previous_value", sa.JSON(), nullable=True),
        sa.Column("corrected_value", sa.JSON(), nullable=True),
        sa.Column("correlation_id", sa.String(length=255), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["analysis_run_id"],
            ["analysis_runs.id"],
            name=op.f("fk_audit_events_analysis_run_id_analysis_runs"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tender_id"],
            ["tenders.id"],
            name=op.f("fk_audit_events_tender_id_tenders"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_events")),
    )
    op.create_index(
        op.f("ix_audit_events_analysis_run_id"),
        "audit_events",
        ["analysis_run_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audit_events_tender_id"), "audit_events", ["tender_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_events_tender_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_analysis_run_id"), table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index(op.f("ix_analysis_runs_tender_id"), table_name="analysis_runs")
    op.drop_index(op.f("ix_analysis_runs_status"), table_name="analysis_runs")
    op.drop_table("analysis_runs")
    op.drop_table("tenders")
