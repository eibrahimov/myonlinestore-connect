# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-27

### Changed

- Improved package metadata with author/contact details, license file declarations, issues and changelog links, and dynamic installed-version resolution.
- Added stronger packaging validation in CI, including wheel and source distribution smoke tests before release.
- Added trusted publishing workflows for TestPyPI and PyPI with Sigstore attestations.
- Added repository security automation with Dependabot, `pip-audit`, `bandit`, and a published security policy.
- Clarified install-vs-import naming in the README and added project badges.

## [1.0.0] - 2026-03-27

### Added

#### Core Client & Async Support
- Full synchronous and asynchronous Python client for MyOnlineStore Connect API v1 and v2-beta
- Pythonic resource-based API design with intuitive resource namespacing
- Context manager support for automatic connection cleanup (sync and async)
- Configuration via `ConnectConfig` dataclass with sensible defaults

#### Resources
- 13 resource groups providing complete API coverage:
  - `articles` — Product articles
  - `orders` — Order management
  - `customers` — Customer management
  - `categories` — Product categories
  - `discount_codes` — Discount code administration
  - `newsletter` — Newsletter subscription management
  - `order_statuses` — Order status definitions
  - `payment_gateways` — Payment gateway configuration
  - `shipping_methods` — Shipping method definitions
  - `store` — Store configuration and metadata
  - `offline_locations` — Offline store locations
  - `tax_policy` — Tax policy configuration
  - `article_fields` — Custom article fields
  - `article_lists` — Product collection management
  - `article_list_options` — Article list filtering options

#### Data Models
- Pydantic v2 models with automatic camelCase alias support for API compatibility
- `PaginatedResponse` wrapper with automatic iteration helpers
- Type hints throughout for IDE autocomplete and static type checking
- Flexible model deserialization with strict validation

#### HTTP Transport & Reliability
- Automatic exponential backoff with full jitter retry mechanism
  - Configurable maximum retry count (default: 3)
  - Configurable retry delay cap (default: 60 seconds)
  - Formula: `random(0, min(cap, 0.5 * 2^attempt))`
- RFC 7231 `Retry-After` header support (numeric seconds and HTTP-date formats)
- Idempotency key auto-injection for POST/PATCH requests
  - UUID-based key generation
  - Configurable header name (default: `Idempotency-Key`)
  - Disableable via configuration
- Transient error retry eligibility:
  - HTTP status codes: 429 (Rate Limit), 5xx (Server Errors)
  - Connection timeouts and network errors
  - Honors idempotency requirements (POST/PATCH only retried with idempotency keys)

#### Timeout Configuration
- Granular timeout control via `ConnectConfig`:
  - Global request timeout (default: 30 seconds)
  - Separate connect timeout with fallback to global timeout
  - Separate read timeout with fallback to global timeout
  - Connection pool acquisition timeout (default: 30 seconds)

#### Connection Pooling
- HTTP connection pooling via httpx with configurable limits:
  - `max_connections` — Maximum concurrent connections (default: 100)
  - `max_keepalive` — Maximum keep-alive connections (default: 20)
- Automatic redirect following
- Keep-alive support for connection reuse

#### Authentication & Configuration
- Token-based authentication via query parameters
- Merchant store token (required)
- Optional partner application token
- Configurable API version selection (v1 stable, v2-beta)
- Custom language support (default: `nl_NL`)
- Response format configuration (default: `json`)
- Custom base URL support for testing and alternative endpoints

#### Logging & Debugging
- Structured logging via `logging.getLogger("myonlinestore")`
- Request-level debug logging with redacted sensitive parameters
- Retry attempt logging with delay information
- Rate limit logging with Retry-After values
- Automatic token and partner token redaction in debug output

#### Error Handling
- Typed exception hierarchy for granular error handling:
  - `ConnectError` — Base exception for all API errors
  - `AuthenticationError` — 401/403 authentication failures
  - `NotFoundError` — 404 resource not found
  - `ValidationError` — 422 validation errors with RFC 7807 problem details support
  - `RateLimitError` — 429 rate limit with `retry_after` attribute
  - `ServerError` — 5xx server-side errors
- Rich exception `__repr__` for better debugging
- Error body truncation (500 character limit) in exceptions for safe handling
- HTTP status codes and response bodies attached to exceptions for inspection

### Security

- Token and partner token redaction in debug and info logs to prevent accidental credential leakage
- Error body truncation to prevent exposure of large or sensitive response data
- Type safety via PEP 561 `py.typed` marker for mypy and other type checkers
- Structured validation via Pydantic v2 to prevent injection attacks

[1.0.1]: https://github.com/eibrahimov/myonlinestore-connect/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/eibrahimov/myonlinestore-connect/releases/tag/v1.0.0
