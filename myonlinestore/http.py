"""Low-level HTTP transport shared by all resources."""

from __future__ import annotations

import asyncio
import logging
import random
import time
import uuid
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from myonlinestore.config import ConnectConfig
from myonlinestore.exceptions import (
    AuthenticationError,
    ConnectError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)

logger = logging.getLogger("myonlinestore")

# Retry-eligible status codes
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

# Methods that are always safe to retry (idempotent by HTTP spec)
_IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS"})


class HttpTransport:
    """Thin wrapper around ``httpx`` that handles auth, versioning, retries, and errors.

    This is an internal class — end-users interact with :class:`ConnectClient`
    and its resource attributes instead.

    Features:
        - Automatic retries with exponential backoff + jitter for transient errors.
        - Respects ``Retry-After`` headers on 429 responses.
        - Idempotency key injection for POST/PATCH requests (safe retries).
        - Structured logging of all requests.
        - Granular timeout configuration (connect / read / pool).
        - Connection pooling via httpx.
    """

    def __init__(self, config: ConnectConfig) -> None:
        self.config = config
        self._sync_client: httpx.Client | None = None
        self._async_client: httpx.AsyncClient | None = None

    # -- Timeout & pool helpers --------------------------------------------------

    def _build_timeout(self) -> httpx.Timeout:
        return httpx.Timeout(
            timeout=self.config.timeout,
            connect=self.config.connect_timeout or self.config.timeout,
            read=self.config.read_timeout or self.config.timeout,
            pool=self.config.pool_timeout,
        )

    def _build_limits(self) -> httpx.Limits:
        return httpx.Limits(
            max_connections=self.config.max_connections,
            max_keepalive_connections=self.config.max_keepalive,
        )

    # -- Lazy client construction ------------------------------------------------

    @property
    def sync_client(self) -> httpx.Client:
        if self._sync_client is None:
            self._sync_client = httpx.Client(
                timeout=self._build_timeout(),
                limits=self._build_limits(),
                follow_redirects=True,
            )
        return self._sync_client

    @property
    def async_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                timeout=self._build_timeout(),
                limits=self._build_limits(),
                follow_redirects=True,
            )
        return self._async_client

    # -- Lifecycle ---------------------------------------------------------------

    def close(self) -> None:
        if self._sync_client is not None:
            self._sync_client.close()
            self._sync_client = None

    async def aclose(self) -> None:
        if self._async_client is not None:
            await self._async_client.aclose()
            self._async_client = None

    # -- Request helpers ---------------------------------------------------------

    def _build_url(self, path: str, version: str | None = None) -> str:
        return self.config.versioned_url(path, version)

    def _merge_params(self, params: dict[str, Any] | None) -> dict[str, Any]:
        merged = dict(self.config.default_params())
        if params:
            merged.update({k: v for k, v in params.items() if v is not None})
        return merged

    @staticmethod
    def _parse_retry_after(response: httpx.Response) -> float | None:
        """Extract wait time from Retry-After header (seconds or HTTP-date)."""
        header = response.headers.get("Retry-After")
        if header is None:
            return None
        # Try numeric first
        try:
            return float(header)
        except ValueError:
            pass
        # Try HTTP-date format
        try:
            retry_date = parsedate_to_datetime(header)
            delay = (retry_date - datetime.now(retry_date.tzinfo)).total_seconds()
            return max(0, delay)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _redact_params(params: dict[str, Any]) -> dict[str, Any]:
        """Redact sensitive values from params for logging."""
        sensitive = {"token", "partner_token"}
        return {k: "***" if k in sensitive else v for k, v in params.items()}

    @staticmethod
    def _raise_for_status(response: httpx.Response, retry_after: float | None = None) -> None:
        """Translate HTTP error status codes into typed exceptions."""
        code = response.status_code
        if code < 400:
            return

        try:
            body = response.json()
        except (ValueError, KeyError):
            body = response.text[:500] if response.text else None

        message = ""
        if isinstance(body, dict):
            message = body.get("title", body.get("message", ""))
        if not message:
            message = f"HTTP {code}"

        if code in (401, 403):
            raise AuthenticationError(message, code, body)
        if code == 404:
            raise NotFoundError(message, code, body)
        if code == 422:
            detail = body.get("detail") if isinstance(body, dict) else None
            raise ValidationError(message, code, body, detail=detail)
        if code == 429:
            raise RateLimitError(message, code, body, retry_after=retry_after)
        if code >= 500:
            raise ServerError(message, code, body)

        raise ConnectError(message, code, body)

    def _backoff_delay(self, attempt: int) -> float:
        """Exponential backoff with full jitter: ``random(0, min(cap, base * 2^attempt))``."""
        base = 0.5
        cap = min(self.config.max_retry_delay, 30.0)
        delay = min(cap, base * (2 ** attempt))
        return random.uniform(0, delay)

    def _should_retry(self, method: str, exc: Exception, attempt: int) -> bool:
        """Decide whether to retry the request."""
        if attempt >= self.config.max_retries:
            return False

        # Always retry timeouts and connection errors
        if isinstance(exc, (httpx.TimeoutException, httpx.ConnectError)):
            return True

        # Retry retryable HTTP status codes
        if isinstance(exc, ConnectError) and exc.status_code in _RETRYABLE_STATUS_CODES:
            # POST/PATCH only retried if idempotency keys are enabled
            if method not in _IDEMPOTENT_METHODS:
                return bool(self.config.idempotency_key_header)
            return True

        return False

    def _inject_idempotency_key(self, method: str, headers: dict[str, str]) -> dict[str, str]:
        """Add an idempotency key header for non-idempotent methods."""
        header_name = self.config.idempotency_key_header
        if header_name and method in ("POST", "PATCH") and header_name not in headers:
            headers[header_name] = str(uuid.uuid4())
        return headers

    def _prepare_request(
        self, method: str, path: str, params: dict[str, Any] | None, headers: dict[str, str] | None
    ) -> tuple[str, dict[str, Any], dict[str, str]]:
        """Prepare URL, merged params, and request headers for a request.

        Returns:
            Tuple of (url, merged_params, request_headers)
        """
        url = self._build_url(path)
        merged = self._merge_params(params)
        req_headers = dict(headers or {})
        self._inject_idempotency_key(method, req_headers)
        return url, merged, req_headers

    # -- Synchronous requests ----------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        version: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Make a synchronous HTTP request with automatic retries."""
        # Build URL with version prefix
        url = self._build_url(path, version)
        merged = self._merge_params(params)
        req_headers = dict(headers or {})
        self._inject_idempotency_key(method, req_headers)

        last_exc: Exception | None = None

        for attempt in range(self.config.max_retries + 1):
            if attempt > 0:
                delay = self._backoff_delay(attempt - 1)
                logger.info(
                    "Retry %d/%d for %s %s (delay=%.2fs)",
                    attempt, self.config.max_retries, method, path, delay,
                )
                time.sleep(delay)

            try:
                logger.debug("%s %s params=%s", method, url, self._redact_params(merged))
                response = self.sync_client.request(
                    method,
                    url,
                    params=merged,
                    json=json,
                    data=data,
                    files=files,
                    headers=req_headers or None,
                )

                # Check for Retry-After on 429 before raising
                retry_after = None
                if response.status_code == 429 and attempt < self.config.max_retries:
                    retry_after = self._parse_retry_after(response)
                    if retry_after is not None:
                        logger.info(
                            "Rate limited on %s %s, Retry-After=%.1fs",
                            method, path, retry_after,
                        )
                        time.sleep(min(retry_after, self.config.max_retry_delay))
                        continue

                self._raise_for_status(response, retry_after=retry_after)

                if response.status_code == 204 or not response.content:
                    return None
                return response.json()

            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                last_exc = exc
                if not self._should_retry(method, exc, attempt):
                    raise ConnectError(
                        f"Connection failed: {exc}", status_code=None, body=None,
                    ) from exc

            except ConnectError as exc:
                last_exc = exc
                if not self._should_retry(method, exc, attempt):
                    raise

        # All retries exhausted
        raise ConnectError(
            f"Max retries ({self.config.max_retries}) exceeded for {method} {path}",
            status_code=getattr(last_exc, "status_code", None),
            body=getattr(last_exc, "body", None),
        ) from last_exc

    def get(self, path: str, *, params: dict[str, Any] | None = None, version: str | None = None) -> Any:
        return self.request("GET", path, params=params, version=version)

    def post(self, path: str, *, json: Any = None, params: dict[str, Any] | None = None, files: Any = None, version: str | None = None) -> Any:
        return self.request("POST", path, json=json, params=params, files=files, version=version)

    def patch(self, path: str, *, json: Any = None, params: dict[str, Any] | None = None, version: str | None = None) -> Any:
        return self.request("PATCH", path, json=json, params=params, version=version)

    def delete(self, path: str, *, params: dict[str, Any] | None = None, version: str | None = None) -> Any:
        return self.request("DELETE", path, params=params, version=version)

    # -- Asynchronous requests ---------------------------------------------------

    async def arequest(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        version: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Make an asynchronous HTTP request with automatic retries."""
        # Build URL with version prefix
        url = self._build_url(path, version)
        merged = self._merge_params(params)
        req_headers = dict(headers or {})
        self._inject_idempotency_key(method, req_headers)

        last_exc: Exception | None = None

        for attempt in range(self.config.max_retries + 1):
            if attempt > 0:
                delay = self._backoff_delay(attempt - 1)
                logger.info(
                    "Retry %d/%d for %s %s (delay=%.2fs)",
                    attempt, self.config.max_retries, method, path, delay,
                )
                await asyncio.sleep(delay)

            try:
                logger.debug("%s %s params=%s", method, url, self._redact_params(merged))
                response = await self.async_client.request(
                    method,
                    url,
                    params=merged,
                    json=json,
                    data=data,
                    files=files,
                    headers=req_headers or None,
                )

                retry_after = None
                if response.status_code == 429 and attempt < self.config.max_retries:
                    retry_after = self._parse_retry_after(response)
                    if retry_after is not None:
                        logger.info(
                            "Rate limited on %s %s, Retry-After=%.1fs",
                            method, path, retry_after,
                        )
                        await asyncio.sleep(min(retry_after, self.config.max_retry_delay))
                        continue

                self._raise_for_status(response, retry_after=retry_after)

                if response.status_code == 204 or not response.content:
                    return None
                return response.json()

            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                last_exc = exc
                if not self._should_retry(method, exc, attempt):
                    raise ConnectError(
                        f"Connection failed: {exc}", status_code=None, body=None,
                    ) from exc

            except ConnectError as exc:
                last_exc = exc
                if not self._should_retry(method, exc, attempt):
                    raise

        raise ConnectError(
            f"Max retries ({self.config.max_retries}) exceeded for {method} {path}",
            status_code=getattr(last_exc, "status_code", None),
            body=getattr(last_exc, "body", None),
        ) from last_exc

    async def aget(self, path: str, *, params: dict[str, Any] | None = None, version: str | None = None) -> Any:
        return await self.arequest("GET", path, params=params, version=version)

    async def apost(self, path: str, *, json: Any = None, params: dict[str, Any] | None = None, files: Any = None, version: str | None = None) -> Any:
        return await self.arequest("POST", path, json=json, params=params, files=files, version=version)

    async def apatch(self, path: str, *, json: Any = None, params: dict[str, Any] | None = None, version: str | None = None) -> Any:
        return await self.arequest("PATCH", path, json=json, params=params, version=version)

    async def adelete(self, path: str, *, params: dict[str, Any] | None = None, version: str | None = None) -> Any:
        return await self.arequest("DELETE", path, params=params, version=version)
