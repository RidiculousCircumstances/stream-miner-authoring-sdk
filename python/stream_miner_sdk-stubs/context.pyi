"""Immutable runtime context visible to parser code."""

from dataclasses import dataclass

from stream_miner_sdk import _vocabularies as vocab

@dataclass(frozen=True, slots=True)
class RunContext:
    """Task/run defaults selected by Control Plane and Agent for this execution."""

    parser_alias: str
    task_alias: str
    run_id: int | None = None
    task_id: int | None = None
    max_concurrent_tasks: int = 1
    thread_config_alias: str | None = None
    request_delay_sec: float = 0.0
    http_transport_mode: vocab.ModeValue = ...
    request_timeout_sec: float = 0.0
    request_max_retries: int = 0
