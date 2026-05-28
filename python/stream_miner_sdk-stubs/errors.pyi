"""Typed parser failures surfaced to History and run diagnostics."""

from collections.abc import Mapping
from typing import Any

class ParserError(Exception):
    """Base class for parser-declared failure intent."""

    code: str
    reason: str
    message: str
    metadata: dict[str, Any]
    def __init__(
        self,
        reason: str,
        *,
        message: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None: ...

class ItemRetry(ParserError):
    """Retry the current item with bounded retry metadata."""

    code: str
    max_attempts: int
    retry_delay_sec: float | None
    def __init__(
        self,
        reason: str,
        *,
        max_attempts: int = 3,
        retry_delay_sec: float | None = None,
        message: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None: ...

class ItemFail(ParserError):
    """Fail the current item and let the run continue."""

    code: str

class RunFail(ParserError):
    """Fail the whole run intentionally."""

    code: str
