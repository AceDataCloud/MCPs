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
    """Analyze and shorten a Midjourney prompt.

    Midjourney's prompt analyzer reads your prompt, highlights the highest-weighted
    tokens, and produces up to 5 shortened candidate prompts that preserve the
    dominant ideas.

    Use this when:
    - You have a long prompt and want to find the most important parts
    - You want to understand which words Midjourney considers most significant
    - You want optimized, concise versions of your prompt
    - You want to identify filler words that don't affect generation

    Returns:
        Up to 5 shortened candidate prompts derived from the input.
    """
    result = await client.shorten(
        prompt=prompt,
    )
    return format_shorten_result(result)
