"""ACE Music generation tools."""

from typing import Annotated, Literal
from urllib.parse import urlsplit

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


@mcp.tool()
async def acemusic_upload_audio(
    audio_url: Annotated[
        str, Field(min_length=1, description="Public HTTPS URL of audio you own or may use.")
    ],
    name: str | None = None,
    audio_id: str | None = None,
    callback_url: str | None = None,
) -> str:
    """Import one reference track as a separate priced operation.

    This does not create a cover automatically. An optional caller-owned
    platform audio_id anchors the import to that track for later reference use.
    Save task_id and query the original task until its single track succeeds.
    """
    parsed = urlsplit(audio_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("A public HTTPS MP3 URL without credentials is required")
    result = await client.generate_audio(
        action="upload",
        audio_url=audio_url,
        **({"name": name} if name else {}),
        **({"audio_id": audio_id} if audio_id else {}),
        **({"callback_url": callback_url} if callback_url else {}),
    )
    return format_result(result, submission=True)


@mcp.tool()
async def acemusic_cover_audio(
    audio_id: Annotated[
        str,
        Field(
            min_length=1, description="Successful caller-owned platform audio ID, not a task ID."
        ),
    ],
    lyric: Annotated[str, Field(min_length=1, description="Lyrics for the new cover.")],
    style: Annotated[str, Field(min_length=1, description="Musical style for the new cover.")],
    title: str | None = None,
    audio_influence: Annotated[float, Field(ge=1, le=100)] = 60,
    model: Literal["acemusic-v1.1"] = "acemusic-v1.1",
    callback_url: str | None = None,
) -> str:
    """Submit one paid cover task targeting two songs from an owned reference.

    Use a public audio ID returned by a successful task. Reference compatibility
    is checked by the service; do not upload again or generate a replacement on
    rejection. Save the original task_id and query it instead of resubmitting.
    """
    if model != "acemusic-v1.1" or not 1 <= audio_influence <= 100:
        raise ValueError("Cover requires acemusic-v1.1 and audio_influence between 1 and 100")
    result = await client.generate_audio(
        action="cover",
        model=model,
        audio_id=audio_id,
        lyric=lyric,
        style=style,
        audio_influence=audio_influence,
        **({"title": title} if title else {}),
        **({"callback_url": callback_url} if callback_url else {}),
    )
    return format_result(result, submission=True)


@mcp.tool()
async def acemusic_mashup_audio(
    mashup_audio_ids: Annotated[
        list[str],
        Field(
            min_length=2,
            max_length=2,
            description="Exactly two distinct successful caller-owned platform audio IDs.",
        ),
    ],
    lyric: Annotated[str, Field(min_length=1, description="Lyrics for the new mashup.")],
    style: Annotated[str, Field(min_length=1, description="Musical style for the new mashup.")],
    title: str | None = None,
    audio_influence: Annotated[float, Field(ge=1, le=100)] = 60,
    model: Literal["acemusic-v1.1"] = "acemusic-v1.1",
    callback_url: str | None = None,
) -> str:
    """Submit one paid two-reference mashup task targeting two songs.

    Both public audio IDs must be caller-owned and compatible references.
    The service rejects incompatible sources; never substitute references or
    perform an extra paid upload automatically. Poll the returned task_id.
    """
    if (
        len(mashup_audio_ids) != 2
        or len(set(mashup_audio_ids)) != 2
        or any(not item.strip() for item in mashup_audio_ids)
    ):
        raise ValueError("Mashup requires exactly two distinct platform audio IDs")
    if model != "acemusic-v1.1" or not 1 <= audio_influence <= 100:
        raise ValueError("Mashup requires acemusic-v1.1 and audio_influence between 1 and 100")
    result = await client.generate_audio(
        action="mashup",
        model=model,
        mashup_audio_ids=mashup_audio_ids,
        lyric=lyric,
        style=style,
        audio_influence=audio_influence,
        **({"title": title} if title else {}),
        **({"callback_url": callback_url} if callback_url else {}),
    )
    return format_result(result, submission=True)
