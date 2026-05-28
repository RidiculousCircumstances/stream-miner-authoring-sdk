"""Types for parser-facing Egress lease control."""

from dataclasses import dataclass
from typing import Any, Protocol

from stream_miner_sdk import _vocabularies as vocab

@dataclass(frozen=True, slots=True)
class EgressLease:
    """Runtime reservation for one Egress member compatible with the request."""

    lease_id: str
    pool_key: str | None = None
    item_type: vocab.TypeValue | None = None
    endpoint: str | None = None
    endpoint_url: str | None = None
    transport_mode: vocab.ModeValue | None = None
    metadata: dict[str, Any] = ...

@dataclass(frozen=True, slots=True)
class EgressSelector:
    """Selector for an exact lease, transport mode, or Egress member type."""

    lease_id: str | None = None
    http_mode: vocab.ModeValue | None = None
    item_type: vocab.TypeValue | None = None
    def to_payload(self) -> dict[str, Any]: ...

class EgressFacade(Protocol):
    """Parser-facing operations; Agent owns the actual lease lifecycle."""

    async def current(self, selector: EgressSelector | None = None) -> EgressLease | None: ...
    async def release(
        self,
        selector: EgressSelector | None = None,
        *,
        reason: str | None = None,
    ) -> None: ...
    async def next(
        self,
        selector: EgressSelector | None = None,
        *,
        reason: str | None = None,
    ) -> EgressLease: ...
    async def ban(
        self,
        selector: EgressSelector | None = None,
        *,
        ttl_sec: int | None = None,
        reason: str | None = None,
    ) -> EgressLease | None: ...
