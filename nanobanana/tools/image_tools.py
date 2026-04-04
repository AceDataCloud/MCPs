"""Image generation and editing tools for NanoBanana API."""

from typing import Annotated, Literal

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_image_result

NanoBananaModel = Literal["nano-banana", "nano-banana-2", "nano-banana-pro"]
AspectRatio = Literal["1:1", "3:2", "2:3", "16:9", "9:16", "4:3", "3:4"]
Resolution = Literal["1K", "2K", "4K"]


@mcp.tool()
async def nanobanana_generate_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of the image to generate. Be descriptive about subject, atmosphere, lighting, camera/lens, and quality. Example: 'A photorealistic close-up portrait of an elderly Japanese ceramicist with deep wrinkles and a warm smile, soft golden hour light, 85mm portrait lens, bokeh background'"
        ),
    ],
    model: Annotated[
        NanoBananaModel,
        Field(
            description="Model to use for generation. 'nano-banana' (default, alias of gemini-2.5-flash-image) is faster. 'nano-banana-2' (alias of gemini-3.1-flash-image) offers pro-level quality at flash speed. 'nano-banana-pro' (alias of gemini-3-pro-image) offers highest quality and supports resolution parameter."
        ),
    ] = "nano-banana",
    aspect_ratio: Annotated[
        AspectRatio,
        Field(
            description="Aspect ratio of the generated image. Options: '1:1' (square, default), '3:2', '2:3', '16:9' (landscape), '9:16' (portrait), '4:3', '3:4'."
        ),
    ] = "1:1",
    resolution: Annotated[
        Resolution | None,
        Field(
            description="Resolution of the generated image. Options: '1K' (default), '2K', '4K'. Only works with 'nano-banana-pro' model."
        ),
    ] = None,
) -> str:
    """Generate an AI image from a text prompt using Google's Nano Banana model.

    This creates high-quality images from detailed text descriptions. The more
    descriptive your prompt, the better the results.

    Use this when:
    - You want to generate a new image from scratch
    - You have a detailed description of the desired image
    - You need photorealistic or artistic image generation

    Prompt writing tips:
    - Include: Main subject + Atmosphere + Lighting + Camera/Lens + Quality keywords
    - Example: "Urban career woman, backlit sunlight, film grain, orange-gold tones, hopeful dawn"

    Returns:
        Task ID, trace ID, and generated image URL.
    """
    payload: dict = {
        "action": "generate",
        "prompt": prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
    }

    if resolution:
        payload["resolution"] = resolution

    result = await client.generate_image_async(**payload)
    return format_image_result(result)


@mcp.tool()
async def nanobanana_edit_image(
    prompt: Annotated[
        str,
        Field(
            description="Description of the edit to perform. Describe how the images should be combined or modified. Example: 'let this person wear this T-shirt', 'place this product in a modern kitchen scene'"
        ),
    ],
    image_urls: Annotated[
        list[str],
        Field(
            description="List of image URLs to edit. Can be HTTP/HTTPS URLs (publicly accessible) or Base64-encoded images (data:image/png;base64,...). When combining multiple images, describe their relationship in the prompt."
        ),
    ],
    model: Annotated[
        NanoBananaModel,
        Field(
            description="Model to use for editing. 'nano-banana' (default, alias of gemini-2.5-flash-image) is faster. 'nano-banana-2' (alias of gemini-3.1-flash-image) offers pro-level quality at flash speed. 'nano-banana-pro' (alias of gemini-3-pro-image) offers highest quality."
        ),
    ] = "nano-banana",
) -> str:
    """Edit or combine images using AI based on a text prompt.

    This allows you to modify existing images or combine multiple images together.
    Perfect for virtual try-on, product placement, image enhancement, and more.

    Use this when:
    - You want to combine multiple images (e.g., person + clothing)
    - You want to modify an existing image
    - You need virtual try-on (putting clothes on a person)
    - You want to place products in different scenes
    - You need to change attributes (materials, colors, styles)

    Common use cases:
    - Portrait replacement: Try different clothing on same person
    - Product scene composition: Place products in realistic environments
    - Attribute replacement: Change materials, colors, or variants
    - Poster editing: Rapidly change styles or themes
    - 2D to 3D conversion: Convert images to 3D product mockups
    - Image restoration: Restore old or damaged photos

    Returns:
        Task ID, trace ID, and edited image URL.
    """
    payload: dict = {
        "action": "edit",
        "prompt": prompt,
        "image_urls": image_urls,
        "model": model,
    }

    result = await client.edit_image_async(**payload)
    return format_image_result(result)
