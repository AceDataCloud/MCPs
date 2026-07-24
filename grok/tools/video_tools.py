"""Video generation tools for Grok Imagine API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_ASPECT_RATIO,
    DEFAULT_DURATION,
    DEFAULT_MODEL,
    DEFAULT_RESOLUTION,
    AspectRatio,
    GrokVideoModel,
    VideoResolution,
)
from core.utils import format_video_result


@mcp.tool()
async def grok_text_to_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about scene, subject, action, camera movement, lighting, and style. Examples: 'A cinematic shot of a kitten chasing a butterfly in a sunlit garden', 'Drone shot flying over a neon-lit cyberpunk city at night'. Required for text-to-video."
        ),
    ],
    model: Annotated[
        GrokVideoModel,
        Field(
            description="Grok Imagine model. Text-to-video is supported by 'grok-imagine-video-1.5-fast:reverse' (default, fast 6-30s), 'grok-imagine-video:reverse' (standard 1-15s), and 'grok-imagine-video:official' (official, higher fidelity). Do NOT use 'grok-imagine-video-1.5:official' here — it is image-to-video only."
        ),
    ] = DEFAULT_MODEL,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. '16:9' for landscape/widescreen, '9:16' for portrait/vertical, '1:1' for square, plus '4:3', '3:4', '3:2', '2:3'."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    resolution: Annotated[
        VideoResolution,
        Field(
            description="Output resolution. '480p' (default, cheaper), '720p', or '1080p'. Higher resolution costs more per second on the per-second-priced models."
        ),
    ] = DEFAULT_RESOLUTION,
    duration: Annotated[
        int,
        Field(
            ge=1,
            le=30,
            description="Video duration in seconds (default 6). 'grok-imagine-video-1.5-fast:reverse' supports 6-30; every other model supports 1-15.",
        ),
    ] = DEFAULT_DURATION,
    callback_url: Annotated[
        str,
        Field(
            description="Optional URL to receive a POST callback when generation completes. The callback will include the task_id and video results."
        ),
    ] = "",
) -> str:
    """Generate AI video from a text prompt using Grok Imagine.

    This creates a video from scratch based on your text description. Grok
    Imagine will interpret your prompt and generate a matching video clip.

    Use this when:
    - You want to create a video from a text description
    - You don't have a reference image to use
    - You want maximum creative freedom

    Only the 'grok-imagine-video-1.5-fast:reverse', 'grok-imagine-video:reverse',
    and 'grok-imagine-video:official' models support text-to-video. For generating
    a video from a reference image, use grok_image_to_video instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "prompt": prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "duration": duration,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def grok_image_to_video(
    image_url: Annotated[
        str,
        Field(
            description="URL of the input image to animate into a video. Required for image-to-video generation."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Optional description of the motion/action to apply to the image. Examples: 'The camera slowly zooms in as the character smiles', 'Gentle wind moves the trees and clouds drift across the sky'. Optional when an image_url is provided."
        ),
    ] = "",
    model: Annotated[
        GrokVideoModel,
        Field(
            description="Grok Imagine model. All models support image-to-video. 'grok-imagine-video-1.5-fast:reverse' (default) is fastest and cheapest; 'grok-imagine-video-1.5:official' offers the highest fidelity (up to 1080p) and is image-to-video only."
        ),
    ] = DEFAULT_MODEL,
    reference_image_urls: Annotated[
        list[str] | None,
        Field(
            description="Optional list of additional reference image URLs used to guide the style or content of the generated video."
        ),
    ] = None,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. Should typically match your input image aspect ratio for best results."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    resolution: Annotated[
        VideoResolution,
        Field(
            description="Output resolution. '480p' (default, cheaper), '720p', or '1080p'. Higher resolution costs more per second on the per-second-priced models."
        ),
    ] = DEFAULT_RESOLUTION,
    duration: Annotated[
        int,
        Field(
            ge=1,
            le=30,
            description="Video duration in seconds (default 6). 'grok-imagine-video-1.5-fast:reverse' supports 6-30; every other model supports 1-15.",
        ),
    ] = DEFAULT_DURATION,
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when generation completes."),
    ] = "",
) -> str:
    """Generate AI video from a reference image using Grok Imagine.

    This animates your input image into a video clip. Provide a prompt to
    describe the motion you want, and optional reference images to guide style.

    Use this when:
    - You have a specific image you want to animate
    - You want consistent visual style from a reference
    - You want to turn a still photo into a short video

    For video generation from text only, use grok_text_to_video instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "image_url": image_url,
        "model": model,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "duration": duration,
    }

    if prompt:
        payload["prompt"] = prompt
    if reference_image_urls:
        payload["reference_image_urls"] = reference_image_urls
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
