"""Type definitions for Fish MCP server."""

from typing import Literal

# Fish TTS model
FishModel = Literal["s1", "s2-pro", "s2.1-pro"]

# Fish reference voice id, accepted as a single model id or a list of model ids
FishReferenceId = str | list[str]

# Fish output format
FishAudioFormat = Literal["mp3", "wav", "pcm"]

# Fish MP3 bitrate
FishMp3Bitrate = Literal[64, 128, 192]

# Fish latency mode
FishLatency = Literal["normal", "balanced"]

# Fish task actions
TaskAction = Literal["retrieve", "retrieve_batch"]

# Default model
DEFAULT_MODEL: FishModel = "s2-pro"

# Default voice ID (example voice from API spec)
DEFAULT_VOICE_ID = "d7900c21663f485ab63ebdb7e5905036"
