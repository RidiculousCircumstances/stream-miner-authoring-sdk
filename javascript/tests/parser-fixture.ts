import {
  BaseParser,
  ItemRetry,
  configField,
  defineConfig,
  type ConfigObject,
  type ParseSet,
  type RequestOptions,
} from 'stream-miner-sdk';

interface ParserConfig extends ConfigObject {
  start_url: string;
  retries: number;
}

export default class Parser extends BaseParser<ParserConfig> {
  static parserAlias = 'authoring_fixture_js';

  static Config = defineConfig({
    start_url: configField('https://example.test', {
      label: 'Start URL',
      description: 'First URL used when the queue item does not provide one.',
    }),
    retries: configField(2, {label: 'Retries', type: 'number'}),
  });

  async parse(set: ParseSet, results: Record<string, unknown>) {
    const options: RequestOptions = {
      retries: this.conf.retries,
      allowStatuses: [200],
      validateResponse: response => response.ok,
    };
    const response = await this.get(String(set.query || this.conf.start_url), {}, options);
    if (!response.ok) {
      throw new ItemRetry('http_error', {
        maxAttempts: 3,
        metadata: {status: response.status},
      });
    }

    await this.egress.next({httpMode: this.runtime.http_transport_mode});
    await this.metric('items_parsed', 1, {source: 'fixture'});
    await this.publishJson('last-item', response.json());
    results.success = true;
    return results;
  }
}
