"""HTTP request and response types for parser authoring."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from stream_miner_sdk import _vocabularies as vocab

@dataclass(slots=True)
class RequestOptions:
    """Per-request overrides; Thread Config still owns execution defaults."""

    headers: dict[str, str] | None = None
    validate_response: Callable[[HttpResponse], bool] | None = None
    http_mode: vocab.ModeValue | None = None
    browser: bool = False
    browser_profile: str | None = None
    timeout: float | None = None
    retries: int | None = None
    allow_statuses: set[int] | None = None
    delay: float | None = None

@dataclass(slots=True)
class HttpResponse:
    """Response returned by Agent-executed HTTP requests."""

    status: int
    headers: dict[str, str]
    body: bytes
    retried: int = 0
    elapsed_ms: float = 0.0
    error_code: vocab.ErrorCodeValue | None = None
    egress: dict[str, Any] | None = None
    transport_mode: vocab.ModeValue | None = None
    def text(self, encoding: str = "utf-8", errors: str = "replace") -> str:
        """Decode the response body to text.

        Example:
            html = response.text()
        """
        ...
    def json(self) -> Any:
        """Decode the response body as JSON."""
        ...
    @property
    def ok(self) -> bool:
        """Return True when the response satisfied the success policy."""
        ...
    @property
    def retries(self) -> int:
        """Number of retry attempts used by the request."""
        ...
    @retries.setter
    def retries(self, value: int) -> None:
        """Set retry count when adapting older runtime response objects."""
        ...
