"""Base parser and host facade types for Python parser authoring."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar, Generic, Protocol, TypeVar

from stream_miner_sdk import _vocabularies as vocab
from stream_miner_sdk.artifacts import DatasetRef, LocalOutputHandle
from stream_miner_sdk.config import ParserConfigField
from stream_miner_sdk.context import RunContext
from stream_miner_sdk.egress import EgressFacade
from stream_miner_sdk.http import HttpResponse, RequestOptions

TConfig = TypeVar("TConfig")

class ParserHost(Protocol):
    """Runtime-owned host binding. Parser code should not implement this directly."""

    @property
    def logger(self) -> Any:
        """Structured logger facade supplied by the runtime host."""
        ...
    @property
    def egress(self) -> EgressFacade:
        """Parser-facing Egress lease facade supplied by the runtime host."""
        ...
    @property
    def queue(self) -> Any:
        """Queue facade for adding follow-up parser items."""
        ...
    @property
    def results_dir(self) -> Path:
        """Run output workspace root resolved by the runtime host."""
        ...
    @property
    def cookies(self) -> Any:
        """Cookie/session facade where the runtime provides one."""
        ...
    @property
    def runtime(self) -> RunContext:
        """Immutable task/run defaults selected for this parser execution."""
        ...
    def thread_id(self) -> str:
        """Return the current worker thread identifier."""
        ...
    async def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        body: Any | None = None,
        options: RequestOptions | None = None,
    ) -> HttpResponse:
        """Execute one HTTP request through the Agent host."""
        ...
    async def read_sensitive_asset(self, asset_ref: int | str) -> bytes:
        """Read a sensitive asset as bytes through the runtime host."""
        ...
    async def publish_dataset(
        self,
        *,
        name: str,
        path: str | Path | None = None,
        content: bytes | str | None = None,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DatasetRef:
        """Publish content or a workspace file as a durable dataset."""
        ...
    async def register_output(
        self,
        *,
        handle: str,
        path: str | Path,
        output_kind: vocab.KindValue = ...,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LocalOutputHandle:
        """Register a workspace file as a run-local output."""
        ...
    async def metric(
        self,
        name: str,
        value: int | float = 1.0,
        labels: Mapping[str, str] | None = None,
    ) -> None:
        """Emit one custom parser metric sample."""
        ...

class BaseParser(Generic[TConfig]):
    """Base class for Python parsers. Runtime operations call the Agent host."""

    __parser_alias__: ClassVar[str]
    Config: ClassVar[type[Any] | None]
    DEFAULT_PLUGINS: ClassVar[dict[str, Any]]
    conf: TConfig

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        """Return defaults extracted from the parser Config declaration."""
        ...
    @classmethod
    def config_fields(cls) -> tuple[ParserConfigField, ...]:
        """Return config field metadata for parser revision metadata."""
        ...
    @classmethod
    def build_config(cls, raw: dict[str, Any] | None) -> TConfig:
        """Build a typed Config instance from raw Control Plane values."""
        ...
    @property
    def logger(self) -> Any:
        """Structured logger facade; Agent owns shipping and retention."""
        ...
    @property
    def egress(self) -> EgressFacade:
        """Parser-facing Egress lease facade."""
        ...
    @property
    def queue(self) -> Any:
        """Queue facade for adding follow-up parser items."""
        ...
    @property
    def results_dir(self) -> Path:
        """Run output workspace root for files produced by this parser."""
        ...
    @property
    def cookies(self) -> Any:
        """Cookie/session facade where the runtime provides one."""
        ...
    @property
    def runtime(self) -> RunContext:
        """Immutable task/run defaults selected for this parser execution."""
        ...
    def thread_id(self) -> str:
        """Return the current worker thread identifier."""
        ...
    async def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        body: Any | None = None,
        options: RequestOptions | None = None,
    ) -> HttpResponse:
        """Execute one HTTP request through the Agent host."""
        ...
    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> HttpResponse:
        """Execute an HTTP GET through the Agent host.

        Example:
            response = await self.get("https://example.test/items", {"page": 1})
        """
        ...
    async def post(
        self,
        url: str,
        body: Any | None = None,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> HttpResponse:
        """Execute an HTTP POST through the Agent host."""
        ...
    async def get_json(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> Any:
        """Execute a GET and return response.json()."""
        ...
    async def post_json(
        self,
        url: str,
        payload: Any,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> Any:
        """Execute a POST and return response.json()."""
        ...
    async def read_sensitive_asset(self, asset_ref: int | str) -> bytes:
        """Read a sensitive asset as bytes."""
        ...
    async def read_sensitive_text(self, asset_ref: int | str, *, encoding: str = "utf-8") -> str:
        """Read a sensitive asset as decoded text."""
        ...
    async def publish_dataset(
        self,
        *,
        name: str,
        path: str | Path | None = None,
        content: bytes | str | None = None,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DatasetRef:
        """Publish content or a workspace file as a durable dataset."""
        ...
    async def publish_json(
        self,
        *,
        name: str,
        payload: Any,
        metadata: dict[str, Any] | None = None,
    ) -> DatasetRef:
        """Publish a JSON-encoded dataset.

        Example:
            await self.publish_json(name="last-item", payload={"id": "sku-1"})
        """
        ...
    async def register_output(
        self,
        *,
        handle: str,
        path: str | Path,
        output_kind: vocab.KindValue = ...,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LocalOutputHandle:
        """Register a workspace file as a run-local output."""
        ...
    async def metric(
        self,
        name: str,
        value: int | float = 1.0,
        labels: Mapping[str, str] | None = None,
    ) -> None:
        """Emit one custom parser metric sample.

        Example:
            await self.metric("items_seen", 1, {"source": "catalog"})
        """
        ...
    async def write_text(self, path: str | Path, data: str, *, encoding: str = "utf-8") -> Path:
        """Write text below the run output workspace and return its path."""
        ...
    async def write_bytes(self, path: str | Path, data: bytes) -> Path:
        """Write bytes below the run output workspace and return its path."""
        ...
    def output_path(self, path: str | Path) -> Path:
        """Resolve a path below the run output workspace."""
        ...
    async def init(self) -> None:
        """Run once before parser work starts."""
        ...
    async def destroy(self) -> None:
        """Run once after parser work finishes or aborts."""
        ...
    async def init_thread(self) -> None:
        """Run before a worker thread starts processing items."""
        ...
    async def destroy_thread(self) -> None:
        """Run after a worker thread stops processing items."""
        ...
    async def parse(self, query: Any) -> None:
        """Handle one queue item.

        Example:
            response = await self.get(str(query))
            await self.publish_json(name="last-item", payload=response.json())
        """
        ...

def metric_payload(
    name: str,
    value: int | float = 1.0,
    labels: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Validate and normalize a custom metric payload before host emission."""
    ...
