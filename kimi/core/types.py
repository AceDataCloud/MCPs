"""Type definitions for Kimi MCP server."""

from typing import Literal

# Chat completion model options
ChatModel = Literal[
    "kimi-k2-thinking-turbo",
    "kimi-k2.5",
    "kimi-k2-thinking",
    "kimi-k2-instruct-0905",
    "kimi-k2-0905-preview",
    "kimi-k2-turbo-preview",
    "kimi-k2-0711-preview",
]

DEFAULT_CHAT_MODEL: ChatModel = "kimi-k2.5"
