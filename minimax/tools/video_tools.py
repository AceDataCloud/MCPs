"""MiniMax H3 multimodal video generation tools."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_DURATION,
    DEFAULT_MODEL,
    DEFAULT_RATIO,
    DEFAULT_RESOLUTION,
    MinimaxContent,
    MinimaxModel,
    MinimaxRatio,
    MinimaxResolution,
)
from core.utils import format_video_result


def _common_payload(
    *,
    model: MinimaxModel,
    resolution: MinimaxResolution,
    ratio: MinimaxRatio,
    duration: int,
    content: list[dict],
    callback_url: str | None,
) -> dict:
    payload: dict = {
        "model": model,
        "content": content,
        "resolution": resolution,
        "ratio": ratio,
        "duration": duration,
    }
    if callback_url:
        payload["callback_url"] = callback_url
    return payload


@mcp.tool()
async def minimax_generate_video_from_text(
    prompt: Annotated[
        str,
        Field(
            min_length=1,
            max_length=7000,
            description="Scene, motion, camera, and style description.",
        ),
    ],
    resolution: Annotated[
        MinimaxResolution, Field(description="Output resolution: 768P or 2K.")
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[MinimaxRatio, Field(description="Output aspect ratio.")] = DEFAULT_RATIO,
    duration: Annotated[
        int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")
    ] = DEFAULT_DURATION,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None, Field(description="Optional public webhook URL for the final result.")
    ] = None,
) -> str:
    """Generate a MiniMax H3 video from a text prompt."""
    payload = _common_payload(
        model=model,
        resolution=resolution,
        ratio=ratio,
        duration=duration,
        content=[{"type": "text", "text": prompt}],
        callback_url=callback_url,
    )
    return format_video_result(await client.generate_video(**payload))


@mcp.tool()
async def minimax_generate_video_from_images(
    image_urls: Annotated[list[str], Field(min_length=1, description="Public image URLs.")],
    prompt: Annotated[
        str, Field(min_length=1, max_length=7000, description="Required motion and style guidance.")
    ],
    resolution: Annotated[
        MinimaxResolution, Field(description="Output resolution: 768P or 2K.")
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[MinimaxRatio, Field(description="Output aspect ratio.")] = DEFAULT_RATIO,
    duration: Annotated[
        int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")
    ] = DEFAULT_DURATION,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None, Field(description="Optional public webhook URL for the final result.")
    ] = None,
) -> str:
    """Generate from one first-frame image or multiple reference images.

    Single image uses first_frame mode; multiple images use reference_image mode.
    The two modes are mutually exclusive per MiniMax H3 v2 API contract.
    """
    # Official constraint: first_frame/last_frame and reference_image are mutually exclusive.
    role = "first_frame" if len(image_urls) == 1 else "reference_image"
    payload = _common_payload(
        model=model,
        resolution=resolution,
        ratio=ratio,
        duration=duration,
        content=[
            {"type": "text", "text": prompt},
            *[
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                    "role": role,
                }
                for image_url in image_urls
            ],
        ],
        callback_url=callback_url,
    )
    return format_video_result(await client.generate_video(**payload))


@mcp.tool()
async def minimax_generate_video_from_audio(
    audio_urls: Annotated[list[str], Field(min_length=1, description="Public audio URLs.")],
    image_urls: Annotated[
        list[str],
        Field(min_length=1, description="Required reference images."),
    ],
    prompt: Annotated[
        str, Field(min_length=1, max_length=7000, description="Required scene and rhythm guidance.")
    ],
    resolution: Annotated[
        MinimaxResolution, Field(description="Output resolution: 768P or 2K.")
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[MinimaxRatio, Field(description="Output aspect ratio.")] = DEFAULT_RATIO,
    duration: Annotated[
        int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")
    ] = DEFAULT_DURATION,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None, Field(description="Optional public webhook URL for the final result.")
    ] = None,
) -> str:
    """Generate a MiniMax H3 video guided by audio and reference images.

    Audio-guided generation uses reference mode exclusively (reference_audio
    forces the entire content into reference-to-video mode per the H3 v2 contract).
    """
    payload = _common_payload(
        model=model,
        resolution=resolution,
        ratio=ratio,
        duration=duration,
        content=[
            {"type": "text", "text": prompt},
            *[
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                    "role": "reference_image",
                }
                for image_url in image_urls
            ],
            *[
                {
                    "type": "audio_url",
                    "audio_url": {"url": audio_url},
                    "role": "reference_audio",
                }
                for audio_url in audio_urls
            ],
        ],
        callback_url=callback_url,
    )
    return format_video_result(await client.generate_video(**payload))


@mcp.tool()
async def minimax_generate_video(
    content: Annotated[
        list[MinimaxContent],
        Field(min_length=1, description="Ordered text, image, video, and audio content items."),
    ],
    resolution: Annotated[
        MinimaxResolution, Field(description="Output resolution: 768P or 2K.")
    ] = DEFAULT_RESOLUTION,
    duration: Annotated[
        int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")
    ] = DEFAULT_DURATION,
    ratio: Annotated[
        MinimaxRatio,
        Field(description="Output aspect ratio: adaptive, 21:9, 16:9, 4:3, 1:1, 3:4, or 9:16."),
    ] = DEFAULT_RATIO,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None, Field(description="Optional public webhook URL for the final result.")
    ] = None,
) -> str:
    """Generate a video from the full MiniMax content schema."""
    payload = _common_payload(
        model=model,
        resolution=resolution,
        ratio=ratio,
        duration=duration,
        content=[item.model_dump(exclude_none=True) for item in content],
        callback_url=callback_url,
    )
    return format_video_result(await client.generate_video(**payload))
