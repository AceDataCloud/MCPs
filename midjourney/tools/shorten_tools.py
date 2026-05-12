"""Prompt shortening tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_shorten_result


@mcp.tool()
async def midjourney_shorten(
    prompt: Annotated[
        str,
        Field(
            description="The prompt to analyze and shorten. Midjourney's prompt analyzer reads the prompt, highlights the highest-weighted tokens and produces up to 5 shortened candidate prompts that preserve the dominant ideas."
        ),
    ],
) -> str:
    """Analyze and shorten a Midjourney prompt into concise candidates.

    Midjourney's built-in prompt analyzer reads your prompt, identifies the
    highest-weighted tokens, and returns up to 5 shortened versions that
    preserve the dominant ideas while removing less-important words.

    Use this when:
    - You have a long or verbose prompt and want more focused alternatives
    - You want to understand which parts of your prompt Midjourney weighs most
    - You want to experiment with leaner prompt variations

    Returns:
        Up to 5 shortened candidate prompts as a JSON array.
    """
    result = await client.shorten(prompt=prompt)
    return format_shorten_result(result)
