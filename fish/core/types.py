"""Type definitions for Fish MCP server."""

from typing import Literal

# Fish TTS model
FishModel = Literal["fish-tts"]

# Fish audio action
FishAudioAction = Literal["speech"]

# Fish task actions
TaskAction = Literal["retrieve", "retrieve_batch"]

# Default model
DEFAULT_MODEL: FishModel = "fish-tts"

# Default voice ID (example voice from API spec)
DEFAULT_VOICE_ID = "d7900c21663f485ab63ebdb7e5905036"
