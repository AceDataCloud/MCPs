"""Voice creation tools for Fish API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_voice_result


@mcp.tool()
async def fish_create_voice(
    voice_url: Annotated[
        str,
        Field(
            description="URL of the audio file to clone a voice from. Must be a publicly accessible URL to an audio file (e.g., MP3, WAV). The audio should be clear speech for best cloning quality."
        ),
    ],
    title: Annotated[
        str | None,
        Field(
            description="Title or name for the voice. Use a descriptive name to identify this voice later."
        ),
    ] = None,
    description: Annotated[
        str | None,
        Field(
            description="Description of the voice. Provide details about the voice characteristics, use cases, or speaker information."
        ),
    ] = None,
    image_url: Annotated[
        str | None,
        Field(
            description="URL for a cover image to associate with this voice. Should be a publicly accessible image URL."
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the voice is created."
        ),
    ] = None,
) -> str:
    """Create a custom voice by cloning from an audio URL.

    Registers a new voice persona by extracting voice characteristics from
    an audio file. The resulting voice_id can then be used with fish_generate_audio.

    Use this when:
    - You want to clone a voice from an existing audio file
    - You want to register a custom voice persona
    - You need a specific speaker's voice for TTS generation

    Returns:
        Task ID and voice creation information including the new voice_id.
    """
    payload: dict = {
        "voice_url": voice_url,
    }

    if title:
        payload["title"] = title
    if description:
        payload["description"] = description
    if image_url:
        payload["image_url"] = image_url
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.create_voice(**payload)
    return format_voice_result(result)
