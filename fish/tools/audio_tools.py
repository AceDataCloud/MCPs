"""Audio generation tools for Fish TTS API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import FishAPIError, FishAuthError
from core.server import mcp
from core.types import DEFAULT_MODEL, DEFAULT_VOICE_ID, FishAudioFormat, FishLatency, FishModel


@mcp.tool()
async def fish_generate_audio(
    text: Annotated[
        str | None,
        Field(
            description="The text to synthesize. Required unless `prompt` is provided."
        ),
    ] = None,
    prompt: Annotated[
        str | None,
        Field(
            description=(
                "Deprecated alias for `text`. "
                "Kept for backward compatibility."
            )
        ),
    ] = None,
    reference_id: Annotated[
        str | None,
        Field(description="Voice model id for single-speaker TTS."),
    ] = None,
    voice_id: Annotated[
        str | None,
        Field(
            description=(
                "Deprecated alias for `reference_id`. "
                f"Example voice model id: {DEFAULT_VOICE_ID}."
            )
        ),
    ] = None,
    model: Annotated[
        FishModel,
        Field(description="TTS model to use. One of `s1` or `s2-pro`."),
    ] = DEFAULT_MODEL,
    format: Annotated[
        FishAudioFormat | None,
        Field(description="Output audio format."),
    ] = None,
    sample_rate: Annotated[
        int | None,
        Field(description="Sampling rate of the output audio."),
    ] = None,
    mp3_bitrate: Annotated[
        int | None,
        Field(description="MP3 bitrate when format=mp3. One of 64, 128, 192."),
    ] = None,
    opus_bitrate: Annotated[
        int | None,
        Field(description="Opus bitrate when format=opus."),
    ] = None,
    latency: Annotated[
        FishLatency | None,
        Field(description="Latency mode. One of `normal` or `balanced`."),
    ] = None,
    chunk_length: Annotated[
        int | None,
        Field(description="Chunk length forwarded to upstream synthesizer."),
    ] = None,
    min_chunk_length: Annotated[
        int | None,
        Field(description="Minimum chunk length."),
    ] = None,
    temperature: Annotated[
        float | None,
        Field(description="Sampling temperature (0.0-1.0)."),
    ] = None,
    top_p: Annotated[
        float | None,
        Field(description="Top-p nucleus sampling parameter."),
    ] = None,
    repetition_penalty: Annotated[
        float | None,
        Field(description="Repetition penalty applied during generation."),
    ] = None,
    max_new_tokens: Annotated[
        int | None,
        Field(description="Maximum number of new tokens to generate."),
    ] = None,
    normalize: Annotated[
        bool | None,
        Field(description="Whether the upstream should apply text normalization."),
    ] = None,
    prosody: Annotated[
        dict | None,
        Field(description="Prosody overrides passed through to upstream."),
    ] = None,
    references: Annotated[
        list[dict] | None,
        Field(description="Inline reference samples passed through to upstream."),
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
            text="Hello, welcome to our service!",
            reference_id="d7900c21663f485ab63ebdb7e5905036"
        )
    """
    resolved_text = text or prompt
    if not resolved_text:
        return json.dumps({"error": "Validation Error", "message": "text (or prompt) is required"})

    resolved_reference_id = reference_id or voice_id

    payload: dict = {
        "text": resolved_text,
    }
    if resolved_reference_id:
        payload["reference_id"] = resolved_reference_id
    if format is not None:
        payload["format"] = format
    if sample_rate is not None:
        payload["sample_rate"] = sample_rate
    if mp3_bitrate is not None:
        payload["mp3_bitrate"] = mp3_bitrate
    if opus_bitrate is not None:
        payload["opus_bitrate"] = opus_bitrate
    if latency is not None:
        payload["latency"] = latency
    if chunk_length is not None:
        payload["chunk_length"] = chunk_length
    if min_chunk_length is not None:
        payload["min_chunk_length"] = min_chunk_length
    if temperature is not None:
        payload["temperature"] = temperature
    if top_p is not None:
        payload["top_p"] = top_p
    if repetition_penalty is not None:
        payload["repetition_penalty"] = repetition_penalty
    if max_new_tokens is not None:
        payload["max_new_tokens"] = max_new_tokens
    if normalize is not None:
        payload["normalize"] = normalize
    if prosody is not None:
        payload["prosody"] = prosody
    if references is not None:
        payload["references"] = references
    if callback_url:
        payload["callback_url"] = callback_url

    try:
        # OpenAPI defines `model` as a request header, not a JSON body field.
        result = await client.generate_audio(model=model, **payload)

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except FishAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except FishAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error generating audio", "message": str(e)})
