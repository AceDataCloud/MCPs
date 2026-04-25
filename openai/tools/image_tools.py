"""Image generation and editing tools for OpenAI API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp
from core.types import (
    DEFAULT_IMAGE_MODEL,
    DEFAULT_IMAGE_OUTPUT_FORMAT,
    DEFAULT_IMAGE_QUALITY,
    DEFAULT_IMAGE_RESPONSE_FORMAT,
    DEFAULT_IMAGE_SIZE,
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
                "'gpt-image-1.5', 'gpt-image-2', 'dall-e-3', 'nano-banana', "
                "'nano-banana-2', 'nano-banana-pro'."
            )
        ),
    ] = DEFAULT_IMAGE_MODEL,
    size: Annotated[
        ImageSize,
        Field(
            description=(
                "Image dimensions. Options: '1024x1024' (square, default), "
                "'1792x1024' (landscape), '1024x1792' (portrait), "
                "'1536x1024', '1024x1536', '256x256', '512x512', 'auto'."
            )
        ),
    ] = DEFAULT_IMAGE_SIZE,
    quality: Annotated[
        ImageQuality,
        Field(
            description=(
                "Image quality. Options: 'auto' (default), 'high', 'medium', 'low', "
                "'hd' (dall-e-3 high detail), 'standard' (dall-e-3 standard)."
            )
        ),
    ] = DEFAULT_IMAGE_QUALITY,
    n: Annotated[
        int | None,
        Field(description="Number of images to generate (1-10). Default is 1."),
    ] = None,
    output_format: Annotated[
        ImageOutputFormat,
        Field(
            description="Output file format. Options: 'png' (default), 'jpeg', 'webp'."
        ),
    ] = DEFAULT_IMAGE_OUTPUT_FORMAT,
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
            description=(
                "Compression level (0-100%) for jpeg/webp output formats. Default is 100."
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
) -> str:
    """Generate images using OpenAI image models via AceDataCloud.

    Creates AI-generated images from text descriptions using models like
    gpt-image-1, dall-e-3, and nano-banana variants.

    Use this when:
    - You want to create an image from a text description
    - You need AI-generated artwork or illustrations
    - You want to generate product mockups or visual concepts

    Returns:
        JSON response containing image URLs or base64 data.
    """
    try:
        payload: dict[str, Any] = {
            "prompt": prompt,
            "model": model,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "response_format": response_format,
        }

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
        if callback_url is not None:
            payload["callback_url"] = callback_url

        result = await client.images_generations(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error generating image", "message": str(e)})


@mcp.tool()
async def openai_edit_image(
    image: Annotated[
        str,
        Field(
            description=(
                "Reference image URL(s). Accepts a single URL string or an array of URLs "
                "for multi-image editing. The image(s) to use as the starting point for edits."
            )
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description=(
                "Text description of the desired edit. Max 1000 characters for gpt-image models. "
                "Describe what you want to change or add to the image."
            )
        ),
    ],
    model: Annotated[
        ImageModel,
        Field(
            description=(
                "The image model to use for editing. Options: 'gpt-image-1' (default), "
                "'gpt-image-1.5', 'gpt-image-2', 'dall-e-3', 'nano-banana' variants."
            )
        ),
    ] = DEFAULT_IMAGE_MODEL,
    size: Annotated[
        ImageEditSize,
        Field(
            description=(
                "Output image dimensions. Options: '1024x1024' (default), "
                "'1536x1024', '1024x1536', '256x256', '512x512', 'auto'."
            )
        ),
    ] = "1024x1024",
    quality: Annotated[
        ImageEditQuality,
        Field(
            description=(
                "Output quality. Options: 'auto' (default), 'high', 'medium', 'low', 'standard'."
            )
        ),
    ] = "auto",
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
    input_fidelity: Annotated[
        ImageInputFidelity | None,
        Field(
            description=(
                "How closely to follow the reference image. 'high' preserves more detail, "
                "'low' allows more creative freedom."
            )
        ),
    ] = None,
    output_format: Annotated[
        ImageOutputFormat,
        Field(
            description="Output file format. Options: 'png' (default), 'jpeg', 'webp'."
        ),
    ] = DEFAULT_IMAGE_OUTPUT_FORMAT,
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
        Field(
            description="Compression level (0-100%) for jpeg/webp output. Default is 100."
        ),
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
) -> str:
    """Edit or modify existing images using OpenAI image models via AceDataCloud.

    Applies AI-powered edits to existing images based on text descriptions.
    Can modify, extend, or transform images while preserving desired elements.

    Use this when:
    - You want to modify an existing image
    - You need to add, remove, or change elements in an image
    - You want to apply a specific style or transformation to an image

    Returns:
        JSON response containing the edited image URL(s) or base64 data.
    """
    try:
        payload: dict[str, Any] = {
            "image": image,
            "prompt": prompt,
            "model": model,
            "size": size,
            "quality": quality,
            "output_format": output_format,
            "response_format": response_format,
        }

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

        result = await client.images_edits(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error editing image", "message": str(e)})
