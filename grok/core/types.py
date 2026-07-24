"""Type definitions for Grok MCP server."""

from typing import Literal

# Grok Imagine video models. The suffix selects the ttapi endpoint:
#   :reverse  -> UnOfficial (fast/standard, cheaper)
#   :official -> Official (higher fidelity, per-second pricing)
GrokVideoModel = Literal[
    "grok-imagine-video-1.5-fast:reverse",
    "grok-imagine-video:reverse",
    "grok-imagine-video:official",
    "grok-imagine-video-1.5:official",
]

# Aspect ratio options
AspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]

# Output resolution options
VideoResolution = Literal["480p", "720p", "1080p"]

# Default model (cheap fast/reverse tier)
DEFAULT_MODEL: GrokVideoModel = "grok-imagine-video-1.5-fast:reverse"

# Default aspect ratio
DEFAULT_ASPECT_RATIO: AspectRatio = "16:9"

# Default resolution
DEFAULT_RESOLUTION: VideoResolution = "480p"

# Default video duration (seconds). Valid range 6-30 for
# grok-imagine-video-1.5-fast:reverse; 1-15 for every other variant.
DEFAULT_DURATION: int = 6

# Grok chat completion models
GrokChatModel = Literal[
    "grok-4",
    "grok-4-1-fast",
    "grok-4-1-fast-non-reasoning",
    "grok-3",
    "grok-3-mini",
    "grok-2-vision",
]

# Reasoning effort options (reasoning-capable chat models)
ReasoningEffort = Literal["low", "high"]

# Default chat model (grok-4 / grok-3 are the broadly-available models)
DEFAULT_CHAT_MODEL: GrokChatModel = "grok-4"
