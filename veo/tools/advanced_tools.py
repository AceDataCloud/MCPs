"""Advanced video manipulation tools for Veo API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import CameraMotionType, ObjectAction, UpsampleAction, VeoExtendModel
from core.utils import format_video_result


@mcp.tool()
async def veo_upsample(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result. This is the 'id' field from the video data, not the task_id."
        ),
    ],
    action: Annotated[
        UpsampleAction,
        Field(
            description="The upsample action. '1080p' upscales to 1080p resolution, '4k' upscales to 4K resolution, 'gif' converts to animated GIF format."
        ),
    ] = "1080p",
    callback_url: Annotated[
        str,
        Field(
            description="Optional URL to receive a POST callback when upsampling completes."
        ),
    ] = "",
) -> str:
    """Upsample a generated video to a higher resolution or convert to GIF.

    Use the /veo/upsample endpoint to convert a completed video to a higher
    resolution or a different format.

    Use this when:
    - You need a 4K version of a video (use action='4k')
    - You need a 1080p HD version (use action='1080p')
    - You want an animated GIF (use action='gif')

    Note: The video must be in 'succeeded' state before requesting an upsample.

    Returns:
        Task ID and upsampled video information including the new video URL.
    """
    payload: dict = {
        "action": action,
        "video_id": video_id,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.upsample(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_extend_video(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previously generated video. The source video must be in 'succeeded' state."
        ),
    ],
    model: Annotated[
        VeoExtendModel,
        Field(
            description="The model used to extend the video. Only Veo 3.1 series models are supported: 'veo31-fast' or 'veo31'."
        ),
    ] = "veo31-fast",
    prompt: Annotated[
        str,
        Field(
            description="Optional prompt that guides the extended section of the video."
        ),
    ] = "",
    callback_url: Annotated[
        str,
        Field(
            description="Optional URL to receive a POST callback when extension completes."
        ),
    ] = "",
) -> str:
    """Extend a previously generated video by adding more content at the end.

    Uses the Veo 3.1 series models to seamlessly continue a video clip.
    The extended portion will follow the visual style and motion of the original.

    Use this when:
    - You want to make an existing video longer
    - You need to continue the action or motion from a generated clip
    - You want to add additional scenes while preserving visual continuity

    Returns:
        Task ID and extended video information including the new video URL.
    """
    payload: dict = {
        "video_id": video_id,
        "model": model,
    }

    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.extend_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_reshoot_video(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previously generated video. Videos produced by veo2 or newer models are supported."
        ),
    ],
    motion_type: Annotated[
        CameraMotionType,
        Field(
            description=(
                "The camera motion to apply when re-rendering the video. "
                "STATIONARY: Fixed camera. "
                "STATIONARY_UP/DOWN/LEFT/RIGHT: Tilt/pan with stationary subject. "
                "STATIONARY_DOLLY_IN_ZOOM_OUT / STATIONARY_DOLLY_OUT_ZOOM_IN: Dolly zoom effects. "
                "UP/DOWN: Camera moves vertically. "
                "LEFT_TO_RIGHT / RIGHT_TO_LEFT: Horizontal tracking shot. "
                "FORWARD/BACKWARD: Camera moves towards or away from subject. "
                "DOLLY_IN_ZOOM_OUT / DOLLY_OUT_ZOOM_IN: Dynamic dolly zoom."
            )
        ),
    ],
    callback_url: Annotated[
        str,
        Field(
            description="Optional URL to receive a POST callback when reshoot completes."
        ),
    ] = "",
) -> str:
    """Re-render a video with a different camera motion.

    Takes an existing generated video and re-renders it with a specified
    camera movement applied, while keeping the subject and scene consistent.

    Use this when:
    - You want to add dynamic camera movement to a static video
    - You need a different cinematic perspective of an existing video
    - You want to create multiple camera angle variations of the same scene

    Returns:
        Task ID and reshooted video information including the new video URL.
    """
    payload: dict = {
        "video_id": video_id,
        "motion_type": motion_type,
    }

    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.reshoot_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_manipulate_objects(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previously generated video. Videos produced by veo2 or newer models are supported."
        ),
    ],
    action: Annotated[
        ObjectAction,
        Field(
            description="'insert' adds an object to the video; 'remove' deletes an object from it."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="For action='insert': describes what object to add (required). For action='remove': describes the object to remove (optional)."
        ),
    ] = "",
    image_mask: Annotated[
        str,
        Field(
            description="URL of a mask image where white pixels indicate the region to operate on. Required for 'insert'; specifies the region for 'remove'."
        ),
    ] = "",
    callback_url: Annotated[
        str,
        Field(
            description="Optional URL to receive a POST callback when the operation completes."
        ),
    ] = "",
) -> str:
    """Insert or remove objects in a generated video.

    Performs AI-powered object manipulation on an existing generated video.
    Use a mask image to specify the region where the operation should be applied.

    Use this when:
    - You want to add a new object to a specific area of a video (action='insert')
    - You want to remove an unwanted object from a video (action='remove')
    - You need precise control over where in the frame the change occurs

    Returns:
        Task ID and modified video information including the new video URL.
    """
    payload: dict = {
        "action": action,
        "video_id": video_id,
    }

    if prompt:
        payload["prompt"] = prompt
    if image_mask:
        payload["image_mask"] = image_mask
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.manipulate_objects(**payload)
    return format_video_result(result)
