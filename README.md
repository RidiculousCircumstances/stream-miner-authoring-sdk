# Stream Miner Authoring SDK

Public authoring packages for Stream Miner parser developers.

This repository intentionally contains type surfaces only. It does not contain
Stream Miner platform runtime code, Control Plane code, Agent code, queue
adapters, persistence code, or UI code.

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

## Publish

Use the per-package READMEs:

- `python/README.md`
- `javascript/README.md`

