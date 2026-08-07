import pytest
from pydantic import ValidationError

from app.domain.schemas import RequirementFinding, RequirementStatus, RequirementType


def test_official_requirement_requires_citation() -> None:
    with pytest.raises(ValidationError, match="require source citations"):
        RequirementFinding(
            requirement="Supplier must hold licence X",
            requirement_type=RequirementType.MANDATORY,
            status=RequirementStatus.UNKNOWN,
            fatal=False,
            rationale="No evidence",
            citations=[],
        )


def test_internal_readiness_check_may_have_no_source_citation() -> None:
    finding = RequirementFinding(
        requirement="Confirm internal delivery capacity",
        requirement_type=RequirementType.READINESS,
        status=RequirementStatus.UNKNOWN,
        fatal=False,
        rationale="Internal check",
        citations=[],
    )
    assert finding.citations == []
