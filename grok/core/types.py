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
    "grok-imagine-video",
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
    "grok-4.5",
    "grok-4",
    "grok-3",
]

# Reasoning effort options (reasoning-capable chat models)
ReasoningEffort = Literal["minimal", "low", "medium", "high"]

# grok-4.5 is the newest model but its provider pool is currently unhealthy
# (500 "No valid account found"), so the default stays on grok-4.
DEFAULT_CHAT_MODEL: GrokChatModel = "grok-4"
