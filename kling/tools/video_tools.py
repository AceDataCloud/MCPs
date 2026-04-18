"""Video generation tools for Kling API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_ASPECT_RATIO,
    DEFAULT_DURATION,
    DEFAULT_MODE,
    DEFAULT_MODEL,
    AspectRatio,
    Duration,
    KlingModel,
    Mode,
)
from core.utils import format_video_result


@mcp.tool()
async def kling_generate_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about the scene, motion, style, and mood. Examples: 'A cat walking through a garden with butterflies', 'Astronauts shuttle from space to volcano', 'Ocean waves crashing on a beach at sunset'"
        ),
    ],
    model: Annotated[
        KlingModel,
        Field(
            description="Kling model to use. Options: 'kling-v1', 'kling-v1-6', 'kling-v2-master' (default), 'kling-v2-1-master', 'kling-v2-5-turbo', 'kling-v2-6', 'kling-v3', 'kling-v3-omni', 'kling-video-o1'."
        ),
    ] = DEFAULT_MODEL,
    mode: Annotated[
        Mode,
        Field(
            description="Generation mode. 'std' (standard, default) for faster generation, 'pro' for higher quality."
        ),
    ] = DEFAULT_MODE,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. Options: '16:9' (landscape, default), '9:16' (portrait), '1:1' (square)."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    duration: Annotated[
        Duration,
        Field(
            description="Video duration in seconds. For kling-v3/kling-v3-omni: 3-15 (integer). Other models: 5 or 10."
        ),
    ] = DEFAULT_DURATION,
    generate_audio: Annotated[
        bool,
        Field(
            description="Whether to generate audio synchronously. Supported by kling-v3, kling-v3-omni, and kling-v2-6 (pro mode only). Default is false."
        ),
    ] = False,
    negative_prompt: Annotated[
        str | None,
        Field(
            description="Things to avoid in the video. Example: 'blurry, low quality, distorted faces'"
        ),
    ] = None,
    cfg_scale: Annotated[
        float | None,
        Field(
            description="Classifier-free guidance scale. Higher values follow the prompt more strictly. Typical range: 0.0-1.0."
        ),
    ] = None,
    camera_control: Annotated[
        str | None,
        Field(
            description='Camera control as JSON string. Example: \'{"type": "simple", "config": {"horizontal": 5, "vertical": 0, "pan": 0, "tilt": 0, "roll": 0, "zoom": 0}}\'. Types: \'simple\', \'down_back\', \'forward_up\', \'left_turn_forward\', \'right_turn_forward\'.'
        ),
    ] = None,
    timeout: Annotated[
        int | None,
        Field(description="Timeout in seconds for the API to return data. Default is 300."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the video is generated."
        ),
    ] = None,
) -> str:
    """Generate AI video from a text prompt using Kling.

    This is the simplest way to create video - just describe what you want and Kling
    will generate a high-quality AI video.

    Use this when:
    - You want to create a video from a text description
    - You don't have reference images
    - You want quick video generation

    For using reference images (start/end frames), use kling_generate_video_from_image instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "action": "text2video",
        "model": model,
        "prompt": prompt,
        "mode": mode,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
        "timeout": timeout,
        "callback_url": callback_url,
    }

    if generate_audio:
        payload["generate_audio"] = True
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if cfg_scale is not None:
        payload["cfg_scale"] = cfg_scale
    if camera_control:
        payload["camera_control"] = camera_control

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def kling_generate_video_from_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video motion and content. Describe what should happen in the video, how objects should move, what transitions to include."
        ),
    ],
    start_image_url: Annotated[
        str,
        Field(
            description="URL of the image to use as the first frame of the video. The video will animate from this image."
        ),
    ] = "",
    end_image_url: Annotated[
        str,
        Field(
            description="URL of the image to use as the last frame of the video. The video will animate towards this image."
        ),
    ] = "",
    model: Annotated[
        KlingModel,
        Field(description="Kling model to use. Default: 'kling-v2-master'."),
    ] = DEFAULT_MODEL,
    mode: Annotated[
        Mode,
        Field(description="Generation mode. 'std' (standard, default) or 'pro' (higher quality)."),
    ] = DEFAULT_MODE,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(description="Video aspect ratio. Usually should match your input image ratio."),
    ] = DEFAULT_ASPECT_RATIO,
    duration: Annotated[
        Duration,
        Field(
            description="Video duration in seconds. For kling-v3/kling-v3-omni: 3-15 (integer). Other models: 5 or 10."
        ),
    ] = DEFAULT_DURATION,
    generate_audio: Annotated[
        bool,
        Field(
            description="Whether to generate audio synchronously. Supported by kling-v3, kling-v3-omni, and kling-v2-6 (pro mode only)."
        ),
    ] = False,
    negative_prompt: Annotated[
        str | None,
        Field(description="Things to avoid in the video."),
    ] = None,
    cfg_scale: Annotated[
        float | None,
        Field(
            description="Classifier-free guidance scale. Higher values follow the prompt more strictly."
        ),
    ] = None,
    camera_control: Annotated[
        str | None,
        Field(description="Camera control as JSON string."),
    ] = None,
    timeout: Annotated[
        int | None,
        Field(description="Timeout in seconds for the API to return data. Default is 300."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Generate AI video using reference images as start and/or end frames.

    This allows you to control the video by specifying what the first frame
    and/or last frame should look like. Kling will generate smooth motion between them.

    Use this when:
    - You have a specific image you want to animate
    - You want to create a video transition between two images
    - You need precise control over the video's visual content

    At least one of start_image_url or end_image_url must be provided.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    if not start_image_url and not end_image_url:
        return "Error: At least one of start_image_url or end_image_url must be provided."

    payload: dict = {
        "action": "image2video",
        "model": model,
        "prompt": prompt,
        "mode": mode,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
        "timeout": timeout,
        "callback_url": callback_url,
    }

    if start_image_url:
        payload["start_image_url"] = start_image_url
    if end_image_url:
        payload["end_image_url"] = end_image_url
    if generate_audio:
        payload["generate_audio"] = True
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if cfg_scale is not None:
        payload["cfg_scale"] = cfg_scale
    if camera_control:
        payload["camera_control"] = camera_control

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def kling_extend_video(
    video_id: Annotated[
        str,
        Field(
            description="ID of the video to extend. This is the 'video_id' field from a previous generation result."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of what should happen in the extended portion of the video. Describe the continuation of motion and new content."
        ),
    ],
    model: Annotated[
        KlingModel,
        Field(description="Kling model to use. Default: 'kling-v2-master'."),
    ] = DEFAULT_MODEL,
    mode: Annotated[
        Mode,
        Field(description="Generation mode. 'std' (standard, default) or 'pro' (higher quality)."),
    ] = DEFAULT_MODE,
    negative_prompt: Annotated[
        str | None,
        Field(description="Things to avoid in the extended video."),
    ] = None,
    cfg_scale: Annotated[
        float | None,
        Field(description="Classifier-free guidance scale."),
    ] = None,
) -> str:
    """Extend an existing video with additional content.

    This allows you to continue a previously generated video, adding more motion
    and content after the original video ends.

    Use this when:
    - A generated video is too short and you want to add more
    - You want to continue the story or motion from a previous video
    - You're building a longer video piece by piece

    Returns:
        Task ID and the extended video information.
    """
    payload: dict = {
        "action": "extend",
        "video_id": video_id,
        "prompt": prompt,
        "model": model,
        "mode": mode,
    }

    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if cfg_scale is not None:
        payload["cfg_scale"] = cfg_scale

    result = await client.generate_video(**payload)
    return format_video_result(result)
