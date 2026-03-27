"""
Pydantic models for MyOnlineStore Connect API.

This module contains all data models for the MyOnlineStore Connect API v1,
including price models, articles, orders, payments, customers, categories, and more.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _ConnectModel(BaseModel):
    """Internal base for all MyOnlineStore models.

    Provides a compact ``__repr__`` that only shows non-None fields,
    making debugging output readable for models with many optional fields.
    """

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if v is not None and not k.startswith("_")
        )
        return f"{type(self).__name__}({fields})"


# ============================================================================
# PRICE MODELS
# ============================================================================


class ArticlePrice(_ConnectModel):
    """Article price information.

    Represents pricing for an article including default, action (discounted),
    and purchase prices.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    default: Optional[str] = None
    """The default price for which the product is offered (incl. tax depending on store.prices_include_tax)"""

    action: Optional[str] = None
    """The discounted price; overrides the default offer (incl. tax depending on store.prices_include_tax)"""

    purchase: Optional[str] = None
    """The purchase price (excl. tax)"""


class TaxPrice(_ConnectModel):
    """Tax price information.

    Represents tax information including VAT rate and amounts.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    rate: Optional[str] = None
    """VAT percentage"""

    amount: Optional[str] = None
    """Amount (excluding tax), may have up to 6 decimals"""

    amount_including_tax: Optional[str] = None
    """Amount (including tax) with exactly 2 decimals"""


class OrderPrice(_ConnectModel):
    """Order total price information.

    Contains tax charges and total order price.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    tax: Optional[list[TaxPrice]] = None
    """VAT charge(s)"""

    total: Optional[str] = None
    """Total order price"""

    @field_validator("tax", mode="before")
    @classmethod
    def _coerce_single_tax_to_list(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return [value]
        return value


# ============================================================================
# ARTICLE MODELS
# ============================================================================


class ArticleExtraFieldSet(_ConnectModel):
    """Extra fields for articles.

    Contains visible and invisible custom fields.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    visible: Optional[dict[str, Any]] = None
    """Visible custom fields"""

    invisible: Optional[dict[str, Any]] = None
    """Invisible custom fields"""


class ArticleImage(_ConnectModel):
    """Article image information.

    Represents an image attached to an article.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    position: Optional[int] = None
    """Image position in the list"""

    id: Optional[str] = None
    """Image identifier (UUID)"""

    original_name: Optional[str] = None
    """Base name of the originally uploaded file"""

    url: Optional[str] = None
    """Deprecated: use urls instead"""

    urls: Optional[dict[str, Any]] = None
    """Image URLs in different sizes"""


class ArticleImagePostable(_ConnectModel):
    """Article image for POST operations.

    Used when creating or updating articles with images.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Image identifier"""

    position: Optional[int] = None
    """Image position"""

    url: Optional[str] = None
    """Image URL"""


class ArticleListOption(_ConnectModel):
    """Option for an article configurator list.

    Represents a single option within an article list (variant options).
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Option identifier"""

    name: Optional[str] = None
    """Option name"""

    price: Optional[str] = None
    """Price modifier for this option"""


class ArticleList(_ConnectModel):
    """Article configurator list.

    Represents a list of options that can be configured for an article.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """List identifier"""

    name: Optional[str] = None
    """List name"""

    description: Optional[str] = None
    """List description"""

    options: Optional[list[ArticleListOption]] = None
    """Available options in this list"""


class ArticleVariantOption(_ConnectModel):
    """Article variant option.

    Represents a selected option in a variant.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    list_id: Optional[int] = None
    """List identifier"""

    option_id: Optional[int] = None
    """Option identifier"""

    name: Optional[str] = None
    """Option name"""


class ArticleVariant(_ConnectModel):
    """Article variant.

    Represents a product variant with specific options and stock.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Variant identifier"""

    options: Optional[list[ArticleVariantOption]] = None
    """Selected options for this variant"""

    stock: Optional[int] = None
    """Available stock for this variant"""

    can_backorder: Optional[bool] = None
    """Whether backorders are allowed for this variant"""


class ArticleLimited(_ConnectModel):
    """Limited article representation returned by category article listings."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Article identifier"""

    name: Optional[str] = None
    """Article name"""

    uuid: Optional[str] = None
    """Article UUID"""

    is_main: Optional[bool] = None
    """Whether this is the primary category for the article"""


class Article(_ConnectModel):
    """Article (product).

    Represents a complete product with all details, pricing, stock, and variants.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Article identifier"""

    uuid: Optional[str] = None
    """Article UUID"""

    name: Optional[str] = None
    """Article name"""

    description: Optional[str] = None
    """Article description"""

    sku: Optional[str] = None
    """Stock keeping unit"""

    badge_text: Optional[str] = None
    """Badge text to display on product"""

    taxable: Optional[bool] = None
    """Whether this article is taxable"""

    price: Optional[ArticlePrice] = None
    """Pricing information"""

    stock: Optional[int] = None
    """Available stock"""

    delivery_days: Optional[int] = None
    """Estimated delivery time in days"""

    meta_title: Optional[str] = None
    """SEO meta title"""

    meta_description: Optional[str] = None
    """SEO meta description"""

    extra: Optional[ArticleExtraFieldSet] = None
    """Extra custom fields"""

    created_date: Optional[str] = None
    """Creation date"""

    created_time: Optional[str] = None
    """Creation time"""

    updated_date: Optional[str] = None
    """Last update date"""

    updated_time: Optional[str] = None
    """Last update time"""

    can_backorder: Optional[bool] = None
    """Whether backorders are allowed"""

    categories: Optional[list[dict[str, Any]]] = None
    """Associated categories"""

    lists: Optional[list[ArticleList]] = None
    """Configurator lists"""

    images: Optional[list[ArticleImage]] = None
    """Article images"""

    variants: Optional[list[ArticleVariant]] = None
    """Product variants"""


# ============================================================================
# ORDER MODELS
# ============================================================================


class OrderComment(_ConnectModel):
    """Order comments.

    Contains customer-facing and internal comments for an order.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    customer: Optional[str] = None
    """Customer-facing comment"""

    internal: Optional[str] = None
    """Internal comment (not visible to customer)"""


class Address(_ConnectModel):
    """Physical address.

    Represents a complete postal address.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Address identifier"""

    gender: Optional[str] = None
    """Gender (M/F)"""

    name: Optional[str] = None
    """Full name"""

    company: Optional[str] = None
    """Company name"""

    phone: Optional[str] = None
    """Phone number"""

    street: Optional[str] = None
    """Street name"""

    number: Optional[str] = None
    """Street number (may include suffix)"""

    zipcode: Optional[str] = None
    """Postal code"""

    city: Optional[str] = None
    """City name"""

    country_code: Optional[str] = None
    """ISO 3166-1 alpha-2 country code"""

    country_description: Optional[str] = None
    """Country name"""

    bankaccount: Optional[str] = None
    """Bank account number"""

    vat_number: Optional[str] = None
    """VAT/Tax number"""


class InvoiceAddress(_ConnectModel):
    """Invoice address.

    Represents the invoice delivery address (same fields as Address).
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Address identifier"""

    gender: Optional[str] = None
    """Gender (M/F)"""

    name: Optional[str] = None
    """Full name"""

    company: Optional[str] = None
    """Company name"""

    phone: Optional[str] = None
    """Phone number"""

    street: Optional[str] = None
    """Street name"""

    number: Optional[str] = None
    """Street number (may include suffix)"""

    zipcode: Optional[str] = None
    """Postal code"""

    city: Optional[str] = None
    """City name"""

    country_code: Optional[str] = None
    """ISO 3166-1 alpha-2 country code"""

    country_description: Optional[str] = None
    """Country name"""

    country: Optional[str] = None
    """Country name"""

    bankaccount: Optional[str] = None
    """Bank account number"""

    vat_number: Optional[str] = Field(None, alias="taxnumber")
    """VAT/Tax number (``taxnumber`` in API)"""


class OrderAddress(_ConnectModel):
    """Order addresses.

    Contains both invoice and delivery addresses for an order.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    invoice: Optional[InvoiceAddress] = None
    """Invoice address"""

    delivery: Optional[Address] = None
    """Delivery address"""


class OrderShippingCountry(_ConnectModel):
    """Shipping country information.

    Represents a country in shipping details.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    description: Optional[str] = None
    """Country name"""

    isocode: Optional[str] = None
    """ISO 3166-1 alpha-2 country code"""


class OrderShipping(_ConnectModel):
    """Order shipping information.

    Contains shipping-related details for an order.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    country: Optional[OrderShippingCountry] = None
    """Shipping destination country"""

    @field_validator("country", mode="before")
    @classmethod
    def _empty_country_list_to_none(cls, value: Any) -> Any:
        if value == []:
            return None
        return value


class OrderDebtor(_ConnectModel):
    """Order debtor (customer) information.

    Represents the customer placing the order.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Debtor identifier"""

    gender: Optional[str] = None
    """Gender (M/F)"""

    name: Optional[str] = None
    """Full name"""

    company: Optional[str] = None
    """Company name"""

    email: Optional[str] = None
    """Email address"""

    phone: Optional[str] = None
    """Phone number"""

    bankaccount: Optional[str] = None
    """Bank account number"""

    link_to_account: Optional[str] = None
    """Link to customer account"""

    address: Optional[OrderAddress] = None
    """Invoice and delivery addresses"""


class OrderPaymentStatus(_ConnectModel):
    """Order payment status details."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Numeric payment status code"""

    text: Optional[str] = None
    """Human-readable payment status"""


class OrderPaymentSummary(_ConnectModel):
    """Order payment summary.

    Contains summary information about the payment method and status.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    gateway_name: Optional[str] = None
    """Payment gateway name"""

    method_name: Optional[str] = None
    """Payment method name"""

    status: Optional[OrderPaymentStatus] = None
    """Payment status"""


class OrderDetail(_ConnectModel):
    """Order line item detail.

    Represents a single item in an order.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Item identifier"""

    type: Optional[str] = None
    """Item type (article, shipping, discount, etc.)"""

    quantity: Optional[int] = None
    """Quantity ordered"""

    unit_price: Optional[str] = None
    """Price per unit"""

    unit_weight: Optional[str] = None
    """Weight per unit"""

    price_override: Optional[bool] = None
    """Whether price was manually overridden"""

    description: Optional[str] = None
    """Item description"""

    price: Optional[TaxPrice | list[TaxPrice]] = None
    """Total price for this item"""

    @field_validator("price", mode="before")
    @classmethod
    def _coerce_single_price(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return TaxPrice.model_validate(value)
        return value


class OrderStatus(_ConnectModel):
    """Order status information.

    Represents the current status of an order.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    status: Optional[int] = None
    """Numeric status code"""

    description: Optional[str] = None
    """Status description"""

    credit_order: Optional[bool] = None
    """Whether this is a credit order"""


class Order(_ConnectModel):
    """Order.

    Represents a complete customer order with all details, items, and payment information.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    number: Optional[str] = None
    """Order number"""

    uuid: Optional[str] = None
    """Order UUID"""

    date: Optional[str] = None
    """Order date"""

    time: Optional[str] = None
    """Order time"""

    status: Optional[int] = None
    """Order status code"""

    status_changed_date: Optional[str] = None
    """Date when status last changed"""

    status_changed_time: Optional[str] = None
    """Time when status last changed"""

    weight: Optional[str] = None
    """Total order weight"""

    archived: Optional[bool] = None
    """Whether the order is archived"""

    finished: Optional[bool] = None
    """Whether the order is finished"""

    taxed: Optional[str] = None
    """Whether tax is applied"""

    locale: Optional[str] = None
    """Customer locale"""

    discountcode: Optional[str] = None
    """Applied discount code"""

    currency: Optional[str] = None
    """Order currency code"""

    currency_format_locale: Optional[str] = None
    """Locale for currency formatting"""

    credited_order_number: Optional[int] = None
    """If this is a credit order, the original order number"""

    credit_order_numbers: Optional[list[str | int]] = None
    """Order numbers of any credit orders created from this order"""

    comments: Optional[OrderComment] = None
    """Order comments"""

    business_model: Optional[str] = None
    """Business model (B2C or B2B)"""

    reference: Optional[str] = None
    """Custom reference (e.g., PO number for B2B)"""

    tax_region: Optional[str] = None
    """Tax region"""

    tax_strategy: Optional[str] = None
    """Applied tax strategy"""

    partner: Optional[dict[str, Any]] = None
    """Partner information"""

    payment_status: Optional[str] = None
    """Payment status"""

    payment: Optional[OrderPaymentSummary] = None
    """Payment summary"""

    debtor: Optional[OrderDebtor] = None
    """Customer/debtor information"""

    price: Optional[OrderPrice] = None
    """Price information"""

    orderlines: Optional[list[OrderDetail]] = None
    """Order line items"""

    shipping: Optional[list[OrderShipping]] = None
    """Shipping information"""


# ============================================================================
# PAYMENT MODELS
# ============================================================================


class PaymentMutation(_ConnectModel):
    """Payment mutation.

    Represents a transaction or status change for a payment.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Mutation identifier"""

    type: Optional[str] = None
    """Mutation type: ``authorize``, ``capture``, ``failed``, ``refund``, or ``void``"""

    reference: Optional[str] = None
    """Reference from payment gateway"""

    price: Optional[str] = None
    """Mutation amount"""

    description: Optional[str] = None
    """Mutation description"""

    created_at: Optional[str] = Field(None, alias="createdAt")
    """When the mutation was created"""

    expires_at: Optional[str] = Field(None, alias="expiresAt")
    """When the mutation expires"""


class Payment(_ConnectModel):
    """Payment.

    Represents a payment transaction.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Payment identifier"""

    gateway: Optional[str] = None
    """Payment gateway name"""

    method: Optional[str] = None
    """Payment method name"""

    gateway_reference: Optional[str] = Field(None, alias="gatewayReference")
    """Reference from payment gateway"""

    price: Optional[str] = None
    """Payment amount"""

    currency: Optional[str] = None
    """Currency code"""

    store_id: Optional[str] = Field(None, alias="storeId")
    """Store identifier"""

    reference: Optional[str] = None
    """Custom reference"""

    is_test: Optional[bool] = Field(None, alias="isTest")
    """Whether this is a test payment"""

    created_at: Optional[str] = Field(None, alias="createdAt")
    """When the payment was created"""

    updated_at: Optional[str] = Field(None, alias="updatedAt")
    """When the payment was last updated"""

    order: Optional[int] = None
    """Associated order number"""

    properties: Optional[dict[str, Any]] = None
    """Additional payment properties"""

    referrer_url: Optional[str] = Field(None, alias="referrerUrl")
    """Referrer URL for this payment"""

    mutations: Optional[list[PaymentMutation]] = None
    """Payment mutations/transactions"""


class PaymentMethod(_ConnectModel):
    """Payment method.

    Represents a specific payment method (e.g., Visa, iDEAL).
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: Optional[str] = None
    """Method technical name"""

    display_name: Optional[str] = Field(None, alias="displayName")
    """User-friendly method name"""


class PaymentGateway(_ConnectModel):
    """Payment gateway.

    Represents a payment service provider and its available methods.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: Optional[str] = None
    """Gateway technical name"""

    display_name: Optional[str] = Field(None, alias="displayName")
    """User-friendly gateway name"""

    website_url: Optional[str] = Field(None, alias="websiteUrl")
    """Gateway website URL"""

    methods: Optional[list[PaymentMethod]] = None
    """Available payment methods"""


# ============================================================================
# CUSTOMER MODELS
# ============================================================================


class CustomerAddress(_ConnectModel):
    """Customer address.

    Represents an address in a customer's address book.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Address identifier (UUID)"""

    first_name: Optional[str] = Field(None, alias="firstName")
    """First name"""

    last_name: Optional[str] = Field(None, alias="lastName")
    """Last name"""

    street: Optional[str] = None
    """Street name"""

    street_number: Optional[str] = Field(None, alias="streetNumber")
    """Street number (may include suffix)"""

    zip_code: Optional[str] = Field(None, alias="zipCode")
    """Postal code"""

    city: Optional[str] = None
    """City name"""

    country_code: Optional[str] = Field(None, alias="countryCode")
    """ISO 3166-1 alpha-2 country code"""

    company: Optional[str] = None
    """Company name"""

    gender: Optional[str] = None
    """Gender (M/F)"""

    phone: Optional[str] = None
    """Phone number"""

    tax_number: Optional[str] = Field(None, alias="taxNumber")
    """VAT/Tax number"""

    iban: Optional[str] = None
    """International Bank Account Number"""

    is_default_for_delivery: Optional[bool] = Field(None, alias="isDefaultForDelivery")
    """Whether this is the default delivery address"""

    is_default_for_invoice: Optional[bool] = Field(None, alias="isDefaultForInvoice")
    """Whether this is the default invoice address"""


class Customer(_ConnectModel):
    """Customer.

    Represents a store customer.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Customer identifier (UUID)"""

    store_id: Optional[str] = Field(None, alias="storeId")
    """Store identifier"""

    email: Optional[str] = None
    """Email address"""

    first_name: Optional[str] = Field(None, alias="firstName")
    """First name"""

    last_name: Optional[str] = Field(None, alias="lastName")
    """Last name"""

    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    """Date of birth (YYYY-MM-DD)"""

    description: Optional[str] = None
    """Customer notes"""

    addresses: Optional[list[CustomerAddress]] = None
    """Customer addresses"""


# ============================================================================
# CATEGORY MODELS
# ============================================================================


class CategorySorting(_ConnectModel):
    """Category sorting information.

    Contains ordering information for categories.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    first: Optional[int] = None
    """First category ID in sort order"""

    last: Optional[int] = None
    """Last category ID in sort order"""

    previous: Optional[int] = None
    """Previous category ID in sort order"""

    next: Optional[int] = Field(None, alias="next")
    """Next category ID in sort order"""


class Category(_ConnectModel):
    """Product category.

    Represents a product category/collection.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[int] = None
    """Category identifier"""

    parent_category_id: Optional[int] = None
    """Parent category identifier (for subcategories)"""

    hidden: Optional[bool] = None
    """Whether the category is hidden from customers"""

    title: Optional[str] = None
    """Category title/name"""

    content: Optional[str] = None
    """Category description"""

    meta_title: Optional[str] = None
    """SEO meta title"""

    meta_description: Optional[str] = None
    """SEO meta description"""

    article_order: Optional[int] = None
    """Default article sort order"""

    leafs: Optional[list["Category"]] = None
    """Subcategories"""

    sorting: Optional[CategorySorting] = None
    """Sorting information"""


# ============================================================================
# DISCOUNT CODE MODELS
# ============================================================================


class DiscountCode(_ConnectModel):
    """Discount code.

    Represents a promotional discount code.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Discount code identifier"""

    code: Optional[str] = None
    """The actual discount code string"""

    description: Optional[str] = None
    """Description of the discount"""

    percentage_discount: Optional[str] = None
    """Percentage discount (e.g., '10' for 10%)"""

    fixed_discount: Optional[str] = None
    """Fixed discount amount"""

    minimum_order_price: Optional[str] = None
    """Minimum order value required"""

    minimum_products: Optional[int] = None
    """Minimum number of products required"""

    applies_to_shipping: Optional[bool] = None
    """Whether discount applies to shipping costs"""

    free_shipping: Optional[bool] = None
    """Whether code provides free shipping"""

    applies_to_action_prices: Optional[bool] = None
    """Whether discount applies to discounted items"""

    single_use: Optional[bool] = None
    """Whether code can only be used once"""

    active: Optional[bool] = None
    """Whether the discount code is currently active"""

    valid_from: Optional[str] = None
    """Code validity start date"""

    valid_until: Optional[str] = None
    """Code validity end date"""

    valid_article_ids: Optional[list[str]] = None
    """Specific articles the code applies to (whitelist)"""

    valid_product_ids: Optional[list[dict[str, Any]]] = None
    """Specific products the code applies to"""

    invalid_article_ids: Optional[list[str]] = None
    """Articles the code does not apply to (blacklist)"""

    invalid_product_ids: Optional[list[str]] = None
    """Products the code does not apply to"""

    valid_category_ids: Optional[list[str]] = None
    """Categories the code applies to"""

    invalid_category_ids: Optional[list[str]] = None
    """Categories the code does not apply to"""

    customer_id: Optional[str] = None
    """Customer ID if code is customer-specific"""


# ============================================================================
# NEWSLETTER MODELS
# ============================================================================


class NewsletterSubscriber(_ConnectModel):
    """Newsletter subscriber.

    Represents a newsletter subscription.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    email: Optional[str] = None
    """Subscriber email address"""

    name: Optional[str] = None
    """Subscriber name"""

    activated: Optional[bool] = None
    """Whether the subscription is activated/confirmed"""

    created_date: Optional[str] = None
    """Subscription creation date"""

    created_time: Optional[str] = None
    """Subscription creation time"""


# ============================================================================
# STORE & LOCATION MODELS
# ============================================================================


class OfflineLocation(_ConnectModel):
    """Physical store location.

    Represents an offline store location (brick-and-mortar).
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Location identifier"""

    name: Optional[str] = None
    """Location name"""

    street: Optional[str] = None
    """Street name"""

    street_number: Optional[str] = None
    """Street number (may include suffix)"""

    zipcode: Optional[str] = None
    """Postal code"""

    city: Optional[str] = None
    """City name"""

    country_code: Optional[str] = None
    """ISO 3166-1 alpha-2 country code"""

    phone: Optional[str] = None
    """Phone number"""

    email: Optional[str] = None
    """Email address"""

    country: Optional[str] = None
    """Country name"""

    deleted: Optional[bool] = None
    """Whether the location is deleted"""

    note: Optional[str] = None
    """Additional notes"""


class ShippingMethod(_ConnectModel):
    """Shipping method.

    Represents a shipping option available in the store.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Shipping method identifier"""

    display_name: Optional[str] = None
    """User-friendly method name"""

    countries: Optional[list[str]] = None
    """Country codes this method applies to"""

    default: Optional[bool] = None
    """Whether this is the default shipping method"""

    no_costs_above: Optional[str] = None
    """Order value above which shipping is free"""


class Store(_ConnectModel):
    """Store information.

    Represents the online store.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = None
    """Store identifier"""

    name: Optional[str] = None
    """Store name"""

    primary_domain: Optional[str] = None
    """Primary domain name"""

    description: Optional[str] = None
    """Store description"""

    open: Optional[bool] = None
    """Whether the store is open to customers"""

    version: Optional[str] = None
    """API version"""

    administration_language: Optional[str] = None
    """Administration interface language"""

    currency: Optional[str] = None
    """Store currency code"""

    email: Optional[str] = None
    """Store contact email"""

    region_code: Optional[str] = None
    """Store region code"""

    default_language: Optional[str] = None
    """Default store language"""

    active_languages: Optional[list[str]] = None
    """Active languages in the store"""

    available_business_models: Optional[str] = None
    """Available business models"""

    currency_format_locale: Optional[str] = None
    """Locale used for currency formatting"""

    prices_include_tax: Optional[bool] = None
    """Whether displayed prices include tax"""


# ============================================================================
# TAX MODELS
# ============================================================================


class TaxPolicyRegion(_ConnectModel):
    """Tax policy for a region.

    Represents tax configuration for a specific region/country.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    region_code: Optional[str] = Field(None, alias="regionCode")
    """ISO 3166-1 alpha-2 region/country code"""

    tax_enabled: Optional[bool] = Field(None, alias="taxEnabled")
    """Whether tax is enabled for this region"""

    tax_number: Optional[str] = Field(None, alias="taxNumber")
    """Tax registration number"""

    tax_rate: Optional[str] = Field(None, alias="taxRate")
    """Default tax rate percentage"""

    shipping_tax_method: Optional[str] = Field(None, alias="shippingTaxMethod")
    """How shipping tax is calculated"""

    shipping_tax_rate: Optional[str] = Field(None, alias="shippingTaxRate")
    """Shipping tax rate percentage"""

    transaction_tax_method: Optional[str] = Field(None, alias="transactionTaxMethod")
    """How transaction tax is calculated"""

    transaction_tax_rate: Optional[str] = Field(None, alias="transactionTaxRate")
    """Transaction tax rate percentage"""


# ============================================================================
# UTILITY MODELS
# ============================================================================


class CountResponse(_ConnectModel):
    """Count response.

    Used by endpoints that return a count of items.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    count: int
    """The count of items"""


# ============================================================================
# EXPORTS
# ============================================================================


__all__ = [
    # Price models
    "ArticlePrice",
    "TaxPrice",
    "OrderPrice",
    # Article models
    "ArticleExtraFieldSet",
    "ArticleImage",
    "ArticleImagePostable",
    "ArticleListOption",
    "ArticleList",
    "ArticleVariantOption",
    "ArticleVariant",
    "ArticleLimited",
    "Article",
    # Order models
    "OrderComment",
    "Address",
    "InvoiceAddress",
    "OrderAddress",
    "OrderDebtor",
    "OrderShippingCountry",
    "OrderShipping",
    "OrderPaymentStatus",
    "OrderPaymentSummary",
    "OrderDetail",
    "Order",
    "OrderStatus",
    # Payment models
    "PaymentMutation",
    "Payment",
    "PaymentMethod",
    "PaymentGateway",
    # Customer models
    "CustomerAddress",
    "Customer",
    # Category models
    "CategorySorting",
    "Category",
    # Discount models
    "DiscountCode",
    # Newsletter models
    "NewsletterSubscriber",
    # Store & location models
    "OfflineLocation",
    "ShippingMethod",
    "Store",
    # Tax models
    "TaxPolicyRegion",
    # Utility models
    "CountResponse",
]
