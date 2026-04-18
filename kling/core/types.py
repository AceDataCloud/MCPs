"""Type definitions for Kling MCP server."""

from typing import Literal

# Kling video models
KlingModel = Literal[
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
    "kling-v3",
    "kling-v3-omni",
    "kling-video-o1",
]

# Kling video actions
KlingAction = Literal["text2video", "image2video", "extend"]

# Kling motion character orientation
CharacterOrientation = Literal["image", "video"]

# Kling video modes
Mode = Literal["std", "pro"]

# Kling video aspect ratios
AspectRatio = Literal["16:9", "9:16", "1:1"]

# Kling video durations (V3/V3-Omni support 3-15s, others support 5 or 10)
Duration = int

# Kling camera control types
CameraControlType = Literal[
    "simple",
    "down_back",
    "forward_up",
    "left_turn_forward",
    "right_turn_forward",
]

# Default values
DEFAULT_MODEL: KlingModel = "kling-v2-master"
DEFAULT_MODE: Mode = "std"
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"
DEFAULT_DURATION: Duration = 5
