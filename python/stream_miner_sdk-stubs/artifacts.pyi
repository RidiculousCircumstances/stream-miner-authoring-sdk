"""Types for parser-produced durable datasets and run-local outputs."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from stream_miner_sdk import _vocabularies as vocab

@dataclass(frozen=True, slots=True)
class DatasetRef:
    """Durable dataset reference returned after publication through the host."""

    id: int
    name: str
    sha256: str
    size_bytes: int
    artifact_blob_id: int | None = None
    content_type: str | None = None
    source_run_id: int | None = None
    source_task_alias: str | None = None
    source_key: str | None = None
    metadata: dict[str, Any] = ...
    created_at: datetime | None = None

@dataclass(frozen=True, slots=True)
class LocalOutputHandle:
    """Run-local output handle for a file already written in the workspace."""

    id: int
    run_id: int
    handle: str
    relative_path: str
    output_kind: vocab.KindValue
    task_alias: str | None = None
    agent_id: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    sha256: str | None = None
    published_dataset_id: int | None = None
    metadata: dict[str, Any] = ...
