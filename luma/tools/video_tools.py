"""Video generation tools for Luma API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_ASPECT_RATIO, AspectRatio
from core.utils import format_video_result


@mcp.tool()
async def luma_generate_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about the scene, motion, style, and mood. Examples: 'A cat walking through a garden with butterflies', 'Astronauts shuttle from space to volcano', 'Ocean waves crashing on a beach at sunset'"
        ),
    ],
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. Options: '16:9' (landscape, default), '9:16' (portrait), '1:1' (square), '4:3', '3:4', '21:9' (ultrawide), '9:21'."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    loop: Annotated[
        bool,
        Field(
            description="If true, generate a looping video where end connects seamlessly to start. Default is false."
        ),
    ] = False,
    enhancement: Annotated[
        bool,
        Field(description="If true, enable clarity enhancement for the video. Default is true."),
    ] = True,
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
    """Generate AI video from a text prompt using Luma Dream Machine.

    This is the simplest way to create video - just describe what you want and Luma
    will generate a high-quality AI video.

    Use this when:
    - You want to create a video from a text description
    - You don't have reference images
    - You want quick video generation

    For using reference images (start/end frames), use luma_generate_video_from_image instead.

    Returns:
        Task ID and generated video information including URLs, dimensions, and thumbnail.
    """
    result = await client.generate_video(
        action="generate",
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        loop=loop,
        enhancement=enhancement,
        timeout=timeout,
        callback_url=callback_url,
    )
    return format_video_result(result)


@mcp.tool()
async def luma_generate_video_from_image(
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
    aspect_ratio: Annotated[
        AspectRatio,
        Field(description="Video aspect ratio. Usually should match your input image ratio."),
    ] = DEFAULT_ASPECT_RATIO,
    loop: Annotated[
        bool,
        Field(description="If true, generate a looping video. Default is false."),
    ] = False,
    enhancement: Annotated[
        bool,
        Field(description="If true, enable clarity enhancement. Default is true."),
    ] = True,
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
    """Generate AI video using reference images as start and/or end frames.

    This allows you to control the video by specifying what the first frame
    and/or last frame should look like. Luma will generate smooth motion between them.

    Use this when:
    - You have a specific image you want to animate
    - You want to create a video transition between two images
    - You need precise control over the video's visual content

    At least one of start_image_url or end_image_url must be provided.

    Returns:
        Task ID and generated video information including URLs, dimensions, and thumbnail.
    """
    if not start_image_url and not end_image_url:
        return "Error: At least one of start_image_url or end_image_url must be provided."

    payload = {
        "action": "generate",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "loop": loop,
        "enhancement": enhancement,
        "timeout": timeout,
        "callback_url": callback_url,
    }

    if start_image_url:
        payload["start_image_url"] = start_image_url
    if end_image_url:
        payload["end_image_url"] = end_image_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def luma_extend_video(
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
    end_image_url: Annotated[
        str,
        Field(
            description="Optional URL of an image to use as the final frame of the extended video."
        ),
    ] = "",
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
    payload = {
        "action": "extend",
        "video_id": video_id,
        "prompt": prompt,
    }

    if end_image_url:
        payload["end_image_url"] = end_image_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def luma_extend_video_from_url(
    video_url: Annotated[
        str,
        Field(
            description="URL of the video to extend. Must be a valid video URL from a previous Luma generation."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of what should happen in the extended portion of the video."
        ),
    ],
    end_image_url: Annotated[
        str,
        Field(
            description="Optional URL of an image to use as the final frame of the extended video."
        ),
    ] = "",
) -> str:
    """Extend an existing video using its URL.

    Similar to luma_extend_video, but uses the video URL instead of video ID.
    This is useful when you have the video URL but not the original video ID.

    Use this when:
    - You have the video URL from a previous generation
    - You want to extend a video but don't have the video_id

    Returns:
        Task ID and the extended video information.
    """
    payload = {
        "action": "extend",
        "video_url": video_url,
        "prompt": prompt,
    }

    if end_image_url:
        payload["end_image_url"] = end_image_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
