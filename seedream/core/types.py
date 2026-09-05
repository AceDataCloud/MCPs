"""Type definitions for Seedream MCP server."""

from typing import Literal

# Seedream model types
SeedreamModel = Literal[
    "doubao-seedream-5-0-pro-260628",
    "doubao-seedream-5-0-260128",
    "doubao-seedream-5-0-lite-260128",
    "doubao-seedream-4-0-250828",
    "doubao-seedream-4-5-251128",
]

# Image size
SeedreamSize = str

# Output image format
OutputFormat = Literal["jpeg", "png"]

# Sequential image generation mode
SequentialMode = Literal["auto", "disabled"]

# Response format
ResponseFormat = Literal["url", "b64_json"]

# Background opacity
Background = Literal["transparent", "opaque"]

# Task action types
TaskAction = Literal["retrieve", "retrieve_batch"]

# Tool types for model tool use
WebSearchToolType = Literal["web_search"]
