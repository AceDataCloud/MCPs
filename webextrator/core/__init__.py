"""Core module for MCP WebExtrator server."""

from core.client import WebExtraterClient
from core.config import settings
from core.exceptions import WebExtraterAPIError, WebExtraterAuthError, WebExtraterValidationError
from core.server import mcp

__all__ = [
    "WebExtraterClient",
    "settings",
    "mcp",
    "WebExtraterAPIError",
    "WebExtraterAuthError",
    "WebExtraterValidationError",
]
