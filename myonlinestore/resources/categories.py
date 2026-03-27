"""Categories resource for the MyOnlineStore API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from myonlinestore.models import ArticleLimited, Category, CountResponse
from myonlinestore.pagination import PaginatedResponse
from myonlinestore.resources.base import Resource

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class CategoriesResource(Resource):
    """Resource for managing categories."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        as_tree: bool | None = None,
        max_depth: int | None = None,
    ) -> PaginatedResponse[Category]:
        """List categories.

        Args:
            limit: Maximum number of items to return.
            offset: Number of items to skip.
            as_tree: Return categories in a tree structure.
            max_depth: Maximum depth of the tree (requires ``as_tree=True``).

        Returns:
            PaginatedResponse containing Category objects
        """
        params = self._list_params(
            limit,
            offset,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            as_tree=as_tree,
            max_depth=max_depth,
        )
        data = self._transport.get("/categories", params=params)
        items = [Category.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    async def alist(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        as_tree: bool | None = None,
        max_depth: int | None = None,
    ) -> PaginatedResponse[Category]:
        """Asynchronously list categories.

        Args:
            limit: Maximum number of items to return.
            offset: Number of items to skip.
            as_tree: Return categories in a tree structure.
            max_depth: Maximum depth of the tree (requires ``as_tree=True``).

        Returns:
            PaginatedResponse containing Category objects
        """
        params = self._list_params(
            limit,
            offset,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            as_tree=as_tree,
            max_depth=max_depth,
        )
        data = await self._transport.aget("/categories", params=params)
        items = [Category.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    def create(self, *, body: dict[str, Any]) -> Category:
        """Create a new category.

        Args:
            body: Category data

        Returns:
            Created Category object
        """
        data = self._transport.post("/categories", json=body)
        return Category.model_validate(data)

    async def acreate(self, *, body: dict[str, Any]) -> Category:
        """Asynchronously create a new category.

        Args:
            body: Category data

        Returns:
            Created Category object
        """
        data = await self._transport.apost("/categories", json=body)
        return Category.model_validate(data)

    def count(
        self,
        *,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
    ) -> int:
        """Get the total count of categories.

        Returns:
            Total number of categories.
        """
        params = self._list_params(
            None,
            None,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
        )
        data = self._transport.get("/categories/count", params=params)
        return CountResponse.model_validate(data).count

    async def acount(
        self,
        *,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
    ) -> int:
        """Asynchronously get the total count of categories.

        Returns:
            Total number of categories.
        """
        params = self._list_params(
            None,
            None,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
        )
        data = await self._transport.aget("/categories/count", params=params)
        return CountResponse.model_validate(data).count

    def get(self, *, category_id: int | str) -> Category:
        """Get a category by ID.

        Args:
            category_id: The category ID

        Returns:
            Category object
        """
        data = self._transport.get(f"/categories/{category_id}")
        return Category.model_validate(data)

    async def aget(self, *, category_id: int | str) -> Category:
        """Asynchronously get a category by ID.

        Args:
            category_id: The category ID

        Returns:
            Category object
        """
        data = await self._transport.aget(f"/categories/{category_id}")
        return Category.model_validate(data)

    def update(self, *, category_id: int | str, body: dict[str, Any]) -> Category:
        """Update a category.

        Args:
            category_id: The category ID
            body: Updated category data

        Returns:
            Updated Category object
        """
        data = self._transport.patch(f"/categories/{category_id}", json=body)
        return Category.model_validate(data)

    async def aupdate(self, *, category_id: int | str, body: dict[str, Any]) -> Category:
        """Asynchronously update a category.

        Args:
            category_id: The category ID
            body: Updated category data

        Returns:
            Updated Category object
        """
        data = await self._transport.apatch(f"/categories/{category_id}", json=body)
        return Category.model_validate(data)

    def list_articles(
        self, *, category_id: int | str, limit: int | None = None, offset: int | None = None
    ) -> PaginatedResponse[ArticleLimited]:
        """List articles in a category.

        Note: This endpoint returns a limited article representation with only
        ``id``, ``name``, ``uuid``, and ``is_main`` fields.

        Args:
            category_id: The category ID

        Returns:
            PaginatedResponse containing ArticleLimited objects
        """
        params = self._list_params(limit, offset)
        data = self._transport.get(f"/categories/{category_id}/articles", params=params)
        items = [ArticleLimited.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    async def alist_articles(
        self, *, category_id: int | str, limit: int | None = None, offset: int | None = None
    ) -> PaginatedResponse[ArticleLimited]:
        """Asynchronously list articles in a category.

        Note: This endpoint returns a limited article representation with only
        ``id``, ``name``, ``uuid``, and ``is_main`` fields.

        Args:
            category_id: The category ID

        Returns:
            PaginatedResponse containing ArticleLimited objects
        """
        params = self._list_params(limit, offset)
        data = await self._transport.aget(f"/categories/{category_id}/articles", params=params)
        items = [ArticleLimited.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)
