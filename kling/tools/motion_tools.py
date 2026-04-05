"""Motion transfer tools for Kling API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import CharacterOrientation, Mode
from core.utils import format_motion_result


@mcp.tool()
async def kling_generate_motion(
    image_url: Annotated[
        str,
        Field(
            description="URL of the character image to animate. The character in this image will be animated with the motion from the reference video."
        ),
    ],
    video_url: Annotated[
        str,
        Field(
            description="URL of the reference video providing the motion. The character movements from this video will be transferred to the image."
        ),
    ],
    character_orientation: Annotated[
        CharacterOrientation,
        Field(
            description="Orientation of the character. 'image' (default) uses the orientation from the character image, 'video' uses the orientation from the reference video."
        ),
    ] = "image",
    mode: Annotated[
        Mode,
        Field(
            description="Generation mode. 'std' (standard, default) for faster generation, 'pro' for higher quality."
        ),
    ] = "std",
    prompt: Annotated[
        str | None,
        Field(
            description="Optional text description to guide the motion transfer. Use to add details about the desired output."
        ),
    ] = None,
    keep_original_sound: Annotated[
        str | None,
        Field(
            description="Whether to keep the original sound from the reference video. Options: 'yes' or 'no'. Default depends on API."
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications."
        ),
    ] = None,
) -> str:
    """Transfer motion from a reference video to a character image.

    This tool enables character animation by extracting motion from a video
    and applying it to a static character image.

    Use this when:
    - You want to animate a character image using motion from a video
    - You want to create a dance or movement video from a still photo
    - You need to transfer specific movements to a character

    Returns:
        Task ID and motion generation information.
    """
    payload: dict = {
        "image_url": image_url,
        "video_url": video_url,
        "character_orientation": character_orientation,
        "mode": mode,
        "callback_url": callback_url,
    }

    if prompt:
        payload["prompt"] = prompt
    if keep_original_sound:
        payload["keep_original_sound"] = keep_original_sound

    result = await client.generate_motion(**payload)
    return format_motion_result(result)
