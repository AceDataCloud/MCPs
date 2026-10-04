"""MiniMax H3 native capability tools."""

import json

from core.client import client
from core.native_types import MaxVideoRequest, PromptEnhancementRequest, RegenerationRequest
from core.server import mcp


@mcp.tool()
async def minimax_generate_max_video(request: MaxVideoRequest) -> str:
    """Generate H3 Max video in 480P/768P, 5–15 seconds. Poll minimax_get_task."""
    result = await client.request(
        "/minimax/videos", request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def minimax_enhance_prompt(request: PromptEnhancementRequest) -> str:
    """Create structured H3 prompt/material guidance. Poll minimax_get_task for the full result."""
    result = await client.request(
        "/minimax/prompt-enhancement",
        request.model_dump(mode="json", by_alias=True, exclude_none=True),
    )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def minimax_regenerate_video(request: RegenerationRequest) -> str:
    """Regenerate an owned H3 768P task at 2K using its exact original materials. Poll minimax_get_task."""
    result = await client.request(
        "/minimax/regenerate", request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    return json.dumps(result, ensure_ascii=False, indent=2)
