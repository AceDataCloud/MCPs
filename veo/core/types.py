"""Type definitions for Veo MCP server."""

from typing import Literal

# Veo model versions
VeoModel = Literal[
    "veo2",
    "veo2-fast",
    "veo3",
    "veo3-fast",
    "veo31",
    "veo31-fast",
    "veo31-fast-ingredients",
]

# Aspect ratio options
AspectRatio = Literal["16:9", "9:16", "3:4", "4:3", "1:1"]

# Default model
DEFAULT_MODEL: VeoModel = "veo2"

# Video resolution options
VideoResolution = Literal["4k", "1080p", "gif"]

# Default aspect ratio
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"

# /veo/upsample actions
UpsampleAction = Literal["1080p", "4k", "gif"]

# /veo/extend supported models
ExtendModel = Literal["veo31-fast", "veo31"]

# /veo/objects actions
ObjectAction = Literal["insert", "remove"]

# /veo/reshoot motion types — short uppercase aliases mapped to upstream
# RESHOOT_MOTION_TYPE_* values by the platform-service worker.
MotionType = Literal[
    "STATIONARY",
    "STATIONARY_UP",
    "STATIONARY_DOWN",
    "STATIONARY_LEFT",
    "STATIONARY_RIGHT",
    "STATIONARY_DOLLY_IN_ZOOM_OUT",
    "STATIONARY_DOLLY_OUT_ZOOM_IN",
    "UP",
    "DOWN",
    "LEFT_TO_RIGHT",
    "RIGHT_TO_LEFT",
    "FORWARD",
    "BACKWARD",
    "DOLLY_IN_ZOOM_OUT",
    "DOLLY_OUT_ZOOM_IN",
]
