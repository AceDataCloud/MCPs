"""Kling native video and commerce capability tools."""

import json

from core.client import client
from core.native_types import (
    ApparelRequest,
    CommerceRequest,
    GoodsRequest,
    StoryboardRequest,
    TryOnRequest,
    TurboRequest,
)
from core.server import mcp


@mcp.tool()
async def kling_generate_turbo_video(request: TurboRequest) -> str:
    """Generate V3 Turbo 720p/1080p, 3–15 seconds. Native audio is included with no off switch. Poll kling_get_task."""
    return json.dumps(
        await client.generate_video(
            **request.model_dump(mode="json", by_alias=True, exclude_none=True)
        ),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
async def kling_generate_storyboard(request: StoryboardRequest) -> str:
    """Generate V3/V3 Omni automatic or custom multishot video. Poll kling_get_task."""
    return json.dumps(
        await client.generate_video(
            **request.model_dump(mode="json", by_alias=True, exclude_none=True)
        ),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
async def kling_apparel_video(request: ApparelRequest) -> str:
    """Generate apparel product video from product_info, source_video and product_image contents. Poll kling_get_task."""
    return json.dumps(
        await client.request(
            "/kling/apparel", request.model_dump(mode="json", by_alias=True, exclude_none=True)
        ),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
async def kling_goods_studio(request: GoodsRequest) -> str:
    """Generate product studio video from ref_image and goods_title contents. Poll kling_get_task."""
    return json.dumps(
        await client.request(
            "/kling/goods-studio", request.model_dump(mode="json", by_alias=True, exclude_none=True)
        ),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
async def kling_video_commerce(request: CommerceRequest) -> str:
    """Generate creator/product voiceover from an avatar and speech_script. Poll kling_get_task."""
    return json.dumps(
        await client.request(
            "/kling/video-commerce",
            request.model_dump(mode="json", by_alias=True, exclude_none=True),
        ),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
async def kling_virtual_try_on(request: TryOnRequest) -> str:
    """Generate try-on images from exactly one product_image and one person_image URL. Poll kling_get_task."""
    return json.dumps(
        await client.request(
            "/kling/virtual-try-on",
            request.model_dump(mode="json", by_alias=True, exclude_none=True),
        ),
        ensure_ascii=False,
        indent=2,
    )
