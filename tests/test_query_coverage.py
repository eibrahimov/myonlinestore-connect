"""Tests for read-only GET parameter coverage improvements."""

from __future__ import annotations

import httpx
import respx

from myonlinestore import ConnectClient


BASE = "https://api.myonlinestore.com/v1"


@respx.mock
def test_article_count_supports_date_filters(client: ConnectClient) -> None:
    route = respx.get(f"{BASE}/articles/count").mock(
        return_value=httpx.Response(200, json={"count": 7})
    )

    count = client.articles.count(
        created_start_date="2024-01-01 00:00:00",
        changed_end_date="2024-12-31 23:59:59",
    )

    assert count == 7
    url = str(route.calls.last.request.url)
    assert "created_start_date=2024-01-01+00%3A00%3A00" in url
    assert "changed_end_date=2024-12-31+23%3A59%3A59" in url


@respx.mock
def test_article_get_supports_use_url_id(client: ConnectClient, sample_article: dict) -> None:
    route = respx.get(f"{BASE}/articles/42").mock(
        return_value=httpx.Response(200, json=sample_article)
    )

    article = client.articles.get(article_id=42, use_url_id=True)

    assert article.id == 42
    assert "use_url_id=true" in str(route.calls.last.request.url)


@respx.mock
def test_article_list_keeps_use_url_id_for_backward_compatibility(client: ConnectClient, sample_article: dict) -> None:
    route = respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[sample_article])
    )

    page = client.articles.list(limit=1, use_url_id=True)

    assert len(page.items) == 1
    assert "use_url_id=true" in str(route.calls.last.request.url)


@respx.mock
def test_category_list_articles_supports_limit_and_offset(client: ConnectClient) -> None:
    route = respx.get(f"{BASE}/categories/5/articles").mock(
        return_value=httpx.Response(200, json=[])
    )

    page = client.categories.list_articles(category_id=5, limit=10, offset=20)

    assert page.limit == 10
    assert page.offset == 20
    url = str(route.calls.last.request.url)
    assert "limit=10" in url
    assert "offset=20" in url


@respx.mock
def test_discount_code_list_supports_filters(client: ConnectClient) -> None:
    route = respx.get(f"{BASE}/discountcodes").mock(
        return_value=httpx.Response(200, json=[])
    )

    client.discount_codes.list(
        active=True,
        valid_start_date="2024-01-01",
        valid_end_date="2024-12-31",
    )

    url = str(route.calls.last.request.url)
    assert "active=true" in url
    assert "valid_start_date=2024-01-01" in url
    assert "valid_end_date=2024-12-31" in url


@respx.mock
def test_newsletter_list_and_count_support_date_filters(client: ConnectClient) -> None:
    list_route = respx.get(f"{BASE}/newsletter/subscribers").mock(
        return_value=httpx.Response(200, json=[])
    )
    count_route = respx.get(f"{BASE}/newsletter/subscribers/count").mock(
        return_value=httpx.Response(200, json={"count": 1})
    )

    client.newsletter.list(
        activated=True,
        created_start_date="2024-01-01 00:00:00",
        changed_end_date="2024-12-31 23:59:59",
    )
    count = client.newsletter.count(
        activated=False,
        created_end_date="2024-06-30 23:59:59",
    )

    assert count == 1
    list_url = str(list_route.calls.last.request.url)
    count_url = str(count_route.calls.last.request.url)
    assert "activated=true" in list_url
    assert "created_start_date=2024-01-01+00%3A00%3A00" in list_url
    assert "changed_end_date=2024-12-31+23%3A59%3A59" in list_url
    assert "activated=false" in count_url
    assert "created_end_date=2024-06-30+23%3A59%3A59" in count_url


@respx.mock
def test_offline_locations_list_supports_deleted_filter(client: ConnectClient) -> None:
    route = respx.get(f"{BASE}/offlinelocations").mock(
        return_value=httpx.Response(200, json=[])
    )

    client.offline_locations.list(deleted=False)

    assert "deleted=false" in str(route.calls.last.request.url)


@respx.mock
def test_newsletter_activate_legacy_alias_still_works(client: ConnectClient) -> None:
    route = respx.get(f"{BASE}/newsletter/subscribers").mock(
        return_value=httpx.Response(200, json=[])
    )

    client.newsletter.list(activate=True)

    assert "activated=true" in str(route.calls.last.request.url)


@respx.mock
def test_orders_list_and_count_support_openapi_date_aliases(client: ConnectClient, sample_order: dict) -> None:
    list_route = respx.get(f"{BASE}/orders").mock(
        return_value=httpx.Response(200, json=[sample_order])
    )
    count_route = respx.get(f"{BASE}/orders/count").mock(
        return_value=httpx.Response(200, json={"count": 3})
    )

    client.orders.list(
        start_date="2024-01-01",
        end_date="2024-12-31",
        ordering="desc",
        status_changed_start_date="2024-06-01 00:00:00",
    )
    count = client.orders.count(
        start_date="2024-01-01",
        end_date="2024-12-31",
    )

    assert count == 3
    list_url = str(list_route.calls.last.request.url)
    count_url = str(count_route.calls.last.request.url)
    assert "start_date=2024-01-01" in list_url
    assert "end_date=2024-12-31" in list_url
    assert "ordering=desc" in list_url
    assert "status_changed_start_date=2024-06-01+00%3A00%3A00" in list_url
    assert "start_date=2024-01-01" in count_url
    assert "end_date=2024-12-31" in count_url


@respx.mock
def test_orders_legacy_aliases_still_work(client: ConnectClient, sample_order: dict) -> None:
    list_route = respx.get(f"{BASE}/orders").mock(
        return_value=httpx.Response(200, json=[sample_order])
    )
    count_route = respx.get(f"{BASE}/orders/count").mock(
        return_value=httpx.Response(200, json={"count": 2})
    )

    client.orders.list(
        created_start_date="2024-01-01",
        created_end_date="2024-12-31",
        changed_start_date="2024-06-01 00:00:00",
    )
    count = client.orders.count(
        debtor_email="customer@example.com",
        created_start_date="2024-01-01",
        changed_end_date="2024-12-31 23:59:59",
    )

    assert count == 2
    list_url = str(list_route.calls.last.request.url)
    count_url = str(count_route.calls.last.request.url)
    assert "start_date=2024-01-01" in list_url
    assert "end_date=2024-12-31" in list_url
    assert "changed_start_date=2024-06-01+00%3A00%3A00" in list_url
    assert "debtor_email=customer%40example.com" in count_url
    assert "start_date=2024-01-01" in count_url
    assert "changed_end_date=2024-12-31+23%3A59%3A59" in count_url


@respx.mock
def test_orders_list_payments_supports_embed(client: ConnectClient, sample_payment: dict) -> None:
    route = respx.get(f"{BASE}/orders/1001/payments").mock(
        return_value=httpx.Response(200, json={"payments": [sample_payment]})
    )

    page = client.orders.list_payments(order_number=1001, embed="transactions")

    assert len(page.items) == 1
    assert "embed=transactions" in str(route.calls.last.request.url)


@respx.mock
def test_primary_and_legacy_id_names_work_for_detail_getters(client: ConnectClient) -> None:
    offline_payload = {"id": "loc-1", "name": "Shop"}
    article_list_payload = {"id": 9, "name": "Sounds", "options": []}

    offline_route = respx.get(f"{BASE}/offlinelocations/loc-1").mock(
        return_value=httpx.Response(200, json=offline_payload)
    )
    article_list_route = respx.get(f"{BASE}/articlelists/9").mock(
        return_value=httpx.Response(200, json=article_list_payload)
    )

    offline_a = client.offline_locations.get(id="loc-1")
    offline_b = client.offline_locations.get(location_id="loc-1")
    article_list_a = client.article_lists.get(id=9)
    article_list_b = client.article_lists.get(list_id=9)

    assert offline_a.id == "loc-1"
    assert offline_b.id == "loc-1"
    assert article_list_a.id == 9
    assert article_list_b.id == 9
    assert offline_route.call_count == 2
    assert article_list_route.call_count == 2


def test_offline_location_and_shipping_method_accept_live_like_ids() -> None:
    from myonlinestore.models import OfflineLocation, ShippingMethod

    location = OfflineLocation.model_validate({"id": "7127e08a-4af0-4fdf-ac7b-157be3345df0"})
    method = ShippingMethod.model_validate({"id": "ship-method-1", "countries": ["NL"], "no_costs_above": "100.00"})

    assert location.id == "7127e08a-4af0-4fdf-ac7b-157be3345df0"
    assert method.id == "ship-method-1"
    assert method.countries == ["NL"]
    assert method.no_costs_above == "100.00"
