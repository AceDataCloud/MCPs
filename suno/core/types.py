"""Type definitions for Suno MCP server."""

from typing import Literal

# Suno model versions
SunoModel = Literal[
    "chirp-v6",
    "chirp-v6-wild",
    "chirp-v6-mini",
    "chirp-v3-0",
    "chirp-v3-5",
    "chirp-v4",
    "chirp-v4-5",
    "chirp-v4-5-plus",
    "chirp-v5",
    "chirp-v5-5",
]

# Lyrics model versions (different from audio models)
LyricsModel = Literal["default", "remi-v1"]

# Vocal gender preference (v4.5+ only)
VocalGender = str

# Variation category preference (v5+ only)
VariationCategory = str

# Replace-section response shape
ReplaceSectionResultMode = Literal["candidates", "full_song"]

# Default model
DEFAULT_MODEL: SunoModel = "chirp-v5-5"

# Default lyrics model
DEFAULT_LYRICS_MODEL: LyricsModel = "default"
