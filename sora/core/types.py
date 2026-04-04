"""Type definitions for Sora MCP server."""

from typing import Literal

# Sora model versions
SoraModel = Literal[
    "sora-2",
    "sora-2-pro",
]

# === Version 1 types ===

# Video size options (version 1: clarity)
VideoSize = Literal["small", "large"]

# Video duration options in seconds (version 1)
VideoDuration = Literal[10, 15, 25]

# Video orientation options (version 1)
VideoOrientation = Literal["landscape", "portrait"]

# === Version 2 types ===

# Video duration in seconds (version 2)
VideoSeconds = Literal[4, 8, 12]

# Video resolution in pixels (version 2)
VideoResolution = Literal["720x1280", "1280x720", "1024x1792", "1792x1024"]

# === Default values ===

# Default model
DEFAULT_MODEL: SoraModel = "sora-2"

# Version 1 defaults
DEFAULT_SIZE: VideoSize = "large"
DEFAULT_DURATION: VideoDuration = 15
DEFAULT_ORIENTATION: VideoOrientation = "landscape"

# Version 2 defaults
DEFAULT_SECONDS: VideoSeconds = 4
DEFAULT_RESOLUTION: VideoResolution = "1280x720"
