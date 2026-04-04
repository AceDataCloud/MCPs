"""Tools module for MCP ShortURL server."""

# Import all tools to register them with the MCP server
from tools import info_tools, shorturl_tools

__all__ = [
    "shorturl_tools",
    "info_tools",
]
