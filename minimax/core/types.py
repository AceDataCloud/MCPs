"""Type definitions for the MiniMax H3 MCP server."""

from typing import Literal

MinimaxModel = Literal["minimax-h3"]
MinimaxRatio = Literal["16:9", "9:16"]

DEFAULT_MODEL: MinimaxModel = "minimax-h3"
DEFAULT_RATIO: MinimaxRatio = "16:9"
DEFAULT_DURATION = 4
