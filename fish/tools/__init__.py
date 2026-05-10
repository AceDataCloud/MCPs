"""Tools module for MCP Fish server."""

# Import all tools to register them with the MCP server
from tools import audio_tools, info_tools, task_tools, voice_tools

__all__ = [
    "audio_tools",
    "voice_tools",
    "task_tools",
    "info_tools",
]
