"""Public Maestro API types."""

from typing import Annotated, Literal

from pydantic import Field

MaestroAction = Literal["generate", "remix", "edit", "extend"]
MaestroAspect = Literal["9:16", "16:9", "1:1"]
MaestroScenario = Literal["auto", "narrated", "captions", "avatar", "drama"]
MaestroStylePreset = Literal[
    "auto",
    "cinematic",
    "glass",
    "luxury",
    "swiss",
    "modern",
    "editorial",
    "warm",
    "vibrant",
    "neon",
    "mono",
    "pastel",
    "bold",
    "industrial",
    "futuristic",
    "retro",
]
MaestroStyle = MaestroStylePreset | str

MaestroVoicePreset = Literal[
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

MaestroVoice = MaestroVoicePreset | Annotated[str, Field(pattern=r"^[0-9a-fA-F]{32}$")]
