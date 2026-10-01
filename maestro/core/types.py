"""Public Maestro API types."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

MaestroAction = Literal["generate", "remix", "edit", "extend"]
MaestroAspect = Literal["9:16", "16:9", "1:1"]
MaestroScenario = Literal["auto", "narrated", "captions", "avatar", "drama"]
MaestroStyle = str
MaestroAudioMode = Literal["auto", "narration", "music", "silent"]
MaestroAssetRole = Literal[
    "reference",
    "logo",
    "product_image",
    "ui_screenshot",
    "product_video",
    "style_reference",
    "music",
]
HexColor = Annotated[str, Field(pattern=r"^#[0-9a-fA-F]{6}$")]


class MaestroAsset(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
    role: MaestroAssetRole
    url: str = Field(min_length=1, max_length=2048)
    name: str | None = Field(default=None, min_length=1, max_length=240)


class MaestroBrandColors(BaseModel):
    model_config = ConfigDict(extra="forbid")
    background: HexColor | None = None
    foreground: HexColor | None = None
    accent: HexColor | None = None


class MaestroCta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str | None = Field(default=None, min_length=1, max_length=100)
    url: str | None = Field(default=None, min_length=1, max_length=2048)


class MaestroBrand(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=100)
    colors: MaestroBrandColors | None = None
    font_set: Literal["inter-noto-sc"] | None = None
    cta: MaestroCta | None = None


MaestroVoice = Literal[
    "auto",
    "warm-female",
    "bright-female",
    "anchor-female",
    "clean-female",
    "calm-male",
    "deep-male",
    "documentary-male",
    "energetic-male",
    "storyteller-male",
]
