from app.domain.schemas import (
    AIAnalysisDraft,
    AnalysisResult,
    GateOutcome,
    RequirementStatus,
    RequirementType,
)


def apply_hard_gate(draft: AIAnalysisDraft) -> AnalysisResult:
    blockers = [
        f"{item.status.value}: {item.requirement}"
        for item in draft.requirements
        if item.status in {RequirementStatus.FAIL, RequirementStatus.UNKNOWN}
        and (item.requirement_type is RequirementType.MANDATORY or item.fatal)
    ]
    return AnalysisResult(
        **draft.model_dump(),
        gate_outcome=GateOutcome.BID_BLOCKED if blockers else GateOutcome.BID_ALLOWED,
        gate_block_reasons=blockers,
    )
