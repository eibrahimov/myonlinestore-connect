"""Newsletter resource for the MyOnlineStore API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from myonlinestore.models import CountResponse, NewsletterSubscriber
from myonlinestore.pagination import PaginatedResponse
from myonlinestore.resources.base import Resource

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class NewsletterResource(Resource):
    """Resource for managing newsletter subscribers."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        activated: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        **legacy_filters: Any,
    ) -> PaginatedResponse[NewsletterSubscriber]:
        """List newsletter subscribers.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            activated: Filter by activated status
            activate: Filter by activate status

        Returns:
            PaginatedResponse containing NewsletterSubscriber objects
        """
        activate = legacy_filters.pop("activate", None)
        if legacy_filters:
            unexpected = ", ".join(sorted(legacy_filters))
            raise TypeError(f"Unexpected keyword argument(s): {unexpected}")
        if activated is None and activate is not None:
            activated = activate
        params = self._list_params(
            limit,
            offset,
            activated=activated,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
        )
        data = self._transport.get("/newsletter/subscribers", params=params)
        items = [NewsletterSubscriber.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    async def alist(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        activated: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        **legacy_filters: Any,
    ) -> PaginatedResponse[NewsletterSubscriber]:
        """Asynchronously list newsletter subscribers.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            activated: Filter by activated status
            activate: Filter by activate status

        Returns:
            PaginatedResponse containing NewsletterSubscriber objects
        """
        activate = legacy_filters.pop("activate", None)
        if legacy_filters:
            unexpected = ", ".join(sorted(legacy_filters))
            raise TypeError(f"Unexpected keyword argument(s): {unexpected}")
        if activated is None and activate is not None:
            activated = activate
        params = self._list_params(
            limit,
            offset,
            activated=activated,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
        )
        data = await self._transport.aget("/newsletter/subscribers", params=params)
        items = [NewsletterSubscriber.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    def create(self, *, body: dict[str, Any]) -> NewsletterSubscriber:
        """Create a new newsletter subscriber.

        Args:
            body: Subscriber data

        Returns:
            Created NewsletterSubscriber object
        """
        data = self._transport.post("/newsletter/subscribers", json=body)
        return NewsletterSubscriber.model_validate(data)

    async def acreate(self, *, body: dict[str, Any]) -> NewsletterSubscriber:
        """Asynchronously create a new newsletter subscriber.

        Args:
            body: Subscriber data

        Returns:
            Created NewsletterSubscriber object
        """
        data = await self._transport.apost("/newsletter/subscribers", json=body)
        return NewsletterSubscriber.model_validate(data)

    def count(
        self,
        *,
        activated: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
    ) -> int:
        """Get the total count of newsletter subscribers.

        Returns:
            Total number of subscribers.
        """
        params = self._list_params(
            None,
            None,
            activated=activated,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
        )
        data = self._transport.get("/newsletter/subscribers/count", params=params)
        return CountResponse.model_validate(data).count

    async def acount(
        self,
        *,
        activated: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
    ) -> int:
        """Asynchronously get the total count of newsletter subscribers.

        Returns:
            Total number of subscribers.
        """
        params = self._list_params(
            None,
            None,
            activated=activated,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
        )
        data = await self._transport.aget("/newsletter/subscribers/count", params=params)
        return CountResponse.model_validate(data).count

    def get(self, *, email: str) -> NewsletterSubscriber:
        """Get a newsletter subscriber by email.

        Args:
            email: The subscriber email

        Returns:
            NewsletterSubscriber object
        """
        data = self._transport.get(f"/newsletter/subscribers/{email}")
        return NewsletterSubscriber.model_validate(data)

    async def aget(self, *, email: str) -> NewsletterSubscriber:
        """Asynchronously get a newsletter subscriber by email.

        Args:
            email: The subscriber email

        Returns:
            NewsletterSubscriber object
        """
        data = await self._transport.aget(f"/newsletter/subscribers/{email}")
        return NewsletterSubscriber.model_validate(data)

    def update(self, *, email: str, body: dict[str, Any]) -> NewsletterSubscriber:
        """Update a newsletter subscriber.

        Args:
            email: The subscriber email
            body: Updated subscriber data

        Returns:
            Updated NewsletterSubscriber object
        """
        data = self._transport.patch(f"/newsletter/subscribers/{email}", json=body)
        return NewsletterSubscriber.model_validate(data)

    async def aupdate(self, *, email: str, body: dict[str, Any]) -> NewsletterSubscriber:
        """Asynchronously update a newsletter subscriber.

        Args:
            email: The subscriber email
            body: Updated subscriber data

        Returns:
            Updated NewsletterSubscriber object
        """
        data = await self._transport.apatch(f"/newsletter/subscribers/{email}", json=body)
        return NewsletterSubscriber.model_validate(data)

    def delete(self, *, email: str) -> None:
        """Delete a newsletter subscriber.

        Args:
            email: The subscriber email
        """
        self._transport.delete(f"/newsletter/subscribers/{email}")

    async def adelete(self, *, email: str) -> None:
        """Asynchronously delete a newsletter subscriber.

        Args:
            email: The subscriber email
        """
        await self._transport.adelete(f"/newsletter/subscribers/{email}")
