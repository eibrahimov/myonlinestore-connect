"""Async method tests — mirrors sync tests for async code paths."""
import httpx
import pytest
import respx

from myonlinestore import ConnectClient, ConnectConfig
from myonlinestore.exceptions import NotFoundError
from myonlinestore.models import Article, Customer, Order, Payment

BASE = "https://api.myonlinestore.com/v1"


@pytest.fixture
def config() -> ConnectConfig:
    return ConnectConfig(store_token="test-token", max_retries=0, idempotency_key_header=None)


@pytest.fixture
def client(config: ConnectConfig) -> ConnectClient:
    return ConnectClient(config=config)


@respx.mock
@pytest.mark.asyncio
async def test_alist_articles(client: ConnectClient) -> None:
    art = {"id": 1, "name": "Widget", "uuid": "abc-123"}
    respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[art])
    )
    page = await client.articles.alist(limit=10)
    assert len(page.items) == 1
    assert isinstance(page.items[0], Article)
    assert page.items[0].name == "Widget"


@respx.mock
@pytest.mark.asyncio
async def test_aget_article(client: ConnectClient) -> None:
    art = {"id": 42, "name": "Gadget", "uuid": "def-456"}
    respx.get(f"{BASE}/articles/42").mock(
        return_value=httpx.Response(200, json=art)
    )
    article = await client.articles.aget(article_id=42)
    assert isinstance(article, Article)
    assert article.id == 42


@respx.mock
@pytest.mark.asyncio
async def test_alist_customers_unwraps(client: ConnectClient) -> None:
    cust = {"id": "cust-uuid-1", "firstName": "Alice", "lastName": "Smith", "email": "alice@example.com"}
    respx.get(f"{BASE}/customers").mock(
        return_value=httpx.Response(200, json={"customers": [cust]})
    )
    page = await client.customers.alist(limit=10)
    assert len(page.items) == 1
    assert isinstance(page.items[0], Customer)


@respx.mock
@pytest.mark.asyncio
async def test_aget_customer_unwraps(client: ConnectClient) -> None:
    cust = {"id": "cust-uuid-99", "firstName": "Bob", "lastName": "Jones", "email": "bob@example.com"}
    respx.get(f"{BASE}/customers/cust-uuid-99").mock(
        return_value=httpx.Response(200, json={"customer": cust})
    )
    customer = await client.customers.aget(customer_id="cust-uuid-99")
    assert isinstance(customer, Customer)
    assert customer.first_name == "Bob"


@respx.mock
@pytest.mark.asyncio
async def test_alist_orders(client: ConnectClient) -> None:
    order = {
        "order_number": "1001",
        "status": 1,
        "debtor": {"email": "test@example.com", "name": "Test User"},
        "price": {"total": "49.99", "tax": []},
        "comments": {"customer": None, "internal": None},
        "details": [],
    }
    respx.get(f"{BASE}/orders").mock(
        return_value=httpx.Response(200, json=[order])
    )
    page = await client.orders.alist(limit=10)
    assert len(page.items) == 1
    assert isinstance(page.items[0], Order)


@respx.mock
@pytest.mark.asyncio
async def test_alist_payments_unwraps(client: ConnectClient) -> None:
    pay = {"id": "pay-uuid-1", "price": "10.00"}
    respx.get(f"{BASE}/orders/1001/payments").mock(
        return_value=httpx.Response(200, json={"payments": [pay]})
    )
    page = await client.orders.alist_payments(order_number=1001)
    assert len(page.items) == 1
    assert isinstance(page.items[0], Payment)


@respx.mock
@pytest.mark.asyncio
async def test_async_not_found(client: ConnectClient) -> None:
    respx.get(f"{BASE}/articles/99999").mock(
        return_value=httpx.Response(404, json={"error": "Not found"})
    )
    with pytest.raises(NotFoundError):
        await client.articles.aget(article_id=99999)


@respx.mock
@pytest.mark.asyncio
async def test_acount_articles(client: ConnectClient) -> None:
    respx.get(f"{BASE}/articles/count").mock(
        return_value=httpx.Response(200, json={"count": 42})
    )
    count = await client.articles.acount()
    assert count == 42
