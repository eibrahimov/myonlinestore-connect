"""Discount codes resource for the MyOnlineStore API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from myonlinestore.models import DiscountCode
from myonlinestore.pagination import PaginatedResponse
from myonlinestore.resources.base import Resource

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class DiscountCodesResource(Resource):
    """Resource for managing discount codes."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        active: bool | None = None,
        valid_start_date: str | None = None,
        valid_end_date: str | None = None,
    ) -> PaginatedResponse[DiscountCode]:
        """List discount codes.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip

        Returns:
            PaginatedResponse containing DiscountCode objects
        """
        params = self._list_params(
            limit,
            offset,
            active=active,
            valid_start_date=valid_start_date,
            valid_end_date=valid_end_date,
        )
        data = self._transport.get("/discountcodes", params=params)
        items = [DiscountCode.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    async def alist(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        active: bool | None = None,
        valid_start_date: str | None = None,
        valid_end_date: str | None = None,
    ) -> PaginatedResponse[DiscountCode]:
        """Asynchronously list discount codes.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip

        Returns:
            PaginatedResponse containing DiscountCode objects
        """
        params = self._list_params(
            limit,
            offset,
            active=active,
            valid_start_date=valid_start_date,
            valid_end_date=valid_end_date,
        )
        data = await self._transport.aget("/discountcodes", params=params)
        items = [DiscountCode.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    def create(self, *, body: dict[str, Any]) -> DiscountCode:
        """Create a new discount code.

        Args:
            body: Discount code data

        Returns:
            Created DiscountCode object
        """
        data = self._transport.post("/discountcodes", json=body)
        return DiscountCode.model_validate(data)

    async def acreate(self, *, body: dict[str, Any]) -> DiscountCode:
        """Asynchronously create a new discount code.

        Args:
            body: Discount code data

        Returns:
            Created DiscountCode object
        """
        data = await self._transport.apost("/discountcodes", json=body)
        return DiscountCode.model_validate(data)

    def update(self, *, body: dict[str, Any]) -> DiscountCode:
        """Update a discount code.

        Note: This endpoint updates via a PATCH on the collection endpoint.

        Args:
            body: Updated discount code data

        Returns:
            Updated DiscountCode object
        """
        data = self._transport.patch("/discountcodes", json=body)
        return DiscountCode.model_validate(data)

    async def aupdate(self, *, body: dict[str, Any]) -> DiscountCode:
        """Asynchronously update a discount code.

        Note: This endpoint updates via a PATCH on the collection endpoint.

        Args:
            body: Updated discount code data

        Returns:
            Updated DiscountCode object
        """
        data = await self._transport.apatch("/discountcodes", json=body)
        return DiscountCode.model_validate(data)

    def get(self, *, code: str) -> DiscountCode:
        """Get a discount code by code string.

        Args:
            code: The discount code

        Returns:
            DiscountCode object
        """
        data = self._transport.get(f"/discountcodes/{code}")
        return DiscountCode.model_validate(data)

    async def aget(self, *, code: str) -> DiscountCode:
        """Asynchronously get a discount code by code string.

        Args:
            code: The discount code

        Returns:
            DiscountCode object
        """
        data = await self._transport.aget(f"/discountcodes/{code}")
        return DiscountCode.model_validate(data)

    def delete(self, *, code: str) -> None:
        """Delete a discount code.

        Args:
            code: The discount code
        """
        self._transport.delete(f"/discountcodes/{code}")

    async def adelete(self, *, code: str) -> None:
        """Asynchronously delete a discount code.

        Args:
            code: The discount code
        """
        await self._transport.adelete(f"/discountcodes/{code}")
