import logging

from agentevalops_eval.base import Evaluator

logger = logging.getLogger("agentevalops.eval.registry")


class EvaluatorRegistry:
    """Central registry for registering and discovering evaluators."""

    def __init__(self) -> None:
        self._registry: dict[str, type[Evaluator]] = {}

    def register(self, evaluator_cls: type[Evaluator]) -> type[Evaluator]:
        name = evaluator_cls.name
        self._registry[name] = evaluator_cls
        logger.info(f"Registered evaluator '{name}' (v{evaluator_cls.version})")
        return evaluator_cls

    def get(self, name: str) -> type[Evaluator]:
        if name not in self._registry:
            raise KeyError(f"Evaluator '{name}' is not registered.")
        return self._registry[name]

    def list_evaluators(self) -> list[dict[str, str]]:
        return [
            {
                "name": cls.name,
                "version": cls.version,
                "description": cls.description,
            }
            for cls in self._registry.values()
        ]

    def clear(self) -> None:
        self._registry.clear()


evaluator_registry = EvaluatorRegistry()
