"""Type definitions for Producer MCP server."""

from typing import Literal

# Producer/FUZZ model versions
ProducerModel = Literal[
    "FUZZ-2.0 Pro",
    "FUZZ-2.0",
    "FUZZ-2.0 Raw",
    "FUZZ-1.1 Pro",
    "FUZZ-1.0 Pro",
    "FUZZ-1.0",
    "FUZZ-1.1",
    "FUZZ-0.8",
]

# Audio generation actions
AudioAction = Literal[
    "generate",
    "extend",
    "cover",
    "variation",
    "swap_vocals",
    "swap_instrumentals",
    "replace_section",
    "stems",
]

# Default model
DEFAULT_MODEL: ProducerModel = "FUZZ-2.0"
