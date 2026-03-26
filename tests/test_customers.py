"""Tests for the Customers resource — verifies response unwrapping."""

from __future__ import annotations

import httpx
import respx

from myonlinestore import ConnectClient
from myonlinestore.models import Customer, CustomerAddress


BASE = "https://api.myonlinestore.com/v1"


@respx.mock
def test_list_customers_unwraps(client: ConnectClient, sample_customer: dict) -> None:
    """List response is wrapped in {"customers": [...]}."""
    respx.get(f"{BASE}/customers").mock(
        return_value=httpx.Response(200, json={"customers": [sample_customer]})
    )
    page = client.customers.list()

    assert len(page.items) == 1
    assert isinstance(page.items[0], Customer)
    assert page.items[0].email == "jane@example.com"


@respx.mock
def test_get_customer_unwraps(client: ConnectClient, sample_customer: dict) -> None:
    """Single customer response is wrapped in {"customer": {...}}."""
    respx.get(f"{BASE}/customers/99").mock(
        return_value=httpx.Response(200, json={"customer": sample_customer})
    )
    customer = client.customers.get(customer_id=99)

    assert isinstance(customer, Customer)
    assert customer.id == "cust-uuid-99"


@respx.mock
def test_list_addresses_unwraps(client: ConnectClient) -> None:
    """Address list is wrapped in {"addresses": [...]}."""
    addr = {"id": "addr-uuid-1", "street": "Main St", "number": "42", "city": "Amsterdam"}
    respx.get(f"{BASE}/customers/99/addresses").mock(
        return_value=httpx.Response(200, json={"addresses": [addr]})
    )
    page = client.customers.list_addresses(customer_id=99)

    assert len(page.items) == 1
    assert isinstance(page.items[0], CustomerAddress)
    assert page.items[0].city == "Amsterdam"


@respx.mock
def test_create_customer_unwraps(client: ConnectClient, sample_customer: dict) -> None:
    """Create returns wrapped {"customer": {...}}."""
    respx.post(f"{BASE}/customers").mock(
        return_value=httpx.Response(200, json={"customer": sample_customer})
    )
    customer = client.customers.create(body={"email": "jane@example.com"})

    assert isinstance(customer, Customer)
    assert customer.first_name == "Jane"
