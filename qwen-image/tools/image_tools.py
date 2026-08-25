"""Image generation and editing tools for Qwen Image 3."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, PromptExtendMode, QwenImageModel
from core.utils import format_image_result

Prompt = Annotated[
    str,
    Field(min_length=1, max_length=18000, description="Detailed text description of the image."),
]
ImageURL = Annotated[str, Field(json_schema_extra={"format": "uri"})]
ImageSize = Annotated[
    str,
    Field(
        pattern=r"^[0-9]+\*[0-9]+$",
        description="WIDTH*HEIGHT, within the supported 512²–2048² pixel-area range.",
    ),
]
CallbackURL = Annotated[
    str,
    Field(json_schema_extra={"format": "uri"}, description="Webhook callback URL."),
]


async def _run(
    prompt: str,
    model: QwenImageModel,
    image_urls: list[str] | None,
    n: int,
    size: str | None,
    prompt_extend: bool,
    prompt_extend_mode: PromptExtendMode,
    enable_thinking: bool,
    negative_prompt: str | None,
    seed: int | None,
    watermark: bool,
    callback_url: str | None,
) -> str:
    payload = {
        "prompt": prompt,
        "model": model,
        "n": n,
        "prompt_extend": prompt_extend,
        "prompt_extend_mode": prompt_extend_mode,
        "enable_thinking": enable_thinking,
        "watermark": watermark,
    }
    if image_urls is not None:
        payload["image_urls"] = image_urls
    if size is not None:
        payload["size"] = size
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    if seed is not None:
        payload["seed"] = seed
    if callback_url:
        payload["callback_url"] = callback_url
    return format_image_result(await client.generate_image(**payload))


@mcp.tool()
async def qwen_image_generate(
    prompt: Prompt,
    model: Annotated[QwenImageModel, Field(description="Qwen Image 3 model.")] = DEFAULT_MODEL,
    n: Annotated[int, Field(ge=1, le=6, description="Number of images to generate.")] = 1,
    size: ImageSize | None = None,
    prompt_extend: bool = True,
    prompt_extend_mode: PromptExtendMode = "direct",
    enable_thinking: bool = True,
    negative_prompt: str | None = None,
    seed: Annotated[int | None, Field(ge=0, le=2147483647)] = None,
    watermark: bool = False,
    callback_url: CallbackURL | None = None,
) -> str:
    """Generate one to six images from text with Qwen Image 3."""
    return await _run(
        prompt,
        model,
        None,
        n,
        size,
        prompt_extend,
        prompt_extend_mode,
        enable_thinking,
        negative_prompt,
        seed,
        watermark,
        callback_url,
    )


@mcp.tool()
async def qwen_image_edit(
    prompt: Prompt,
    image_urls: Annotated[
        list[ImageURL],
        Field(min_length=1, max_length=3, description="One to three public reference image URLs."),
    ],
    model: Annotated[QwenImageModel, Field(description="Qwen Image 3 model.")] = DEFAULT_MODEL,
    n: Annotated[int, Field(ge=1, le=6)] = 1,
    size: ImageSize | None = None,
    prompt_extend: bool = True,
    prompt_extend_mode: PromptExtendMode = "direct",
    enable_thinking: bool = True,
    negative_prompt: str | None = None,
    seed: Annotated[int | None, Field(ge=0, le=2147483647)] = None,
    watermark: bool = False,
    callback_url: CallbackURL | None = None,
) -> str:
    """Edit images with one to three references and a text instruction."""
    return await _run(
        prompt,
        model,
        image_urls,
        n,
        size,
        prompt_extend,
        prompt_extend_mode,
        enable_thinking,
        negative_prompt,
        seed,
        watermark,
        callback_url,
    )
