"""MiniMax H3 multimodal video generation tools."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_DURATION, DEFAULT_MODEL, DEFAULT_RATIO, MinimaxModel, MinimaxRatio
from core.utils import format_video_result


def _common_payload(
    *,
    model: MinimaxModel,
    ratio: MinimaxRatio,
    duration: int,
    prompt: str | None,
    callback_url: str | None,
) -> dict:
    payload: dict = {"model": model, "ratio": ratio, "duration": duration}
    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url
    return payload


@mcp.tool()
async def minimax_generate_video_from_text(
    prompt: Annotated[str, Field(description="Detailed scene, motion, camera, and style description.")],
    ratio: Annotated[MinimaxRatio, Field(description="Output aspect ratio: 16:9 or 9:16.")] = DEFAULT_RATIO,
    duration: Annotated[int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")] = DEFAULT_DURATION,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[str | None, Field(description="Optional public webhook URL for the final result.")] = None,
) -> str:
    """Generate a MiniMax H3 video from a text prompt."""
    payload = _common_payload(model=model, ratio=ratio, duration=duration, prompt=prompt, callback_url=callback_url)
    return format_video_result(await client.generate_video(**payload))


@mcp.tool()
async def minimax_generate_video_from_images(
    image_urls: Annotated[
        list[str],
        Field(min_length=1, max_length=9, description="One to nine public reference image URLs."),
    ],
    prompt: Annotated[str | None, Field(description="Optional motion, camera, and style guidance.")] = None,
    ratio: Annotated[MinimaxRatio, Field(description="Output aspect ratio: 16:9 or 9:16.")] = DEFAULT_RATIO,
    duration: Annotated[int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")] = DEFAULT_DURATION,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[str | None, Field(description="Optional public webhook URL for the final result.")] = None,
) -> str:
    """Generate a MiniMax H3 video from one or more reference images."""
    payload = _common_payload(model=model, ratio=ratio, duration=duration, prompt=prompt, callback_url=callback_url)
    payload["image_urls"] = image_urls
    return format_video_result(await client.generate_video(**payload))


@mcp.tool()
async def minimax_generate_video_from_audio(
    audio_urls: Annotated[
        list[str],
        Field(min_length=1, max_length=3, description="One to three public reference audio URLs."),
    ],
    prompt: Annotated[str | None, Field(description="Optional scene, motion, camera, and style guidance.")] = None,
    image_urls: Annotated[
        list[str] | None,
        Field(min_length=1, max_length=9, description="Optional one to nine public reference image URLs."),
    ] = None,
    ratio: Annotated[MinimaxRatio, Field(description="Output aspect ratio: 16:9 or 9:16.")] = DEFAULT_RATIO,
    duration: Annotated[int, Field(ge=4, le=15, description="Integer output duration from 4 to 15 seconds.")] = DEFAULT_DURATION,
    model: Annotated[MinimaxModel, Field(description="MiniMax H3 model name.")] = DEFAULT_MODEL,
    callback_url: Annotated[str | None, Field(description="Optional public webhook URL for the final result.")] = None,
) -> str:
    """Generate a MiniMax H3 video guided by reference audio."""
    payload = _common_payload(model=model, ratio=ratio, duration=duration, prompt=prompt, callback_url=callback_url)
    payload["audio_urls"] = audio_urls
    if image_urls:
        payload["image_urls"] = image_urls
    return format_video_result(await client.generate_video(**payload))
