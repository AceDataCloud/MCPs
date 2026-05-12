"""Prompt shortening tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_translate_result


@mcp.tool()
async def midjourney_shorten(
    prompt: Annotated[
        str,
        Field(
            description="Long Midjourney prompt to shorten. Returns up to 5 shortened prompt candidates preserving key weighted terms."
        ),
    ],
) -> str:
    """Shorten a Midjourney prompt into concise alternatives."""
    result = await client.shorten(prompt=prompt)
    return format_translate_result(result)
