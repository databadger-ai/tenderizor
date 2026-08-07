from datetime import timedelta

from pydantic_ai import Agent
from pydantic_ai.durable_exec.temporal import PydanticAIWorkflow, TemporalDurability
from pydantic_ai.models.openai import OpenAIResponsesModelSettings
from temporalio import workflow
from temporalio.common import RetryPolicy

from app.core.config import get_settings
from app.domain.policy import apply_hard_gate
from app.domain.schemas import AIAnalysisDraft, AnalysisResult
from app.services.analyzer import build_analysis_prompt
from app.workflows.contracts import (
    MarkRunningInput,
    PersistAnalysisInput,
    PersistFailureInput,
    TenderAnalysisContext,
    TenderWorkflowInput,
)

settings = get_settings()
model_settings: OpenAIResponsesModelSettings = {
    "openai_reasoning_effort": settings.openai_reasoning_effort
}

tender_analysis_agent = Agent(
    "openai:gpt-5.6-sol",
    name="canadabuys_tender_analysis_v1",
    output_type=AIAnalysisDraft,
    instructions=(
        "Return only the requested typed tender analysis. Preserve uncertainty. "
        "Never invent official facts, supplier capabilities, or external actions."
    ),
    model_settings=model_settings,
    capabilities=[TemporalDurability()],
)

ACTIVITY_RETRY = RetryPolicy(maximum_attempts=3)


@workflow.defn
class TenderAnalysisWorkflow(PydanticAIWorkflow):
    __pydantic_ai_agents__ = [tender_analysis_agent]  # noqa: RUF012

    @workflow.run
    async def run(self, payload: TenderWorkflowInput) -> AnalysisResult:
        await workflow.execute_activity(
            "mark_analysis_running",
            MarkRunningInput(run_id=payload.run_id, correlation_id=payload.correlation_id),
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=ACTIVITY_RETRY,
            result_type=None,
        )
        try:
            context = await workflow.execute_activity(
                "load_tender_analysis_context",
                payload,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=ACTIVITY_RETRY,
                result_type=TenderAnalysisContext,
            )
            result = await tender_analysis_agent.run(
                build_analysis_prompt(context.title, context.source_text)
            )
            analysis = apply_hard_gate(result.output)
            await workflow.execute_activity(
                "persist_tender_analysis",
                PersistAnalysisInput(
                    run_id=payload.run_id,
                    correlation_id=payload.correlation_id,
                    analysis=analysis,
                ),
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=ACTIVITY_RETRY,
                result_type=None,
            )
            return analysis
        except Exception as exc:
            await workflow.execute_activity(
                "persist_tender_analysis_failure",
                PersistFailureInput(
                    run_id=payload.run_id,
                    correlation_id=payload.correlation_id,
                    error_code=type(exc).__name__,
                ),
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=ACTIVITY_RETRY,
                result_type=None,
            )
            raise
