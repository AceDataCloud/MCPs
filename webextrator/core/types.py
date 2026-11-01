"""Type definitions for WebExtrator MCP server."""

from typing import Literal

from pydantic import BaseModel

# Wait condition options
WaitUntil = Literal["load", "domcontentloaded", "networkidle", "commit"]

# Resource types to block
BlockResource = Literal["image", "font", "media", "stylesheet", "xhr", "fetch"]

# Expected content type hints
ExpectedType = Literal["product", "article", "general"]

# Task action options
TaskAction = Literal["retrieve", "retrieve_batch"]


class Cookie(BaseModel):
    """Cookie to inject before navigating the requested page."""

    name: str
    value: str
    domain: str
    path: str | None = None
    expires: float | None = None
    httpOnly: bool | None = None
    secure: bool | None = None
    sameSite: Literal["Strict", "Lax", "None"] | None = None
