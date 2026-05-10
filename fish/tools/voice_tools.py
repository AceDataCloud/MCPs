"""Voice cloning tools for Fish API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import FishAPIError, FishAuthError
from core.server import mcp


@mcp.tool()
async def fish_create_voice(
    voice_url: Annotated[
        str,
        Field(
            description=(
                "Public URL of an audio file to use as the voice sample. "
                "Must be accessible from the internet. Required."
            )
        ),
    ],
    title: Annotated[
        str | None,
        Field(description="Optional title/name for this voice."),
    ] = None,
    description: Annotated[
        str | None,
        Field(description="Optional description of this voice."),
    ] = None,
    image_url: Annotated[
        str | None,
        Field(description="Optional cover image URL for this voice."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description=(
                "Optional callback URL to receive the result asynchronously. "
                "If provided, the API returns immediately with a task_id."
            )
        ),
    ] = None,
) -> str:
    """Clone a voice from an audio sample URL.

    Creates a custom voice by cloning from an audio sample. The resulting
    voice_id can then be used with fish_generate_audio for text-to-speech.

    Use this when:
    - You want to clone a specific person's voice for TTS
    - You need a custom voice for audio generation
    - You have an audio sample you want to use as a TTS voice

    Returns:
        JSON response containing task_id and the voice_id for the cloned voice.

    Example:
        fish_create_voice(
            voice_url="https://example.com/my-voice-sample.mp3",
            title="My Custom Voice"
        )
    """
    if not voice_url:
        return json.dumps({"error": "Validation Error", "message": "voice_url is required"})

    payload: dict = {"voice_url": voice_url}
    if title:
        payload["title"] = title
    if description:
        payload["description"] = description
    if image_url:
        payload["image_url"] = image_url
    if callback_url:
        payload["callback_url"] = callback_url

    try:
        result = await client.create_voice(**payload)

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except FishAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except FishAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating voice", "message": str(e)})
