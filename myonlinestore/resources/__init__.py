"""MyOnlineStore API Resources."""
from __future__ import annotations

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

__all__ = [
    "ArticlesResource",
    "CategoriesResource",
    "CustomersResource",
    "DiscountCodesResource",
    "NewsletterResource",
    "OrdersResource",
    "ArticleFieldsResource",
    "ArticleListOptionsResource",
    "ArticleListsResource",
    "OfflineLocationsResource",
    "OrderStatusesResource",
    "PaymentGatewaysResource",
    "ShippingMethodsResource",
    "StoreResource",
    "TaxPolicyResource",
]
