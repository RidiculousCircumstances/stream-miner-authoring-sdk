# Stream Miner JavaScript Authoring Types

This package is the JavaScript/TypeScript authoring surface for parser
developers. It exposes declarations for the public `stream-miner-sdk` module
without shipping the platform runtime implementation.

Use it when writing parser code in a client repository. The parser runs inside
Stream Miner through the platform-pinned SDK and Agent host protocol.

## Included

- `index.d.ts` declarations for public parser SDK names.
- JSDoc comments for IDE hover help.
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

## Client Installation

For a client parser repository:

```bash
npm install --save-dev stream-miner-sdk
```

Then parser code can keep the normal import surface:

```ts
import { BaseParser, configField, defineConfig } from 'stream-miner-sdk';
```

This package contains declarations only. Parser code that needs HTTP, Egress,
queue, logs, metrics, assets, or outputs must be published and run through
Stream Miner.

## Maintainer Checklist Before Publish

- Confirm the public surface still matches the platform JavaScript SDK contract.
- Run authoring type verification from the repository root.
- Inspect the npm tarball contents before publishing.
- Publish with public access.
- Install the published package in a scratch project and run `tsc --noEmit`.
- Do not reuse a version after upload.

## Maintainer Commands

From the repository root:

```bash
make verify-javascript
make verify
git diff --check
```

Inspect the package:

```bash
cd javascript
npm ci
npm run typecheck
npm run pack:dry-run
```

Publish to npm:

```bash
npm login
npm publish --access public
```

Install in a scratch project:

```bash
mkdir -p /tmp/stream-miner-sdk-npm-check
cd /tmp/stream-miner-sdk-npm-check
npm init -y
npm install --save-dev typescript stream-miner-sdk@0.1.0
cat > parser.ts <<'EOF'
import { BaseParser, configField, defineConfig } from 'stream-miner-sdk';

export default class Parser extends BaseParser {
  static parserAlias = 'install_check';
  static Config = defineConfig({
    start_url: configField('https://example.test', { label: 'Start URL' }),
  });
}
EOF
npx tsc --noEmit --strict --moduleResolution bundler --module ESNext --target ES2022 parser.ts
```

## Preferred Registry Automation

For cloud-hosted CI, use npm Trusted Publishing/OIDC and provenance instead of
a long-lived npm token. For a self-hosted runner, npm Trusted Publishing may not
be available yet; use manual publish or a tightly scoped npm automation token
until the registry supports your runner model.
