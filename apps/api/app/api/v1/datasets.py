
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from agentevalops_schemas.dataset import DatasetCaseSchema, DatasetSchema, ExperimentRunSchema
from app.infrastructure.datasets import dataset_store

router = APIRouter(prefix="/datasets", tags=["Datasets & Experiments"])


class CreateDatasetRequest(BaseModel):
    name: str
    description: str | None = None
    organization_id: str = "org_default"
    project_id: str = "proj_default"


class RunExperimentRequest(BaseModel):
    experiment_id: str
    dataset_id: str
    agent_id: str
    agent_version: str = "1.0.0"


@router.post("", response_model=DatasetSchema, status_code=status.HTTP_201_CREATED)
async def create_dataset(payload: CreateDatasetRequest) -> DatasetSchema:
    import uuid

    ds_id = f"ds_{uuid.uuid4().hex[:8]}"
    ds = DatasetSchema(
        dataset_id=ds_id,
        name=payload.name,
        description=payload.description,
        organization_id=payload.organization_id,
        project_id=payload.project_id,
    )
    return dataset_store.create_dataset(ds)


@router.get("", response_model=list[DatasetSchema])
async def list_datasets() -> list[DatasetSchema]:
    return dataset_store.list_datasets()


@router.post("/{dataset_id}/cases", response_model=DatasetSchema)
async def add_dataset_case(dataset_id: str, case: DatasetCaseSchema) -> DatasetSchema:
    ds = dataset_store.add_case(dataset_id, case)
    if not ds:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found.")
    return ds


@router.post("/experiments/run", response_model=ExperimentRunSchema)
async def run_experiment(payload: RunExperimentRequest) -> ExperimentRunSchema:
    return dataset_store.run_experiment(
        experiment_id=payload.experiment_id,
        dataset_id=payload.dataset_id,
        agent_id=payload.agent_id,
        agent_version=payload.agent_version,
    )
