"""Stem, sound-effect, and speed tools from the public Suno audio contract."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_MODEL,
    SunoAudioFormat,
    SunoModel,
    SunoSoundType,
    SunoStemType,
    SunoVariety,
)
from core.utils import format_audio_result


@mcp.tool()
async def suno_add_stem(
    audio_id: Annotated[str, Field(min_length=1, description="Source audio ID.")],
    stem_type: SunoStemType,
    model: SunoModel = DEFAULT_MODEL,
    prompt: str | None = None,
    title: str | None = None,
    style: str | None = None,
    negative_tags: str | None = None,
    weirdness: Annotated[float | None, Field(ge=0, le=1)] = None,
    style_influence: Annotated[float | None, Field(ge=0, le=1)] = None,
    audio_weight: Annotated[float | None, Field(ge=0, le=1)] = None,
    max_mode: Annotated[
        bool | None,
        Field(
            description="Enhanced mode has a higher API price. Omitted/false keeps normal pricing."
        ),
    ] = None,
    variety: SunoVariety | None = None,
    callback_url: str | None = None,
) -> str:
    """Generate a selected instrument or voice stem for an existing audio. Poll suno_get_task."""
    payload = {
        "action": "add_stem",
        "audio_id": audio_id,
        "stem_type": stem_type,
        "model": model,
        "prompt": prompt,
        "title": title,
        "style": style,
        "negative_tags": negative_tags,
        "weirdness": weirdness,
        "style_influence": style_influence,
        "audio_weight": audio_weight,
        "max_mode": max_mode,
        "variety": variety,
        "callback_url": callback_url,
    }
    result = await client.generate_audio(**{k: v for k, v in payload.items() if v is not None})
    return format_audio_result(result)


@mcp.tool()
async def suno_extract_stem(
    audio_id: Annotated[str, Field(min_length=1)],
    stem_type: SunoStemType,
    model: SunoModel = DEFAULT_MODEL,
    audio_format: SunoAudioFormat | None = None,
    callback_url: str | None = None,
) -> str:
    """Extract a selected stem and its complementary remainder. Preserve both returned pairs."""
    payload = {
        "action": "extract_stem",
        "audio_id": audio_id,
        "stem_type": stem_type,
        "model": model,
        "audio_format": audio_format,
        "callback_url": callback_url,
    }
    result = await client.generate_audio(**{k: v for k, v in payload.items() if v is not None})
    return format_audio_result(result)


@mcp.tool()
async def suno_generate_sound(
    sound: Annotated[str, Field(min_length=1, description="Description of the sound effect.")],
    sound_type: SunoSoundType,
    model: SunoModel = DEFAULT_MODEL,
    bpm: Annotated[int | None, Field(ge=1, le=300)] = None,
    key: Annotated[str | None, Field(pattern=r"^[A-G](?:#|b)?m?$")] = None,
    audio_format: SunoAudioFormat | None = None,
    callback_url: str | None = None,
) -> str:
    """Create a one-shot or looping sound effect. Optional bpm and musical key guide the result."""
    payload = {
        "action": "sounds",
        "sound": sound,
        "sound_type": sound_type,
        "model": model,
        "bpm": bpm,
        "key": key,
        "audio_format": audio_format,
        "callback_url": callback_url,
    }
    result = await client.generate_audio(**{k: v for k, v in payload.items() if v is not None})
    return format_audio_result(result)


@mcp.tool()
async def suno_adjust_speed(
    audio_id: Annotated[str, Field(min_length=1)],
    title: Annotated[str, Field(min_length=1, description="Title of the adjusted audio.")],
    speed_multiplier: Annotated[float, Field(ge=0.25, le=4)],
    keep_pitch: bool = False,
    callback_url: str | None = None,
) -> str:
    """Adjust audio playback speed, optionally preserving pitch. Poll the returned task ID."""
    payload = {
        "action": "adjust_speed",
        "audio_id": audio_id,
        "title": title,
        "speed_multiplier": speed_multiplier,
        "keep_pitch": keep_pitch,
        "callback_url": callback_url,
    }
    result = await client.generate_audio(**{k: v for k, v in payload.items() if v is not None})
    return format_audio_result(result)
