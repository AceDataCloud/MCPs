"""Type definitions for NanoBanana MCP server."""

from typing import Literal

# NanoBanana action types
NanoBananaAction = Literal["generate", "edit"]

# Task action types
TaskAction = Literal["retrieve", "retrieve_batch"]
