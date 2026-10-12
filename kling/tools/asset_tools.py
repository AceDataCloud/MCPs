"""Manage Kling assets and use platform-owned references."""

import json

from core.asset_types import AssetManagementRequest, AssetVideoRequest, VoiceCreationRequest
from core.client import client
from core.server import mcp


# Not published until its backend Document is public.
async def kling_manage_elements(request: AssetManagementRequest) -> str:
    """List/retrieve verified preset or owned elements; presets cannot be deleted. Custom creation is unavailable."""
    result = await client.request(
        "/kling/elements", request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


# Not published until its backend Document is public.
async def kling_manage_voices(request: AssetManagementRequest | VoiceCreationRequest) -> str:
    """Create a voice (0.07 Credits), list/retrieve assets, or delete an owned voice. IDs are platform IDs. Poll creation with kling_get_task."""
    result = await client.request(
        "/kling/voices", request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def kling_generate_with_assets(request: AssetVideoRequest) -> str:
    """Generate with platform element or voice IDs. Specified V2.6 voices cost 1.68 Credits/second. Ownership is verified by the service."""
    result = await client.generate_video(
        **request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)
