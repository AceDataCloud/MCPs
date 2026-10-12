"""Requests for Kling Turbo, storyboards and commerce solutions."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class NativeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    async_: bool = Field(default=True, alias="async")
    callback_url: str | None = None


class TurboRequest(NativeRequest):
    model: Literal["kling-v3-turbo"] = "kling-v3-turbo"
    action: Literal["text2video", "image2video"] = "text2video"
    prompt: str = Field(min_length=1, max_length=2500)
    mode: Literal["std", "pro"] = "std"
    duration: int = Field(default=5, ge=3, le=15)
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    start_image_url: str | None = None
    generate_audio: Literal[True] = True

    @model_validator(mode="after")
    def check_first_frame(self) -> "TurboRequest":
        if self.action == "image2video" and not self.start_image_url:
            raise ValueError("image2video requires start_image_url")
        return self


class Shot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    index: int = Field(ge=1, le=6)
    prompt: str = Field(min_length=1, max_length=512)
    duration: int = Field(ge=1)


class StoryboardRequest(NativeRequest):
    model: Literal["kling-v3", "kling-v3-omni"] = "kling-v3"
    action: Literal["text2video", "image2video"] = "text2video"
    prompt: str | None = None
    mode: Literal["std", "pro", "4k"] = "std"
    duration: int = Field(default=5, ge=3, le=15)
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    generate_audio: bool = False
    start_image_url: str | None = None
    end_image_url: str | None = None
    multi_shot: Literal[True] = True
    shot_type: Literal["intelligence", "customize"] = "intelligence"
    multi_prompt: list[Shot] | None = Field(default=None, min_length=1, max_length=6)

    @model_validator(mode="after")
    def check_shots(self) -> "StoryboardRequest":
        if self.shot_type == "customize":
            if (
                not self.multi_prompt
                or sum(shot.duration for shot in self.multi_prompt) != self.duration
            ):
                raise ValueError("custom shot durations must sum to duration")
            if [shot.index for shot in self.multi_prompt] != list(
                range(1, len(self.multi_prompt) + 1)
            ):
                raise ValueError("shot indices must be consecutive from 1")
        elif not self.prompt or self.multi_prompt:
            raise ValueError("intelligence needs prompt and omits multi_prompt")
        if self.action == "image2video" and not self.start_image_url:
            raise ValueError("image2video requires start_image_url")
        if self.end_image_url and not self.start_image_url:
            raise ValueError("an end frame requires a start frame")
        return self


class Content(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal[
        "product_info",
        "source_video",
        "product_image",
        "model_image",
        "bgm",
        "voice",
        "ref_image",
        "goods_title",
        "goods_description",
        "avatar_image",
        "avatar_id",
        "goods_price",
        "goods_target_audience",
        "goods_selling_point",
        "speech_script",
        "person_image",
    ]
    text: str | None = None
    url: str | None = None
    voice_id: str | None = None


class ApparelSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resolution: Literal["720p", "1080p"] = "720p"
    aspect_ratio: Literal["9:16", "2:3", "3:4", "1:1", "4:3", "3:2", "16:9", "21:9"] | None = None


class GoodsSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resolution: Literal["720p", "1080p"] = "720p"
    aspect_ratio: Literal["9:16", "1:1", "16:9"]
    duration: Literal[15, 30, 60]


class CommerceSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resolution: Literal["720p", "1080p"] = "720p"
    aspect_ratio: Literal["9:16", "16:9"] = "9:16"
    allow_polish: bool | None = None
    bgm_enabled: bool | None = None
    voice_id: str | None = None
    speech_rate: float | None = Field(
        default=None,
        description="Supported speech rates: 0.8, 1.0, 1.2; unavailable for product voiceover.",
    )
    action_prompt: str | None = None


class TryOnSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    keep_face: bool = True
    keep_pose: bool = True
    keep_background: bool = True


class SolutionRequest(NativeRequest):
    contents: list[Content] = Field(min_length=1)
    watermark: bool | None = None


class ApparelRequest(SolutionRequest):
    settings: ApparelSettings = Field(default_factory=ApparelSettings)


class GoodsRequest(SolutionRequest):
    settings: GoodsSettings


class CommerceRequest(SolutionRequest):
    settings: CommerceSettings = Field(default_factory=CommerceSettings)


class TryOnRequest(SolutionRequest):
    settings: TryOnSettings = Field(default_factory=TryOnSettings)
