"""Public Maestro API types."""

from typing import Literal

MaestroAction = Literal["generate", "remix", "edit", "extend"]
MaestroAspect = Literal["9:16", "16:9", "1:1"]
MaestroQuality = Literal["draft", "standard", "premium"]
MaestroScenario = Literal["auto", "narrated", "drama", "avatar", "motion", "slideshow"]
MaestroStyle = Literal[
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
