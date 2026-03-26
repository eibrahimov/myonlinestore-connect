"""Quick-start example for the MyOnlineStore Connect API client."""

import os

from myonlinestore import ConnectClient
from myonlinestore.pagination import iterate_all


def main():
    # Initialize the client with your tokens
    client = ConnectClient(
        store_token=os.environ["MOS_STORE_TOKEN"],
        partner_token=os.environ.get("MOS_PARTNER_TOKEN"),
        language="en_GB",
    )

    # ── Articles ───────────────────────────────────────────────
    # List first 20 articles
    page = client.articles.list(limit=20)
    print(f"Found {len(page.items)} articles (page 1)")

    for article in page.items:
        print(f"  [{article.sku}] {article.name} — €{article.price}")

    # Get total count
    total = client.articles.count()
    print(f"Total articles in store: {total}")

    # Iterate ALL articles automatically (handles pagination)
    for article in iterate_all(client.articles.list, page_size=100):
        pass  # process each article

    # Get a single article by ID
    article = client.articles.get(article_id=42)
    print(f"Article: {article.name}")

    # Create a new article
    new_article = client.articles.create(body={
        "name": "Wireless Headphones",
        "sku": "WH-100",
        "price": {"default": "49.99"},
        "stock": 150,
        "description": "Premium wireless headphones with noise cancellation.",
    })
    print(f"Created article #{new_article.id}")

    # Update an article
    updated = client.articles.update(article_id=new_article.id, body={
        "price": {"default": "44.99", "action": "39.99"},
    })

    # ── Orders ─────────────────────────────────────────────────
    # List recent orders
    orders = client.orders.list(limit=10)
    for order in orders.items:
        print(f"  Order #{order.number} — status {order.status} — €{order.price}")

    # Get a single order with all details
    order = client.orders.get(order_number=100001)
    print(f"Order #{order.number} from {order.debtor.email if order.debtor else 'unknown'}")

    # Filter orders by status and date range
    shipped = client.orders.list(
        status_id=3,
        created_start_date="2025-01-01 00:00:00",
        created_end_date="2025-12-31 23:59:59",
    )

    # List payments for an order
    payments = client.orders.list_payments(order_number=100001)
    for p in payments.items:
        print(f"  Payment {p.id}: {p.gateway} via {p.method}")

    # ── Customers ──────────────────────────────────────────────
    customers = client.customers.list(limit=10)
    for c in customers.items:
        print(f"  {c.first_name} {c.last_name} — {c.email}")

    # ── Store info ─────────────────────────────────────────────
    store = client.store.get()
    print(f"Store: {store.name} ({store.primary_domain})")

    # ── Discount codes ─────────────────────────────────────────
    codes = client.discount_codes.list()
    for code in codes.items:
        print(f"  {code.code}: {code.percentage_discount}% off")

    # Clean up
    client.close()


if __name__ == "__main__":
    main()
