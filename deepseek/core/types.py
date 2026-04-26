"""Type definitions for DeepSeek MCP server."""

from typing import Literal

# Chat completion model options
ChatModel = Literal[
    "deepseek-r1",
    "deepseek-r1-0528",
    "deepseek-v3",
    "deepseek-v3-250324",
    "deepseek-v3.2-exp",
]

DEFAULT_CHAT_MODEL: ChatModel = "deepseek-v3"
