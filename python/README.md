# Stream Miner Python SDK Stubs

This package is the Python authoring surface for parser developers. It publishes
PEP 561-style stubs for the public `stream_miner_sdk` import names so IDEs and
type checkers can guide parser code without installing Stream Miner runtime
services.

Use it when writing parser code in a client repository. The parser still runs
inside Stream Miner through the platform-pinned SDK and Agent host protocol.

## What Is Included

- `stream_miner_sdk` `.pyi` declarations for public parser SDK names.
- Comments and docstrings that explain what each facade means at authoring
  time.
- No Control Plane, Agent, framework, database, queue, Proxy Manager, or Stats
  Forge implementation code.

## What Is Not Included

- No local HTTP, Egress, queue, log, metric, asset, or output execution.
- No runtime host binding.
- No compatibility shim for importing platform internals.

If parser code needs to execute platform operations, publish it through Control
Plane and let the platform run it with the pinned runtime SDK.

## Package Names

- Distribution name: `stream-miner-sdk-stubs`.
- Imported package covered by the stubs: `stream_miner_sdk`.
- Runtime implementation: platform-owned, not included here.

## Client Installation

For a client parser repository:

```bash
python -m pip install --upgrade stream-miner-sdk-stubs
```

Then parser code can keep the normal import surface:

```python
from stream_miner_sdk import BaseParser, RequestOptions, config_field
```

## Maintainer Checklist Before Publish

- Confirm the public surface still matches the Stream Miner platform SDK
  contract for the target release.
- Run authoring type verification from the repository root.
- Build a clean wheel and source distribution.
- Upload to TestPyPI first.
- Install from TestPyPI in a temporary environment and typecheck a fixture.
- Publish the same version to PyPI.
- Do not reuse a version after upload; PyPI files are immutable.

## Maintainer Commands

From the repository root:

```bash
make verify-python
make verify
git diff --check
```

## Example

This repository includes `examples/catalog_parser.py`, a copyable parser example
that exercises typed config, HTTP, Egress, metrics, datasets, and run-local
outputs.

Build and inspect the package:

```bash
cd python
python -m pip install --upgrade build twine setuptools wheel
rm -rf dist
python -m build
python -m twine check dist/*
```

Copy the repository example into a parser project:

```bash
cp examples/catalog_parser.py ./catalog_parser.py
```

Publish to TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

Install from TestPyPI in a scratch virtual environment:

```bash
python -m venv /tmp/stream-miner-sdk-stubs-check
/tmp/stream-miner-sdk-stubs-check/bin/python -m pip install --upgrade pip mypy
/tmp/stream-miner-sdk-stubs-check/bin/python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  stream-miner-sdk-stubs==0.1.0
/tmp/stream-miner-sdk-stubs-check/bin/python -m mypy \
  --config-file mypy.ini \
  tests/fixture_parser.py
```

Publish to PyPI:

```bash
python -m twine upload dist/*
```

## Preferred Registry Automation

For CI publishing, use PyPI Trusted Publishing/OIDC instead of a long-lived
PyPI token. Configure the PyPI project to trust the exact GitHub repository,
workflow file, and protected release environment before enabling automatic
publication.
