"""Audio generation tools for Fish API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, DEFAULT_VOICE_ID, FishModel
from core.utils import format_audio_result


@mcp.tool()
async def fish_generate_audio(
    prompt: Annotated[
        str,
        Field(
            description="The input text to convert to speech. Use natural, clear sentences with proper punctuation for best results. Examples: 'Hello, how are you today?', 'Welcome to our service. We are pleased to assist you.'"
        ),
    ],
    voice_id: Annotated[
        str,
        Field(
            description="The voice ID to use for speech generation. This identifies which voice persona to use. Use the default or a voice_id returned from fish_create_voice."
        ),
    ] = DEFAULT_VOICE_ID,
    model: Annotated[
        FishModel,
        Field(description="The TTS model to use. Currently 'fish-tts' is the available model."),
    ] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the audio is generated."
        ),
    ] = None,
) -> str:
    """Generate speech audio from text using the Fish TTS API.

    Converts text to natural-sounding speech using a specified voice. Supports
    voice cloning via the voice_id parameter.

    Use this when:
    - You want to convert text to speech
    - You need to generate audio from a text prompt
    - You want to use a specific voice for narration

    Returns:
        Task ID and generated audio information including URLs and status.
    """
    payload: dict = {
        "action": "speech",
        "prompt": prompt,
        "voice_id": voice_id,
        "model": model,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_audio(**payload)
    return format_audio_result(result)
