"""Type definitions for Hailuo MCP server."""

from typing import Literal

# Hailuo video models
HailuoModel = Literal[
    "minimax-t2v",
    "minimax-i2v",
    "minimax-i2v-director",
]

# Default model
DEFAULT_MODEL: HailuoModel = "minimax-t2v"
