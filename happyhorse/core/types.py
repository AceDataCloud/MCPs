"""Type definitions for the Happy Horse MCP server."""

from typing import Literal

HappyHorseAction = Literal[
    "generate",
    "image_to_video",
    "reference_to_video",
    "video_edit",
]

TextToVideoModel = Literal["happyhorse-1.0-t2v", "happyhorse-1.1-t2v"]
ImageToVideoModel = Literal["happyhorse-1.0-i2v", "happyhorse-1.1-i2v"]
ReferenceToVideoModel = Literal["happyhorse-1.0-r2v", "happyhorse-1.1-r2v"]
VideoEditModel = Literal["happyhorse-1.0-video-edit"]
HappyHorseModel = TextToVideoModel | ImageToVideoModel | ReferenceToVideoModel | VideoEditModel

Resolution = Literal["720P", "1080P"]
AspectRatio = Literal["16:9", "9:16", "1:1", "4:3", "3:4"]
AudioSetting = Literal["auto", "origin"]

DEFAULT_TEXT_TO_VIDEO_MODEL: TextToVideoModel = "happyhorse-1.1-t2v"
DEFAULT_IMAGE_TO_VIDEO_MODEL: ImageToVideoModel = "happyhorse-1.1-i2v"
DEFAULT_REFERENCE_TO_VIDEO_MODEL: ReferenceToVideoModel = "happyhorse-1.1-r2v"
DEFAULT_VIDEO_EDIT_MODEL: VideoEditModel = "happyhorse-1.0-video-edit"
DEFAULT_RESOLUTION: Resolution = "1080P"
DEFAULT_RATIO: AspectRatio = "16:9"
DEFAULT_DURATION = 5
MIN_DURATION = 3
MAX_DURATION = 15
MAX_REFERENCE_IMAGES = 9
MAX_EDIT_REFERENCE_IMAGES = 5
MAX_SEED = 2_147_483_647
