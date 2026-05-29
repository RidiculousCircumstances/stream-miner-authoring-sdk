# Stream Miner JavaScript Authoring Types

This package is the JavaScript/TypeScript authoring surface for parser
developers. It exposes declarations for the public `stream-miner-sdk` module
without shipping the platform runtime implementation.

Use it when writing parser code in a client repository. The parser runs inside
Stream Miner through the platform-pinned SDK and Agent host protocol.

## Included

- `index.d.ts` declarations for public parser SDK names.
- JSDoc comments for IDE hover help.
- `examples/catalog-parser.ts`, a copyable parser example that exercises typed
  config, HTTP, Egress, metrics, datasets, and run-local outputs.
- A local TypeScript fixture used by repository verification.

## Not Included

- No executable `sdk.mjs`.
- No local HTTP, Egress, queue, log, metric, asset, or output execution.
- No Control Plane, Agent, framework, Proxy Manager, Stats Forge, or queue
  internals.

## Package Names

- npm package name: `stream-miner-sdk`.
- Type declaration entrypoint: `index.d.ts`.
- Runtime implementation: platform-owned, not included here.

## Installation

```bash
npm install --save-dev stream-miner-sdk
```

## Usage

```ts
import { BaseParser, configField, defineConfig } from 'stream-miner-sdk';
```

This package contains declarations only. Parser code that needs HTTP, Egress,
queue, logs, metrics, assets, or outputs must be published and run through
Stream Miner.

## Example

```ts
import { BaseParser, configField, defineConfig } from 'stream-miner-sdk';

export default class Parser extends BaseParser {
  static parserAlias = 'catalog_parser';

  static Config = defineConfig({
    start_url: configField('https://example.test', {
      label: 'Start URL',
    }),
  });
}
```

A full example parser is available at:

```bash
cp node_modules/stream-miner-sdk/examples/catalog-parser.ts ./catalog-parser.ts
```

## Type Checking

```bash
npm install
npx tsc --noEmit
```