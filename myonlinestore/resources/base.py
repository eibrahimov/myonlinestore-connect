"""Base resource class for API resources."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class Resource:
    """Base class for API resources."""

    def __init__(self, transport: HttpTransport) -> None:
        self._transport = transport

    def _list_params(
        self, limit: int | None, offset: int | None, **filters: Any
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        for k, v in filters.items():
            if v is not None:
                params[k] = v
        return params

    @staticmethod
    def _unwrap(data: Any, key: str) -> Any:
        """Unwrap a response that may be wrapped in ``{key: ...}``.

        Some endpoints return ``{"customer": {...}}`` or ``{"payments": [...]}``.
        This helper extracts the inner value when the wrapper is present,
        and returns *data* unchanged otherwise (for forward-compatibility).
        """
        if isinstance(data, dict) and key in data:
            return data[key]
        return data

    @staticmethod
    def _unwrap_list(data: Any, key: str) -> list[Any]:
        """Unwrap a list response that may be ``{key: [...]}`` or a flat list."""
        if isinstance(data, dict) and key in data:
            return data[key]
        if isinstance(data, list):
            return data
        return []
