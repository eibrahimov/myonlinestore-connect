"""Simple resources for the MyOnlineStore API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from myonlinestore.models import (
    Article,
    ArticleList,
    OfflineLocation,
    OrderStatus,
    PaymentGateway,
    ShippingMethod,
    Store,
    TaxPolicyRegion,
)
from myonlinestore.pagination import PaginatedResponse
from myonlinestore.resources.base import Resource

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class OrderStatusesResource(Resource):
    """Resource for retrieving order statuses."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(self) -> PaginatedResponse[OrderStatus]:
        """List order statuses.

        Returns:
            PaginatedResponse containing OrderStatus objects
        """
        data = self._transport.get("/orderstatuses")
        items = [OrderStatus.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist(self) -> PaginatedResponse[OrderStatus]:
        """Asynchronously list order statuses.

        Returns:
            PaginatedResponse containing OrderStatus objects
        """
        data = await self._transport.aget("/orderstatuses")
        items = [OrderStatus.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)


class PaymentGatewaysResource(Resource):
    """Resource for retrieving payment gateways."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(self) -> PaginatedResponse[PaymentGateway]:
        """List payment gateways (requires PartnerToken).

        Returns:
            PaginatedResponse containing PaymentGateway objects
        """
        data = self._transport.get("/payment/gateways")
        raw_items = self._unwrap_list(data, "gateways")
        items = [PaymentGateway.model_validate(item) for item in raw_items]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist(self) -> PaginatedResponse[PaymentGateway]:
        """Asynchronously list payment gateways (requires PartnerToken).

        Returns:
            PaginatedResponse containing PaymentGateway objects
        """
        data = await self._transport.aget("/payment/gateways")
        raw_items = self._unwrap_list(data, "gateways")
        items = [PaymentGateway.model_validate(item) for item in raw_items]
        return PaginatedResponse(items=items, limit=50, offset=0)

    def list_for_store(self, *, store: str) -> PaginatedResponse[PaymentGateway]:
        """List payment gateways for a specific store (requires PartnerToken).

        Args:
            store: The store identifier

        Returns:
            PaginatedResponse containing PaymentGateway objects
        """
        data = self._transport.get(f"/payment/stores/{store}/gateways")
        raw_items = self._unwrap_list(data, "gateways")
        items = [PaymentGateway.model_validate(item) for item in raw_items]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist_for_store(self, *, store: str) -> PaginatedResponse[PaymentGateway]:
        """Asynchronously list payment gateways for a specific store (requires PartnerToken).

        Args:
            store: The store identifier

        Returns:
            PaginatedResponse containing PaymentGateway objects
        """
        data = await self._transport.aget(f"/payment/stores/{store}/gateways")
        raw_items = self._unwrap_list(data, "gateways")
        items = [PaymentGateway.model_validate(item) for item in raw_items]
        return PaginatedResponse(items=items, limit=50, offset=0)


class ShippingMethodsResource(Resource):
    """Resource for retrieving shipping methods."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(self) -> PaginatedResponse[ShippingMethod]:
        """List shipping methods.

        Returns:
            PaginatedResponse containing ShippingMethod objects
        """
        data = self._transport.get("/shipping/methods")
        items = [ShippingMethod.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist(self) -> PaginatedResponse[ShippingMethod]:
        """Asynchronously list shipping methods.

        Returns:
            PaginatedResponse containing ShippingMethod objects
        """
        data = await self._transport.aget("/shipping/methods")
        items = [ShippingMethod.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)


class StoreResource(Resource):
    """Resource for retrieving store information."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def get(self) -> Store:
        """Get store information.

        Returns:
            Store object
        """
        data = self._transport.get("/store")
        return Store.model_validate(data)

    async def aget(self) -> Store:
        """Asynchronously get store information.

        Returns:
            Store object
        """
        data = await self._transport.aget("/store")
        return Store.model_validate(data)


class OfflineLocationsResource(Resource):
    """Resource for managing offline locations."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(self) -> PaginatedResponse[OfflineLocation]:
        """List offline locations.

        Returns:
            PaginatedResponse containing OfflineLocation objects
        """
        data = self._transport.get("/offlinelocations")
        items = [OfflineLocation.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist(self) -> PaginatedResponse[OfflineLocation]:
        """Asynchronously list offline locations.

        Returns:
            PaginatedResponse containing OfflineLocation objects
        """
        data = await self._transport.aget("/offlinelocations")
        items = [OfflineLocation.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)

    def get(self, *, location_id: int | str) -> OfflineLocation:
        """Get an offline location by ID.

        Args:
            location_id: The location ID

        Returns:
            OfflineLocation object
        """
        data = self._transport.get(f"/offlinelocations/{location_id}")
        return OfflineLocation.model_validate(data)

    async def aget(self, *, location_id: int | str) -> OfflineLocation:
        """Asynchronously get an offline location by ID.

        Args:
            location_id: The location ID

        Returns:
            OfflineLocation object
        """
        data = await self._transport.aget(f"/offlinelocations/{location_id}")
        return OfflineLocation.model_validate(data)


class TaxPolicyResource(Resource):
    """Resource for retrieving tax policy information."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(self) -> PaginatedResponse[TaxPolicyRegion]:
        """List tax policy regions.

        Returns:
            PaginatedResponse containing TaxPolicyRegion objects
        """
        data = self._transport.get("/tax-policy/regions")
        items = [TaxPolicyRegion.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist(self) -> PaginatedResponse[TaxPolicyRegion]:
        """Asynchronously list tax policy regions.

        Returns:
            PaginatedResponse containing TaxPolicyRegion objects
        """
        data = await self._transport.aget("/tax-policy/regions")
        items = [TaxPolicyRegion.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=50, offset=0)

    def get(self, *, code: str) -> TaxPolicyRegion:
        """Get a tax policy region by code.

        Args:
            code: The region code

        Returns:
            TaxPolicyRegion object
        """
        data = self._transport.get(f"/tax-policy/regions/{code}")
        return TaxPolicyRegion.model_validate(self._unwrap(data, "region"))

    async def aget(self, *, code: str) -> TaxPolicyRegion:
        """Asynchronously get a tax policy region by code.

        Args:
            code: The region code

        Returns:
            TaxPolicyRegion object
        """
        data = await self._transport.aget(f"/tax-policy/regions/{code}")
        return TaxPolicyRegion.model_validate(self._unwrap(data, "region"))


class ArticleFieldsResource(Resource):
    """Resource for managing article fields."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def create(self, *, article_id: int | str, body: dict[str, Any]) -> Article:
        """Create an article field.

        Args:
            article_id: The article ID
            body: Field data

        Returns:
            Updated Article object
        """
        data = self._transport.post(f"/articlefields/{article_id}", json=body)
        return Article.model_validate(data)

    async def acreate(
        self, *, article_id: int | str, body: dict[str, Any]
    ) -> Article:
        """Asynchronously create an article field.

        Args:
            article_id: The article ID
            body: Field data

        Returns:
            Updated Article object
        """
        data = await self._transport.apost(f"/articlefields/{article_id}", json=body)
        return Article.model_validate(data)

    def delete(self, *, article_id: int | str) -> Article:
        """Delete an article field.

        Args:
            article_id: The article ID

        Returns:
            Updated Article object
        """
        data = self._transport.delete(f"/articlefields/{article_id}")
        return Article.model_validate(data)

    async def adelete(self, *, article_id: int | str) -> Article:
        """Asynchronously delete an article field.

        Args:
            article_id: The article ID

        Returns:
            Updated Article object
        """
        data = await self._transport.adelete(f"/articlefields/{article_id}")
        return Article.model_validate(data)


class ArticleListsResource(Resource):
    """Resource for managing article lists."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def get(self, *, list_id: int | str) -> ArticleList:
        """Get an article list by ID.

        Args:
            list_id: The article list ID

        Returns:
            ArticleList object
        """
        data = self._transport.get(f"/articlelists/{list_id}")
        return ArticleList.model_validate(data)

    async def aget(self, *, list_id: int | str) -> ArticleList:
        """Asynchronously get an article list by ID.

        Args:
            list_id: The article list ID

        Returns:
            ArticleList object
        """
        data = await self._transport.aget(f"/articlelists/{list_id}")
        return ArticleList.model_validate(data)

    def add(self, *, list_id: int | str, body: dict[str, Any]) -> Article:
        """Add items to an article list.

        Args:
            list_id: The article list ID
            body: Data for items to add

        Returns:
            Updated Article object
        """
        data = self._transport.post(f"/articlelists/{list_id}", json=body)
        return Article.model_validate(data)

    async def aadd(self, *, list_id: int | str, body: dict[str, Any]) -> Article:
        """Asynchronously add items to an article list.

        Args:
            list_id: The article list ID
            body: Data for items to add

        Returns:
            Updated Article object
        """
        data = await self._transport.apost(f"/articlelists/{list_id}", json=body)
        return Article.model_validate(data)

    def remove(self, *, list_id: int | str) -> Article:
        """Remove items from an article list.

        Args:
            list_id: The article list ID

        Returns:
            Updated Article object
        """
        data = self._transport.delete(f"/articlelists/{list_id}")
        return Article.model_validate(data)

    async def aremove(self, *, list_id: int | str) -> Article:
        """Asynchronously remove items from an article list.

        Args:
            list_id: The article list ID

        Returns:
            Updated Article object
        """
        data = await self._transport.adelete(f"/articlelists/{list_id}")
        return Article.model_validate(data)


class ArticleListOptionsResource(Resource):
    """Resource for managing article list options."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def create(
        self, *, articlelist_id: int | str, body: dict[str, Any]
    ) -> ArticleList:
        """Create an article list option.

        Args:
            articlelist_id: The article list ID
            body: Option data

        Returns:
            ArticleList object
        """
        data = self._transport.post(f"/articlelistoptions/{articlelist_id}", json=body)
        return ArticleList.model_validate(data)

    async def acreate(
        self, *, articlelist_id: int | str, body: dict[str, Any]
    ) -> ArticleList:
        """Asynchronously create an article list option.

        Args:
            articlelist_id: The article list ID
            body: Option data

        Returns:
            ArticleList object
        """
        data = await self._transport.apost(
            f"/articlelistoptions/{articlelist_id}", json=body
        )
        return ArticleList.model_validate(data)

    def delete(self, *, articlelist_id: int | str) -> None:
        """Delete an article list option.

        Args:
            articlelist_id: The article list ID
        """
        self._transport.delete(f"/articlelistoptions/{articlelist_id}")

    async def adelete(self, *, articlelist_id: int | str) -> None:
        """Asynchronously delete an article list option.

        Args:
            articlelist_id: The article list ID
        """
        await self._transport.adelete(f"/articlelistoptions/{articlelist_id}")
