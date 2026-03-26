"""Pagination helpers for list endpoints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator, Callable, Coroutine, Generic, Iterator, TypeVar

T = TypeVar("T")


@dataclass
class PaginatedResponse(Generic[T]):
    """A page of results from a list endpoint.

    Attributes:
        items: The items on this page.
        limit: Page size that was requested.
        offset: Offset that was requested.
        total: Total number of items (if a count endpoint exists), otherwise ``None``.
    """

    items: list[T]
    limit: int
    offset: int
    total: int | None = None

    @property
    def has_next(self) -> bool:
        """Whether there are more items after this page."""
        if self.total is not None:
            return (self.offset + self.limit) < self.total
        # If we don't know the total, assume more pages if we got a full page.
        return len(self.items) >= self.limit

    @property
    def next_offset(self) -> int:
        """Offset for the next page."""
        return self.offset + self.limit


def iterate_all(
    fetch_page: Callable[..., PaginatedResponse[T]],
    *,
    page_size: int = 100,
    **kwargs: Any,
) -> Iterator[T]:
    """Synchronously iterate through all pages of a list endpoint.

    Usage::

        for article in iterate_all(client.articles.list, page_size=100):
            print(article.name)

    Args:
        fetch_page: A resource ``.list()`` method.
        page_size: Number of items per page (max 100).
        **kwargs: Extra keyword arguments forwarded to *fetch_page*.
    """
    if page_size is not None and page_size < 1:
        raise ValueError(f"page_size must be >= 1, got {page_size}")
    offset = 0
    while True:
        page = fetch_page(limit=page_size, offset=offset, **kwargs)
        yield from page.items
        if not page.has_next:
            break
        offset = page.next_offset


async def aiterate_all(
    fetch_page: Callable[..., Coroutine[Any, Any, PaginatedResponse[T]]],
    *,
    page_size: int = 100,
    **kwargs: Any,
) -> AsyncIterator[T]:
    """Asynchronously iterate through all pages of a list endpoint.

    Usage::

        async for article in aiterate_all(client.articles.alist, page_size=100):
            print(article.name)

    Args:
        fetch_page: A resource ``.alist()`` method.
        page_size: Number of items per page (max 100).
        **kwargs: Extra keyword arguments forwarded to *fetch_page*.
    """
    if page_size is not None and page_size < 1:
        raise ValueError(f"page_size must be >= 1, got {page_size}")
    offset = 0
    while True:
        page = await fetch_page(limit=page_size, offset=offset, **kwargs)
        for item in page.items:
            yield item
        if not page.has_next:
            break
        offset = page.next_offset
