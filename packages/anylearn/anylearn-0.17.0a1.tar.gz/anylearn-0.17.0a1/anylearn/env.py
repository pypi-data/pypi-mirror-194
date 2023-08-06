import os
from pathlib import Path
from typing import Optional, List


ARTIFACT_IDS = 'ANYLEARN_ARTIFACT_IDS'
TASK_ID = 'ANYLEARN_TASK_ID'


def get_artifact_ids() -> List[str]:
    ids_str = os.environ.get(ARTIFACT_IDS, None)
    if not ids_str:
        return []
    return ids_str.replace(" ", "").split(",")


def get_artifact_paths() -> List[Path]:
    ids = get_artifact_ids()
    paths = {}
    for id_ in ids:
        p = os.environ.get(id_, None)
        if not p:
            continue
        p = Path(p)
        if not p.exists():
            continue
        paths[id_] = p
    return paths


def get_task_id(default: Optional[str]=None):
    return os.environ.get(TASK_ID, default)
