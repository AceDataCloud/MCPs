"""Type definitions for the Digital Human MCP server."""

from typing import Literal

DigitalHumanEngine = Literal["latentsync", "heygem"]
DigitalHumanResolution = Literal["720p", "540p"]
DigitalHumanVoiceLanguage = Literal["zh", "en"]
DigitalHumanTaskAction = Literal["retrieve", "retrieve_batch", "delete"]

DEFAULT_ENGINE: DigitalHumanEngine = "latentsync"
DEFAULT_GUIDANCE = 2.0
DEFAULT_STEPS = 40
DEFAULT_SEAM_FIX = True
DEFAULT_SPEED = 1.0
DEFAULT_RESOLUTION: DigitalHumanResolution = "720p"
DEFAULT_VOICE_LANGUAGE: DigitalHumanVoiceLanguage = "zh"
