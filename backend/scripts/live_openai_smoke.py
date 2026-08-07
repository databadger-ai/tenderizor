"""Run a live, content-redacted OpenAI smoke test against the synthetic fixture."""

import asyncio
import json
import os
from pathlib import Path

from app.db.repositories import validate_citations
from app.domain.policy import apply_hard_gate
from app.services.analyzer import build_analysis_prompt
from app.workflows.definition import tender_analysis_agent


async def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not present")

    fixture_path = Path(__file__).parents[2] / "fixtures" / "sample-tender.txt"
    source_text = fixture_path.read_text(encoding="utf-8")
    result = await tender_analysis_agent.run(
        build_analysis_prompt("Synthetic rugged laptop tender", source_text)
    )
    validate_citations(source_text, result.output)
    analysis = apply_hard_gate(result.output)
    print(
        json.dumps(
            {
                "status": "passed",
                "model": analysis.model,
                "definition_version": analysis.definition_version,
                "gate_outcome": analysis.gate_outcome,
                "material_field_count": len(analysis.cited_material_fields),
                "requirement_count": len(analysis.requirements),
            }
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
