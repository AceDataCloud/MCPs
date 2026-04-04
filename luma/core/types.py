"""Type definitions for Luma MCP server."""

from typing import Literal

# Luma video aspect ratios
AspectRatio = Literal[
    "16:9",
    "9:16",
    "1:1",
    "4:3",
    "3:4",
    "21:9",
    "9:21",
]

# Luma video actions
LumaAction = Literal["generate", "extend"]

# Default aspect ratio
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"
