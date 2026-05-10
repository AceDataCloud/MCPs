"""Audio generation tools for Fish TTS API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import FishAPIError, FishAuthError
from core.server import mcp
from core.types import DEFAULT_MODEL, DEFAULT_VOICE_ID, FishAudioAction, FishModel


@mcp.tool()
async def fish_generate_audio(
    prompt: Annotated[
        str,
        Field(
            description="The input text to convert to speech. Required."
        ),
    ],
    voice_id: Annotated[
        str,
        Field(
            description=(
                f"The voice ID to use for speech synthesis. "
                f"Use fish_create_voice to clone your own voice and get a voice_id. "
                f"Default example voice: {DEFAULT_VOICE_ID}. Required."
            )
        ),
    ],
    action: Annotated[
        FishAudioAction,
        Field(description="The audio generation action. Currently only 'speech' is supported."),
    ] = "speech",
    model: Annotated[
        FishModel,
        Field(description="The TTS model to use. Currently only 'fish-tts' is supported."),
    ] = DEFAULT_MODEL,
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
    """Generate speech audio from text using Fish TTS voice cloning.

    Converts text to speech using a specified voice ID. The voice can be one
    of Fish's built-in voices or a custom voice cloned via fish_create_voice.

    Use this when:
    - You want to convert text to speech
    - You want to clone a voice for TTS
    - You need AI-generated audio narration

    Returns:
        JSON response containing task_id and audio data when complete.

    Example:
        fish_generate_audio(
            prompt="Hello, welcome to our service!",
            voice_id="d7900c21663f485ab63ebdb7e5905036"
        )
    """
    if not prompt:
        return json.dumps({"error": "Validation Error", "message": "prompt is required"})

    if not voice_id:
        return json.dumps({"error": "Validation Error", "message": "voice_id is required"})

    payload: dict = {
        "action": action,
        "prompt": prompt,
        "voice_id": voice_id,
        "model": model,
    }
    if callback_url:
        payload["callback_url"] = callback_url

    try:
        result = await client.generate_audio(**payload)

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except FishAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except FishAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error generating audio", "message": str(e)})
