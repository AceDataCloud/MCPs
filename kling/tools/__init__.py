"""Tools module for MCP Kling server."""

# Import all tools to register them with the MCP server
from tools import info_tools, motion_tools, task_tools, video_tools

__all__ = [
    "video_tools",
    "motion_tools",
    "task_tools",
    "info_tools",
]
