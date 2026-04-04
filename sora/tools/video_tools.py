"""Video generation tools for Sora API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_DURATION,
    DEFAULT_MODEL,
    DEFAULT_ORIENTATION,
    DEFAULT_RESOLUTION,
    DEFAULT_SECONDS,
    DEFAULT_SIZE,
    SoraModel,
    VideoDuration,
    VideoOrientation,
    VideoResolution,
    VideoSeconds,
    VideoSize,
)
from core.utils import format_video_result


@mcp.tool()
async def sora_generate_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about the scene, action, style, and mood. Examples: 'A cat running on the river', 'A futuristic cityscape with flying cars at sunset', 'A person walking through a snowy forest'"
        ),
    ],
    model: Annotated[
        SoraModel,
        Field(
            description="Sora model version. 'sora-2' is the standard model. 'sora-2-pro' offers higher quality and supports 25-second videos."
        ),
    ] = DEFAULT_MODEL,
    size: Annotated[
        VideoSize,
        Field(
            description="Video resolution. 'small' for lower resolution, 'large' for higher resolution."
        ),
    ] = DEFAULT_SIZE,
    duration: Annotated[
        VideoDuration,
        Field(
            description="Video duration in seconds. Options: 10, 15, or 25 (25 only available with sora-2-pro model)."
        ),
    ] = DEFAULT_DURATION,
    orientation: Annotated[
        VideoOrientation,
        Field(
            description="Video orientation. 'landscape' for horizontal (16:9), 'portrait' for vertical (9:16)."
        ),
    ] = DEFAULT_ORIENTATION,
) -> str:
    """Generate an AI video from a text prompt using Sora.

    This is the primary way to create videos - describe what you want and Sora
    will generate a video matching your description.

    Use this when:
    - You want to generate a video from a text description
    - You don't have reference images
    - You want creative AI-generated video content

    For image-to-video generation, use sora_generate_video_from_image instead.
    For character-based video generation, use sora_generate_video_with_character.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    # Validate duration for non-pro model
    if model == "sora-2" and duration == 25:
        return "Error: 25-second duration is only available with sora-2-pro model. Please use sora-2-pro or choose 10 or 15 seconds."

    result = await client.generate_video(
        prompt=prompt,
        model=model,
        size=size,
        duration=duration,
        orientation=orientation,
    )
    return format_video_result(result)


@mcp.tool()
async def sora_generate_video_from_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate based on the image. Describe the action or motion you want to see."
        ),
    ],
    image_urls: Annotated[
        list[str],
        Field(
            description="List of reference image URLs to use for video generation. Can be image URLs or Base64 encoded images."
        ),
    ],
    model: Annotated[
        SoraModel,
        Field(description="Sora model version. 'sora-2' or 'sora-2-pro' for higher quality."),
    ] = DEFAULT_MODEL,
    size: Annotated[
        VideoSize,
        Field(
            description="Video resolution. 'small' for lower resolution, 'large' for higher resolution."
        ),
    ] = DEFAULT_SIZE,
    duration: Annotated[
        VideoDuration,
        Field(
            description="Video duration in seconds. Options: 10, 15, or 25 (25 only for sora-2-pro)."
        ),
    ] = DEFAULT_DURATION,
    orientation: Annotated[
        VideoOrientation,
        Field(description="Video orientation. 'landscape', 'portrait'."),
    ] = DEFAULT_ORIENTATION,
) -> str:
    """Generate an AI video from reference images using Sora (Image-to-Video).

    This allows you to animate or create videos based on provided images.
    The AI will use the images as visual references for the generated video.

    Use this when:
    - You have reference images you want to animate
    - You want the video to match a specific visual style
    - You want to bring static images to life

    Returns:
        Task ID and generated video information including URLs and state.
    """
    # Validate duration for non-pro model
    if model == "sora-2" and duration == 25:
        return "Error: 25-second duration is only available with sora-2-pro model. Please use sora-2-pro or choose 10 or 15 seconds."

    result = await client.generate_video(
        prompt=prompt,
        image_urls=image_urls,
        model=model,
        size=size,
        duration=duration,
        orientation=orientation,
    )
    return format_video_result(result)


@mcp.tool()
async def sora_generate_video_with_character(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate featuring the character. Describe the scene and action."
        ),
    ],
    character_url: Annotated[
        str,
        Field(
            description="URL of the video containing the character to use. IMPORTANT: The video must NOT contain real people, only animated/digital characters."
        ),
    ],
    character_start: Annotated[
        float,
        Field(
            description="Start position of the character in the reference video (0-1 range). For example, 0.2 means the character appears at 20% from the start."
        ),
    ] = 0,
    character_end: Annotated[
        float,
        Field(
            description="End position of the character in the reference video (0-1 range). For example, 0.8 means the character ends at 80% of the video."
        ),
    ] = 1,
    model: Annotated[
        SoraModel,
        Field(description="Sora model version. 'sora-2' or 'sora-2-pro' for higher quality."),
    ] = DEFAULT_MODEL,
    size: Annotated[
        VideoSize,
        Field(
            description="Video resolution. 'small' for lower resolution, 'large' for higher resolution."
        ),
    ] = DEFAULT_SIZE,
    duration: Annotated[
        VideoDuration,
        Field(
            description="Video duration in seconds. Options: 10, 15, or 25 (25 only for sora-2-pro)."
        ),
    ] = DEFAULT_DURATION,
    orientation: Annotated[
        VideoOrientation,
        Field(description="Video orientation. 'landscape', 'portrait'."),
    ] = DEFAULT_ORIENTATION,
) -> str:
    """Generate an AI video featuring a character from a reference video.

    This allows you to create new videos featuring a specific character
    extracted from another video. The character will be placed in the
    new scene described by the prompt.

    IMPORTANT: The reference video must NOT contain real people.
    Only animated or digital characters are supported.

    Use this when:
    - You want to reuse a character in different scenes
    - You're creating a series with the same character
    - You want consistent character appearance across videos

    Returns:
        Task ID and generated video information including URLs and state.
    """
    # Validate duration for non-pro model
    if model == "sora-2" and duration == 25:
        return "Error: 25-second duration is only available with sora-2-pro model. Please use sora-2-pro or choose 10 or 15 seconds."

    result = await client.generate_video(
        prompt=prompt,
        character_url=character_url,
        character_start=character_start,
        character_end=character_end,
        model=model,
        size=size,
        duration=duration,
        orientation=orientation,
    )
    return format_video_result(result)


@mcp.tool()
async def sora_generate_video_async(
    prompt: Annotated[
        str,
        Field(description="Description of the video to generate."),
    ],
    callback_url: Annotated[
        str,
        Field(
            description="URL to receive the callback when video generation is complete. The result will be POSTed to this URL as JSON."
        ),
    ],
    model: Annotated[
        SoraModel,
        Field(description="Sora model version."),
    ] = DEFAULT_MODEL,
    size: Annotated[
        VideoSize,
        Field(description="Video resolution."),
    ] = DEFAULT_SIZE,
    duration: Annotated[
        VideoDuration,
        Field(description="Video duration in seconds."),
    ] = DEFAULT_DURATION,
    orientation: Annotated[
        VideoOrientation,
        Field(description="Video orientation."),
    ] = DEFAULT_ORIENTATION,
    image_urls: Annotated[
        list[str] | None,
        Field(description="Optional list of reference image URLs for image-to-video generation."),
    ] = None,
) -> str:
    """Generate an AI video asynchronously with callback notification.

    This is useful for long-running video generation tasks. Instead of waiting
    for the video to complete, you'll receive a callback at your specified URL
    when the generation is finished.

    Use this when:
    - You don't want to wait for the generation to complete
    - You have a webhook endpoint to receive results
    - You're integrating with an async workflow

    The callback will receive a POST request with the same response format
    as the synchronous generation tools.

    Returns:
        Task ID that you can use to correlate with the callback.
    """
    # Validate duration for non-pro model
    if model == "sora-2" and duration == 25:
        return "Error: 25-second duration is only available with sora-2-pro model."

    payload: dict = {
        "prompt": prompt,
        "callback_url": callback_url,
        "model": model,
        "size": size,
        "duration": duration,
        "orientation": orientation,
    }

    if image_urls:
        payload["image_urls"] = image_urls

    result = await client.generate_video(**payload)
    return format_video_result(result)


# === Version 2 Tools ===


@mcp.tool()
async def sora_generate_video_v2(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about the scene, action, style, and mood."
        ),
    ],
    model: Annotated[
        SoraModel,
        Field(
            description="Sora model version. 'sora-2' is standard, 'sora-2-pro' offers higher quality."
        ),
    ] = DEFAULT_MODEL,
    duration: Annotated[
        VideoSeconds,
        Field(description="Video duration in seconds. Options: 4, 8, or 12."),
    ] = DEFAULT_SECONDS,
    size: Annotated[
        VideoResolution,
        Field(
            description="Video resolution in pixels. Options: '720x1280' (vertical), '1280x720' (horizontal), '1024x1792' (tall vertical), '1792x1024' (wide horizontal)."
        ),
    ] = DEFAULT_RESOLUTION,
    image_urls: Annotated[
        list[str] | None,
        Field(
            description="Optional list of reference image URLs. Only the first image is used for version 2. Image dimensions should match the size parameter."
        ),
    ] = None,
) -> str:
    """Generate an AI video using Sora Version 2 (partner channel).

    Version 2 offers shorter video durations (4/8/12 seconds) with
    precise pixel-based resolution control. This is ideal for quick
    video generation with specific resolution requirements.

    Use this when:
    - You need precise pixel resolution control (e.g., 1280x720)
    - You want shorter videos (4, 8, or 12 seconds)
    - You want to use the partner channel for generation

    For longer videos (10-25 seconds) or character-based generation,
    use the version 1 tools (sora_generate_video, etc.) instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "prompt": prompt,
        "model": model,
        "version": 2,
        "duration": duration,
        "size": size,
    }

    if image_urls:
        payload["image_urls"] = image_urls

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def sora_generate_video_v2_async(
    prompt: Annotated[
        str,
        Field(description="Description of the video to generate."),
    ],
    callback_url: Annotated[
        str,
        Field(
            description="URL to receive the callback when video generation is complete. The result will be POSTed to this URL as JSON."
        ),
    ],
    model: Annotated[
        SoraModel,
        Field(description="Sora model version."),
    ] = DEFAULT_MODEL,
    duration: Annotated[
        VideoSeconds,
        Field(description="Video duration in seconds. Options: 4, 8, or 12."),
    ] = DEFAULT_SECONDS,
    size: Annotated[
        VideoResolution,
        Field(description="Video resolution in pixels."),
    ] = DEFAULT_RESOLUTION,
    image_urls: Annotated[
        list[str] | None,
        Field(description="Optional list of reference image URLs. Only the first image is used."),
    ] = None,
) -> str:
    """Generate an AI video asynchronously using Sora Version 2 with callback.

    Similar to sora_generate_video_v2 but returns immediately with a task ID.
    The result will be POSTed to your callback URL when generation completes.

    Use this when:
    - You don't want to wait for the generation to complete
    - You have a webhook endpoint to receive results
    - You're integrating with an async workflow

    Returns:
        Task ID that you can use to correlate with the callback.
    """
    payload: dict = {
        "prompt": prompt,
        "callback_url": callback_url,
        "model": model,
        "version": 2,
        "duration": duration,
        "size": size,
    }

    if image_urls:
        payload["image_urls"] = image_urls

    result = await client.generate_video(**payload)
    return format_video_result(result)
