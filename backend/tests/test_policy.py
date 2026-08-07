from app.domain.policy import apply_hard_gate
from app.domain.schemas import (
    AIAnalysisDraft,
    Citation,
    GateOutcome,
    Recommendation,
    RequirementFinding,
    RequirementStatus,
    RequirementType,
)


def draft_with(status: RequirementStatus, *, fatal: bool) -> AIAnalysisDraft:
    return AIAnalysisDraft(
        summary="Summary",
        recommendation=Recommendation.INCLUDE,
        confidence=0.9,
        cited_material_fields=[],
        requirements=[
            RequirementFinding(
                requirement="Registration requirement",
                requirement_type=RequirementType.MANDATORY,
                status=status,
                fatal=fatal,
                rationale="fixture",
                citations=[Citation(line_start=1, line_end=1, quote="Registration requirement")],
            )
        ],
        missing_facts=[],
        risks=[],
    )


def test_fatal_fail_blocks_bid() -> None:
    result = apply_hard_gate(draft_with(RequirementStatus.FAIL, fatal=True))
    assert result.gate_outcome is GateOutcome.BID_BLOCKED
    assert result.gate_block_reasons == ["FAIL: Registration requirement"]


def test_fatal_unknown_blocks_bid() -> None:
    result = apply_hard_gate(draft_with(RequirementStatus.UNKNOWN, fatal=True))
    assert result.gate_outcome is GateOutcome.BID_BLOCKED


def test_nonfatal_unknown_does_not_block_bid() -> None:
    result = apply_hard_gate(draft_with(RequirementStatus.PASS, fatal=False))
    assert result.gate_outcome is GateOutcome.BID_ALLOWED


def test_model_cannot_clear_fatal_flag_on_mandatory_fail() -> None:
    result = apply_hard_gate(draft_with(RequirementStatus.FAIL, fatal=False))
    assert result.gate_outcome is GateOutcome.BID_BLOCKED
