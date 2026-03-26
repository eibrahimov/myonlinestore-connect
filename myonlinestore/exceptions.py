"""Exception classes for the MyOnlineStore Connect API client."""

from __future__ import annotations

from typing import Any


class ConnectError(Exception):
    """Base exception for all API errors.

    Attributes:
        status_code: HTTP status code (``None`` for connection errors).
        body: Parsed response body (dict or string).
    """

    def __init__(self, message: str, status_code: int | None = None, body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return f"{type(self).__name__}(message={str(self)!r}, status_code={self.status_code!r})"


class AuthenticationError(ConnectError):
    """Raised on 401 / 403 responses (bad or missing token)."""


class NotFoundError(ConnectError):
    """Raised on 404 responses."""


class ValidationError(ConnectError):
    """Raised on 422 responses (RFC 7807 problem details).

    Attributes:
        detail: The ``detail`` field from the RFC 7807 error body, if present.
    """

    def __init__(self, message: str, status_code: int = 422, body: Any = None, detail: str | None = None):
        super().__init__(message, status_code, body)
        self.detail = detail

    def __repr__(self) -> str:
        return (
            f"ValidationError(message={str(self)!r}, status_code={self.status_code!r}, "
            f"detail={self.detail!r})"
        )


class RateLimitError(ConnectError):
    """Raised on 429 responses.

    Attributes:
        retry_after: Value of the ``Retry-After`` header in seconds, or ``None``.
    """

    def __init__(
        self, message: str, status_code: int = 429, body: Any = None, retry_after: float | None = None,
    ):
        super().__init__(message, status_code, body)
        self.retry_after = retry_after


class ServerError(ConnectError):
    """Raised on 5xx responses."""
