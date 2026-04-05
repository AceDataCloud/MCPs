"""Video generation tools for Wan API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_RESOLUTION, Duration, Resolution, ShotType
from core.utils import format_video_result


@mcp.tool()
async def wan_generate_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about the scene, motion, style, and mood."
        ),
    ],
    negative_prompt: Annotated[
        str,
        Field(description="Content to exclude from the video. Maximum 500 characters."),
    ] = "",
    duration: Annotated[
        Duration | None,
        Field(
            description="Video duration in seconds. Options: 5, 10, or 15. Default depends on model."
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
    timeout: Annotated[
        int | None,
        Field(description="Timeout in seconds for the API to return data. Default is 1800."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the video is generated."
        ),
    ] = None,
) -> str:
    """Generate AI video from a text prompt using Wan text-to-video model.

    This uses the wan2.6-t2v model to create video from text descriptions.
    For creating video from images, use wan_generate_video_from_image instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "action": "text2video",
        "model": "wan2.6-t2v",
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
    if timeout is not None:
        payload["timeout"] = timeout
    if callback_url:
        payload["callback_url"] = callback_url

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
        str,
        Field(
            description="Model to use. Options: 'wan2.6-i2v' (standard image-to-video), 'wan2.6-r2v' (reference video-to-video), 'wan2.6-i2v-flash' (fast image-to-video). Default: 'wan2.6-i2v'."
        ),
    ] = "wan2.6-i2v",
    negative_prompt: Annotated[
        str,
        Field(description="Content to exclude from the video. Maximum 500 characters."),
    ] = "",
    duration: Annotated[
        Duration | None,
        Field(description="Video duration in seconds. Options: 5, 10, or 15."),
    ] = None,
    resolution: Annotated[
        Resolution,
        Field(description="Video resolution. Options: '480P', '720P' (default), '1080P'."),
    ] = DEFAULT_RESOLUTION,
    reference_video_urls: Annotated[
        str | None,
        Field(
            description="Comma-separated URLs of reference videos for character/timbre extraction. Used with wan2.6-r2v model."
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
    timeout: Annotated[
        int | None,
        Field(description="Timeout in seconds. Default is 1800."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
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
        payload["reference_video_urls"] = [url.strip() for url in reference_video_urls.split(",")]
    if shot_type is not None:
        payload["shot_type"] = shot_type
    if audio_url:
        payload["audio_url"] = audio_url
    if timeout is not None:
        payload["timeout"] = timeout
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
