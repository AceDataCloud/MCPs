"""Typed requests for MiniMax H3 Max, prompt enhancement and regeneration."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.types import MediaUrl, MinimaxContent, MinimaxRatio


class NativeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    async_: bool = Field(default=True, alias="async")
    callback_url: str | None = None


class MaxVideoRequest(NativeRequest):
    model: Literal["MiniMax-H3-Max"] = "MiniMax-H3-Max"
    content: list[MinimaxContent] = Field(min_length=1)
    resolution: Literal["480P", "768P"] = "768P"
    ratio: MinimaxRatio = "16:9"
    duration: int = Field(default=5, ge=5, le=15)


class PromptEnhancementRequest(NativeRequest):
    model: Literal["MiniMax-H3"] = "MiniMax-H3"
    content: list[MinimaxContent] = Field(min_length=1)
    ratio: MinimaxRatio = "16:9"
    duration: int = Field(default=5, ge=4, le=15)


class SourceRegenerationRequest(NativeRequest):
    model: Literal["MiniMax-H3"] = "MiniMax-H3"
    resolution: Literal["2K"] = "2K"
    source_task_id: str = Field(
        min_length=1,
        description="An owned completed H3 768P platform task ID with original materials available.",
    )
    aigc_watermark: bool = False


class RegenerationContent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["text", "image_url", "video_url", "audio_url"]
    text: str | None = None
    image_url: MediaUrl | None = None
    video_url: MediaUrl | None = None
    audio_url: MediaUrl | None = None
    role: (
        Literal[
            "base_video",
            "first_frame",
            "last_frame",
            "reference_image",
            "reference_video",
            "reference_audio",
        ]
        | None
    ) = None

    @model_validator(mode="after")
    def check_material(self) -> "RegenerationContent":
        if self.type == "text":
            if not self.text or not self.text.strip():
                raise ValueError("text must be non-empty")
        elif getattr(self, self.type) is None:
            raise ValueError(self.type + " is required")
        if self.role == "base_video" and self.type != "video_url":
            raise ValueError("base_video must use video_url")
        return self


class BaseVideoRegenerationRequest(NativeRequest):
    model: Literal["MiniMax-H3"] = "MiniMax-H3"
    resolution: Literal["2K"] = "2K"
    content: list[RegenerationContent] = Field(
        min_length=2,
        description="The exact original generation prompt and materials, plus one base_video.",
    )
    aigc_watermark: bool = False

    @model_validator(mode="after")
    def check_base_video(self) -> "BaseVideoRegenerationRequest":
        if sum(item.role == "base_video" for item in self.content) != 1:
            raise ValueError("exactly one base_video is required")
        if not any(item.type == "text" for item in self.content):
            raise ValueError("the original prompt is required")
        return self


RegenerationRequest = SourceRegenerationRequest | BaseVideoRegenerationRequest
