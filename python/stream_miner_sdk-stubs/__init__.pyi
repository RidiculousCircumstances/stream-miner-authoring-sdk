"""Stub-only authoring surface for Stream Miner Python parser code.

These declarations are for editors and type checkers. Platform execution is
owned by Control Plane, Parser Builder, Agent, and the runner host protocol.
"""

from stream_miner_sdk.artifacts import DatasetRef as DatasetRef
from stream_miner_sdk.artifacts import LocalOutputHandle as LocalOutputHandle
from stream_miner_sdk.config import ConfigFieldOption as ConfigFieldOption
from stream_miner_sdk.config import ConfigFieldType as ConfigFieldType
from stream_miner_sdk.config import ParserConfigField as ParserConfigField
from stream_miner_sdk.config import config_field as config_field
from stream_miner_sdk.context import RunContext as RunContext
from stream_miner_sdk.egress import EgressFacade as EgressFacade
from stream_miner_sdk.egress import EgressLease as EgressLease
from stream_miner_sdk.egress import EgressSelector as EgressSelector
from stream_miner_sdk.errors import ItemFail as ItemFail
from stream_miner_sdk.errors import ItemRetry as ItemRetry
from stream_miner_sdk.errors import ParserError as ParserError
from stream_miner_sdk.errors import RunFail as RunFail
from stream_miner_sdk.http import HttpResponse as HttpResponse
from stream_miner_sdk.http import RequestOptions as RequestOptions
from stream_miner_sdk.parser import BaseParser as BaseParser

__all__: list[str]
