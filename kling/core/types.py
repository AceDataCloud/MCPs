"""Type definitions for Kling MCP server."""

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

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
    "kling-o1",
]

# Kling video actions
KlingAction = Literal["text2video", "image2video", "extend"]

# Kling motion character orientation
CharacterOrientation = Literal["image", "video"]

# Kling video modes
Mode = Literal["std", "pro", "4k"]

# Kling motion modes
MotionMode = Literal["std", "pro"]

# Kling motion sound options
KeepOriginalSound = Literal["yes", "no"]

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


class KlingCameraControlConfig(BaseModel):
    """Numeric camera controls accepted by Kling's simple preset."""

    horizontal: float | None = Field(default=None, ge=-1, le=1)
    vertical: float | None = Field(default=None, ge=-1, le=1)
    pan: float | None = Field(default=None, ge=-1, le=1)
    tilt: float | None = Field(default=None, ge=-1, le=1)
    roll: float | None = Field(default=None, ge=-1, le=1)
    zoom: float | None = Field(default=None, ge=-1, le=1)


class KlingCameraControl(BaseModel):
    """Structured camera-control request."""

    type: CameraControlType
    config: KlingCameraControlConfig | None = None


class KlingReferenceImage(BaseModel):
    """Omni reference image, optionally used as a first or end frame."""

    image_url: HttpUrl
    type: Literal["first_frame", "end_frame"] | None = None


class KlingReferenceVideo(BaseModel):
    """Omni feature reference or editable base video."""

    video_url: HttpUrl
    refer_type: Literal["feature", "base"] = "feature"
    keep_original_sound: Literal["yes", "no"] = "no"


# Kling lip-sync mode
LipSyncMode = Literal["audio2video", "text2video"]

# Kling lip-sync audio type
LipSyncAudioType = Literal["url", "file"]

# Kling lip-sync voice language
VoiceLanguage = Literal["zh", "en"]

# Kling talking-photo models (subset of KlingModel that supports talking-photo)
TalkingPhotoModel = Literal[
    "kling-v1",
    "kling-v1-6",
    "kling-v2-master",
    "kling-v2-1-master",
    "kling-v2-5-turbo",
    "kling-v2-6",
]

# Kling talking-photo duration (seconds)
TalkingPhotoDuration = Literal[5, 10]

# Kling talking-photo mode
TalkingPhotoMode = Literal["std", "pro"]

# Default values
DEFAULT_MODEL: KlingModel = "kling-v1"
DEFAULT_MODE: Mode = "std"
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"
DEFAULT_DURATION: Duration = 5

# Talking-photo defaults
DEFAULT_TALKING_PHOTO_MODEL: TalkingPhotoModel = "kling-v2-1-master"
DEFAULT_TALKING_PHOTO_DURATION: TalkingPhotoDuration = 5
DEFAULT_TALKING_PHOTO_MODE: TalkingPhotoMode = "pro"
