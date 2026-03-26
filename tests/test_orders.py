"""Tests for the Orders resource."""

from __future__ import annotations

import httpx
import respx

from myonlinestore import ConnectClient
from myonlinestore.models import Order, Payment


BASE = "https://api.myonlinestore.com/v1"


@respx.mock
def test_list_orders(client: ConnectClient, sample_order: dict) -> None:
    respx.get(f"{BASE}/orders").mock(
        return_value=httpx.Response(200, json=[sample_order])
    )
    page = client.orders.list(limit=10)

    assert len(page.items) == 1
    assert isinstance(page.items[0], Order)


@respx.mock
def test_get_order(client: ConnectClient, sample_order: dict) -> None:
    respx.get(f"{BASE}/orders/1001").mock(
        return_value=httpx.Response(200, json=sample_order)
    )
    order = client.orders.get(order_number=1001)

    assert isinstance(order, Order)


@respx.mock
def test_list_payments_unwraps(client: ConnectClient, sample_payment: dict) -> None:
    """Payments list response is wrapped in {"payments": [...]}."""
    respx.get(f"{BASE}/orders/1001/payments").mock(
        return_value=httpx.Response(200, json={"payments": [sample_payment]})
    )
    page = client.orders.list_payments(order_number=1001)

    assert len(page.items) == 1
    assert isinstance(page.items[0], Payment)
    assert page.items[0].gateway == "ideal"


@respx.mock
def test_create_payment_unwraps(client: ConnectClient, sample_payment: dict) -> None:
    """Create payment response is wrapped in {"payment": {...}, "url": "..."}."""
    respx.post(f"{BASE}/orders/1001/payments").mock(
        return_value=httpx.Response(201, json={
            "payment": sample_payment,
            "url": "https://pay.example.com/redirect",
        })
    )
    payment = client.orders.create_payment(order_number=1001, body={"gateway": "ideal"})

    assert isinstance(payment, Payment)
    assert payment.gateway == "ideal"


@respx.mock
def test_create_payment_raw(client: ConnectClient, sample_payment: dict) -> None:
    """create_payment_raw returns the full dict with url."""
    respx.post(f"{BASE}/orders/1001/payments").mock(
        return_value=httpx.Response(201, json={
            "payment": sample_payment,
            "url": "https://pay.example.com/redirect",
        })
    )
    result = client.orders.create_payment_raw(order_number=1001, body={"gateway": "ideal"})

    assert "url" in result
    assert result["url"] == "https://pay.example.com/redirect"
    assert "payment" in result


@respx.mock
def test_create_credit_returns_order(client: ConnectClient, sample_order: dict) -> None:
    respx.post(f"{BASE}/orders/credit").mock(
        return_value=httpx.Response(200, json=sample_order)
    )
    order = client.orders.create_credit(body={"original_order": 1001})

    assert isinstance(order, Order)


@respx.mock
def test_count_orders(client: ConnectClient) -> None:
    respx.get(f"{BASE}/orders/count").mock(
        return_value=httpx.Response(200, json={"count": 42})
    )
    count = client.orders.count()

    assert count == 42
    assert isinstance(count, int)
