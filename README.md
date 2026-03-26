# MyOnlineStore Connect API — Python Client

[![PyPI version](https://img.shields.io/pypi/v/myonlinestore-connect.svg)](https://pypi.org/project/myonlinestore-connect/)
[![Python versions](https://img.shields.io/pypi/pyversions/myonlinestore-connect.svg)](https://pypi.org/project/myonlinestore-connect/)
[![CI](https://github.com/eibrahimov/myonlinestore-connect/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/eibrahimov/myonlinestore-connect/actions/workflows/python-package.yml)
[![License](https://img.shields.io/pypi/l/myonlinestore-connect.svg)](https://github.com/eibrahimov/myonlinestore-connect/blob/main/LICENSE)

A typed Python SDK for the [MyOnlineStore Connect API](https://connect.myonlinestore.com/), providing sync and async access to all API endpoints with Pydantic-validated models.

> **PyPI package name:** `myonlinestore-connect`
> **Python import name:** `myonlinestore`

## Installation

```bash
pip install myonlinestore-connect
```

Then import it in Python with:

```python
import myonlinestore
```

Or install from source:

```bash
pip install -e .
```

## Quick start

```python
from myonlinestore import ConnectClient

client = ConnectClient(
    store_token="your-store-token",
    partner_token="your-partner-token",  # optional
)

# List articles
page = client.articles.list(limit=20)
for article in page.items:
    print(f"{article.name} — {article.price}")

# Get a single order
order = client.orders.get(order_number=12345)
print(order.debtor.email)

client.close()
```

## Async usage

Every method has an async counterpart prefixed with `a`:

```python
import asyncio
from myonlinestore import ConnectClient

async def main():
    async with ConnectClient(store_token="your-token") as client:
        page = await client.articles.alist(limit=50)
        order = await client.orders.aget(order_number=12345)

asyncio.run(main())
```

## Pagination

List endpoints return a `PaginatedResponse` with built-in page tracking:

```python
page = client.articles.list(limit=100, offset=0)
print(page.has_next)     # True if more pages exist
print(page.next_offset)  # offset for the next page
```

To iterate all items automatically:

```python
from myonlinestore.pagination import iterate_all

for article in iterate_all(client.articles.list, page_size=100):
    process(article)
```

Async iteration:

```python
from myonlinestore.pagination import aiterate_all

async for article in aiterate_all(client.articles.alist, page_size=100):
    await process(article)
```

## Available resources

| Resource | Accessor | Key methods |
|---|---|---|
| Articles | `client.articles` | list, get, create, update, delete, count, upload_image, delete_image |
| Orders | `client.orders` | list, get, create, update, count, create_credit, list_payments, create_payment, create_payment_raw, update_payment, delete_payment |
| Customers | `client.customers` | list, get, create, update, delete, list_addresses, get_address, create_address, update_address, delete_address |
| Categories | `client.categories` | list, get, create, update, count, list_articles |
| Discount codes | `client.discount_codes` | list, get, create, update, delete |
| Newsletter | `client.newsletter` | list, get, create, update, delete, count |
| Order statuses | `client.order_statuses` | list |
| Payment gateways | `client.payment_gateways` | list, list_for_store |
| Shipping methods | `client.shipping_methods` | list |
| Store info | `client.store` | get |
| Offline locations | `client.offline_locations` | list, get |
| Tax policy | `client.tax_policy` | list, get |
| Article fields | `client.article_fields` | create, delete |
| Article lists | `client.article_lists` | get, add, remove |
| Article list options | `client.article_list_options` | create, delete |

> **Note:** `list_articles` on categories returns `ArticleLimited` objects (id, name, uuid, is_main only).
> `create_payment_raw` returns the full API response dict including the payment redirect URL.

## Configuration

```python
from myonlinestore import ConnectClient, ConnectConfig

config = ConnectConfig(
    store_token="xxx",
    partner_token="yyy",
    api_version="1",            # "1" (stable) or "2-beta"
    language="en_GB",            # response language
    timeout=60.0,                # default timeout (seconds)
    connect_timeout=5.0,         # TCP connect timeout
    read_timeout=30.0,           # response read timeout
    pool_timeout=30.0,           # pool acquire timeout
    max_connections=100,         # connection pool size
    max_keepalive=20,            # keep-alive connections
    default_limit=50,            # default page size
    max_retries=3,               # retry attempts (0 to disable)
    max_retry_delay=60.0,        # cap on retry backoff (seconds)
    idempotency_key_header="Idempotency-Key",  # None to disable
)

client = ConnectClient(config=config)
```

## Retry and resilience

The SDK automatically retries on transient errors (429, 500, 502, 503, 504, and connection/timeout errors) using exponential backoff with full jitter:

```
delay = random(0, min(max_retry_delay, 0.5 * 2^attempt))
```

Key behaviors:

- **Retry-After headers** are respected on 429 responses (both numeric seconds and HTTP-date formats).
- **POST and PATCH** are only retried when idempotency keys are enabled, preventing duplicate mutations.
- **Idempotency keys** are auto-injected as UUIDs on POST/PATCH requests via the `Idempotency-Key` header.
- Set `max_retries=0` to disable retries entirely.

## Error handling

All API errors raise typed exceptions:

```python
from myonlinestore import (
    ConnectError,         # base class
    AuthenticationError,  # 401/403
    NotFoundError,        # 404
    ValidationError,      # 422
    RateLimitError,       # 429 (includes retry_after attribute)
    ServerError,          # 5xx
)

try:
    article = client.articles.get(article_id=99999)
except NotFoundError:
    print("Article not found")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except AuthenticationError:
    print("Check your API token")
```

All exceptions carry `status_code`, `body`, and a compact `__repr__` for logging.

## Logging

The SDK logs via Python's standard `logging` module under the `"myonlinestore"` logger:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("myonlinestore").setLevel(logging.DEBUG)
```

Log levels used:

- **DEBUG** — request method, URL, and (redacted) params
- **INFO** — retries, rate-limit pauses, Retry-After delays

Auth tokens are automatically redacted in all log output.

## API version support

The SDK defaults to API v1. To use the v2-beta:

```python
client = ConnectClient(store_token="xxx", api_version="2-beta")
```

## Type safety

The SDK is fully typed with PEP 561 support (`py.typed` marker included). All models use Pydantic v2 with:

- `snake_case` Python fields with `camelCase` aliases for API compatibility
- `extra="ignore"` to silently drop unknown fields (forward-compatible)
- Compact `__repr__` on all models showing only non-None fields

Works out of the box with mypy, pyright, and IDE autocomplete.

## Requirements

- Python 3.10+
- httpx >=0.24.0, <1.0
- pydantic >=2.0.0, <3.0
