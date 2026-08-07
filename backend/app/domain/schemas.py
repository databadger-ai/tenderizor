from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonBlank = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
SourceText = Annotated[str, StringConstraints(min_length=1)]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Recommendation(StrEnum):
    INCLUDE = "INCLUDE"
    REVIEW = "REVIEW"
    EXCLUDE = "EXCLUDE"


class RequirementType(StrEnum):
    MANDATORY = "MANDATORY"
    RATED = "RATED"
    READINESS = "READINESS"


class RequirementStatus(StrEnum):
    PASS = "PASS"
    REMEDIABLE = "REMEDIABLE"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class GateOutcome(StrEnum):
    BID_ALLOWED = "BID_ALLOWED"
    BID_BLOCKED = "BID_BLOCKED"


class RunStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class AuditAction(StrEnum):
    TENDER_CREATED = "TENDER_CREATED"
    ANALYSIS_REQUESTED = "ANALYSIS_REQUESTED"
    ANALYSIS_STARTED = "ANALYSIS_STARTED"
    ANALYSIS_COMPLETED = "ANALYSIS_COMPLETED"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    CORRECTION = "CORRECTION"
    REVIEW = "REVIEW"


class Citation(StrictModel):
    line_start: int = Field(ge=1)
    line_end: int = Field(ge=1)
    quote: NonBlank

    @model_validator(mode="after")
    def validate_line_range(self) -> "Citation":
        if self.line_end < self.line_start:
            raise ValueError("line_end must be greater than or equal to line_start")
        return self


class MaterialField(StrictModel):
    field_name: NonBlank
    value: NonBlank
    citations: list[Citation] = Field(min_length=1)


class RequirementFinding(StrictModel):
    requirement: NonBlank
    requirement_type: RequirementType
    status: RequirementStatus
    fatal: bool
    rationale: NonBlank
    citations: list[Citation] = Field(default_factory=list)
    remediation: str | None = None

    @model_validator(mode="after")
    def validate_remediation(self) -> "RequirementFinding":
        if self.status is RequirementStatus.REMEDIABLE and not self.remediation:
            raise ValueError("remediation is required for REMEDIABLE requirements")
        if self.requirement_type in {RequirementType.MANDATORY, RequirementType.RATED}:
            if not self.citations:
                raise ValueError("MANDATORY and RATED requirements require source citations")
        return self


class MissingFact(StrictModel):
    fact: NonBlank
    impact: NonBlank


class RiskFinding(StrictModel):
    risk: NonBlank
    severity: Annotated[int, Field(ge=1, le=5)]
    rationale: NonBlank
    citations: list[Citation] = Field(default_factory=list)


class AIAnalysisDraft(StrictModel):
    summary: NonBlank
    recommendation: Recommendation
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    cited_material_fields: list[MaterialField]
    requirements: list[RequirementFinding]
    missing_facts: list[MissingFact]
    risks: list[RiskFinding]


class AnalysisResult(AIAnalysisDraft):
    gate_outcome: GateOutcome
    gate_block_reasons: list[str]
    model: Literal["openai:gpt-5.6-sol"] = "openai:gpt-5.6-sol"
    definition_version: Literal["canadabuys_tender_analysis_v1"] = (
        "canadabuys_tender_analysis_v1"
    )


class TenderCreate(StrictModel):
    title: NonBlank
    source_text: SourceText
    buyer: str | None = None
    deadline: datetime | None = None
    reference_number: str | None = None
    solicitation_number: str | None = None

    @model_validator(mode="after")
    def validate_deadline(self) -> "TenderCreate":
        if not self.source_text.strip():
            raise ValueError("source_text must contain non-whitespace evidence")
        if self.deadline is not None and self.deadline.tzinfo is None:
            raise ValueError("deadline must include a timezone")
        return self


class TenderSummary(StrictModel):
    id: UUID
    title: str
    buyer: str | None
    deadline: datetime | None
    reference_number: str | None
    solicitation_number: str | None
    source_sha256: str
    line_count: int
    latest_run_id: UUID | None
    latest_run_status: RunStatus | None
    recommendation: Recommendation | None
    gate_outcome: GateOutcome | None
    created_at: datetime
    updated_at: datetime


class TenderDetail(TenderSummary):
    source_text: str


class TenderList(StrictModel):
    items: list[TenderSummary]
    total: int


class AnalysisRunCreate(StrictModel):
    requested_by: NonBlank


class AnalysisRunAccepted(StrictModel):
    run_id: UUID
    workflow_id: str
    status: RunStatus


class AnalysisRunDetail(StrictModel):
    run_id: UUID
    tender_id: UUID
    workflow_id: str
    status: RunStatus
    analysis: AnalysisResult | None
    error_code: str | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None


class CorrectionCreate(StrictModel):
    actor_id: NonBlank
    action: AuditAction
    reason: NonBlank
    analysis_run_id: UUID | None = None
    field_path: NonBlank
    previous_value: Any | None = None
    corrected_value: Any | None = None

    @model_validator(mode="after")
    def validate_action(self) -> "CorrectionCreate":
        if self.action not in {AuditAction.CORRECTION, AuditAction.REVIEW}:
            raise ValueError("action must be CORRECTION or REVIEW")
        return self


class AuditEventView(StrictModel):
    id: UUID
    tender_id: UUID
    analysis_run_id: UUID | None
    action: AuditAction
    actor_id: str
    reason: str | None
    field_path: str | None
    previous_value: Any | None
    corrected_value: Any | None
    correlation_id: str
    occurred_at: datetime


class ActivityList(StrictModel):
    items: list[AuditEventView]
    total: int


class DependencyStatus(StrictModel):
    status: str
    error_class: str | None = None


class HealthResponse(StrictModel):
    status: str
    service: str


class ReadinessResponse(StrictModel):
    status: str
    database: DependencyStatus
    temporal: DependencyStatus
