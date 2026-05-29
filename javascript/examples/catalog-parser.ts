import {
  BaseParser,
  ItemRetry,
  configField,
  defineConfig,
  type ConfigObject,
  type ParseSet,
  type RequestOptions,
} from 'stream-miner-sdk';

interface CatalogConfig extends ConfigObject {
  start_url: string;
  retries: number;
}

export default class CatalogParser extends BaseParser<CatalogConfig> {
  static parserAlias = 'catalog_example_js';

  static Config = defineConfig({
    start_url: configField('https://example.test/catalog.json', {
      label: 'Start URL',
      description: 'Catalog endpoint used when the queue item is empty.',
    }),
    retries: configField(2, {
      label: 'Retries',
      type: 'number',
      description: 'Per-request retry count for catalog fetches.',
    }),
  });

  async parse(set: ParseSet, results: Record<string, unknown>) {
    const url = String(set.query || this.conf.start_url);
    const options: RequestOptions = {
      retries: this.conf.retries,
      allowStatuses: [200],
      validateResponse: response => response.ok,
    };

    const response = await this.get(url, {}, options);
    if (!response.ok) {
      throw new ItemRetry('catalog_http_error', {
        maxAttempts: 3,
        retryDelaySec: 30,
        metadata: {status: response.status, url},
      });
    }

    const lease = await this.egress.next({
      httpMode: this.runtime.http_transport_mode,
      reason: 'catalog_fetch',
    });
    const payload = response.json();
    const outputPath = 'catalog/last-response.json';

    await this.metric('catalog_pages_seen', 1, {
      transport: String(lease.transport_mode || 'unknown'),
    });
    await this.publishJson('catalog-last-response', payload, {
      metadata: {url},
    });
    await this.writeText(outputPath, JSON.stringify(payload, null, 2));
    await this.registerOutput('last-response', outputPath, {
      outputKind: 'file',
      contentType: 'application/json',
      metadata: {url},
    });

    results.url = url;
    results.dataset = 'catalog-last-response';
    return results;
  }
}
