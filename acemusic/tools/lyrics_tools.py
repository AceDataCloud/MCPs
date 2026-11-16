"""ACE Music lyrics assistant."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_result


@mcp.tool()
async def acemusic_generate_lyrics(
    prompt: Annotated[str, Field(min_length=1, description="Theme and story for the lyrics.")],
    style: str = "",
) -> str:
    """Generate a title and lyrics. This is a separately priced request.

    Show or edit the lyrics before a separate custom music generation. Do not
    call this implicitly when the user has already supplied complete lyrics.
    """
    return format_result(
        await client.generate_lyrics(prompt=prompt, **({"style": style} if style else {}))
    )
