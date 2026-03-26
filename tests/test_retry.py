"""Tests for retry logic, rate limiting, and error handling."""

from __future__ import annotations

import httpx
import pytest
import respx

from myonlinestore import ConnectClient, ConnectError, RateLimitError, ServerError
from myonlinestore.config import ConnectConfig


BASE = "https://api.myonlinestore.com/v1"


@respx.mock
def test_retry_on_500(config_with_retries: ConnectConfig) -> None:
    """Should retry on 500 and succeed on the next attempt."""
    client = ConnectClient(config=config_with_retries)
    route = respx.get(f"{BASE}/articles").mock(
        side_effect=[
            httpx.Response(500, json={"title": "Internal Server Error"}),
            httpx.Response(200, json=[{"id": 1, "name": "Product"}]),
        ]
    )
    page = client.articles.list()

    assert route.call_count == 2
    assert len(page.items) == 1


@respx.mock
def test_retry_exhausted_raises(config_with_retries: ConnectConfig) -> None:
    """Should raise after all retries are exhausted."""
    client = ConnectClient(config=config_with_retries)
    route = respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(500, json={"title": "Internal Server Error"})
    )
    with pytest.raises(ServerError):
        client.articles.list()

    # Should have attempted 1 initial + 2 retries = 3 total
    assert route.call_count == 3


@respx.mock
def test_no_retry_on_404() -> None:
    """Should NOT retry on 404 (not a transient error)."""
    config = ConnectConfig(store_token="t", max_retries=2, idempotency_key_header=None)
    client = ConnectClient(config=config)
    route = respx.get(f"{BASE}/articles/999").mock(
        return_value=httpx.Response(404, json={"title": "Not Found"})
    )
    with pytest.raises(Exception):
        client.articles.get(article_id=999)

    assert route.call_count == 1  # No retry


@respx.mock
def test_retry_respects_retry_after_header(config_with_retries: ConnectConfig) -> None:
    """Should respect Retry-After header on 429."""
    client = ConnectClient(config=config_with_retries)
    respx.get(f"{BASE}/articles").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "0"}, json={"title": "Rate limited"}),
            httpx.Response(200, json=[]),
        ]
    )
    page = client.articles.list()

    assert page.items == []


@respx.mock
def test_no_retry_when_disabled() -> None:
    """max_retries=0 should disable all retries."""
    config = ConnectConfig(store_token="t", max_retries=0, idempotency_key_header=None)
    client = ConnectClient(config=config)
    route = respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(500, json={"title": "Error"})
    )
    with pytest.raises(ServerError):
        client.articles.list()

    assert route.call_count == 1


@respx.mock
def test_exception_chaining_on_timeout() -> None:
    """Timeout exceptions should be chained with 'from' for traceback."""
    config = ConnectConfig(store_token="t", max_retries=0, idempotency_key_header=None)
    client = ConnectClient(config=config)
    respx.get(f"{BASE}/articles").mock(side_effect=httpx.ReadTimeout("timed out"))

    with pytest.raises(ConnectError) as exc_info:
        client.articles.list()

    # Verify exception chaining
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, httpx.ReadTimeout)
