"""Tests for the Articles resource."""

from __future__ import annotations

import httpx
import pytest
import respx

from myonlinestore import ConnectClient, NotFoundError
from myonlinestore.models import Article


BASE = "https://api.myonlinestore.com/v1"


@respx.mock
def test_list_articles(client: ConnectClient, sample_article: dict) -> None:
    route = respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[sample_article])
    )
    page = client.articles.list(limit=10)

    assert route.called
    assert len(page.items) == 1
    assert isinstance(page.items[0], Article)
    assert page.items[0].name == "Test Product"
    assert page.items[0].id == 42


@respx.mock
def test_get_article(client: ConnectClient, sample_article: dict) -> None:
    respx.get(f"{BASE}/articles/42").mock(
        return_value=httpx.Response(200, json=sample_article)
    )
    article = client.articles.get(article_id=42)

    assert isinstance(article, Article)
    assert article.id == 42
    assert article.name == "Test Product"


@respx.mock
def test_create_article(client: ConnectClient, sample_article: dict) -> None:
    respx.post(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=sample_article)
    )
    article = client.articles.create(body={"name": "Test Product"})

    assert isinstance(article, Article)
    assert article.name == "Test Product"


@respx.mock
def test_delete_article(client: ConnectClient) -> None:
    respx.delete(f"{BASE}/articles/42").mock(
        return_value=httpx.Response(204)
    )
    # Should not raise
    client.articles.delete(article_id=42)


@respx.mock
def test_count_articles(client: ConnectClient) -> None:
    respx.get(f"{BASE}/articles/count").mock(
        return_value=httpx.Response(200, json={"count": 137})
    )
    count = client.articles.count()

    assert count == 137
    assert isinstance(count, int)


@respx.mock
def test_article_not_found(client: ConnectClient) -> None:
    respx.get(f"{BASE}/articles/99999").mock(
        return_value=httpx.Response(404, json={"title": "Not Found"})
    )
    with pytest.raises(NotFoundError) as exc_info:
        client.articles.get(article_id=99999)

    assert exc_info.value.status_code == 404


@respx.mock
def test_list_articles_empty(client: ConnectClient) -> None:
    respx.get(f"{BASE}/articles").mock(
        return_value=httpx.Response(200, json=[])
    )
    page = client.articles.list()

    assert page.items == []
    assert not page.has_next
