"""Type definitions for NanoBanana MCP server."""

from typing import Literal

# NanoBanana action types
NanoBananaAction = Literal["generate", "edit"]

# Task action types
TaskAction = Literal["retrieve", "retrieve_batch"]

# NanoBanana image generation models
NanoBananaModel = Literal[
    "nano-banana",
    "nano-banana-2-lite",
    "nano-banana-2",
    "nano-banana-pro",
    "nano-banana:official",
    "nano-banana-2-lite:official",
    "nano-banana-2:official",
    "nano-banana-pro:official",
]

# Aspect ratio options
AspectRatio = Literal["1:1", "3:2", "2:3", "16:9", "9:16", "4:3", "3:4"]

# Resolution options
Resolution = Literal["1K", "2K", "4K"]
