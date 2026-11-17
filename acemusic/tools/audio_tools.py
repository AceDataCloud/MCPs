"""ACE Music generation tools."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, AceMusicModel
from core.utils import format_result


@mcp.tool()
async def acemusic_generate_music(
    prompt: Annotated[
        str, Field(min_length=1, description="Describe the song theme and musical style.")
    ],
    model: AceMusicModel = DEFAULT_MODEL,
    callback_url: str | None = None,
) -> str:
    """Submit one ACE Music task from an idea, targeting two song candidates.

    This is a paid generation. Save the returned task ID and use acemusic_get_task
    until the group reaches a terminal state. Never resubmit to check progress.
    A callback is optional; use a real webhook you control.
    """
    result = await client.generate_audio(
        action="generate",
        model=model,
        custom=False,
        prompt=prompt,
        **({"callback_url": callback_url} if callback_url else {}),
    )
    return format_result(result, submission=True)


@mcp.tool()
async def acemusic_generate_custom_music(
    lyric: Annotated[
        str,
        Field(
            min_length=1, description="Custom lyrics, optionally with [Verse]/[Chorus] sections."
        ),
    ],
    style: Annotated[
        str,
        Field(min_length=1, description="Musical style, instruments, mood and vocal description."),
    ],
    title: Annotated[str, Field(min_length=1, description="Title for the custom song.")],
    model: AceMusicModel = DEFAULT_MODEL,
    callback_url: str | None = None,
) -> str:
    """Submit one paid ACE Music task using the user's lyrics and style.

    Lyrics are sent as the singular platform field lyric. This creates a new
    song group; it does not upload, cover, extend or separate existing audio.
    """
    result = await client.generate_audio(
        action="generate",
        model=model,
        custom=True,
        lyric=lyric,
        style=style,
        title=title,
        **({"callback_url": callback_url} if callback_url else {}),
    )
    return format_result(result, submission=True)
