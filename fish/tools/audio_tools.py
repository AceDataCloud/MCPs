"""Audio generation tools for Fish TTS API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import FishAPIError, FishAuthError
from core.server import mcp
from core.types import (
    DEFAULT_MODEL,
    DEFAULT_VOICE_ID,
    FishAudioFormat,
    FishLatency,
    FishModel,
)


@mcp.tool()
async def fish_generate_audio(
    text: Annotated[
        str | None,
        Field(description="The text to synthesize. Required."),
    ] = None,
    reference_id: Annotated[
        str | None,
        Field(
            description=(
                "Voice model id (single speaker). "
                f"Default example voice model ID: {DEFAULT_VOICE_ID}."
            )
        ),
    ] = None,
    prompt: Annotated[
        str | None,
        Field(description="Deprecated alias for `text`."),
    ] = None,
    voice_id: Annotated[
        str | None,
        Field(description="Deprecated alias for `reference_id`."),
    ] = None,
    model: Annotated[
        FishModel,
        Field(description="The TTS model to use. Supported values: 's1', 's2-pro'."),
    ] = DEFAULT_MODEL,
    format: Annotated[
        FishAudioFormat,
        Field(description="Output audio format. Defaults to 'mp3'."),
    ] = "mp3",
    sample_rate: Annotated[
        int | None,
        Field(description="Sampling rate of the output audio (e.g. 16000, 22050, 44100)."),
    ] = None,
    mp3_bitrate: Annotated[
        int | None,
        Field(description="MP3 bit rate when format='mp3'. Supported values: 64, 128, 192."),
    ] = None,
    opus_bitrate: Annotated[
        int | None,
        Field(description="Opus bit rate when format='opus'."),
    ] = None,
    latency: Annotated[
        FishLatency | None,
        Field(description="Latency mode. Supported values: 'normal', 'balanced'."),
    ] = None,
    chunk_length: Annotated[
        int | None,
        Field(description="Chunk length passed through to the upstream synthesiser."),
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
        Field(description="Prosody overrides forwarded to the upstream."),
    ] = None,
    references: Annotated[
        list[dict] | None,
        Field(description="Inline reference samples forwarded to the upstream."),
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
    """Generate speech audio from text using Fish TTS.

    Use this when:
    - You want to convert text to speech
    - You need AI-generated audio narration

    Returns:
        JSON response containing task_id and audio data when complete.

    Example:
        fish_generate_audio(
            text="Hello, welcome to our service!",
            reference_id="d7900c21663f485ab63ebdb7e5905036"
        )
    """
    if text is not None and prompt is not None and text != prompt:
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "Provide either text or prompt (deprecated), not both.",
            }
        )
    if reference_id is not None and voice_id is not None and reference_id != voice_id:
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "Provide either reference_id or voice_id (deprecated), not both.",
            }
        )
    request_text = text or prompt
    request_reference_id = reference_id or voice_id
    if not request_text:
        return json.dumps({"error": "Validation Error", "message": "text is required"})

    payload: dict = {"text": request_text, "format": format, "model": model}
    if request_reference_id:
        payload["reference_id"] = request_reference_id
    optional_payload = {
        "sample_rate": sample_rate,
        "mp3_bitrate": mp3_bitrate,
        "opus_bitrate": opus_bitrate,
        "latency": latency,
        "chunk_length": chunk_length,
        "min_chunk_length": min_chunk_length,
        "temperature": temperature,
        "top_p": top_p,
        "repetition_penalty": repetition_penalty,
        "max_new_tokens": max_new_tokens,
        "normalize": normalize,
        "prosody": prosody,
        "references": references,
    }
    for key, value in optional_payload.items():
        if value is not None:
            payload[key] = value
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
