"""Tests for model validation, aliases, and __repr__."""

from __future__ import annotations

from myonlinestore.models import (
    Article,
    ArticleLimited,
    Customer,
    InvoiceAddress,
    Payment,
    PaymentMutation,
    Store,
    TaxPolicyRegion,
)


def test_customer_camel_case_aliases() -> None:
    data = {"firstName": "Jane", "lastName": "Doe", "email": "jane@test.com"}
    c = Customer.model_validate(data)
    assert c.first_name == "Jane"
    assert c.last_name == "Doe"


def test_payment_mutation_aliases() -> None:
    data = {"id": 42, "createdAt": "2024-01-01", "expiresAt": "2024-02-01", "price": "10.50", "type": "capture"}
    m = PaymentMutation.model_validate(data)
    assert m.created_at == "2024-01-01"
    assert m.expires_at == "2024-02-01"
    assert m.id == 42
    assert m.price == "10.50"


def test_invoice_address_taxnumber_alias() -> None:
    data = {"taxnumber": "NL123456", "country": "Netherlands"}
    inv = InvoiceAddress.model_validate(data)
    assert inv.vat_number == "NL123456"
    assert inv.country == "Netherlands"


def test_tax_policy_region_aliases() -> None:
    data = {"regionCode": "NL", "taxEnabled": True, "taxRate": "21.0"}
    r = TaxPolicyRegion.model_validate(data)
    assert r.region_code == "NL"
    assert r.tax_enabled is True
    assert r.tax_rate == "21.0"


def test_extra_fields_allowed() -> None:
    """Models should accept unknown fields without error (forward compatibility)."""
    data = {"id": 1, "name": "Test", "some_future_field": "value"}
    a = Article.model_validate(data)
    assert a.id == 1
    assert a.name == "Test"


def test_article_limited_fields() -> None:
    data = {"id": 5, "name": "Widget", "uuid": "abc-123", "is_main": True}
    a = ArticleLimited.model_validate(data)
    assert a.id == 5
    assert a.is_main is True


def test_repr_compact() -> None:
    """__repr__ should only show non-None fields."""
    a = ArticleLimited.model_validate({"id": 5, "name": "Widget"})
    r = repr(a)
    assert "ArticleLimited(" in r
    assert "id=5" in r
    assert "name='Widget'" in r
    # None fields should not appear
    assert "uuid" not in r
    assert "is_main" not in r


def test_repr_on_payment() -> None:
    p = Payment.model_validate({"id": "pay_1", "gateway": "ideal", "price": "25.00"})
    r = repr(p)
    assert "Payment(" in r
    assert "gateway='ideal'" in r


def test_store_extra_fields() -> None:
    data = {"id": "store-1", "name": "My Shop", "email": "shop@example.com", "prices_include_tax": True}
    s = Store.model_validate(data)
    assert s.id == "store-1"
    assert s.email == "shop@example.com"
    assert s.prices_include_tax is True
