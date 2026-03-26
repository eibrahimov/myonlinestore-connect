"""Customers resource for the MyOnlineStore API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from myonlinestore.models import Customer, CustomerAddress
from myonlinestore.pagination import PaginatedResponse
from myonlinestore.resources.base import Resource

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class CustomersResource(Resource):
    """Resource for managing customers.

    Note: The customer API wraps responses in ``{"customer": {...}}`` and
    ``{"addresses": [...]}`` — this resource handles unwrapping automatically.
    """

    # -- Customers CRUD ----------------------------------------------------------

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        q: str | None = None,
        embed: str | None = None,
    ) -> PaginatedResponse[Customer]:
        """List customers.

        Args:
            limit: Maximum number of items to return.
            offset: Number of items to skip.
            q: Search query string to filter customers.
            embed: Embed related resources (e.g. ``"addresses"``).
        """
        params = self._list_params(limit, offset, q=q, embed=embed)
        data = self._transport.get("/customers", params=params)
        raw = self._unwrap_list(data, "customers")
        items = [Customer.model_validate(item) for item in raw]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    async def alist(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        q: str | None = None,
        embed: str | None = None,
    ) -> PaginatedResponse[Customer]:
        """Asynchronously list customers.

        Args:
            limit: Maximum number of items to return.
            offset: Number of items to skip.
            q: Search query string to filter customers.
            embed: Embed related resources (e.g. ``"addresses"``).
        """
        params = self._list_params(limit, offset, q=q, embed=embed)
        data = await self._transport.aget("/customers", params=params)
        raw = self._unwrap_list(data, "customers")
        items = [Customer.model_validate(item) for item in raw]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    def create(self, *, body: dict[str, Any]) -> Customer:
        """Create a new customer."""
        data = self._transport.post("/customers", json=body)
        return Customer.model_validate(self._unwrap(data, "customer"))

    async def acreate(self, *, body: dict[str, Any]) -> Customer:
        """Asynchronously create a new customer."""
        data = await self._transport.apost("/customers", json=body)
        return Customer.model_validate(self._unwrap(data, "customer"))

    def get(self, *, customer_id: int | str) -> Customer:
        """Get a customer by ID."""
        data = self._transport.get(f"/customers/{customer_id}")
        return Customer.model_validate(self._unwrap(data, "customer"))

    async def aget(self, *, customer_id: int | str) -> Customer:
        """Asynchronously get a customer by ID."""
        data = await self._transport.aget(f"/customers/{customer_id}")
        return Customer.model_validate(self._unwrap(data, "customer"))

    def update(self, *, customer_id: int | str, body: dict[str, Any]) -> Customer:
        """Update a customer."""
        data = self._transport.patch(f"/customers/{customer_id}", json=body)
        return Customer.model_validate(self._unwrap(data, "customer"))

    async def aupdate(self, *, customer_id: int | str, body: dict[str, Any]) -> Customer:
        """Asynchronously update a customer."""
        data = await self._transport.apatch(f"/customers/{customer_id}", json=body)
        return Customer.model_validate(self._unwrap(data, "customer"))

    def delete(self, *, customer_id: int | str) -> None:
        """Delete a customer."""
        self._transport.delete(f"/customers/{customer_id}")

    async def adelete(self, *, customer_id: int | str) -> None:
        """Asynchronously delete a customer."""
        await self._transport.adelete(f"/customers/{customer_id}")

    # -- Addresses ---------------------------------------------------------------

    def list_addresses(
        self, *, customer_id: int | str
    ) -> PaginatedResponse[CustomerAddress]:
        """List addresses for a customer."""
        data = self._transport.get(f"/customers/{customer_id}/addresses")
        raw = self._unwrap_list(data, "addresses")
        items = [CustomerAddress.model_validate(item) for item in raw]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist_addresses(
        self, *, customer_id: int | str
    ) -> PaginatedResponse[CustomerAddress]:
        """Asynchronously list addresses for a customer."""
        data = await self._transport.aget(f"/customers/{customer_id}/addresses")
        raw = self._unwrap_list(data, "addresses")
        items = [CustomerAddress.model_validate(item) for item in raw]
        return PaginatedResponse(items=items, limit=50, offset=0)

    def create_address(
        self, *, customer_id: int | str, body: dict[str, Any]
    ) -> CustomerAddress:
        """Create an address for a customer."""
        data = self._transport.post(f"/customers/{customer_id}/addresses", json=body)
        return CustomerAddress.model_validate(self._unwrap(data, "address"))

    async def acreate_address(
        self, *, customer_id: int | str, body: dict[str, Any]
    ) -> CustomerAddress:
        """Asynchronously create an address for a customer."""
        data = await self._transport.apost(f"/customers/{customer_id}/addresses", json=body)
        return CustomerAddress.model_validate(self._unwrap(data, "address"))

    def get_address(
        self, *, customer_id: int | str, address_id: int | str
    ) -> CustomerAddress:
        """Get an address for a customer."""
        data = self._transport.get(f"/customers/{customer_id}/addresses/{address_id}")
        return CustomerAddress.model_validate(self._unwrap(data, "address"))

    async def aget_address(
        self, *, customer_id: int | str, address_id: int | str
    ) -> CustomerAddress:
        """Asynchronously get an address for a customer."""
        data = await self._transport.aget(f"/customers/{customer_id}/addresses/{address_id}")
        return CustomerAddress.model_validate(self._unwrap(data, "address"))

    def update_address(
        self, *, customer_id: int | str, address_id: int | str, body: dict[str, Any],
    ) -> CustomerAddress:
        """Update an address for a customer."""
        data = self._transport.patch(f"/customers/{customer_id}/addresses/{address_id}", json=body)
        return CustomerAddress.model_validate(self._unwrap(data, "address"))

    async def aupdate_address(
        self, *, customer_id: int | str, address_id: int | str, body: dict[str, Any],
    ) -> CustomerAddress:
        """Asynchronously update an address for a customer."""
        data = await self._transport.apatch(f"/customers/{customer_id}/addresses/{address_id}", json=body)
        return CustomerAddress.model_validate(self._unwrap(data, "address"))

    def delete_address(
        self, *, customer_id: int | str, address_id: int | str
    ) -> None:
        """Delete an address for a customer."""
        self._transport.delete(f"/customers/{customer_id}/addresses/{address_id}")

    async def adelete_address(
        self, *, customer_id: int | str, address_id: int | str
    ) -> None:
        """Asynchronously delete an address for a customer."""
        await self._transport.adelete(f"/customers/{customer_id}/addresses/{address_id}")
