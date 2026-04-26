"""Type definitions for Grok MCP server."""

from typing import Literal

# Chat completion model options
ChatModel = Literal[
    "grok-4",
    "grok-4-1-fast",
    "grok-4-1-fast-non-reasoning",
    "grok-3",
    "grok-3-mini",
    "grok-2-vision",
]

DEFAULT_CHAT_MODEL: ChatModel = "grok-3"
