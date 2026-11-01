"""Public voice creation is distinct from one-shot reference conditioning."""

import json
from unittest.mock import AsyncMock, patch

import httpx
import respx

from core.client import FishClient
from core.server import mcp
from tools import model_tools  # noqa: F401


async def test_create_model_mcp_schema_and_optional_false_values():
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    schema = tools["fish_create_model"].inputSchema
    assert schema["required"] == ["title", "voices"]
    assert "visibility" not in schema["properties"]
    assert "public" in tools["fish_create_model"].description
    args = {
        "title": "My voice",
        "voices": "https://example.com/audio.wav",
        "cover_image": "https://example.com/cover.png",
        "tags": ["English"],
        "texts": ["Reference transcript"],
        "enhance_audio_quality": False,
        "generate_sample": False,
    }
    with patch(
        "tools.model_tools.client.create_model", new=AsyncMock(return_value={"_id": "voice-id"})
    ) as call:
        await mcp.call_tool("fish_create_model", args)
    assert call.await_args.kwargs == args


@respx.mock
async def test_create_model_uses_post_and_accepts_created_response():
    route = respx.post("https://api.test.com/fish/model").mock(
        return_value=httpx.Response(201, json={"_id": "voice-id", "title": "My voice"})
    )
    client = FishClient(api_token="test-token", base_url="https://api.test.com")
    result = await client.create_model(
        title="My voice", voices="https://example.com/audio.wav", generate_sample=False
    )
    assert result["_id"] == "voice-id"
    assert json.loads(route.calls[0].request.content) == {
        "title": "My voice",
        "voices": "https://example.com/audio.wav",
        "generate_sample": False,
    }
