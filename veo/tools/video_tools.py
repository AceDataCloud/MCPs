"""Video generation tools for Veo API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_ASPECT_RATIO,
    DEFAULT_MODEL,
    AspectRatio,
    ExtendModel,
    MotionType,
    UpsampleAction,
    VeoModel,
    VideoResolution,
)
from core.utils import format_video_result


@mcp.tool()
async def veo_text_to_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Be descriptive about scene, subject, action, camera movement, lighting, and style. Examples: 'A white ceramic coffee mug on a glossy marble countertop, steam rising, soft morning light', 'Cinematic drone shot over a forest at sunset, golden hour lighting'"
        ),
    ],
    model: Annotated[
        VeoModel,
        Field(
            description="Veo model version. 'veo2' for quality mode, 'veo2-fast' for faster generation. 'veo3'/'veo31' offer improved quality. Models with '-fast' suffix are faster but slightly lower quality."
        ),
    ] = DEFAULT_MODEL,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. '16:9' for landscape/widescreen, '9:16' for portrait/vertical, '1:1' for square, '4:3' for standard, '3:4' for portrait standard."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    translation: Annotated[
        bool,
        Field(
            description="If true, automatically translate the prompt to English for better generation quality. Useful for non-English prompts."
        ),
    ] = False,
    resolution: Annotated[
        VideoResolution | None,
        Field(
            description="Video resolution. Options: '4k' for highest quality, '1080p' for standard HD, 'gif' for animated GIF format. If not specified, uses the model's default resolution."
        ),
    ] = None,
    callback_url: Annotated[
        str,
        Field(
            description="Optional URL to receive a POST callback when generation completes. The callback will include the task_id and video results."
        ),
    ] = "",
) -> str:
    """Generate AI video from a text prompt using Veo.

    This creates a video from scratch based on your text description. Veo
    will interpret your prompt and generate a matching video clip.

    Use this when:
    - You want to create a video from a text description
    - You don't have a reference image to use
    - You want maximum creative freedom for Veo

    For video generation starting from an image, use veo_image_to_video instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    payload: dict = {
        "action": "text2video",
        "prompt": prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
    }

    if translation:
        payload["translation"] = translation
    if resolution:
        payload["resolution"] = resolution
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_image_to_video(
    prompt: Annotated[
        str,
        Field(
            description="Description of the video motion and action. Describe what should happen to the subject in the image. Examples: 'The coffee steam rises gently', 'The person turns and smiles at the camera', 'Camera slowly zooms out revealing the landscape'"
        ),
    ],
    image_urls: Annotated[
        list[str],
        Field(
            description="List of image URLs to use as reference. For first-frame mode, provide 1 image. For first-last frame mode, provide 2-3 images. The first image is the starting frame, the last image is the ending frame. Maximum 3 images."
        ),
    ],
    model: Annotated[
        VeoModel,
        Field(
            description="Veo model version. Note: 'veo31-fast-ingredients' is for multi-image fusion mode only. Other models support 1 image (first frame) or 2-3 images (first/last frame)."
        ),
    ] = DEFAULT_MODEL,
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Video aspect ratio. Should typically match your input image aspect ratio for best results."
        ),
    ] = DEFAULT_ASPECT_RATIO,
    translation: Annotated[
        bool,
        Field(
            description="If true, automatically translate the prompt to English for better generation quality."
        ),
    ] = False,
    resolution: Annotated[
        VideoResolution | None,
        Field(
            description="Video resolution. Options: '4k' for highest quality, '1080p' for standard HD, 'gif' for animated GIF format."
        ),
    ] = None,
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when generation completes."),
    ] = "",
) -> str:
    """Generate AI video from one or more reference images using Veo.

    This creates a video using your image(s) as reference frames. The video
    will animate from/between your provided images according to the prompt.

    Image modes:
    - 1 image: First-frame mode - the video starts from your image
    - 2-3 images: First-last frame mode - video interpolates between images
    - veo31-fast-ingredients model: Multi-image fusion - blends elements from all images

    Use this when:
    - You have a specific image you want to animate
    - You want consistent visual style from a reference
    - You need to create a video transition between two images

    For video generation from text only, use veo_text_to_video instead.

    Returns:
        Task ID and generated video information including URLs and state.
    """
    action = "ingredients2video" if model == "veo31-fast-ingredients" else "image2video"
    payload: dict = {
        "action": action,
        "prompt": prompt,
        "image_urls": image_urls,
        "model": model,
        "aspect_ratio": aspect_ratio,
    }

    if translation:
        payload["translation"] = translation
    if resolution:
        payload["resolution"] = resolution
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_get_1080p(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result. This is the 'id' field from the video data, not the task_id."
        ),
    ],
) -> str:
    """Get the 1080p high-resolution version of a generated video.

    By default, Veo generates videos at a lower resolution for faster processing.
    Use this tool to get the full 1080p version of a completed video.

    Use this when:
    - You need a higher resolution version for production use
    - The initial video generation is complete and you want to upscale
    - You need a clearer, more detailed video output

    Note: The video must be in 'succeeded' state before requesting 1080p version.

    Returns:
        Task ID and the 1080p video information including the new video URL.
    """
    result = await client.get_1080p(video_id)
    return format_video_result(result)


@mcp.tool()
async def veo_upsample(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result (the 'id' field of a video data item, not the task_id). May come from any of veo_text_to_video, veo_image_to_video, veo_extend, veo_reshoot, veo_object_insert, veo_object_remove."
        ),
    ],
    action: Annotated[
        UpsampleAction,
        Field(
            description="What to produce. '1080p' upscales to 1080p HD, '4k' upscales to 4K, 'gif' renders an animated GIF preview."
        ),
    ],
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when the upsample completes."),
    ] = "",
) -> str:
    """Upsample a generated Veo video to 1080p / 4K, or render a GIF preview.

    Successor to veo_get_1080p — use this whenever you want anything other
    than just 1080p, or when you want the new dedicated /veo/upsample
    endpoint instead of the legacy /veo/videos action=get1080p alias.

    Use this when:
    - You need 4K resolution for production-quality delivery
    - You need an animated GIF preview for embedding/sharing
    - You want explicit semantics over the legacy get1080p alias

    Note: The source video must be in 'succeeded' state.

    Returns:
        Task ID and the upsampled video information.
    """
    payload: dict = {"video_id": video_id, "action": action}
    if callback_url:
        payload["callback_url"] = callback_url
    result = await client.upsample_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_extend(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result (the 'id' field of a video data item, not the task_id). The source video must NOT itself be the result of /veo/reshoot or /veo/objects — extend can chain on its own outputs but not on those."
        ),
    ],
    model: Annotated[
        ExtendModel,
        Field(
            description="Model to extend with. Only the Veo 3.1 series is supported upstream: 'veo31-fast' for the cheap fast tier, 'veo31' for the higher-quality slower tier."
        ),
    ] = "veo31-fast",
    prompt: Annotated[
        str,
        Field(
            description="Optional prompt that guides the extended section's content. Examples: 'the camera slowly zooms out to reveal more of the landscape', 'the bird flies up toward the moon'. If empty, the model continues the existing scene's momentum on its own."
        ),
    ] = "",
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when the extension completes."),
    ] = "",
) -> str:
    """Extend the duration of a previously generated Veo video.

    Adds extra seconds to the end of an existing video. The model continues
    the scene; an optional prompt steers what happens next.

    Use this when:
    - The first generation was too short and you want to keep it going
    - You want to add a specific follow-up action (described via prompt)
    - You want a longer final piece without re-running the whole prompt

    Important constraints (enforced upstream):
    - Only veo31-fast / veo31 models are supported.
    - Outputs of /veo/extend can be extended further, but cannot be passed
      to /veo/reshoot, /veo/objects (insert/remove). The platform returns
      400 in that case with a clear message.

    Returns:
        Task ID and the extended video information.
    """
    payload: dict = {"video_id": video_id, "model": model}
    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url
    result = await client.extend_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_reshoot(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result (the 'id' field of a video data item, not the task_id). NOT supported on outputs of /veo/extend."
        ),
    ],
    motion_type: Annotated[
        MotionType,
        Field(
            description=(
                "Camera motion to apply when re-rendering. STATIONARY* keeps the camera "
                "fixed (with optional pan/tilt/dolly-zoom). UP/DOWN move the camera "
                "vertically. LEFT_TO_RIGHT/RIGHT_TO_LEFT translate it horizontally. "
                "FORWARD/BACKWARD move it along the depth axis. DOLLY_IN_ZOOM_OUT / "
                "DOLLY_OUT_ZOOM_IN apply the classic Hitchcock dolly-zoom effect."
            )
        ),
    ],
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when the reshoot completes."),
    ] = "",
) -> str:
    """Re-render an existing Veo video with a different camera motion.

    Keeps the same scene content (subjects, action, lighting) but changes
    how the camera moves through it. Useful for trying alternative shot
    framings without re-prompting the whole video.

    Use this when:
    - You like the content but want a different camera move (push-in,
      tracking, dolly zoom, etc.)
    - You want to A/B-test framings cheaply
    - You need a static-camera version (e.g. STATIONARY) of a video that
      originally had unwanted motion

    Important: NOT supported on /veo/extend outputs (upstream limitation).

    Returns:
        Task ID and the reshot video information.
    """
    payload: dict = {"video_id": video_id, "motion_type": motion_type}
    if callback_url:
        payload["callback_url"] = callback_url
    result = await client.reshoot_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_object_insert(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result (the 'id' field of a video data item, not the task_id). NOT supported on outputs of /veo/extend."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="What to insert. Examples: 'add a flying pig with black wings', 'add a small bird gliding past the moon', 'add a coffee cup on the table in the foreground'."
        ),
    ],
    image_mask: Annotated[
        str,
        Field(
            description=(
                "Optional mask. Either a publicly reachable HTTP(S) URL to a JPEG, or a "
                "base64-encoded JPEG string (with or without a 'data:image/jpeg;base64,' "
                "prefix). White pixels mark where to insert. If omitted, the AI "
                "auto-determines placement based on the prompt."
            )
        ),
    ] = "",
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when the insert completes."),
    ] = "",
) -> str:
    """Insert an object into a previously generated Veo video.

    Adds a new element to the scene without re-prompting the whole video.

    Use this when:
    - You want to add a character, prop, or visual effect to existing footage
    - You like the original video but it's missing one element
    - You want fine-grained control over placement (via image_mask)

    Important: NOT supported on /veo/extend outputs (upstream limitation).

    Returns:
        Task ID and the modified video information.
    """
    payload: dict = {"video_id": video_id, "action": "insert", "prompt": prompt}
    if image_mask:
        payload["image_mask"] = image_mask
    if callback_url:
        payload["callback_url"] = callback_url
    result = await client.manipulate_object(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_object_remove(
    video_id: Annotated[
        str,
        Field(
            description="The video ID from a previous generation result (the 'id' field of a video data item, not the task_id). NOT supported on outputs of /veo/extend."
        ),
    ],
    image_mask: Annotated[
        str,
        Field(
            description=(
                "REQUIRED for remove. Either a publicly reachable HTTP(S) URL to a JPEG, "
                "or a base64-encoded JPEG string. White pixels mark the object to erase; "
                "the AI fills the area with contextually appropriate content."
            )
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Optional description of what is being removed. Mostly used for logging — the actual erase region is defined entirely by image_mask. Examples: 'remove the white cloud', 'remove the person in the foreground'."
        ),
    ] = "",
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when the remove completes."),
    ] = "",
) -> str:
    """Remove an object from a previously generated Veo video.

    Erases a region defined by an image mask and inpaints contextually
    appropriate replacement content.

    Use this when:
    - You need to remove an unwanted element (logo, person, prop, distraction)
    - You want a clean version of footage that came out almost-right
    - The mask is what's authoritative — prompt is just for log/audit

    Important: NOT supported on /veo/extend outputs (upstream limitation).

    Returns:
        Task ID and the modified video information.
    """
    payload: dict = {"video_id": video_id, "action": "remove", "image_mask": image_mask}
    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url
    result = await client.manipulate_object(**payload)
    return format_video_result(result)


@mcp.tool()
async def veo_ingredients_to_video(
    image_urls: Annotated[
        list[str],
        Field(
            description="1-3 reference image URLs whose elements should be fused into the generated video. Unlike veo_image_to_video (which uses images as start/end frames), this blends multiple visual elements into a single new scene."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Optional prompt to steer how the elements are combined. Examples: 'the cat from image 1 wearing the hat from image 2 walking through the meadow from image 3'."
        ),
    ] = "",
    aspect_ratio: Annotated[
        AspectRatio,
        Field(description="Video aspect ratio. '16:9' for landscape, '9:16' for portrait."),
    ] = DEFAULT_ASPECT_RATIO,
    translation: Annotated[
        bool,
        Field(description="If true, auto-translate the prompt to English for better quality."),
    ] = False,
    callback_url: Annotated[
        str,
        Field(description="Optional URL to receive a POST callback when generation completes."),
    ] = "",
) -> str:
    """Generate a video by fusing 1-3 reference images (ingredients mode).

    Uses the dedicated veo31-fast-ingredients model to blend multiple
    visual elements into a single new scene. Different from
    veo_image_to_video, which uses images as start/end frames.

    Use this when:
    - You have multiple images representing parts of what you want
      (character + outfit + setting)
    - You want a fused/blended result, not a frame-by-frame transition
    - You're combining 2-3 distinct visual concepts into one shot

    Returns:
        Task ID and the generated video information.
    """
    payload: dict = {
        "action": "ingredients2video",
        "image_urls": image_urls,
        "aspect_ratio": aspect_ratio,
    }
    if prompt:
        payload["prompt"] = prompt
    if translation:
        payload["translation"] = translation
    if callback_url:
        payload["callback_url"] = callback_url
    result = await client.generate_video(**payload)
    return format_video_result(result)
