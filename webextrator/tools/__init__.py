"""Tools module for MCP WebExtrator server."""

# Import all tools to register them with the MCP server
from tools import extract_tools, info_tools, task_tools  # noqa: F401

__all__ = [
    "extract_tools",
    "info_tools",
    "task_tools",
]
