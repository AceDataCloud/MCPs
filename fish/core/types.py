"""Type definitions for Fish MCP server."""

from typing import Literal

# Fish TTS models
FishModel = Literal["fish-tts"]

# Fish audio action types
FishAudioAction = Literal["speech"]

# Fish task action types
FishTaskAction = Literal["retrieve", "retrieve_batch"]

# Default model
DEFAULT_MODEL: FishModel = "fish-tts"

# Default voice ID (example from API docs)
DEFAULT_VOICE_ID: str = "d7900c21663f485ab63ebdb7e5905036"
