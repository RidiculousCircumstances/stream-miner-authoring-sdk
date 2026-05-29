"""Types for parser-authored config metadata."""

from dataclasses import Field
from typing import Any, Callable, Literal

ConfigFieldType = Literal["text", "number", "select", "multiselect"]
RawConfigOption = ConfigFieldOption | tuple[Any, str] | str | int | float | bool

class ConfigFieldOption:
    """One selectable config value as it appears in parser metadata."""

    value: str
    label: str | None
    def __init__(self, value: str, label: str | None = None) -> None:
        """Create one selectable config option."""
        ...
    def to_dict(self) -> dict[str, str | None]:
        """Serialize the option into parser revision metadata."""
        ...

class ParserConfigField:
    """Metadata for one parser config field extracted from a dataclass."""

    name: str
    label: str
    type: ConfigFieldType
    description: str | None
    placeholder: str | None
    options: tuple[ConfigFieldOption, ...]
    def __init__(
        self,
        name: str,
        label: str,
        type: ConfigFieldType = "text",
        description: str | None = None,
        placeholder: str | None = None,
        options: tuple[ConfigFieldOption, ...] = ...,
    ) -> None:
        """Create metadata for one parser config field."""
        ...
    def to_dict(self) -> dict[str, Any]:
        """Serialize the field into parser revision metadata."""
        ...

def config_field(
    default: Any = ...,
    *,
    default_factory: Callable[[], Any] | object = ...,
    label: str | None = None,
    type: ConfigFieldType | None = None,
    description: str | None = None,
    placeholder: str | None = None,
    choices: list[Any] | tuple[Any, ...] | None = None,
    options: list[RawConfigOption] | tuple[RawConfigOption, ...] | None = None,
) -> Any:
    """Declare parser config metadata on a dataclass field.

    Example:
        start_url: str = config_field("https://example.test", label="Start URL")
    """
    ...

def config_defaults(config_cls: type[Any]) -> dict[str, Any]:
    """Return default config values extracted from the parser Config dataclass."""
    ...

def config_fields(config_cls: type[Any]) -> tuple[ParserConfigField, ...]:
    """Return field metadata extracted from the parser Config dataclass."""
    ...

def build_config(config_cls: type[Any], raw: dict[str, Any] | None) -> Any:
    """Build a typed Config instance from raw Control Plane config values."""
    ...

def typed_config_schema(config_cls: type[Any]) -> dict[str, Any]:
    """Return the metadata schema written into parser revision metadata."""
    ...
