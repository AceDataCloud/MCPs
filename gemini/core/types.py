"""Type definitions for Gemini MCP server."""

from typing import Literal

# Chat completion model options (OpenAI-compatible endpoint)
ChatModel = Literal[
    "gemini-3.1-pro",
    "gemini-3.0-pro",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

# Native Gemini API model options
NativeGeminiModel = Literal[
    "gemini-3.1-pro",
    "gemini-3.0-pro",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]

DEFAULT_CHAT_MODEL: ChatModel = "gemini-2.5-flash"
