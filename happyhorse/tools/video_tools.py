"""Video generation and editing tools for Happy Horse."""

from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_DURATION,
    DEFAULT_IMAGE_TO_VIDEO_MODEL,
    DEFAULT_RATIO,
    DEFAULT_REFERENCE_TO_VIDEO_MODEL,
    DEFAULT_RESOLUTION,
    DEFAULT_TEXT_TO_VIDEO_MODEL,
    DEFAULT_VIDEO_EDIT_MODEL,
    MAX_DURATION,
    MAX_EDIT_REFERENCE_IMAGES,
    MAX_REFERENCE_IMAGES,
    MAX_SEED,
    MIN_DURATION,
    AspectRatio,
    AudioSetting,
    ImageToVideoModel,
    ReferenceToVideoModel,
    Resolution,
    TextToVideoModel,
    VideoEditModel,
)
from core.utils import format_video_result


def _generation_options(
    resolution: Resolution,
    duration: int,
    watermark: bool,
    seed: int | None,
    callback_url: str | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "resolution": resolution,
        "duration": duration,
        "watermark": watermark,
    }
    if seed is not None:
        payload["seed"] = seed
    if callback_url:
        payload["callback_url"] = callback_url
    return payload


@mcp.tool()
async def happyhorse_generate_video(
    prompt: Annotated[
        str,
        Field(
            description=(
                "Detailed text-to-video prompt describing subject, motion, camera, lighting, "
                "style, and mood."
            ),
            min_length=1,
        ),
    ],
    model: Annotated[
        TextToVideoModel,
        Field(description="Text-to-video model: happyhorse-1.0-t2v or happyhorse-1.1-t2v."),
    ] = DEFAULT_TEXT_TO_VIDEO_MODEL,
    resolution: Annotated[
        Resolution,
        Field(description="Output resolution: 720P or 1080P."),
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[
        AspectRatio,
        Field(description="Output aspect ratio: 16:9, 9:16, 1:1, 4:3, or 3:4."),
    ] = DEFAULT_RATIO,
    duration: Annotated[
        int,
        Field(
            description="Output duration in seconds, from 3 through 15.",
            ge=MIN_DURATION,
            le=MAX_DURATION,
        ),
    ] = DEFAULT_DURATION,
    watermark: Annotated[
        bool,
        Field(description="Whether to add a Happy Horse watermark."),
    ] = False,
    seed: Annotated[
        int | None,
        Field(description="Optional reproducibility seed.", ge=0, le=MAX_SEED),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL. Omit it to receive a task ID for polling."),
    ] = None,
) -> str:
    """Generate a video from a text prompt with Happy Horse."""
    payload = {
        "action": "generate",
        "model": model,
        "prompt": prompt,
        "ratio": ratio,
        **_generation_options(resolution, duration, watermark, seed, callback_url),
    }
    return format_video_result(await client.generate_video(payload))


@mcp.tool()
async def happyhorse_generate_video_from_image(
    image_url: Annotated[
        str,
        Field(description="Public URL of the image to use as the first frame.", min_length=1),
    ],
    prompt: Annotated[
        str | None,
        Field(description="Optional motion and camera instructions for animating the image."),
    ] = None,
    model: Annotated[
        ImageToVideoModel,
        Field(description="Image-to-video model: happyhorse-1.0-i2v or happyhorse-1.1-i2v."),
    ] = DEFAULT_IMAGE_TO_VIDEO_MODEL,
    resolution: Annotated[
        Resolution,
        Field(description="Output resolution: 720P or 1080P."),
    ] = DEFAULT_RESOLUTION,
    duration: Annotated[
        int,
        Field(
            description="Output duration in seconds, from 3 through 15.",
            ge=MIN_DURATION,
            le=MAX_DURATION,
        ),
    ] = DEFAULT_DURATION,
    watermark: Annotated[
        bool,
        Field(description="Whether to add a Happy Horse watermark."),
    ] = False,
    seed: Annotated[
        int | None,
        Field(description="Optional reproducibility seed.", ge=0, le=MAX_SEED),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL. Omit it to receive a task ID for polling."),
    ] = None,
) -> str:
    """Animate a first-frame image with Happy Horse."""
    payload = {
        "action": "image_to_video",
        "model": model,
        "image_url": image_url,
        "prompt": prompt,
        **_generation_options(resolution, duration, watermark, seed, callback_url),
    }
    return format_video_result(await client.generate_video(payload))


@mcp.tool()
async def happyhorse_generate_video_from_references(
    prompt: Annotated[
        str,
        Field(
            description=(
                "Video prompt. Refer to supplied images as character1, character2, and so on "
                "in list order."
            ),
            min_length=1,
        ),
    ],
    image_urls: Annotated[
        list[str],
        Field(
            description="One to nine public reference image URLs.",
            min_length=1,
            max_length=MAX_REFERENCE_IMAGES,
        ),
    ],
    model: Annotated[
        ReferenceToVideoModel,
        Field(description="Reference model: happyhorse-1.0-r2v or happyhorse-1.1-r2v."),
    ] = DEFAULT_REFERENCE_TO_VIDEO_MODEL,
    resolution: Annotated[
        Resolution,
        Field(description="Output resolution: 720P or 1080P."),
    ] = DEFAULT_RESOLUTION,
    ratio: Annotated[
        AspectRatio,
        Field(description="Output aspect ratio: 16:9, 9:16, 1:1, 4:3, or 3:4."),
    ] = DEFAULT_RATIO,
    duration: Annotated[
        int,
        Field(
            description="Output duration in seconds, from 3 through 15.",
            ge=MIN_DURATION,
            le=MAX_DURATION,
        ),
    ] = DEFAULT_DURATION,
    watermark: Annotated[
        bool,
        Field(description="Whether to add a Happy Horse watermark."),
    ] = False,
    seed: Annotated[
        int | None,
        Field(description="Optional reproducibility seed.", ge=0, le=MAX_SEED),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL. Omit it to receive a task ID for polling."),
    ] = None,
) -> str:
    """Generate a video guided by one or more reference images."""
    if not 1 <= len(image_urls) <= MAX_REFERENCE_IMAGES:
        return f"Error: image_urls must contain between 1 and {MAX_REFERENCE_IMAGES} URLs."
    payload = {
        "action": "reference_to_video",
        "model": model,
        "prompt": prompt,
        "image_urls": image_urls,
        "ratio": ratio,
        **_generation_options(resolution, duration, watermark, seed, callback_url),
    }
    return format_video_result(await client.generate_video(payload))


@mcp.tool()
async def happyhorse_edit_video(
    prompt: Annotated[
        str,
        Field(description="Instructions describing the desired changes.", min_length=1),
    ],
    video_url: Annotated[
        str,
        Field(description="Public URL of the source video to edit.", min_length=1),
    ],
    image_urls: Annotated[
        list[str] | None,
        Field(
            description="Optional style or subject reference images, up to five.",
            max_length=MAX_EDIT_REFERENCE_IMAGES,
        ),
    ] = None,
    model: Annotated[
        VideoEditModel,
        Field(description="Video-edit model. Currently happyhorse-1.0-video-edit."),
    ] = DEFAULT_VIDEO_EDIT_MODEL,
    resolution: Annotated[
        Resolution,
        Field(description="Output resolution: 720P or 1080P."),
    ] = DEFAULT_RESOLUTION,
    audio_setting: Annotated[
        AudioSetting,
        Field(description="Audio policy: auto, or origin to preserve the source audio."),
    ] = "auto",
    watermark: Annotated[
        bool,
        Field(description="Whether to add a Happy Horse watermark."),
    ] = False,
    seed: Annotated[
        int | None,
        Field(description="Optional reproducibility seed.", ge=0, le=MAX_SEED),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Optional webhook URL. Omit it to receive a task ID for polling."),
    ] = None,
) -> str:
    """Edit a source video using text and optional reference images."""
    if image_urls is not None and len(image_urls) > MAX_EDIT_REFERENCE_IMAGES:
        return f"Error: image_urls supports at most {MAX_EDIT_REFERENCE_IMAGES} references."
    payload: dict[str, Any] = {
        "action": "video_edit",
        "model": model,
        "prompt": prompt,
        "video_url": video_url,
        "resolution": resolution,
        "audio_setting": audio_setting,
        "watermark": watermark,
    }
    if image_urls:
        payload["image_urls"] = image_urls
    if seed is not None:
        payload["seed"] = seed
    if callback_url:
        payload["callback_url"] = callback_url
    return format_video_result(await client.generate_video(payload))
