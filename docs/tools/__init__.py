"""Tools module for the AceDataCloud Docs MCP server."""

# Import all tool modules so their @mcp.tool() functions register.
from tools import catalog_tools, doc_tools, example_tools, meta_tools, model_tools

__all__ = [
    "doc_tools",
    "catalog_tools",
    "model_tools",
    "example_tools",
    "meta_tools",
]
