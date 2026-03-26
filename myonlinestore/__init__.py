"""MyOnlineStore Connect API - Python Client SDK."""

from myonlinestore.client import ConnectClient
from myonlinestore.config import ConnectConfig
from myonlinestore.exceptions import (
    AuthenticationError,
    ConnectError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from myonlinestore.pagination import PaginatedResponse

__version__ = "1.0.0"
__all__ = [
    "ConnectClient",
    "ConnectConfig",
    "PaginatedResponse",
    "ConnectError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
]
