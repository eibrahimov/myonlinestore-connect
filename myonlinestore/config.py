"""Configuration for the MyOnlineStore Connect API client."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ConnectConfig:
    """Configuration for connecting to the MyOnlineStore API.

    Args:
        store_token: Merchant-specific API token (created in Settings > API).
        partner_token: Partner application token (obtained by registering your app).
        api_version: API version to use. Either ``"1"`` (stable) or ``"2-beta"``.
        base_url: Base URL for the API.
        language: Default language code for responses (e.g. ``"nl_NL"``, ``"en_GB"``).
        response_format: Response format — ``"json"`` or ``"xml"``.
        timeout: Request timeout in seconds (default for all phases).
        connect_timeout: TCP connection timeout in seconds. Falls back to *timeout*.
        read_timeout: Response read timeout in seconds. Falls back to *timeout*.
        pool_timeout: Connection pool acquire timeout in seconds.
        max_connections: Maximum concurrent connections in the pool.
        max_keepalive: Maximum keep-alive connections in the pool.
        default_limit: Default page size for list endpoints (max 100).
        max_retries: Number of automatic retries on transient errors (429, 5xx, timeouts).
            Set to ``0`` to disable retries.
        idempotency_key_header: Header name used for idempotency keys on POST/PATCH.
            Set to ``None`` to disable.
    """

    store_token: str
    partner_token: str | None = None
    api_version: str = "1"
    base_url: str = "https://api.myonlinestore.com"
    language: str = "nl_NL"
    response_format: str = "json"

    # Timeouts (seconds)
    timeout: float = 30.0
    connect_timeout: float | None = None
    read_timeout: float | None = None
    pool_timeout: float = 30.0

    # Connection pool
    max_connections: int = 100
    max_keepalive: int = 20

    # Pagination
    default_limit: int = 50

    # Retry policy
    max_retries: int = 3
    max_retry_delay: float = 60.0

    # Idempotency
    idempotency_key_header: str | None = "Idempotency-Key"

    def auth_params(self) -> dict[str, str]:
        """Return query parameters used for authentication."""
        params: dict[str, str] = {"token": self.store_token}
        if self.partner_token:
            params["partner_token"] = self.partner_token
        return params

    def default_params(self) -> dict[str, str]:
        """Return default query parameters included on every request."""
        params = self.auth_params()
        params["language"] = self.language
        params["format"] = self.response_format
        return params

    def versioned_url(self, path: str, version: str | None = None) -> str:
        """Build a full URL with version prefix.

        Args:
            path: Path without version prefix, e.g. ``"/articles"``.
            version: Override API version for this request.
        """
        v = version or self.api_version
        return f"{self.base_url.rstrip('/')}/v{v}{path}"
