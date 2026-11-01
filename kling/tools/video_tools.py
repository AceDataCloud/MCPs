"""Video generation tools for Kling API."""

from collections.abc import Sequence
from typing import Annotated

from pydantic import BaseModel, Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_ASPECT_RATIO,
    DEFAULT_DURATION,
    DEFAULT_MODE,
    DEFAULT_MODEL,
    AspectRatio,
    Duration,
    KlingCameraControl,
    KlingModel,
    KlingReferenceImage,
    KlingReferenceVideo,
    Mode,
)
from core.utils import format_video_result
from core.video_contract import validate_video_request as _validate_video_request


def _dump_models(items: Sequence[BaseModel] | None) -> list[dict] | None:
    if items is None:
        return None
    return [item.model_dump(mode="json", exclude_none=True) for item in items]


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
            description="Kling model to use. Options: 'kling-v1', 'kling-v1-6', 'kling-v2-master' (default), 'kling-v2-1-master', 'kling-v2-5-turbo', 'kling-v2-6', 'kling-v3', 'kling-v3-omni', 'kling-o1'."
        ),
    ] = DEFAULT_MODEL,
    mode: Annotated[
        Mode,
        Field(
            description="Generation mode. 'std' (standard, default) for faster generation, 'pro' for higher quality, '4k' for native 4K (only supported by kling-v3 and kling-v3-omni, not compatible with motion control)."
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
            description="Video duration in seconds. kling-v3/kling-v3-omni: 3-15; kling-o1: 5 only; other models: 5 or 10."
        ),
    ] = DEFAULT_DURATION,
    generate_audio: Annotated[
        bool | None,
        Field(
            description="Whether to generate audio synchronously. Supported by kling-v3, kling-v3-omni, and kling-v2-6 (pro mode only). Omit for the model default. Turbo always includes native audio."
        ),
    ] = None,
    negative_prompt: Annotated[
        str | None,
        Field(
            description="Things to avoid in the video. Example: 'blurry, low quality, distorted faces'"
        ),
    ] = None,
    cfg_scale: Annotated[
        float | None,
        Field(
            ge=0,
            le=1,
            description="Classifier-free guidance scale from 0 to 1. Not supported by Omni generation.",
        ),
    ] = None,
    camera_control: Annotated[
        KlingCameraControl | None,
        Field(description="Structured camera control. Not supported by Omni generation."),
    ] = None,
    image_list: Annotated[
        list[KlingReferenceImage] | None,
        Field(
            description="Omni reference images for kling-o1 or kling-v3-omni. Cite them as <<<image_1>>>, <<<image_2>>>, and so on."
        ),
    ] = None,
    video_list: Annotated[
        list[KlingReferenceVideo] | None,
        Field(
            description="One Omni reference video for kling-o1 or kling-v3-omni. Cite it as <<<video_1>>>. Use refer_type='feature' to reference it or 'base' (default) to edit it. Reference video pricing is separate: base bills actual output duration rounded to integer seconds; feature uses the requested duration. Read final billed seconds from usage.reference_video_seconds. Reference images alone do not trigger this tier; generate_audio must not be true."
        ),
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
    validation_error = _validate_video_request(
        model=model,
        mode=mode,
        duration=duration,
        generate_audio=generate_audio,
        negative_prompt=negative_prompt,
        cfg_scale=cfg_scale,
        camera_control=camera_control,
        image_list=image_list,
        video_list=video_list,
    )
    if validation_error:
        return validation_error

    payload: dict = {
        "action": "text2video",
        "model": model,
        "prompt": prompt,
        "mode": mode,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
    }

    if callback_url:
        payload["callback_url"] = callback_url
    if generate_audio is not None:
        payload["generate_audio"] = generate_audio
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if cfg_scale is not None:
        payload["cfg_scale"] = cfg_scale
    if camera_control:
        payload["camera_control"] = camera_control.model_dump(exclude_none=True)
    dumped_images = _dump_models(image_list)
    if dumped_images is not None:
        payload["image_list"] = dumped_images
    dumped_videos = _dump_models(video_list)
    if dumped_videos is not None:
        payload["video_list"] = dumped_videos

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
        Field(description="Required URL of the image to use as the first frame of the video."),
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
        Field(
            description="Generation mode. 'std' (standard, default), 'pro' (higher quality), or '4k' (native 4K, only for kling-v3 and kling-v3-omni)."
        ),
    ] = DEFAULT_MODE,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(description="Video aspect ratio. Usually should match your input image ratio."),
    ] = DEFAULT_ASPECT_RATIO,
    duration: Annotated[
        Duration,
        Field(
            description="Video duration in seconds. kling-v3/kling-v3-omni: 3-15; kling-o1: 5 only; other models: 5 or 10."
        ),
    ] = DEFAULT_DURATION,
    generate_audio: Annotated[
        bool | None,
        Field(
            description="Whether to generate audio synchronously. Supported by kling-v3, kling-v3-omni, and kling-v2-6 (pro mode only)."
        ),
    ] = None,
    negative_prompt: Annotated[
        str | None,
        Field(description="Things to avoid in the video."),
    ] = None,
    cfg_scale: Annotated[
        float | None,
        Field(
            ge=0,
            le=1,
            description="Classifier-free guidance scale from 0 to 1. Not supported by Omni generation.",
        ),
    ] = None,
    camera_control: Annotated[
        KlingCameraControl | None,
        Field(description="Structured camera control. Not supported by Omni generation."),
    ] = None,
    image_list: Annotated[
        list[KlingReferenceImage] | None,
        Field(
            description="Additional Omni reference images for kling-o1 or kling-v3-omni. Do not set type='first_frame' or 'end_frame' when the same frame is already supplied through start_image_url or end_image_url."
        ),
    ] = None,
    video_list: Annotated[
        list[KlingReferenceVideo] | None,
        Field(
            description="One Omni reference video for kling-o1 or kling-v3-omni. Reference video pricing is separate: base (default) bills actual output duration rounded to integer seconds; feature uses the requested duration. Read final billed seconds from usage.reference_video_seconds. Reference images alone do not trigger this tier; generate_audio must not be true."
        ),
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

    start_image_url is required. end_image_url is optional.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    if not start_image_url:
        return "Error: start_image_url is required for image-to-video generation."

    validation_error = _validate_video_request(
        model=model,
        mode=mode,
        duration=duration,
        generate_audio=generate_audio,
        negative_prompt=negative_prompt,
        cfg_scale=cfg_scale,
        camera_control=camera_control,
        image_list=image_list,
        video_list=video_list,
        start_image_url=start_image_url,
        end_image_url=end_image_url or None,
    )
    if validation_error:
        return validation_error

    payload: dict = {
        "action": "image2video",
        "model": model,
        "prompt": prompt,
        "mode": mode,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
    }

    if callback_url:
        payload["callback_url"] = callback_url
    if start_image_url:
        payload["start_image_url"] = start_image_url
    if end_image_url:
        payload["end_image_url"] = end_image_url
    if generate_audio is not None:
        payload["generate_audio"] = generate_audio
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if cfg_scale is not None:
        payload["cfg_scale"] = cfg_scale
    if camera_control:
        payload["camera_control"] = camera_control.model_dump(exclude_none=True)
    dumped_images = _dump_models(image_list)
    if dumped_images is not None:
        payload["image_list"] = dumped_images
    dumped_videos = _dump_models(video_list)
    if dumped_videos is not None:
        payload["video_list"] = dumped_videos

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
        Field(
            description="Generation mode. 'std' (standard, default), 'pro' (higher quality), or '4k' (native 4K, only for kling-v3 and kling-v3-omni)."
        ),
    ] = DEFAULT_MODE,
    duration: Annotated[
        Duration,
        Field(description="Duration of the extended segment in seconds. Supports 5 or 10."),
    ] = DEFAULT_DURATION,
    negative_prompt: Annotated[
        str | None,
        Field(description="Things to avoid in the extended video."),
    ] = None,
    cfg_scale: Annotated[
        float | None,
        Field(description="Classifier-free guidance scale."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL for asynchronous result notification."),
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
    if model == "kling-o1":
        return "Error: action=extend is not supported by kling-o1."
    if model in ("kling-v3", "kling-v3-omni"):
        if not 3 <= duration <= 15:
            return f"Error: {model} duration must be an integer from 3 to 15."
    elif duration not in (5, 10):
        return f"Error: {model} duration must be 5 or 10."
    if mode == "4k" and model not in ("kling-v3", "kling-v3-omni"):
        return f"Error: mode=4k is not supported by {model}."

    payload: dict = {
        "action": "extend",
        "video_id": video_id,
        "prompt": prompt,
        "model": model,
        "mode": mode,
        "duration": duration,
    }

    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if cfg_scale is not None:
        payload["cfg_scale"] = cfg_scale
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
