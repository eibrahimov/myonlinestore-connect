"""MyOnlineStore Connect API - Python Client SDK."""

from importlib.metadata import PackageNotFoundError, version

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

try:
    __version__ = version("myonlinestore-connect")
except PackageNotFoundError:
    __version__ = "0+unknown"

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
