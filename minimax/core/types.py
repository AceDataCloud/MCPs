"""Type definitions for the MiniMax H3 MCP server."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

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

    @model_validator(mode="after")
    def validate_content_schema(self) -> "MinimaxContent":
        if self.type == "text":
            if self.text is None:
                raise ValueError("text is required when type is 'text'")
            return self

        if self.type == "image_url":
            if self.image_url is None:
                raise ValueError("image_url is required when type is 'image_url'")
            if self.role not in {None, "first_frame", "last_frame", "reference_image"}:
                raise ValueError(
                    "role for image_url must be one of first_frame, last_frame, reference_image"
                )
            return self

        if self.type == "video_url":
            if self.video_url is None:
                raise ValueError("video_url is required when type is 'video_url'")
            if self.role != "reference_video":
                raise ValueError("role is required and must be 'reference_video' for video_url")
            return self

        if self.type == "audio_url":
            if self.audio_url is None:
                raise ValueError("audio_url is required when type is 'audio_url'")
            if self.role != "reference_audio":
                raise ValueError("role is required and must be 'reference_audio' for audio_url")
            return self

        return self
