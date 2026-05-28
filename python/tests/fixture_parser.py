from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from stream_miner_sdk import BaseParser, EgressSelector, ItemRetry, RequestOptions, config_field


@dataclass
class Config:
    start_url: str = config_field(
        "https://example.test",
        label="Start URL",
        description="First URL used when the queue item does not provide one.",
    )
    retries: int = config_field(2, label="Retries", type="number")


class Parser(BaseParser[Config]):
    __parser_alias__ = "authoring_fixture"
    Config = Config

    async def parse(self, query: Any) -> None:
        response = await self.get(
            str(query or self.conf.start_url),
            options=RequestOptions(
                retries=self.conf.retries,
                allow_statuses={200},
                validate_response=lambda item: item.ok,
            ),
        )
        if not response.ok:
            raise ItemRetry("http_error", max_attempts=3, metadata={"status": response.status})

        await self.egress.next(EgressSelector(http_mode=self.runtime.http_transport_mode))
        await self.metric("items_parsed", 1, {"source": "fixture"})
        await self.publish_json(name="last-item", payload=response.json())

