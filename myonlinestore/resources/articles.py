"""Articles resource for the MyOnlineStore API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from myonlinestore.models import Article, CountResponse
from myonlinestore.pagination import PaginatedResponse
from myonlinestore.resources.base import Resource

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class ArticlesResource(Resource):
    """Resource for managing articles."""

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
        ids: list[int] | None = None,
        uuids: list[str] | None = None,
        use_url_id: bool | None = None,
    ) -> PaginatedResponse[Article]:
        """List articles.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            created_start_date: Filter by creation date (start)
            created_end_date: Filter by creation date (end)
            changed_start_date: Filter by change date (start)
            changed_end_date: Filter by change date (end)
            ids: Filter by article IDs
            uuids: Filter by article UUIDs
            use_url_id: Use URL ID instead of numeric ID

        Returns:
            PaginatedResponse containing Article objects
        """
        params = self._list_params(
            limit,
            offset,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            ids=ids,
            uuids=uuids,
            use_url_id=use_url_id,
        )
        data = self._transport.get("/articles", params=params)
        items = [Article.model_validate(item) for item in (data or [])]
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
        ids: list[int] | None = None,
        uuids: list[str] | None = None,
        use_url_id: bool | None = None,
    ) -> PaginatedResponse[Article]:
        """Asynchronously list articles.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            created_start_date: Filter by creation date (start)
            created_end_date: Filter by creation date (end)
            changed_start_date: Filter by change date (start)
            changed_end_date: Filter by change date (end)
            ids: Filter by article IDs
            uuids: Filter by article UUIDs
            use_url_id: Use URL ID instead of numeric ID

        Returns:
            PaginatedResponse containing Article objects
        """
        params = self._list_params(
            limit,
            offset,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            ids=ids,
            uuids=uuids,
            use_url_id=use_url_id,
        )
        data = await self._transport.aget("/articles", params=params)
        items = [Article.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    def create(self, *, body: dict[str, Any]) -> Article:
        """Create a new article.

        Args:
            body: Article data

        Returns:
            Created Article object
        """
        data = self._transport.post("/articles", json=body)
        return Article.model_validate(data)

    async def acreate(self, *, body: dict[str, Any]) -> Article:
        """Asynchronously create a new article.

        Args:
            body: Article data

        Returns:
            Created Article object
        """
        data = await self._transport.apost("/articles", json=body)
        return Article.model_validate(data)

    def get(self, *, article_id: int | str) -> Article:
        """Get an article by ID.

        Args:
            article_id: The article ID

        Returns:
            Article object
        """
        data = self._transport.get(f"/articles/{article_id}")
        return Article.model_validate(data)

    async def aget(self, *, article_id: int | str) -> Article:
        """Asynchronously get an article by ID.

        Args:
            article_id: The article ID

        Returns:
            Article object
        """
        data = await self._transport.aget(f"/articles/{article_id}")
        return Article.model_validate(data)

    def update(self, *, article_id: int | str, body: dict[str, Any]) -> Article:
        """Update an article.

        Args:
            article_id: The article ID
            body: Updated article data

        Returns:
            Updated Article object
        """
        data = self._transport.patch(f"/articles/{article_id}", json=body)
        return Article.model_validate(data)

    async def aupdate(self, *, article_id: int | str, body: dict[str, Any]) -> Article:
        """Asynchronously update an article.

        Args:
            article_id: The article ID
            body: Updated article data

        Returns:
            Updated Article object
        """
        data = await self._transport.apatch(f"/articles/{article_id}", json=body)
        return Article.model_validate(data)

    def delete(self, *, article_id: int | str) -> None:
        """Delete an article.

        Args:
            article_id: The article ID
        """
        self._transport.delete(f"/articles/{article_id}")

    async def adelete(self, *, article_id: int | str) -> None:
        """Asynchronously delete an article.

        Args:
            article_id: The article ID
        """
        await self._transport.adelete(f"/articles/{article_id}")

    def count(self) -> int:
        """Get the total count of articles.

        Returns:
            Total number of articles.
        """
        data = self._transport.get("/articles/count")
        return CountResponse.model_validate(data).count

    async def acount(self) -> int:
        """Asynchronously get the total count of articles.

        Returns:
            Total number of articles.
        """
        data = await self._transport.aget("/articles/count")
        return CountResponse.model_validate(data).count

    def upload_image(
        self, *, article_id: int | str, filename: str, content: str
    ) -> str:
        """Upload an image to an article.

        Args:
            article_id: The article ID
            filename: The filename of the image
            content: The base64-encoded image content

        Returns:
            The uploaded image URL or identifier string.
        """
        body = {"filename": filename, "content": content}
        data = self._transport.post(f"/articles/uploadImage/{article_id}", json=body)
        if data is None:
            return ""
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            return data.get("url", data.get("src", str(data)))
        return str(data)

    async def aupload_image(
        self, *, article_id: int | str, filename: str, content: str
    ) -> str:
        """Asynchronously upload an image to an article.

        Args:
            article_id: The article ID
            filename: The filename of the image
            content: The base64-encoded image content

        Returns:
            The uploaded image URL or identifier string.
        """
        body = {"filename": filename, "content": content}
        data = await self._transport.apost(
            f"/articles/uploadImage/{article_id}", json=body
        )
        if data is None:
            return ""
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            return data.get("url", data.get("src", str(data)))
        return str(data)

    def delete_image(self, *, image_id: int | str) -> None:
        """Delete an image.

        Args:
            image_id: The image ID
        """
        self._transport.delete(f"/deleteImage/{image_id}")

    async def adelete_image(self, *, image_id: int | str) -> None:
        """Asynchronously delete an image.

        Args:
            image_id: The image ID
        """
        await self._transport.adelete(f"/deleteImage/{image_id}")
