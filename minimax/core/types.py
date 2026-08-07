"""Type definitions for the MiniMax H3 MCP server."""

from typing import Literal

MinimaxModel = Literal["minimax-h3"]
MinimaxRatio = Literal["16:9", "9:16"]
MinimaxResolution = Literal["768P", "2K"]

DEFAULT_MODEL: MinimaxModel = "minimax-h3"
DEFAULT_RATIO: MinimaxRatio = "16:9"
DEFAULT_RESOLUTION: MinimaxResolution = "2K"
DEFAULT_DURATION = 4
