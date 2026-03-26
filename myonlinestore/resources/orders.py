"""Orders resource for the MyOnlineStore API."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from myonlinestore.models import CountResponse, Order, Payment
from myonlinestore.pagination import PaginatedResponse
from myonlinestore.resources.base import Resource

if TYPE_CHECKING:
    from myonlinestore.http import HttpTransport


class OrdersResource(Resource):
    """Resource for managing orders."""

    def __init__(self, transport: HttpTransport) -> None:
        super().__init__(transport)

    def list(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        status_id: int | None = None,
        debtor_email: str | None = None,
        debtor_id: int | None = None,
        archived: bool | None = None,
        test: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        status_changed_start_date: str | None = None,
        status_changed_end_date: str | None = None,
    ) -> PaginatedResponse[Order]:
        """List orders.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            status_id: Filter by order status ID
            debtor_email: Filter by debtor email
            debtor_id: Filter by debtor ID
            archived: Filter by archived status
            test: Filter by test status
            created_start_date: Filter by creation date (start)
            created_end_date: Filter by creation date (end)
            changed_start_date: Filter by change date (start)
            changed_end_date: Filter by change date (end)
            status_changed_start_date: Filter by status change date (start)
            status_changed_end_date: Filter by status change date (end)

        Returns:
            PaginatedResponse containing Order objects
        """
        params = self._list_params(
            limit,
            offset,
            status_id=status_id,
            debtor_email=debtor_email,
            debtor_id=debtor_id,
            archived=archived,
            test=test,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            status_changed_start_date=status_changed_start_date,
            status_changed_end_date=status_changed_end_date,
        )
        data = self._transport.get("/orders", params=params)
        items = [Order.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    async def alist(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        status_id: int | None = None,
        debtor_email: str | None = None,
        debtor_id: int | None = None,
        archived: bool | None = None,
        test: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        status_changed_start_date: str | None = None,
        status_changed_end_date: str | None = None,
    ) -> PaginatedResponse[Order]:
        """Asynchronously list orders.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            status_id: Filter by order status ID
            debtor_email: Filter by debtor email
            debtor_id: Filter by debtor ID
            archived: Filter by archived status
            test: Filter by test status
            created_start_date: Filter by creation date (start)
            created_end_date: Filter by creation date (end)
            changed_start_date: Filter by change date (start)
            changed_end_date: Filter by change date (end)
            status_changed_start_date: Filter by status change date (start)
            status_changed_end_date: Filter by status change date (end)

        Returns:
            PaginatedResponse containing Order objects
        """
        params = self._list_params(
            limit,
            offset,
            status_id=status_id,
            debtor_email=debtor_email,
            debtor_id=debtor_id,
            archived=archived,
            test=test,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            status_changed_start_date=status_changed_start_date,
            status_changed_end_date=status_changed_end_date,
        )
        data = await self._transport.aget("/orders", params=params)
        items = [Order.model_validate(item) for item in (data or [])]
        return PaginatedResponse(items=items, limit=limit if limit is not None else 50, offset=offset if offset is not None else 0)

    def create(
        self,
        *,
        body: dict[str, Any],
        override_stock: bool | None = None,
        disable_shipping: bool | None = None,
        send_customer_notification: bool | None = None,
        send_merchant_notification: bool | None = None,
    ) -> Order:
        """Create a new order.

        Args:
            body: Order data
            override_stock: Override stock checks
            disable_shipping: Disable shipping calculation
            send_customer_notification: Send notification email to customer
            send_merchant_notification: Send notification email to merchant

        Returns:
            Created Order object
        """
        params: dict[str, Any] = {}
        if override_stock is not None:
            params["override_stock"] = override_stock
        if disable_shipping is not None:
            params["disable_shipping"] = disable_shipping
        if send_customer_notification is not None:
            params["send_customer_notification"] = send_customer_notification
        if send_merchant_notification is not None:
            params["send_merchant_notification"] = send_merchant_notification
        data = self._transport.post("/orders", json=body, params=params)
        return Order.model_validate(data)

    async def acreate(
        self,
        *,
        body: dict[str, Any],
        override_stock: bool | None = None,
        disable_shipping: bool | None = None,
        send_customer_notification: bool | None = None,
        send_merchant_notification: bool | None = None,
    ) -> Order:
        """Asynchronously create a new order.

        Args:
            body: Order data
            override_stock: Override stock checks
            disable_shipping: Disable shipping calculation
            send_customer_notification: Send notification email to customer
            send_merchant_notification: Send notification email to merchant

        Returns:
            Created Order object
        """
        params: dict[str, Any] = {}
        if override_stock is not None:
            params["override_stock"] = override_stock
        if disable_shipping is not None:
            params["disable_shipping"] = disable_shipping
        if send_customer_notification is not None:
            params["send_customer_notification"] = send_customer_notification
        if send_merchant_notification is not None:
            params["send_merchant_notification"] = send_merchant_notification
        data = await self._transport.apost("/orders", json=body, params=params)
        return Order.model_validate(data)

    def get(self, *, order_number: int | str) -> Order:
        """Get an order by order number.

        Args:
            order_number: The order number

        Returns:
            Order object
        """
        data = self._transport.get(f"/orders/{order_number}")
        return Order.model_validate(data)

    async def aget(self, *, order_number: int | str) -> Order:
        """Asynchronously get an order by order number.

        Args:
            order_number: The order number

        Returns:
            Order object
        """
        data = await self._transport.aget(f"/orders/{order_number}")
        return Order.model_validate(data)

    def update(self, *, order_number: int | str, body: dict[str, Any]) -> Order:
        """Update an order.

        Args:
            order_number: The order number
            body: Updated order data

        Returns:
            Updated Order object
        """
        data = self._transport.patch(f"/orders/{order_number}", json=body)
        return Order.model_validate(data)

    async def aupdate(self, *, order_number: int | str, body: dict[str, Any]) -> Order:
        """Asynchronously update an order.

        Args:
            order_number: The order number
            body: Updated order data

        Returns:
            Updated Order object
        """
        data = await self._transport.apatch(f"/orders/{order_number}", json=body)
        return Order.model_validate(data)

    def count(
        self,
        *,
        status_id: int | None = None,
        debtor_email: str | None = None,
        debtor_id: int | None = None,
        archived: bool | None = None,
        test: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        status_changed_start_date: str | None = None,
        status_changed_end_date: str | None = None,
    ) -> int:
        """Get the total count of orders.

        Args:
            status_id: Filter by order status ID
            debtor_email: Filter by debtor email
            debtor_id: Filter by debtor ID
            archived: Filter by archived status
            test: Filter by test status
            created_start_date: Filter by creation date (start)
            created_end_date: Filter by creation date (end)
            changed_start_date: Filter by change date (start)
            changed_end_date: Filter by change date (end)
            status_changed_start_date: Filter by status change date (start)
            status_changed_end_date: Filter by status change date (end)

        Returns:
            Total number of orders.
        """
        params = self._list_params(
            None,
            None,
            status_id=status_id,
            debtor_email=debtor_email,
            debtor_id=debtor_id,
            archived=archived,
            test=test,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            status_changed_start_date=status_changed_start_date,
            status_changed_end_date=status_changed_end_date,
        )
        data = self._transport.get("/orders/count", params=params)
        return CountResponse.model_validate(data).count

    async def acount(
        self,
        *,
        status_id: int | None = None,
        debtor_email: str | None = None,
        debtor_id: int | None = None,
        archived: bool | None = None,
        test: bool | None = None,
        created_start_date: str | None = None,
        created_end_date: str | None = None,
        changed_start_date: str | None = None,
        changed_end_date: str | None = None,
        status_changed_start_date: str | None = None,
        status_changed_end_date: str | None = None,
    ) -> int:
        """Asynchronously get the total count of orders.

        Args:
            status_id: Filter by order status ID
            debtor_email: Filter by debtor email
            debtor_id: Filter by debtor ID
            archived: Filter by archived status
            test: Filter by test status
            created_start_date: Filter by creation date (start)
            created_end_date: Filter by creation date (end)
            changed_start_date: Filter by change date (start)
            changed_end_date: Filter by change date (end)
            status_changed_start_date: Filter by status change date (start)
            status_changed_end_date: Filter by status change date (end)

        Returns:
            Total number of orders.
        """
        params = self._list_params(
            None,
            None,
            status_id=status_id,
            debtor_email=debtor_email,
            debtor_id=debtor_id,
            archived=archived,
            test=test,
            created_start_date=created_start_date,
            created_end_date=created_end_date,
            changed_start_date=changed_start_date,
            changed_end_date=changed_end_date,
            status_changed_start_date=status_changed_start_date,
            status_changed_end_date=status_changed_end_date,
        )
        data = await self._transport.aget("/orders/count", params=params)
        return CountResponse.model_validate(data).count

    def create_credit(self, *, body: dict[str, Any]) -> Order:
        """Create a credit order.

        Args:
            body: Credit order data

        Returns:
            Created credit Order object
        """
        data = self._transport.post("/orders/credit", json=body)
        return Order.model_validate(data)

    async def acreate_credit(self, *, body: dict[str, Any]) -> Order:
        """Asynchronously create a credit order.

        Args:
            body: Credit order data

        Returns:
            Created credit Order object
        """
        data = await self._transport.apost("/orders/credit", json=body)
        return Order.model_validate(data)

    def list_payments(
        self, *, order_number: int | str
    ) -> PaginatedResponse[Payment]:
        """List payments for an order.

        Args:
            order_number: The order number

        Returns:
            PaginatedResponse containing Payment objects
        """
        data = self._transport.get(f"/orders/{order_number}/payments")
        raw = self._unwrap_list(data, "payments")
        items = [Payment.model_validate(item) for item in raw]
        return PaginatedResponse(items=items, limit=50, offset=0)

    async def alist_payments(
        self, *, order_number: int | str
    ) -> PaginatedResponse[Payment]:
        """Asynchronously list payments for an order.

        Args:
            order_number: The order number

        Returns:
            PaginatedResponse containing Payment objects
        """
        data = await self._transport.aget(f"/orders/{order_number}/payments")
        raw = self._unwrap_list(data, "payments")
        items = [Payment.model_validate(item) for item in raw]
        return PaginatedResponse(items=items, limit=50, offset=0)

    def create_payment(
        self, *, order_number: int | str, body: dict[str, Any]
    ) -> Payment:
        """Create a payment for an order.

        The API returns ``{"payment": {...}, "url": "..."}`` on success (HTTP 201).
        The ``url`` field contains the payment redirect URL when applicable.

        Args:
            order_number: The order number
            body: Payment data

        Returns:
            Created Payment object
        """
        data = self._transport.post(f"/orders/{order_number}/payments", json=body)
        return Payment.model_validate(self._unwrap(data, "payment"))

    async def acreate_payment(
        self, *, order_number: int | str, body: dict[str, Any]
    ) -> Payment:
        """Asynchronously create a payment for an order.

        The API returns ``{"payment": {...}, "url": "..."}`` on success (HTTP 201).
        The ``url`` field contains the payment redirect URL when applicable.

        Args:
            order_number: The order number
            body: Payment data

        Returns:
            Created Payment object
        """
        data = await self._transport.apost(f"/orders/{order_number}/payments", json=body)
        return Payment.model_validate(self._unwrap(data, "payment"))

    def create_payment_raw(
        self, *, order_number: int | str, body: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a payment and return the full response including the redirect URL.

        Args:
            order_number: The order number
            body: Payment data

        Returns:
            Dict with ``"payment"`` and ``"url"`` keys.
        """
        data = self._transport.post(f"/orders/{order_number}/payments", json=body)
        return data

    async def acreate_payment_raw(
        self, *, order_number: int | str, body: dict[str, Any]
    ) -> dict[str, Any]:
        """Asynchronously create a payment and return the full response including the redirect URL.

        Args:
            order_number: The order number
            body: Payment data

        Returns:
            Dict with ``"payment"`` and ``"url"`` keys.
        """
        data = await self._transport.apost(f"/orders/{order_number}/payments", json=body)
        return data

    def update_payment(
        self, *, order_number: int | str, payment_id: int | str, body: dict[str, Any]
    ) -> Payment:
        """Update a payment.

        Args:
            order_number: The order number
            payment_id: The payment ID
            body: Updated payment data

        Returns:
            Updated Payment object
        """
        data = self._transport.patch(
            f"/orders/{order_number}/payments/{payment_id}", json=body
        )
        return Payment.model_validate(self._unwrap(data, "payment"))

    async def aupdate_payment(
        self, *, order_number: int | str, payment_id: int | str, body: dict[str, Any]
    ) -> Payment:
        """Asynchronously update a payment.

        Args:
            order_number: The order number
            payment_id: The payment ID
            body: Updated payment data

        Returns:
            Updated Payment object
        """
        data = await self._transport.apatch(
            f"/orders/{order_number}/payments/{payment_id}", json=body
        )
        return Payment.model_validate(self._unwrap(data, "payment"))

    def delete_payment(self, *, order_number: int | str, payment_id: int | str) -> None:
        """Delete a payment.

        Args:
            order_number: The order number
            payment_id: The payment ID
        """
        self._transport.delete(f"/orders/{order_number}/payments/{payment_id}")

    async def adelete_payment(
        self, *, order_number: int | str, payment_id: int | str
    ) -> None:
        """Asynchronously delete a payment.

        Args:
            order_number: The order number
            payment_id: The payment ID
        """
        await self._transport.adelete(f"/orders/{order_number}/payments/{payment_id}")
