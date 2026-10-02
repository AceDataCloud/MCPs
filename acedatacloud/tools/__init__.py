"""Tools module for the Platform MCP server."""

# Import all tool modules so their @mcp.tool() decorators register with the server.
from tools import (
    admin_tools,
    blog_tools,
    catalog_tools,
    docs_tools,
    info_tools,
    model_tools,
    read_tools,
    user,
    write_tools,
)

__all__ = [
    "read_tools",
    "write_tools",
    "admin_tools",
    "blog_tools",
    "info_tools",
    "catalog_tools",
    "docs_tools",
    "model_tools",
    "user",
]
