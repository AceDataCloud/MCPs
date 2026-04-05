"""Video generation tools for Hailuo API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, HailuoModel
from core.utils import format_video_result


@mcp.tool()
async def hailuo_generate_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about the scene, motion, style, and mood. Examples: 'A cat walking through a garden with butterflies', 'Ocean waves crashing on a beach at sunset', 'A futuristic city with flying cars'"
        ),
    ],
    model: Annotated[
        HailuoModel,
        Field(
            description="Video generation model. Options: 'minimax-t2v' (text-to-video, default), 'minimax-i2v' (image-to-video, requires first_image_url), 'minimax-i2v-director' (director-mode image-to-video, requires first_image_url)."
        ),
    ] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the video is generated."
        ),
    ] = None,
) -> str:
    """Generate AI video from a text prompt using Hailuo (MiniMax).

    This is the simplest way to create video - just describe what you want and Hailuo
    will generate a high-quality AI video.

    Use this when:
    - You want to create a video from a text description
    - You don't have reference images
    - You want quick text-to-video generation

    For using a reference image, use hailuo_generate_video_from_image instead.

    Returns:
        Task ID and generated video information including URLs and status.
    """
    payload: dict = {
        "action": "generate",
        "prompt": prompt,
        "model": model,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def hailuo_generate_video_from_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video motion and content. Describe what should happen in the video, how objects should move, what transitions to include."
        ),
    ],
    first_image_url: Annotated[
        str,
        Field(
            description="URL of the reference image for image-to-video generation. The video will be generated based on this image. Required for minimax-i2v and minimax-i2v-director models."
        ),
    ],
    model: Annotated[
        HailuoModel,
        Field(
            description="Video generation model. Options: 'minimax-i2v' (image-to-video, default for this tool), 'minimax-i2v-director' (director-mode image-to-video with more creative control)."
        ),
    ] = "minimax-i2v",
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the video is generated."
        ),
    ] = None,
) -> str:
    """Generate AI video from a reference image using Hailuo (MiniMax).

    This allows you to create a video based on a reference image. Hailuo will
    animate the image content according to your text prompt.

    Use this when:
    - You have a specific image you want to animate
    - You want to create a video based on visual content
    - You need image-to-video generation

    The first_image_url parameter is required for this tool.

    Returns:
        Task ID and generated video information including URLs and status.
    """
    payload: dict = {
        "action": "generate",
        "prompt": prompt,
        "model": model,
        "first_image_url": first_image_url,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
