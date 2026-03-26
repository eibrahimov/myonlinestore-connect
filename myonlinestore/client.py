"""High-level client for the MyOnlineStore Connect API.

Usage::

    from myonlinestore import ConnectClient

    client = ConnectClient(store_token="your-token")

    # List articles
    page = client.articles.list(limit=20)
    for article in page.items:
        print(article.name)

    # Get a single order
    order = client.orders.get(order_number=12345)
    print(order.status)

    # Async usage
    import asyncio

    async def main():
        async with ConnectClient(store_token="your-token") as client:
            page = await client.articles.alist(limit=20)
            print(page.items)

    asyncio.run(main())
"""

from __future__ import annotations

from typing import Any

from myonlinestore.config import ConnectConfig
from myonlinestore.http import HttpTransport
from myonlinestore.resources.articles import ArticlesResource
from myonlinestore.resources.categories import CategoriesResource
from myonlinestore.resources.customers import CustomersResource
from myonlinestore.resources.discount_codes import DiscountCodesResource
from myonlinestore.resources.newsletter import NewsletterResource
from myonlinestore.resources.orders import OrdersResource
from myonlinestore.resources.simple import (
    ArticleFieldsResource,
    ArticleListOptionsResource,
    ArticleListsResource,
    OfflineLocationsResource,
    OrderStatusesResource,
    PaymentGatewaysResource,
    ShippingMethodsResource,
    StoreResource,
    TaxPolicyResource,
)


class ConnectClient:
    """Pythonic client for the MyOnlineStore Connect API.

    Args:
        store_token: Merchant API token (required).
        partner_token: Partner application token (optional, needed for some endpoints).
        api_version: ``"1"`` (stable) or ``"2-beta"``.
        base_url: Override the default API base URL.
        language: Default language for responses (e.g. ``"en_GB"``).
        timeout: HTTP request timeout in seconds.
        config: Pass a pre-built :class:`ConnectConfig` instead of individual args.

    Examples::

        # Simple initialization
        client = ConnectClient(store_token="abc123")

        # With partner token and custom settings
        client = ConnectClient(
            store_token="abc123",
            partner_token="partner456",
            api_version="1",
            language="en_GB",
            timeout=60,
        )

        # Context manager (auto-closes connections)
        with ConnectClient(store_token="abc123") as client:
            articles = client.articles.list()

        # Async context manager
        async with ConnectClient(store_token="abc123") as client:
            articles = await client.articles.alist()
    """

    def __init__(
        self,
        store_token: str | None = None,
        *,
        partner_token: str | None = None,
        api_version: str = "1",
        base_url: str = "https://api.myonlinestore.com",
        language: str = "nl_NL",
        timeout: float = 30.0,
        config: ConnectConfig | None = None,
    ) -> None:
        if config is not None:
            self._config = config
        else:
            if store_token is None:
                raise ValueError("store_token is required (or pass a ConnectConfig via config=)")
            self._config = ConnectConfig(
                store_token=store_token,
                partner_token=partner_token,
                api_version=api_version,
                base_url=base_url,
                language=language,
                timeout=timeout,
            )

        self._transport = HttpTransport(self._config)

        # -- Resource namespaces -------------------------------------------------
        self.articles = ArticlesResource(self._transport)
        self.orders = OrdersResource(self._transport)
        self.customers = CustomersResource(self._transport)
        self.categories = CategoriesResource(self._transport)
        self.discount_codes = DiscountCodesResource(self._transport)
        self.newsletter = NewsletterResource(self._transport)
        self.order_statuses = OrderStatusesResource(self._transport)
        self.payment_gateways = PaymentGatewaysResource(self._transport)
        self.shipping_methods = ShippingMethodsResource(self._transport)
        self.store = StoreResource(self._transport)
        self.offline_locations = OfflineLocationsResource(self._transport)
        self.tax_policy = TaxPolicyResource(self._transport)
        self.article_fields = ArticleFieldsResource(self._transport)
        self.article_lists = ArticleListsResource(self._transport)
        self.article_list_options = ArticleListOptionsResource(self._transport)

    # -- Configuration access ----------------------------------------------------

    @property
    def config(self) -> ConnectConfig:
        """The active configuration."""
        return self._config

    # -- Context managers --------------------------------------------------------

    def __enter__(self) -> ConnectClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    async def __aenter__(self) -> ConnectClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    # -- Cleanup -----------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connections."""
        self._transport.close()

    async def aclose(self) -> None:
        """Asynchronously close the underlying HTTP connections."""
        await self._transport.aclose()
