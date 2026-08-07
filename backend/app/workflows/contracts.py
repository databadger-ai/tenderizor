from uuid import UUID

from app.domain.schemas import AnalysisResult, StrictModel


class TenderWorkflowInput(StrictModel):
    api_version: str = "v1"
    tender_id: UUID
    run_id: UUID
    workflow_id: str
    correlation_id: str


class TenderAnalysisContext(StrictModel):
    tender_id: UUID
    run_id: UUID
    title: str
    source_text: str
    source_sha256: str


class PersistAnalysisInput(StrictModel):
    run_id: UUID
    correlation_id: str
    analysis: AnalysisResult


class PersistFailureInput(StrictModel):
    run_id: UUID
    correlation_id: str
    error_code: str


class MarkRunningInput(StrictModel):
    run_id: UUID
    correlation_id: str
