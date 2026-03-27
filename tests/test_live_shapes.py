"""Tests for live API response shapes observed from safe GET endpoints."""

from __future__ import annotations

import httpx
import respx

from myonlinestore import ConnectClient
from myonlinestore.models import OrderPaymentStatus, Store, TaxPrice


BASE = "https://api.myonlinestore.com/v1"


@respx.mock
def test_store_accepts_uuid_and_string_business_model(client: ConnectClient) -> None:
    payload = {
        "id": "940bbdce-6be1-11e9-a722-44a8421b9960",
        "name": "My Shop",
        "available_business_models": "B2C",
        "active_languages": ["nl_NL"],
        "prices_include_tax": True,
    }
    respx.get(f"{BASE}/store").mock(return_value=httpx.Response(200, json=payload))

    store = client.store.get()

    assert isinstance(store, Store)
    assert store.id == "940bbdce-6be1-11e9-a722-44a8421b9960"
    assert store.available_business_models == "B2C"
    assert store.active_languages == ["nl_NL"]


@respx.mock
def test_order_accepts_live_like_nested_shapes(client: ConnectClient) -> None:
    payload = {
        "number": "1001",
        "uuid": "af88e19b-a57b-4aae-a92b-f7078454d1e3",
        "date": "2025-01-01",
        "time": "12:00:00",
        "status": 2,
        "payment": {
            "gateway_name": "basic",
            "method_name": "advance",
            "status": {"id": 1, "text": "Successful"},
        },
        "price": {
            "tax": {"amount": "11.80", "rate": "21.00"},
            "total": "68.00",
        },
        "orderlines": [
            {
                "id": "5e77ab8b-c46f-11ec-9c3c-aaee87cff863",
                "type": "article",
                "quantity": 1,
                "description": "Product",
                "price": {
                    "amount": "56.198347",
                    "amount_including_tax": "68.00",
                    "rate": "21.00",
                },
            }
        ],
        "shipping": [{"country": []}],
        "credited_order_number": 999,
        "credit_order_numbers": [],
        "debtor": {"email": "test@example.com", "name": "Test User"},
    }
    respx.get(f"{BASE}/orders/1001").mock(return_value=httpx.Response(200, json=payload))

    order = client.orders.get(order_number=1001)

    assert order.number == "1001"
    assert order.payment is not None
    assert isinstance(order.payment.status, OrderPaymentStatus)
    assert order.payment.status.id == 1
    assert order.price is not None
    assert order.price.tax is not None
    assert len(order.price.tax) == 1
    assert order.orderlines is not None
    assert order.orderlines[0].id == "5e77ab8b-c46f-11ec-9c3c-aaee87cff863"
    assert isinstance(order.orderlines[0].price, TaxPrice)
    assert order.shipping is not None
    assert order.shipping[0].country is None
    assert order.credited_order_number == 999
    assert order.credit_order_numbers == []


@respx.mock
def test_tax_policy_list_unwraps_regions_wrapper(client: ConnectClient) -> None:
    payload = {
        "regions": [
            {
                "regionCode": "NL",
                "taxEnabled": True,
                "taxRate": "0.21",
                "shippingTaxMethod": "fixed",
            }
        ]
    }
    respx.get(f"{BASE}/tax-policy/regions").mock(return_value=httpx.Response(200, json=payload))

    page = client.tax_policy.list()

    assert len(page.items) == 1
    assert page.items[0].region_code == "NL"
    assert page.items[0].tax_enabled is True
