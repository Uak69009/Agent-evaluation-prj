from abc import ABC

from agentevalops_eval.base import Evaluator


class DeterministicEvaluator(Evaluator, ABC):
    """Evaluator using exact rule-based or assertion-based checks."""

    name = "deterministic_evaluator"


class LLMJudgeEvaluator(Evaluator, ABC):
    """Evaluator leveraging LLM-as-a-judge for semantic quality assessment."""

    name = "llm_judge_evaluator"


class TrajectoryEvaluator(Evaluator, ABC):
    """Evaluator analyzing agent step execution sequence and plan adherence."""

    name = "trajectory_evaluator"


class ToolEvaluator(Evaluator, ABC):
    """Evaluator checking tool call parameters, schema correctness, and outputs."""

    name = "tool_evaluator"


class RAGEvaluator(Evaluator, ABC):
    """Evaluator assessing context relevance, faithfulness, and answer relevance."""

    name = "rag_evaluator"


class SafetyEvaluator(Evaluator, ABC):
    """Evaluator verifying safety guardrails, prompt injection, and PII leakage."""

    name = "safety_evaluator"


class CostEvaluator(Evaluator, ABC):
    """Evaluator checking token consumption and budget thresholds."""

    name = "cost_evaluator"


class LatencyEvaluator(Evaluator, ABC):
    """Evaluator measuring latency, time-to-first-token, and SLA compliance."""

    name = "latency_evaluator"


class ReliabilityEvaluator(Evaluator, ABC):
    """Evaluator evaluating error resilience, retry rates, and state integrity."""

    name = "reliability_evaluator"
