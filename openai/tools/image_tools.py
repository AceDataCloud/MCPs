"""Image generation and editing tools for OpenAI API."""

import json
from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIError, format_tool_error
from core.server import mcp
from core.types import (
    DEFAULT_IMAGE_MODEL,
    DEFAULT_IMAGE_OUTPUT_FORMAT,
    DEFAULT_IMAGE_QUALITY,
    DEFAULT_IMAGE_RESPONSE_FORMAT,
    DEFAULT_IMAGE_SIZE,
    GIF_IMAGE_MODELS,
    ImageBackground,
    ImageEditQuality,
    ImageEditSize,
    ImageInputFidelity,
    ImageModel,
    ImageModeration,
    ImageOutputFormat,
    ImageQuality,
    ImageResponseFormat,
    ImageSize,
    ImageStyle,
)
from core.utils import format_submission_result


def _validate_gif_options(
    model: str, output_format: str, frame_count: int | None, frame_duration_ms: int | None
) -> None:
    if output_format == "gif" and model not in GIF_IMAGE_MODELS:
        raise OpenAIError(
            "GIF requires GPT Image 2.6 Flare/Sunburst (standard/reverse/official).",
            code="validation_error",
        )
    for name, value in (("frame_count", frame_count), ("frame_duration_ms", frame_duration_ms)):
        if value is None:
            continue
        if output_format != "gif":
            raise OpenAIError(f"{name} requires output_format=gif.", code="validation_error")
        minimum, maximum = (2, 16) if name == "frame_count" else (20, 655350)
        if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
            raise OpenAIError(
                f"{name} must be an integer between {minimum} and {maximum}.",
                code="validation_error",
            )


@mcp.tool()
async def openai_generate_image(
    prompt: Annotated[
        str,
        Field(
            description=(
                "A text description of the desired image(s). Be descriptive about the "
                "subject, style, lighting, and composition. "
                "Example: 'A serene mountain landscape at sunset with golden light'"
            )
        ),
    ],
    model: Annotated[
        ImageModel,
        Field(
            description=(
                "The image model to use. Options: 'gpt-image-1' (default, versatile), "
                "'gpt-image-1.5', 'gpt-image-2', 'gpt-image-2.5-flare', "
                "'gpt-image-2.5-flare:reverse', 'gpt-image-2.5-flare:official', "
                "'gpt-image-2.5-sunburst', 'gpt-image-2.5-sunburst:reverse', "
                "'gpt-image-2.5-sunburst:official', 'gpt-image-2.6-flare', "
                "'gpt-image-2.6-flare:reverse', 'gpt-image-2.6-flare:official', "
                "'gpt-image-2.6-sunburst', 'gpt-image-2.6-sunburst:reverse', "
                "'gpt-image-2.6-sunburst:official', 'dall-e-3', 'dall-e-2', "
                "'nano-banana', 'nano-banana-2-lite', 'nano-banana-2', 'nano-banana-2.1', 'nano-banana-pro'. Nano Banana 2.1 has no ':official' variant. GPT Image ':official' variants use actual-token billing."
            )
        ),
    ] = DEFAULT_IMAGE_MODEL,
    size: Annotated[
        ImageSize,
        Field(
            description=(
                "Image dimensions as 'WIDTHxHEIGHT' or 'auto' (default). "
                "GPT Image 2, 2.5 and 2.6 models accept custom dimensions matching the format "
                "(multiples of 16, longer side ≤ 3840, total pixels 655,360–8,294,400, "
                "aspect ratio ≤ 3:1). "
                "Common presets — 1K: '1024x1024', '1536x1024', '1024x1536', "
                "'1792x1024', '1024x1792'; 2K: '2048x2048', '2048x1536', "
                "'1536x2048', '2048x1152', '1152x2048'; 4K: '2880x2880', "
                "'3264x2448', '2448x3264', '3840x2160', '2160x3840'. "
                "dall-e-2: '256x256', '512x512', '1024x1024'. "
                "dall-e-3: '1024x1024', '1792x1024', '1024x1792'."
            )
        ),
    ] = DEFAULT_IMAGE_SIZE,
    quality: Annotated[
        ImageQuality,
        Field(
            description=(
                "Image quality. GPT Image: 'auto' (default), 'high', 'medium', 'low'. "
                "GPT Image 2.5 and 2.6 Flare/Sunburst (including ':reverse' and ':official') "
                "also support 'xhigh' and 'max'. Official variants bill actual token usage. "
                "dall-e-3: 'hd' or 'standard'; dall-e-2: 'standard' only."
            )
        ),
    ] = DEFAULT_IMAGE_QUALITY,
    complexity: Annotated[
        Literal["low", "medium", "high"] | None,
        Field(
            description="GPT Image 2.6 planning complexity, independent of quality. Omit for model default high."
        ),
    ] = None,
    n: Annotated[
        int | None,
        Field(description="Number of images to generate (1-10). Default is 1."),
    ] = None,
    output_format: Annotated[
        ImageOutputFormat,
        Field(
            description="Output format: png (default), jpeg, webp; gif for GPT Image 2.6 Flare/Sunburst (standard/reverse/official). GIF defaults to a 512x512 preview, 9 frames, 200ms per frame; static 4K sizes do not apply to GIF."
        ),
    ] = DEFAULT_IMAGE_OUTPUT_FORMAT,
    frame_count: Annotated[
        int | None,
        Field(ge=2, le=16, strict=True, description="GIF frame count, 2-16. Defaults to 9."),
    ] = None,
    frame_duration_ms: Annotated[
        int | None,
        Field(
            ge=20,
            le=655350,
            strict=True,
            description="GIF frame duration in milliseconds, 20-655350; rounded to 10ms. Defaults to 200.",
        ),
    ] = None,
    response_format: Annotated[
        ImageResponseFormat,
        Field(
            description=(
                "How to return the image. 'url' (default) returns a URL, "
                "'b64_json' returns base64-encoded image data."
            )
        ),
    ] = DEFAULT_IMAGE_RESPONSE_FORMAT,
    style: Annotated[
        ImageStyle | None,
        Field(
            description=(
                "Image style for dall-e-3. 'vivid' generates hyper-real and dramatic images, "
                "'natural' produces more natural, less hyper-real looking images."
            )
        ),
    ] = None,
    background: Annotated[
        ImageBackground | None,
        Field(
            description=(
                "Background type for gpt-image models. 'transparent' removes the background, "
                "'opaque' keeps it, 'auto' decides automatically."
            )
        ),
    ] = None,
    moderation: Annotated[
        ImageModeration | None,
        Field(
            description=(
                "Content moderation level. 'auto' uses default moderation, "
                "'low' applies less strict filtering."
            )
        ),
    ] = None,
    output_compression: Annotated[
        int | None,
        Field(
            description=("Compression level (0-100%) for jpeg/webp output formats. Default is 100.")
        ),
    ] = None,
    partial_images: Annotated[
        int | None,
        Field(
            description=(
                "Number of partial images to emit during streaming (0-3). "
                "0 returns the final image in one event."
            )
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description=(
                "Optional webhook URL. When provided, the API returns a task_id immediately "
                "and POSTs the result to this URL when generation completes."
            )
        ),
    ] = None,
    async_: Annotated[
        bool | None,
        Field(
            validation_alias="async", description="Whether to process the request asynchronously."
        ),
    ] = None,
) -> str:
    """Generate images using OpenAI image models via AceDataCloud.

    Creates AI-generated images from text descriptions using models like
    gpt-image-1, dall-e-3, and nano-banana variants.

    Use this when:
    - You want to create an image from a text description
    - You need AI-generated artwork or illustrations
    - You want to generate product mockups or visual concepts

    Returns:
        JSON with a `task_id`. Generation runs asynchronously — poll
        `openai_get_task` with that id until it reports `finished_at`, then
        read the image URLs from its `response`. When `callback_url` is set the
        result is POSTed there instead.
    """
    try:
        _validate_gif_options(model, output_format, frame_count, frame_duration_ms)
        if complexity is not None and model not in GIF_IMAGE_MODELS:
            raise OpenAIError("complexity requires GPT Image 2.6.", code="validation_error")
        if output_format == "gif" and output_compression is not None:
            raise OpenAIError("GIF does not support output_compression.", code="validation_error")
        payload: dict[str, Any] = {
            "prompt": prompt,
            "model": model,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "response_format": response_format,
        }

        if complexity is not None:
            payload["complexity"] = complexity
        if frame_count is not None:
            payload["frame_count"] = frame_count
        if frame_duration_ms is not None:
            payload["frame_duration_ms"] = frame_duration_ms
        if n is not None:
            payload["n"] = n
        if style is not None:
            payload["style"] = style
        if background is not None:
            payload["background"] = background
        if moderation is not None:
            payload["moderation"] = moderation
        if output_compression is not None:
            payload["output_compression"] = output_compression
        if partial_images is not None:
            payload["partial_images"] = partial_images
        if callback_url is not None:
            payload["callback_url"] = callback_url
        if async_ is not None:
            payload["async"] = async_

        result = await client.images_generations_async(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return format_submission_result(result)

    except Exception as e:
        return format_tool_error(e, "Error generating image")


@mcp.tool()
async def openai_edit_image(
    image: Annotated[
        str | Annotated[list[str], Field(min_length=1, max_length=16)],
        Field(
            description=(
                "Reference image URL(s). Pass one URL as a string, or multiple URLs as a real "
                "JSON array of strings (maximum 16) in the intended reference order. For example: "
                '["https://example.com/base.png", "https://example.com/logo.png"]. Never join '
                "multiple URLs with commas and never JSON-stringify the array. The first image "
                "should normally be the base image; describe the role of later references in prompt."
            )
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description=(
                "Text description of the desired edit. GPT Image models allow up to 32000 characters; dall-e-2 allows up to 1000. "
                "Describe what you want to change or add to the image."
            )
        ),
    ],
    model: Annotated[
        ImageModel,
        Field(
            description=(
                "The image model to use for editing. Options: 'dall-e-3' (default), "
                "'gpt-image-1.5', 'gpt-image-2', 'gpt-image-2.5-flare', "
                "'gpt-image-2.5-flare:reverse', 'gpt-image-2.5-flare:official', "
                "'gpt-image-2.5-sunburst', 'gpt-image-2.5-sunburst:reverse', "
                "'gpt-image-2.5-sunburst:official', 'gpt-image-2.6-flare', "
                "'gpt-image-2.6-flare:reverse', 'gpt-image-2.6-flare:official', "
                "'gpt-image-2.6-sunburst', 'gpt-image-2.6-sunburst:reverse', "
                "'gpt-image-2.6-sunburst:official', 'dall-e-3', and 'nano-banana' variants including 'nano-banana-2.1' (no ':official' variant)."
            )
        ),
    ] = "dall-e-3",
    size: Annotated[
        ImageEditSize,
        Field(
            description=(
                "Output image dimensions as 'WIDTHxHEIGHT' or 'auto'. Default is 'auto'. "
                "GPT Image 2, 2.5 and 2.6 models accept custom dimensions (multiples of 16, longer side ≤ 3840, "
                "total pixels 655,360–8,294,400, aspect ratio ≤ 3:1). Common presets — 1K: '1024x1024', '1536x1024', "
                "'1024x1536', '1792x1024', '1024x1792'; 2K: '2048x2048', "
                "'2048x1536', '1536x2048', '2048x1152', '1152x2048'; 4K: "
                "'2880x2880', '3264x2448', '2448x3264', '3840x2160', '2160x3840'. "
                "dall-e-2: '256x256', '512x512', '1024x1024'."
            )
        ),
    ] = "auto",
    quality: Annotated[
        ImageEditQuality,
        Field(
            description=(
                "Output quality. GPT Image: 'auto' (default), 'high', 'medium', 'low'. "
                "GPT Image 2.5 and 2.6 Flare/Sunburst (including ':reverse' and ':official') "
                "also support 'xhigh' and 'max'. Official variants bill actual token usage. "
                "dall-e-2: 'standard' only."
            )
        ),
    ] = "auto",
    complexity: Annotated[
        Literal["low", "medium", "high"] | None,
        Field(
            description="GPT Image 2.6 planning complexity, independent of quality. Omit for model default high."
        ),
    ] = None,
    n: Annotated[
        int | None,
        Field(description="Number of images to generate (1-10). Default is 1."),
    ] = None,
    background: Annotated[
        ImageBackground | None,
        Field(
            description=(
                "Background handling. 'transparent' removes background, "
                "'opaque' keeps it, 'auto' decides automatically."
            )
        ),
    ] = None,
    markup: Annotated[
        str | None,
        Field(
            description="GPT Image 2.6 static edit annotation: transparent PNG HTTPS URL or data URL, matching the first reference dimensions, maximum 40MB. Cannot combine with GIF."
        ),
    ] = None,
    input_fidelity: Annotated[
        ImageInputFidelity | None,
        Field(
            description=(
                "Omit for GPT Image 2/2.5/2.6. For earlier supported models, high preserves more detail, "
                "'low' allows more creative freedom."
            )
        ),
    ] = None,
    output_format: Annotated[
        ImageOutputFormat,
        Field(
            description="Output format: png (default), jpeg, webp; gif for GPT Image 2.6 Flare/Sunburst (standard/reverse/official). GIF defaults to a 512x512 preview, 9 frames, 200ms per frame; static 4K sizes do not apply to GIF."
        ),
    ] = DEFAULT_IMAGE_OUTPUT_FORMAT,
    frame_count: Annotated[
        int | None,
        Field(ge=2, le=16, strict=True, description="GIF frame count, 2-16. Defaults to 9."),
    ] = None,
    frame_duration_ms: Annotated[
        int | None,
        Field(
            ge=20,
            le=655350,
            strict=True,
            description="GIF frame duration in milliseconds, 20-655350; rounded to 10ms. Defaults to 200.",
        ),
    ] = None,
    response_format: Annotated[
        ImageResponseFormat,
        Field(
            description=(
                "How to return the image. 'url' (default) returns a URL, "
                "'b64_json' returns base64-encoded image data."
            )
        ),
    ] = DEFAULT_IMAGE_RESPONSE_FORMAT,
    output_compression: Annotated[
        int | None,
        Field(description="Compression level (0-100%) for jpeg/webp output. Default is 100."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description=(
                "Optional webhook URL. When provided, returns task_id immediately and "
                "POSTs result to this URL when complete."
            )
        ),
    ] = None,
    async_: Annotated[
        bool | None,
        Field(
            validation_alias="async", description="Whether to process the request asynchronously."
        ),
    ] = None,
) -> str:
    """Edit or modify existing images using OpenAI image models via AceDataCloud.

    Applies AI-powered edits to existing images based on text descriptions.
    Can modify, extend, or transform images while preserving desired elements.

    Use this when:
    - You want to modify an existing image
    - You need to add, remove, or change elements in an image
    - You want to apply a specific style or transformation to an image

    Returns:
        JSON with a `task_id`. Editing runs asynchronously — poll
        `openai_get_task` with that id until it reports `finished_at`, then
        read the image URLs from its `response`. When `callback_url` is set the
        result is POSTed there instead.
    """
    try:
        _validate_gif_options(model, output_format, frame_count, frame_duration_ms)
        if complexity is not None and model not in GIF_IMAGE_MODELS:
            raise OpenAIError("complexity requires GPT Image 2.6.", code="validation_error")
        if output_format == "gif" and output_compression is not None:
            raise OpenAIError("GIF does not support output_compression.", code="validation_error")
        if markup is not None and (model not in GIF_IMAGE_MODELS or output_format == "gif"):
            raise OpenAIError(
                "markup requires a GPT Image 2.6 static edit.", code="validation_error"
            )
        payload: dict[str, Any] = {
            "image": image,
            "prompt": prompt,
            "model": model,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "response_format": response_format,
        }

        if markup is not None:
            payload["markup"] = markup
        if complexity is not None:
            payload["complexity"] = complexity
        if frame_count is not None:
            payload["frame_count"] = frame_count
        if frame_duration_ms is not None:
            payload["frame_duration_ms"] = frame_duration_ms
        if n is not None:
            payload["n"] = n
        if background is not None:
            payload["background"] = background
        if input_fidelity is not None:
            payload["input_fidelity"] = input_fidelity
        if output_compression is not None:
            payload["output_compression"] = output_compression
        if callback_url is not None:
            payload["callback_url"] = callback_url
        if async_ is not None:
            payload["async"] = async_

        result = await client.images_edits_async(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return format_submission_result(result)

    except Exception as e:
        return format_tool_error(e, "Error editing image")
