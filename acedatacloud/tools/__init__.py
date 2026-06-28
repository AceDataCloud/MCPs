"""Tools module for the AceDataCloud MCP server."""

# Import all tool modules so their @mcp.tool() decorators register with the server.
from tools import (  # noqa: F401
    admin_tools,
    catalog_tools,
    docs_tools,
    info_tools,
    model_tools,
    read_tools,
    write_tools,
)

__all__ = [
    "catalog_tools",
    "docs_tools",
    "model_tools",
    "read_tools",
    "write_tools",
    "admin_tools",
    "info_tools",
]
