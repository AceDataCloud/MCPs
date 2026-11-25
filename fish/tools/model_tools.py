"""Create reusable public Fish voice models."""

import json
from typing import Annotated

from mcp.types import ToolAnnotations
from pydantic import Field, HttpUrl

from core.client import client
from core.server import mcp


@mcp.tool(
    annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=False)
)
async def fish_create_model(
    title: Annotated[str, Field(min_length=1, description="Name of the reusable public voice.")],
    voices: Annotated[
        HttpUrl,
        Field(
            description="One HTTP(S) URL to authorized reference audio; a string, not an array or upload."
        ),
    ],
    description: str | None = None,
    cover_image: HttpUrl | None = None,
    tags: list[str] | None = None,
    texts: list[str] | None = None,
    enhance_audio_quality: bool | None = None,
    generate_sample: bool | None = None,
) -> str:
    """Save a cloned voice long-term and publicly; other users may discover and use it.

    Use only reference audio authorized for processing and publication as a
    reusable voice. There is no private/unlisted option. For one-shot reference
    conditioning without saving a reusable model, use fish_generate_audio.
    A successful create returns HTTP 201 and a voice _id; pass that _id as
    reference_id to fish_generate_audio. Do not retry an uncertain create blindly.
    """
    if not title.strip():
        raise ValueError("title must not be blank")
    payload = {
        "title": title,
        "voices": str(voices),
        "description": description,
        "cover_image": str(cover_image) if cover_image is not None else None,
        "tags": tags,
        "texts": texts,
        "enhance_audio_quality": enhance_audio_quality,
        "generate_sample": generate_sample,
    }
    result = await client.create_model(**{k: v for k, v in payload.items() if v is not None})
    return json.dumps(result, ensure_ascii=False, indent=2)
