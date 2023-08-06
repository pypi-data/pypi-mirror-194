from anylearn.applications import (
    report_intermediate_metric,
    report_final_metric,
    sync_algorithm,
    quick_train,
)
from anylearn.config import (
    AnyLearnAuthException,
    AnylearnConfig,
    init_sdk,
)
from anylearn.sdk import (
    DatasetArtifact,
    FileArtifact,
    ModelArtifact,
    Task,
    get_task_output,
)


def get_dataset(full_name: str) -> DatasetArtifact:
    return DatasetArtifact.from_full_name(full_name)


def get_model(full_name: str) -> ModelArtifact:
    return ModelArtifact.from_full_name(full_name)
