from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from stream_miner_sdk import BaseParser, EgressSelector, ItemRetry, RequestOptions, config_field


@dataclass
class CatalogConfig:
    start_url: str = config_field(
        "https://example.test/catalog.json",
        label="Start URL",
        description="Catalog endpoint used when the queue item is empty.",
    )
    retries: int = config_field(
        2,
        label="Retries",
        type="number",
        description="Per-request retry count for catalog fetches.",
    )


class CatalogParser(BaseParser[CatalogConfig]):
    __parser_alias__ = "catalog_example_py"
    Config = CatalogConfig

    async def parse(self, query: Any) -> None:
        url = str(query or self.conf.start_url)
        response = await self.get(
            url,
            options=RequestOptions(
                retries=self.conf.retries,
                allow_statuses={200},
                validate_response=lambda item: item.ok,
            ),
        )
        if not response.ok:
            raise ItemRetry(
                "catalog_http_error",
                max_attempts=3,
                retry_delay_sec=30,
                metadata={"status": response.status, "url": url},
            )

        lease = await self.egress.next(
            EgressSelector(http_mode=self.runtime.http_transport_mode),
            reason="catalog_fetch",
        )
        payload = response.json()
        output_path = await self.write_text("catalog/last-response.json", response.text())

        await self.metric(
            "catalog_pages_seen",
            1,
            {"transport": str(lease.transport_mode or "unknown")},
        )
        await self.publish_json(
            name="catalog-last-response",
            payload=payload,
            metadata={"url": url},
        )
        await self.register_output(
            handle="last-response",
            path=output_path,
            output_kind="file",
            content_type="application/json",
            metadata={"url": url},
        )
