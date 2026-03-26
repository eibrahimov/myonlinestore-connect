"""Shared fixtures for MyOnlineStore SDK tests."""

from __future__ import annotations

import pytest

from myonlinestore import ConnectClient
from myonlinestore.config import ConnectConfig
from myonlinestore.http import HttpTransport

BASE_URL = "https://api.myonlinestore.com"
STORE_TOKEN = "test-store-token"
PARTNER_TOKEN = "test-partner-token"


@pytest.fixture
def config() -> ConnectConfig:
    """A ConnectConfig with retries disabled for deterministic tests."""
    return ConnectConfig(
        store_token=STORE_TOKEN,
        partner_token=PARTNER_TOKEN,
        max_retries=0,  # Disable retries in unit tests
        idempotency_key_header=None,  # Disable idempotency for predictable headers
    )


@pytest.fixture
def config_with_retries() -> ConnectConfig:
    """A ConnectConfig with retries enabled for retry-specific tests."""
    return ConnectConfig(
        store_token=STORE_TOKEN,
        partner_token=PARTNER_TOKEN,
        max_retries=2,
        idempotency_key_header="Idempotency-Key",
    )


@pytest.fixture
def transport(config: ConnectConfig) -> HttpTransport:
    return HttpTransport(config)


@pytest.fixture
def client(config: ConnectConfig) -> ConnectClient:
    return ConnectClient(config=config)


# -- Sample API response data -----------------------------------------------

@pytest.fixture
def sample_article() -> dict:
    return {
        "id": 42,
        "name": "Test Product",
        "uuid": "abc-123-def",
        "description": "A test product",
        "price": {"default": "19.99", "action": None, "purchase": "10.00"},
        "stock": 100,
        "weight": "0.5",
        "visible": True,
    }


@pytest.fixture
def sample_order() -> dict:
    return {
        "order_number": "1001",
        "status": 1,
        "debtor": {"email": "test@example.com", "name": "Test User"},
        "price": {"total": "49.99", "tax": []},
        "comments": {"customer": None, "internal": None},
        "details": [],
    }


@pytest.fixture
def sample_customer() -> dict:
    return {
        "id": "cust-uuid-99",
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane@example.com",
        "company": "Test Corp",
    }


@pytest.fixture
def sample_payment() -> dict:
    return {
        "id": "pay_123",
        "gateway": "ideal",
        "method": "ideal",
        "price": "25.00",
        "currency": "EUR",
        "createdAt": "2024-01-15T10:00:00Z",
        "updatedAt": "2024-01-15T10:05:00Z",
        "mutations": [],
    }


@pytest.fixture
def sample_category() -> dict:
    return {
        "id": 5,
        "name": "Electronics",
        "visible": True,
    }
