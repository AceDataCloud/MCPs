"""Audio speech tools for OpenAI API."""

import base64
import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp
from core.types import (
    DEFAULT_AUDIO_SPEECH_MODEL,
    DEFAULT_AUDIO_SPEECH_RESPONSE_FORMAT,
    DEFAULT_AUDIO_SPEECH_VOICE,
    AudioSpeechModel,
    AudioSpeechResponseFormat,
    AudioSpeechVoice,
)


@mcp.tool()
async def openai_text_to_speech(
    input: Annotated[
        str,
        Field(
            description=(
                "The text to synthesize into speech. "
                "Example: 'Hello, welcome to our service!'"
            )
        ),
    ],
    model: Annotated[
        AudioSpeechModel,
        Field(
            description=(
                "The TTS model to use. Options: 'tts-1-hd' (default, higher quality), "
                "'tts-1' (faster, lower latency)."
            )
        ),
    ] = DEFAULT_AUDIO_SPEECH_MODEL,
    voice: Annotated[
        AudioSpeechVoice,
        Field(
            description=(
                "The voice to use for synthesis. Options: 'alloy' (default), 'echo', "
                "'fable', 'onyx', 'nova', 'shimmer'."
            )
        ),
    ] = DEFAULT_AUDIO_SPEECH_VOICE,
    response_format: Annotated[
        AudioSpeechResponseFormat,
        Field(
            description=(
                "Audio output format. Options: 'mp3' (default), 'opus', 'aac', 'flac', "
                "'wav', 'pcm'."
            )
        ),
    ] = DEFAULT_AUDIO_SPEECH_RESPONSE_FORMAT,
    speed: Annotated[
        float | None,
        Field(
            description=(
                "Speaking speed multiplier. Range: 0.25 to 4.0. Default is 1.0 (normal speed)."
            )
        ),
    ] = None,
) -> str:
    """Generate speech audio from text using OpenAI TTS models via AceDataCloud.

    Converts text to natural-sounding speech using OpenAI's text-to-speech models.

    Use this when:
    - You need to convert text to spoken audio
    - You want to generate voiceovers or narration
    - You need audio output from text content

    Returns:
        JSON response containing base64-encoded audio data and format information.
        Decode the 'audio' field with base64 to get the raw audio bytes.
    """
    try:
        payload: dict = {
            "model": model,
            "input": input,
            "voice": voice,
            "response_format": response_format,
        }

        if speed is not None:
            payload["speed"] = speed

        audio_bytes = await client.audio_speech(**payload)

        if not audio_bytes:
            return json.dumps({"error": "No audio data received."})

        return json.dumps(
            {
                "audio": base64.b64encode(audio_bytes).decode("utf-8"),
                "format": response_format,
                "encoding": "base64",
                "size_bytes": len(audio_bytes),
            }
        )

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error generating speech", "message": str(e)})
