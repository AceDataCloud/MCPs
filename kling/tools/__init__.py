"""Tools module for MCP Kling server."""

# Import all tools to register them with the MCP server
from tools import (
    asset_tools,
    info_tools,
    lip_sync_tools,
    motion_tools,
    native_tools,
    task_tools,
    video_tools,
)

__all__ = [
    "asset_tools",
    "video_tools",
    "native_tools",
    "motion_tools",
    "lip_sync_tools",
    "task_tools",
    "info_tools",
]
