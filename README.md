# Stream Miner Authoring SDK

Public authoring packages for Stream Miner parser developers.

This repository contains type surfaces.

## Packages

- `python/`: `stream-miner-sdk-stubs`, a PEP 561 stub-only package for the
  `stream_miner_sdk` import surface.
- `javascript/`: `stream-miner-sdk`, a declaration-only npm package for the
  JavaScript/TypeScript parser SDK import surface.
- `go/`: v1 design note. Go authoring types are deferred because Go parser code
  compiles against a real module.

## Verify

```bash
make verify
```

Run one language:

```bash
make verify-python
make verify-javascript
```

Inspect publish artifacts:

```bash
make pack-python
make pack-javascript
```

## Examples

- `python/examples/catalog_parser.py`: Python parser example using typed config,
  HTTP, Egress, metrics, datasets, and run-local outputs.
- `javascript/examples/catalog-parser.ts`: JavaScript/TypeScript parser example
  using the same authoring surface.

