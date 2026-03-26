"""Extended tests for updates, filters, and edge cases."""

from __future__ import annotations

import httpx
import pytest
import respx

from myonlinestore import ConnectClient
from myonlinestore.models import Article, Order


BASE = "https://api.myonlinestore.com/v1"


# ============================================================================
# UPDATE TESTS
# ============================================================================


@respx.mock
def test_update_article(client: ConnectClient, sample_article: dict) -> None:
    """Test updating an article via PATCH."""
    updated_article = {**sample_article, "name": "Updated Product"}
    respx.patch(f"{BASE}/articles/42").mock(
        return_value=httpx.Response(200, json=updated_article)
    )
    article = client.articles.update(
        article_id=42, body={"name": "Updated Product"}
    )

    assert isinstance(article, Article)
    assert article.name == "Updated Product"
    assert article.id == 42


@respx.mock
def test_update_order(client: ConnectClient, sample_order: dict) -> None:
    """Test updating an order via PATCH."""
    updated_order = {**sample_order, "comments": {"customer": "Updated comment", "internal": None}}
    respx.patch(f"{BASE}/orders/1001").mock(
        return_value=httpx.Response(200, json=updated_order)
    )
    order = client.orders.update(
        order_number=1001, body={"comments": {"customer": "Updated comment"}}
    )

    assert isinstance(order, Order)
    assert order.comments.customer == "Updated comment"


# ============================================================================
# FILTER PARAMETER TESTS
# ============================================================================


@respx.mock
def test_list_articles_with_filters(client: ConnectClient, sample_article: dict) -> None:
    """Test that filter parameters are passed correctly to list articles."""
    route = respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[sample_article])
    )
    page = client.articles.list(
        limit=10,
        offset=0,
        created_start_date="2024-01-01",
        created_end_date="2024-12-31",
    )

    assert route.called
    # Check that the query params were sent
    assert "limit=10" in str(route.calls.last.request.url)
    assert "offset=0" in str(route.calls.last.request.url)
    assert "created_start_date=2024-01-01" in str(route.calls.last.request.url)
    assert "created_end_date=2024-12-31" in str(route.calls.last.request.url)
    assert len(page.items) == 1


@respx.mock
def test_list_orders_with_status_filter(client: ConnectClient, sample_order: dict) -> None:
    """Test that status filter is passed correctly to list orders."""
    route = respx.get(f"{BASE}/orders").mock(
        return_value=httpx.Response(200, json=[sample_order])
    )
    page = client.orders.list(status_id=5)

    assert route.called
    assert "status_id=5" in str(route.calls.last.request.url)
    assert len(page.items) == 1


@respx.mock
def test_list_customers_with_search_filter(client: ConnectClient, sample_customer: dict) -> None:
    """Test that search query is passed correctly to list customers."""
    route = respx.get(f"{BASE}/customers").mock(
        return_value=httpx.Response(200, json={"customers": [sample_customer]})
    )
    page = client.customers.list(q="jane@example.com")

    assert route.called
    assert "q=jane%40example.com" in str(route.calls.last.request.url)
    assert len(page.items) == 1


# ============================================================================
# EDGE CASE TESTS
# ============================================================================


@respx.mock
def test_list_returns_none_response(client: ConnectClient) -> None:
    """Test that None/null responses are handled gracefully."""
    respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=None)
    )
    page = client.articles.list()

    assert page.items == []
    assert not page.has_next


@respx.mock
def test_upload_image_returns_dict(client: ConnectClient) -> None:
    """Test that upload_image handles dict responses with url field."""
    respx.post(f"{BASE}/articles/uploadImage/42").mock(
        return_value=httpx.Response(200, json={"url": "https://example.com/image.jpg"})
    )
    result = client.articles.upload_image(
        article_id=42, filename="test.jpg", content="base64content"
    )

    assert result == "https://example.com/image.jpg"


@respx.mock
def test_upload_image_returns_dict_with_src(client: ConnectClient) -> None:
    """Test that upload_image extracts src field when url is not present."""
    respx.post(f"{BASE}/articles/uploadImage/42").mock(
        return_value=httpx.Response(200, json={"src": "https://example.com/src.jpg"})
    )
    result = client.articles.upload_image(
        article_id=42, filename="test.jpg", content="base64content"
    )

    assert result == "https://example.com/src.jpg"


@respx.mock
def test_upload_image_returns_string(client: ConnectClient) -> None:
    """Test that upload_image passes through string responses directly."""
    respx.post(f"{BASE}/articles/uploadImage/42").mock(
        return_value=httpx.Response(200, json="https://example.com/image.jpg")
    )
    result = client.articles.upload_image(
        article_id=42, filename="test.jpg", content="base64content"
    )

    assert result == "https://example.com/image.jpg"


@respx.mock
def test_upload_image_returns_none(client: ConnectClient) -> None:
    """Test that upload_image returns empty string when API returns None."""
    respx.post(f"{BASE}/articles/uploadImage/42").mock(
        return_value=httpx.Response(200, json=None)
    )
    result = client.articles.upload_image(
        article_id=42, filename="test.jpg", content="base64content"
    )

    assert result == ""


@respx.mock
def test_upload_image_returns_dict_without_url_or_src(client: ConnectClient) -> None:
    """Test that upload_image converts dict to string when url/src not found."""
    respx.post(f"{BASE}/articles/uploadImage/42").mock(
        return_value=httpx.Response(200, json={"id": "img_123", "status": "uploaded"})
    )
    result = client.articles.upload_image(
        article_id=42, filename="test.jpg", content="base64content"
    )

    assert isinstance(result, str)
    assert "id" in result  # Should be a string representation of the dict


@respx.mock
def test_pagination_bounds_check(client: ConnectClient) -> None:
    """Test that iterate_all raises ValueError for invalid page_size."""
    from myonlinestore.pagination import iterate_all

    def mock_list(**kwargs):
        return []

    with pytest.raises(ValueError, match="page_size must be >= 1"):
        list(iterate_all(mock_list, page_size=0))

    with pytest.raises(ValueError, match="page_size must be >= 1"):
        list(iterate_all(mock_list, page_size=-1))


@pytest.mark.asyncio
async def test_pagination_bounds_check_async() -> None:
    """Test that aiterate_all raises ValueError for invalid page_size."""
    from myonlinestore.pagination import aiterate_all

    async def mock_alist(**kwargs):
        from myonlinestore.pagination import PaginatedResponse
        return PaginatedResponse(items=[], limit=100, offset=0)

    # The error is raised when the generator is created
    with pytest.raises(ValueError, match="page_size must be >= 1"):
        async for _ in aiterate_all(mock_alist, page_size=0):
            pass


@respx.mock
def test_list_articles_with_multiple_filters(client: ConnectClient, sample_article: dict) -> None:
    """Test that multiple filter parameters are all passed correctly."""
    route = respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[sample_article])
    )
    page = client.articles.list(
        limit=25,
        offset=50,
        created_start_date="2024-01-01",
        created_end_date="2024-12-31",
        changed_start_date="2024-06-01",
        changed_end_date="2024-12-31",
    )

    assert route.called
    url_str = str(route.calls.last.request.url)
    assert "limit=25" in url_str
    assert "offset=50" in url_str
    assert "created_start_date=2024-01-01" in url_str
    assert "created_end_date=2024-12-31" in url_str
    assert "changed_start_date=2024-06-01" in url_str
    assert "changed_end_date=2024-12-31" in url_str
    assert len(page.items) == 1


@respx.mock
def test_list_orders_with_multiple_filters(client: ConnectClient, sample_order: dict) -> None:
    """Test that multiple order filters are all passed correctly."""
    route = respx.get(f"{BASE}/orders").mock(
        return_value=httpx.Response(200, json=[sample_order])
    )
    page = client.orders.list(
        limit=20,
        status_id=5,
        debtor_email="customer@example.com",
        archived=False,
        test=False,
    )

    assert route.called
    url_str = str(route.calls.last.request.url)
    assert "limit=20" in url_str
    assert "status_id=5" in url_str
    assert "debtor_email=" in url_str
    assert "archived=False" in url_str or "archived=false" in url_str.lower()
    assert len(page.items) == 1


@respx.mock
def test_list_empty_articles(client: ConnectClient) -> None:
    """Test listing articles when API returns empty array."""
    respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[])
    )
    page = client.articles.list()

    assert page.items == []
    assert not page.has_next
    assert page.has_next is False


@respx.mock
def test_list_empty_orders(client: ConnectClient) -> None:
    """Test listing orders when API returns empty array."""
    respx.get(f"{BASE}/orders").mock(
        return_value=httpx.Response(200, json=[])
    )
    page = client.orders.list()

    assert page.items == []
    assert not page.has_next
    assert page.has_next is False


@respx.mock
def test_pagination_has_next_logic(client: ConnectClient, sample_article: dict) -> None:
    """Test pagination has_next property with different item counts."""
    # Less than limit items -> no next page
    respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[sample_article])
    )
    page = client.articles.list(limit=10)
    assert len(page.items) < 10
    assert not page.has_next

    # Exactly limit items -> might have next page (can't determine without total)
    respx.reset()
    respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[sample_article] * 10)
    )
    page = client.articles.list(limit=10)
    assert len(page.items) == 10
    assert page.has_next  # Assumes there might be more


@respx.mock
def test_count_articles_returns_int(client: ConnectClient) -> None:
    """Test that count endpoint returns an integer."""
    respx.get(f"{BASE}/articles/count").mock(
        return_value=httpx.Response(200, json={"count": 42})
    )
    count = client.articles.count()

    assert count == 42
    assert isinstance(count, int)


@respx.mock
def test_count_orders_returns_int(client: ConnectClient) -> None:
    """Test that count endpoint returns an integer."""
    respx.get(f"{BASE}/orders/count").mock(
        return_value=httpx.Response(200, json={"count": 15})
    )
    count = client.orders.count()

    assert count == 15
    assert isinstance(count, int)
