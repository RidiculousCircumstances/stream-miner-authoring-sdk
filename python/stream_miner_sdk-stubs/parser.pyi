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
    def logger(self) -> Any: ...
    @property
    def egress(self) -> EgressFacade: ...
    @property
    def queue(self) -> Any: ...
    @property
    def results_dir(self) -> Path: ...
    @property
    def cookies(self) -> Any: ...
    @property
    def runtime(self) -> RunContext: ...
    def thread_id(self) -> str: ...
    async def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        body: Any | None = None,
        options: RequestOptions | None = None,
    ) -> HttpResponse: ...
    async def read_sensitive_asset(self, asset_ref: int | str) -> bytes: ...
    async def publish_dataset(
        self,
        *,
        name: str,
        path: str | Path | None = None,
        content: bytes | str | None = None,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DatasetRef: ...
    async def register_output(
        self,
        *,
        handle: str,
        path: str | Path,
        output_kind: vocab.KindValue = ...,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LocalOutputHandle: ...
    async def metric(
        self,
        name: str,
        value: int | float = 1.0,
        labels: Mapping[str, str] | None = None,
    ) -> None: ...

class BaseParser(Generic[TConfig]):
    """Base class for Python parsers. Runtime operations call the Agent host."""

    __parser_alias__: ClassVar[str]
    Config: ClassVar[type[Any] | None]
    DEFAULT_PLUGINS: ClassVar[dict[str, Any]]
    conf: TConfig

    @classmethod
    def default_config(cls) -> dict[str, Any]: ...
    @classmethod
    def config_fields(cls) -> tuple[ParserConfigField, ...]: ...
    @classmethod
    def build_config(cls, raw: dict[str, Any] | None) -> TConfig: ...
    @property
    def logger(self) -> Any: ...
    @property
    def egress(self) -> EgressFacade: ...
    @property
    def queue(self) -> Any: ...
    @property
    def results_dir(self) -> Path: ...
    @property
    def cookies(self) -> Any: ...
    @property
    def runtime(self) -> RunContext: ...
    def thread_id(self) -> str: ...
    async def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        body: Any | None = None,
        options: RequestOptions | None = None,
    ) -> HttpResponse: ...
    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> HttpResponse: ...
    async def post(
        self,
        url: str,
        body: Any | None = None,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> HttpResponse: ...
    async def get_json(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> Any: ...
    async def post_json(
        self,
        url: str,
        payload: Any,
        params: dict[str, Any] | None = None,
        *,
        options: RequestOptions | None = None,
    ) -> Any: ...
    async def read_sensitive_asset(self, asset_ref: int | str) -> bytes: ...
    async def read_sensitive_text(self, asset_ref: int | str, *, encoding: str = "utf-8") -> str: ...
    async def publish_dataset(
        self,
        *,
        name: str,
        path: str | Path | None = None,
        content: bytes | str | None = None,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DatasetRef: ...
    async def publish_json(
        self,
        *,
        name: str,
        payload: Any,
        metadata: dict[str, Any] | None = None,
    ) -> DatasetRef: ...
    async def register_output(
        self,
        *,
        handle: str,
        path: str | Path,
        output_kind: vocab.KindValue = ...,
        content_type: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LocalOutputHandle: ...
    async def metric(
        self,
        name: str,
        value: int | float = 1.0,
        labels: Mapping[str, str] | None = None,
    ) -> None: ...
    async def write_text(self, path: str | Path, data: str, *, encoding: str = "utf-8") -> Path: ...
    async def write_bytes(self, path: str | Path, data: bytes) -> Path: ...
    def output_path(self, path: str | Path) -> Path: ...
    async def init(self) -> None: ...
    async def destroy(self) -> None: ...
    async def init_thread(self) -> None: ...
    async def destroy_thread(self) -> None: ...
    async def parse(self, query: Any) -> None: ...

def metric_payload(
    name: str,
    value: int | float = 1.0,
    labels: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Validate and normalize a custom metric payload before host emission."""
    ...
