"""Type definitions for WebExtrator MCP server."""

from typing import Literal

# Wait condition options
WaitUntil = Literal["load", "domcontentloaded", "networkidle", "commit"]

# Resource types to block
BlockResource = Literal["image", "font", "media", "stylesheet", "xhr", "fetch"]

# Expected content type hints
ExpectedType = Literal["product", "article", "general"]

# Task action options
TaskAction = Literal["retrieve", "retrieve_batch"]
