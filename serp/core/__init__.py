"""Core module for MCP Serp server."""

from core.client import SerpClient
from core.config import settings
from core.exceptions import SerpAPIError, SerpAuthError, SerpValidationError
from core.server import mcp

__all__ = [
    "SerpClient",
    "settings",
    "mcp",
    "SerpAPIError",
    "SerpAuthError",
    "SerpValidationError",
]
