"""Video generation tools for Wan API."""

import re
from typing import Annotated

from pydantic import BeforeValidator, Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_RESOLUTION,
    Duration,
    MediaItem,
    Ratio,
    Resolution,
    ShotType,
    WanModel,
)
from core.utils import format_video_result

_LEGACY_REFERENCE_SEPARATOR = re.compile(r",\s*(?=https?://)", re.IGNORECASE)


def _normalize_reference_video_urls(value: list[str] | str) -> list[str]:
    if isinstance(value, str):
        value = _LEGACY_REFERENCE_SEPARATOR.split(value)
    return [url.strip() for url in value if url.strip()]


ReferenceVideoURLs = Annotated[
    list[str],
    BeforeValidator(_normalize_reference_video_urls),
    Field(min_length=1),
]


@mcp.tool()
async def wan_generate_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about the scene, motion, style, and mood."
        ),
    ],
    model: Annotated[
        WanModel,
        Field(description="Wan model to use. Default: 'wan2.6-t2v'."),
    ] = "wan2.6-t2v",
    negative_prompt: Annotated[
        str,
        Field(description="Content to exclude from the video. Maximum 500 characters."),
    ] = "",
    duration: Annotated[
        Duration | None,
        Field(
            description="Video duration in seconds. Use 2-30, or -1 when supported by the model."
        ),
    ] = None,
    resolution: Annotated[
        Resolution,
        Field(description="Video resolution. Options: '480P', '720P' (default), '1080P'."),
    ] = DEFAULT_RESOLUTION,
    audio: Annotated[
        bool,
        Field(description="Whether the generated video should include audio. Default is false."),
    ] = False,
    audio_url: Annotated[
        str | None,
        Field(
            description="URL of reference audio to use in the video. Only used when audio is enabled."
        ),
    ] = None,
    prompt_extend: Annotated[
        bool,
        Field(
            description="Enable LLM-based prompt rewriting for better results. Default is false."
        ),
    ] = False,
    size: Annotated[
        str | None,
        Field(description="The size of the generated video (e.g., '1280x720')."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the video is generated."
        ),
    ] = None,
    media: Annotated[
        list[MediaItem] | None,
        Field(
            max_length=10,
            description="Optional media inputs with a type and URL, supported by wan3.0-video.",
        ),
    ] = None,
    ratio: Annotated[
        Ratio | None,
        Field(description="Video aspect ratio. Options include 'adaptive', '16:9', and '9:16'."),
    ] = None,
    seed: Annotated[
        int | None,
        Field(ge=0, le=2147483647, description="Optional random seed."),
    ] = None,
    watermark: Annotated[
        bool,
        Field(description="Whether to add a watermark. Default is false."),
    ] = False,
) -> str:
    """Generate AI video from a text prompt using Wan text-to-video model.

    This uses the wan2.6-t2v model to create video from text descriptions.
    For creating video from images, use wan_generate_video_from_image instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "action": "text2video",
        "model": model,
        "prompt": prompt,
        "resolution": resolution,
        "audio": audio,
        "prompt_extend": prompt_extend,
    }

    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if duration is not None:
        payload["duration"] = duration
    if audio_url:
        payload["audio_url"] = audio_url
    if size:
        payload["size"] = size
    if callback_url:
        payload["callback_url"] = callback_url
    if media is not None:
        payload["media"] = [item.model_dump() for item in media]
    if ratio is not None:
        payload["ratio"] = ratio
    if seed is not None:
        payload["seed"] = seed
    if watermark:
        payload["watermark"] = watermark

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def wan_generate_video_from_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video motion and content. Describe what should happen in the video."
        ),
    ],
    image_url: Annotated[
        str,
        Field(
            description="URL of the reference image for video generation. The video will be generated based on this image."
        ),
    ],
    model: Annotated[
        WanModel,
        Field(description="Wan model to use. Default: 'wan2.6-i2v'."),
    ] = "wan2.6-i2v",
    negative_prompt: Annotated[
        str,
        Field(description="Content to exclude from the video. Maximum 500 characters."),
    ] = "",
    duration: Annotated[
        Duration | None,
        Field(
            description="Video duration in seconds. Use 2-30, or -1 when supported by the model."
        ),
    ] = None,
    resolution: Annotated[
        Resolution,
        Field(description="Video resolution. Options: '480P', '720P' (default), '1080P'."),
    ] = DEFAULT_RESOLUTION,
    reference_video_urls: Annotated[
        ReferenceVideoURLs | None,
        Field(
            description=(
                "JSON array of reference video URLs for character/timbre extraction. Used with "
                "the wan2.6-r2v model. Pass each URL as a separate array item; never join URLs "
                "with commas and never JSON-stringify the array. Legacy comma-separated strings "
                "are still accepted for backward compatibility."
            )
        ),
    ] = None,
    shot_type: Annotated[
        ShotType | None,
        Field(
            description="Shot type: 'single' for continuous shot, 'multi' for multi-cut editing."
        ),
    ] = None,
    audio: Annotated[
        bool,
        Field(description="Whether the generated video should include audio. Default is false."),
    ] = False,
    audio_url: Annotated[
        str | None,
        Field(description="URL of reference audio to use in the video."),
    ] = None,
    prompt_extend: Annotated[
        bool,
        Field(description="Enable LLM-based prompt rewriting. Default is false."),
    ] = False,
    size: Annotated[
        str | None,
        Field(description="The size of the generated video (e.g., '1280x720')."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
    media: Annotated[
        list[MediaItem] | None,
        Field(
            max_length=10,
            description="Optional media inputs with a type and URL, supported by wan3.0-video.",
        ),
    ] = None,
    ratio: Annotated[
        Ratio | None,
        Field(description="Video aspect ratio. Options include 'adaptive', '16:9', and '9:16'."),
    ] = None,
    seed: Annotated[
        int | None,
        Field(ge=0, le=2147483647, description="Optional random seed."),
    ] = None,
    watermark: Annotated[
        bool,
        Field(description="Whether to add a watermark. Default is false."),
    ] = False,
) -> str:
    """Generate AI video from a reference image using Wan image-to-video models.

    This supports three models:
    - wan2.6-i2v: Standard image-to-video generation
    - wan2.6-r2v: Reference video-to-video with character/timbre extraction
    - wan2.6-i2v-flash: Fast image-to-video generation

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "action": "image2video",
        "model": model,
        "prompt": prompt,
        "image_url": image_url,
        "resolution": resolution,
        "audio": audio,
        "prompt_extend": prompt_extend,
    }

    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if duration is not None:
        payload["duration"] = duration
    if reference_video_urls:
        payload["reference_video_urls"] = _normalize_reference_video_urls(reference_video_urls)
    if shot_type is not None:
        payload["shot_type"] = shot_type
    if audio_url:
        payload["audio_url"] = audio_url
    if size:
        payload["size"] = size
    if callback_url:
        payload["callback_url"] = callback_url
    if media is not None:
        payload["media"] = [item.model_dump() for item in media]
    if ratio is not None:
        payload["ratio"] = ratio
    if seed is not None:
        payload["seed"] = seed
    if watermark:
        payload["watermark"] = watermark

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def wan_generate_video_all_in_one(
    prompt: Annotated[
        str,
        Field(description="Video intent; refer to media as image 1, video 1, or audio 1 by order."),
    ] = "",
    media: Annotated[
        list[dict[str, str]] | None,
        Field(
            description="Media objects with type and URL. Types: first_frame, last_frame, reference_image, reference_video, reference_audio, file, link."
        ),
    ] = None,
    duration: Annotated[
        int, Field(description="Output seconds: 2-30, or -1 for automatic duration.", ge=-1, le=30)
    ] = 5,
    resolution: Annotated[str, Field(description="480P, 720P, or 1080P.")] = "1080P",
    ratio: Annotated[
        str, Field(description="adaptive, 16:9, 4:3, 1:1, 3:4, or 9:16.")
    ] = "adaptive",
    audio: bool = True,
    seed: Annotated[int | None, Field(ge=0, le=2147483647)] = None,
    watermark: bool = False,
    callback_url: str | None = None,
) -> str:
    """Generate a Wan 3 video from text, frames, reference media, a file, or a public link."""
    if duration == 0 or duration == 1:
        raise ValueError("duration must be -1 or 2-30")
    payload: dict = {
        "model": "wan3.0-video",
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution,
        "ratio": ratio,
        "audio": audio,
        "watermark": watermark,
    }
    if media is not None:
        payload["media"] = media
    if seed is not None:
        payload["seed"] = seed
    if callback_url:
        payload["callback_url"] = callback_url
    return format_video_result(await client.generate_video(**payload))
