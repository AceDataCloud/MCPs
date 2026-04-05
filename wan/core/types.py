"""Type definitions for Wan MCP server."""

from typing import Literal

# Wan video models
WanModel = Literal[
    "wan2.6-t2v",
    "wan2.6-i2v",
    "wan2.6-r2v",
    "wan2.6-i2v-flash",
]

# Text-to-video models
T2VModel = Literal["wan2.6-t2v"]

# Image-to-video models
I2VModel = Literal[
    "wan2.6-i2v",
    "wan2.6-r2v",
    "wan2.6-i2v-flash",
]

# Wan video actions
WanAction = Literal["text2video", "image2video"]

# Video resolution
Resolution = Literal["480P", "720P", "1080P"]

# Video duration in seconds
Duration = Literal[5, 10, 15]

# Shot type
ShotType = Literal["single", "multi"]

# Defaults
DEFAULT_MODEL: WanModel = "wan2.6-t2v"
DEFAULT_RESOLUTION: Resolution = "720P"
