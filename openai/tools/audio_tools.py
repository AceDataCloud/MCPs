"""Audio speech tools for OpenAI API."""

import base64
import json
from typing import Annotated

import httpx
from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp
from core.types import (
    DEFAULT_AUDIO_SPEECH_MODEL,
    DEFAULT_AUDIO_SPEECH_RESPONSE_FORMAT,
    DEFAULT_AUDIO_SPEECH_VOICE,
    DEFAULT_AUDIO_TRANSCRIPTION_MODEL,
    DEFAULT_AUDIO_TRANSCRIPTION_RESPONSE_FORMAT,
    AudioSpeechModel,
    AudioSpeechResponseFormat,
    AudioSpeechVoice,
    AudioTranscriptionModel,
    AudioTranscriptionResponseFormat,
    AudioTranscriptionTimestampGranularity,
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


@mcp.tool()
async def openai_transcribe_audio(
    url: Annotated[
        str,
        Field(
            description=(
                "URL of the audio file to transcribe. The file will be downloaded and sent "
                "to the Whisper model. Supported formats: flac, mp3, mp4, mpeg, mpga, m4a, "
                "ogg, wav, webm. Maximum file size: 25 MB."
            )
        ),
    ],
    model: Annotated[
        AudioTranscriptionModel,
        Field(description="The transcription model to use. Currently only 'whisper-1' is supported."),
    ] = DEFAULT_AUDIO_TRANSCRIPTION_MODEL,
    language: Annotated[
        str | None,
        Field(
            description=(
                "The language of the audio in ISO-639-1 format (e.g. 'en', 'fr', 'de'). "
                "Providing this improves accuracy and latency. If omitted, Whisper auto-detects."
            )
        ),
    ] = None,
    prompt: Annotated[
        str | None,
        Field(
            description=(
                "Optional text to guide the model's style or continue a previous audio segment. "
                "The prompt should match the audio language."
            )
        ),
    ] = None,
    response_format: Annotated[
        AudioTranscriptionResponseFormat,
        Field(
            description=(
                "Format of the transcription output. Options: 'json' (default, returns "
                "structured JSON with 'text' field), 'text' (plain text), "
                "'srt' (SubRip subtitle format), 'verbose_json' (detailed JSON with timestamps "
                "and segments), 'vtt' (WebVTT subtitle format)."
            )
        ),
    ] = DEFAULT_AUDIO_TRANSCRIPTION_RESPONSE_FORMAT,
    temperature: Annotated[
        float | None,
        Field(
            description=(
                "Sampling temperature between 0 and 1. Higher values produce more creative "
                "but potentially less accurate output. Default is 0 (deterministic)."
            )
        ),
    ] = None,
    timestamp_granularities: Annotated[
        list[AudioTranscriptionTimestampGranularity] | None,
        Field(
            description=(
                "Granularity of timestamps in verbose_json output. Options: 'word' "
                "(word-level timestamps), 'segment' (segment-level timestamps). "
                "Only used when response_format is 'verbose_json'."
            )
        ),
    ] = None,
) -> str:
    """Transcribe audio to text using OpenAI Whisper via AceDataCloud.

    Downloads audio from the given URL and sends it to Whisper for transcription.
    Supports a wide range of audio formats and optional language hints.

    Use this when:
    - You need to convert spoken audio to text
    - You want subtitles or captions from a video/audio file
    - You need timestamped transcripts for processing

    Returns:
        JSON response containing the transcribed text (and timestamps if verbose_json).
        For 'text', 'srt', and 'vtt' formats the raw string is returned in a
        {"text": "..."} wrapper for consistent handling.
    """
    try:
        async with httpx.AsyncClient() as http:
            dl_response = await http.get(url, follow_redirects=True, timeout=60.0)
            dl_response.raise_for_status()
            audio_bytes = dl_response.content

        if not audio_bytes:
            return json.dumps({"error": "Downloaded audio file is empty."})

        kwargs: dict = {"model": model, "response_format": response_format}
        if language is not None:
            kwargs["language"] = language
        if prompt is not None:
            kwargs["prompt"] = prompt
        if temperature is not None:
            kwargs["temperature"] = temperature
        if timestamp_granularities is not None:
            kwargs["timestamp_granularities"] = timestamp_granularities

        result = await client.audio_transcriptions(audio_bytes, **kwargs)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except httpx.HTTPStatusError as e:
        return json.dumps({"error": "Failed to download audio file", "message": str(e)})
    except Exception as e:
        return json.dumps({"error": "Error transcribing audio", "message": str(e)})
