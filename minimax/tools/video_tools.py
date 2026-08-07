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
    prompt: str,
    aigc_watermark: bool,
    callback_url: str | None,
) -> dict:
    payload: dict = {
        "model": model,
        "prompt": prompt,
        "resolution": resolution,
        "ratio": ratio,
        "duration": duration,
        "aigc_watermark": aigc_watermark,
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
    ratio: Annotated[
        MinimaxRatio, Field(description="Output aspect ratio: 16:9 or 9:16.")
    ] = DEFAULT_RATIO,
    duration: Annotated[
        int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")
    ] = DEFAULT_DURATION,
    aigc_watermark: Annotated[bool, Field(description="Add an AIGC watermark.")] = False,
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
        prompt=prompt,
        aigc_watermark=aigc_watermark,
        callback_url=callback_url,
    )
    return format_video_result(await client.generate_video(**payload))


@mcp.tool()
async def minimax_generate_video_from_images(
    image_urls: Annotated[
        list[str], Field(min_length=1, max_length=9, description="One to nine public image URLs.")
    ],
    prompt: Annotated[
        str, Field(min_length=1, max_length=7000, description="Required motion and style guidance.")
    ],
    resolution: Annotated[
        MinimaxResolution, Field(description="Output resolution: 768P or 2K.")
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[
        MinimaxRatio, Field(description="Output aspect ratio: 16:9 or 9:16.")
    ] = DEFAULT_RATIO,
    duration: Annotated[
        int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")
    ] = DEFAULT_DURATION,
    aigc_watermark: Annotated[bool, Field(description="Add an AIGC watermark.")] = False,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None, Field(description="Optional public webhook URL for the final result.")
    ] = None,
) -> str:
    """Generate from one first-frame image or multiple reference images."""
    payload = _common_payload(
        model=model,
        resolution=resolution,
        ratio=ratio,
        duration=duration,
        prompt=prompt,
        aigc_watermark=aigc_watermark,
        callback_url=callback_url,
    )
    payload["image_urls"] = image_urls
    return format_video_result(await client.generate_video(**payload))


@mcp.tool()
async def minimax_generate_video_from_audio(
    audio_urls: Annotated[
        list[str], Field(min_length=1, max_length=3, description="One to three public audio URLs.")
    ],
    image_urls: Annotated[
        list[str],
        Field(min_length=1, max_length=9, description="One to nine required reference images."),
    ],
    prompt: Annotated[
        str, Field(min_length=1, max_length=7000, description="Required scene and rhythm guidance.")
    ],
    resolution: Annotated[
        MinimaxResolution, Field(description="Output resolution: 768P or 2K.")
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[
        MinimaxRatio, Field(description="Output aspect ratio: 16:9 or 9:16.")
    ] = DEFAULT_RATIO,
    duration: Annotated[
        int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")
    ] = DEFAULT_DURATION,
    aigc_watermark: Annotated[bool, Field(description="Add an AIGC watermark.")] = False,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None, Field(description="Optional public webhook URL for the final result.")
    ] = None,
) -> str:
    """Generate a MiniMax H3 video guided by audio and reference images."""
    payload = _common_payload(
        model=model,
        resolution=resolution,
        ratio=ratio,
        duration=duration,
        prompt=prompt,
        aigc_watermark=aigc_watermark,
        callback_url=callback_url,
    )
    payload["audio_urls"] = audio_urls
    payload["image_urls"] = image_urls
    return format_video_result(await client.generate_video(**payload))
