"""Type definitions for Grok MCP server."""

from typing import Literal

# Grok Imagine video models
GrokVideoModel = Literal[
    "grok-imagine-video",
    "grok-imagine-video-1.5-preview",
]

# Aspect ratio options
AspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]

# Output resolution options
VideoResolution = Literal["480p", "720p"]

# Default model
DEFAULT_MODEL: GrokVideoModel = "grok-imagine-video"

# Default aspect ratio
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"

# Default resolution
DEFAULT_RESOLUTION: VideoResolution = "480p"

# Default video duration (seconds); valid range 1-15
DEFAULT_DURATION: int = 8
