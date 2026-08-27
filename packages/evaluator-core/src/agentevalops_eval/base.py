from abc import ABC, abstractmethod
from typing import Any

from agentevalops_schemas.eval import EvaluationResultSchema


class Evaluator(ABC):
    """Abstract Base Class for all AgentEvalOps Evaluators."""

    name: str = "base_evaluator"
    version: str = "0.1.0"
    description: str = "Base evaluator interface"

    @abstractmethod
    def evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        """Evaluate an agent run or trace synchronously."""
        pass

    async def async_evaluate(
        self, run_data: dict[str, Any], context: dict[str, Any] | None = None
    ) -> EvaluationResultSchema:
        """Evaluate an agent run or trace asynchronously. Default falls back to sync evaluate."""
        return self.evaluate(run_data, context)
