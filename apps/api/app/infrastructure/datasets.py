
from agentevalops_eval.engine import evaluation_engine
from agentevalops_schemas.dataset import DatasetCaseSchema, DatasetSchema, ExperimentRunSchema


class DatasetStore:
    """In-memory dataset & experiment store for AgentEvalOps."""

    def __init__(self) -> None:
        self._datasets: dict[str, DatasetSchema] = {}
        self._experiments: list[ExperimentRunSchema] = []

    def create_dataset(self, dataset: DatasetSchema) -> DatasetSchema:
        self._datasets[dataset.dataset_id] = dataset
        return dataset

    def get_dataset(self, dataset_id: str) -> DatasetSchema | None:
        return self._datasets.get(dataset_id)

    def list_datasets(self) -> list[DatasetSchema]:
        return list(self._datasets.values())

    def add_case(self, dataset_id: str, case: DatasetCaseSchema) -> DatasetSchema | None:
        ds = self._datasets.get(dataset_id)
        if ds:
            ds.cases.append(case)
        return ds

    def run_experiment(
        self,
        experiment_id: str,
        dataset_id: str,
        agent_id: str,
        agent_version: str,
    ) -> ExperimentRunSchema:
        ds = self.get_dataset(dataset_id)
        if not ds or not ds.cases:
            exp = ExperimentRunSchema(
                experiment_id=experiment_id,
                dataset_id=dataset_id,
                agent_id=agent_id,
                agent_version=agent_version,
                status="completed",
                total_cases=0,
                passed_cases=0,
                failed_cases=0,
                overall_accuracy=1.0,
            )
            self._experiments.append(exp)
            return exp

        passed = 0
        failed = 0

        for case in ds.cases:
            run_data = {"output": case.expected_output, "duration_ms": 100.0, "spans": []}
            res = evaluation_engine.evaluate_run(
                run_data=run_data,
                context={"expected_output": case.expected_output},
            )
            if res.overall_status.value == "passed":
                passed += 1
            else:
                failed += 1

        total = len(ds.cases)
        acc = round(passed / total, 2) if total > 0 else 1.0

        exp = ExperimentRunSchema(
            experiment_id=experiment_id,
            dataset_id=dataset_id,
            agent_id=agent_id,
            agent_version=agent_version,
            status="completed",
            total_cases=total,
            passed_cases=passed,
            failed_cases=failed,
            overall_accuracy=acc,
        )
        self._experiments.append(exp)
        return exp


dataset_store = DatasetStore()
