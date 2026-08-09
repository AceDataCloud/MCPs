"""Type definitions for the MiniMax H3 MCP server."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

MinimaxModel = Literal["MiniMax-H3"]
MinimaxRatio = Literal["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"]
MinimaxResolution = Literal["768P", "2K"]
MinimaxContentType = Literal["text", "image_url", "video_url", "audio_url"]
MinimaxContentRole = Literal[
    "first_frame", "last_frame", "reference_image", "reference_video", "reference_audio"
]

DEFAULT_MODEL: MinimaxModel = "MiniMax-H3"
DEFAULT_RATIO: MinimaxRatio = "16:9"
DEFAULT_RESOLUTION: MinimaxResolution = "2K"
DEFAULT_DURATION = 4


class MediaUrl(BaseModel):
    """A publicly accessible media URL."""

    model_config = ConfigDict(extra="forbid")

    url: str


class MinimaxContent(BaseModel):
    """A single MiniMax video generation content item."""

    model_config = ConfigDict(extra="forbid")

    type: MinimaxContentType
    text: str | None = Field(default=None, max_length=7000)
    image_url: MediaUrl | None = None
    video_url: MediaUrl | None = None
    audio_url: MediaUrl | None = None
    role: MinimaxContentRole | None = None
