"""Public owned asset IDs and management contracts."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.native_types import NativeRequest


class AssetManagementRequest(NativeRequest):
    action: Literal["list", "presets", "retrieve", "delete"] = "list"
    id: str | None = None
    page_num: int = Field(default=1, ge=1, le=1000)
    page_size: int = Field(default=30, ge=1, le=500)

    @model_validator(mode="after")
    def check_id(self) -> "AssetManagementRequest":
        if self.action in ("retrieve", "delete") and not self.id:
            raise ValueError("retrieve/delete requires a platform asset id")
        return self


class VoiceCreationRequest(NativeRequest):
    action: Literal["create"] = "create"
    voice_name: str = Field(min_length=1, max_length=20)
    voice_url: str = Field(
        pattern=r"^https?://",
        description="Clean single voice, 5–30 seconds; mp3/wav/mp4/mov. Creation costs 0.07 Credits.",
    )


class ElementReference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    element_id: str = Field(
        min_length=1, description="Owned or verified preset platform element ID."
    )


class VoiceReference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    voice_id: str = Field(min_length=1, description="Owned or verified preset platform voice ID.")


class AssetVideoRequest(NativeRequest):
    model: Literal["kling-v3", "kling-v3-omni", "kling-o1", "kling-v2-6"] = "kling-v3"
    action: Literal["text2video", "image2video"] = "text2video"
    prompt: str = Field(min_length=1)
    mode: Literal["std", "pro", "4k"] = "std"
    duration: int = Field(default=5, ge=3, le=15)
    aspect_ratio: Literal["16:9", "9:16", "1:1"] = "16:9"
    generate_audio: bool = False
    start_image_url: str | None = None
    end_image_url: str | None = None
    element_list: list[ElementReference] | None = Field(default=None, min_length=1, max_length=3)
    voice_list: list[VoiceReference] | None = Field(default=None, min_length=1, max_length=2)

    @model_validator(mode="after")
    def check_asset_configuration(self) -> "AssetVideoRequest":
        if bool(self.element_list) == bool(self.voice_list):
            raise ValueError("provide exactly one element_list or voice_list")
        if self.element_list and self.model not in ("kling-v3", "kling-v3-omni", "kling-o1"):
            raise ValueError("this model does not support element references")
        if self.voice_list:
            if self.model != "kling-v2-6" or self.mode != "pro" or not self.generate_audio:
                raise ValueError("specified voices require V2.6 pro and generate_audio=true")
            indices = [int(value) for value in re.findall(r"<<<voice_(\d+)>>>", self.prompt)]
            if not indices or any(value < 1 or value > len(self.voice_list) for value in indices):
                raise ValueError("prompt must reference only selected voices")
        if self.model == "kling-o1" and (
            self.duration != 5 or self.mode == "4k" or self.generate_audio
        ):
            raise ValueError("O1 requires 5 seconds, std/pro and no native audio")
        if self.model == "kling-v2-6" and self.duration not in (5, 10):
            raise ValueError("V2.6 duration must be 5 or 10 seconds")
        if self.action == "image2video" and not self.start_image_url:
            raise ValueError("image2video requires a start frame")
        return self
