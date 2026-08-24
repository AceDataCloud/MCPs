"""Type definitions for Wan MCP server."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field

# Wan video models
WanModel = Literal[
    "wan2.6-t2v",
    "wan2.6-i2v",
    "wan2.6-r2v",
    "wan2.6-i2v-flash",
    "wan3.0-video",
]

# Text-to-video models
T2VModel = Literal["wan2.6-t2v", "wan3.0-video"]

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
Duration = Literal[-1] | Annotated[int, Field(ge=2, le=30)]

# Shot type
ShotType = Literal["single", "multi"]

# Media input type
MediaType = Literal[
    "first_frame",
    "last_frame",
    "reference_image",
    "reference_video",
    "reference_audio",
    "file",
    "link",
]


class MediaItem(BaseModel):
    """A media input for video generation."""

    type: MediaType
    url: str


# Video aspect ratio
Ratio = Literal["adaptive", "16:9", "4:3", "1:1", "3:4", "9:16"]

# Defaults
DEFAULT_MODEL: WanModel = "wan2.6-t2v"
DEFAULT_RESOLUTION: Resolution = "720P"
