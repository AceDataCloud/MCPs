"""Unit tests for NanoBanana image tools."""

import json

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from core.server import mcp
from tools import image_tools


@pytest.mark.asyncio
async def test_generate_image_forwards_count_and_callback(monkeypatch, mock_image_response):
    captured_payload: dict[str, object] = {}

    async def mock_generate_image_async(**kwargs):
        captured_payload.update(kwargs)
        return mock_image_response

    monkeypatch.setattr(image_tools.client, "generate_image_async", mock_generate_image_async)

    response = await image_tools.nanobanana_generate_image(
        prompt="test",
        count=2,
        callback_url="https://example.com/callback",
    )

    assert captured_payload["count"] == 2
    assert captured_payload["callback_url"] == "https://example.com/callback"
    assert json.loads(response)["task_id"] == "test-task-123"


def test_image_tools_expose_nano_banana_2_1_without_official_variant():
    tools = {tool.name: tool for tool in mcp._tool_manager.list_tools()}
    for name in ("nanobanana_generate_image", "nanobanana_edit_image"):
        model = tools[name].parameters["properties"]["model"]
        assert "nano-banana-2.1" in model["enum"]
        assert "nano-banana-2.1:official" not in model["enum"]
        assert model["default"] == "nano-banana"


@pytest.mark.asyncio
@pytest.mark.parametrize("resolution", ["1K", "2K", "4K"])
@pytest.mark.parametrize(
    ("tool_name", "action", "extra_arguments"),
    [
        ("nanobanana_generate_image", "generate", {}),
        (
            "nanobanana_edit_image",
            "edit",
            {"image_urls": ["https://example.com/image.png"]},
        ),
    ],
)
async def test_dispatch_forwards_nano_banana_2_1(
    monkeypatch, resolution, tool_name, action, extra_arguments
):
    captured_payload: dict[str, object] = {}

    async def mock_request(endpoint, payload):
        captured_payload.update(payload)
        assert endpoint == "/nano-banana/images"
        return {"task_id": "test-task-123"}

    monkeypatch.setattr(image_tools.client, "request", mock_request)
    result = await mcp.call_tool(
        tool_name,
        {
            "prompt": "test",
            "model": "nano-banana-2.1",
            "resolution": resolution,
            "count": 2,
            **extra_arguments,
        },
    )

    assert result
    assert captured_payload["action"] == action
    assert captured_payload["model"] == "nano-banana-2.1"
    assert captured_payload["resolution"] == resolution
    assert captured_payload["count"] == 2
    assert captured_payload["async"] is True
    if action == "edit":
        assert captured_payload["image_urls"] == extra_arguments["image_urls"]
        assert "aspect_ratio" not in captured_payload


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name", ["nanobanana_generate_image", "nanobanana_edit_image"])
async def test_dispatch_rejects_nano_banana_2_1_official(monkeypatch, tool_name):
    async def unexpected_request(*_args, **_kwargs):
        pytest.fail("An unsupported model must not reach the API")

    monkeypatch.setattr(image_tools.client, "request", unexpected_request)
    arguments = {"prompt": "test", "model": "nano-banana-2.1:official"}
    if tool_name == "nanobanana_edit_image":
        arguments["image_urls"] = ["https://example.com/image.png"]
    with pytest.raises(ToolError):
        await mcp.call_tool(tool_name, arguments)


@pytest.mark.asyncio
async def test_edit_image_forwards_count_and_callback(monkeypatch, mock_image_response):
    captured_payload: dict[str, object] = {}

    async def mock_edit_image_async(**kwargs):
        captured_payload.update(kwargs)
        return mock_image_response

    monkeypatch.setattr(image_tools.client, "edit_image_async", mock_edit_image_async)

    response = await image_tools.nanobanana_edit_image(
        prompt="test",
        image_urls=["https://example.com/image.png"],
        count=2,
        callback_url="https://example.com/callback",
    )

    assert captured_payload["count"] == 2
    assert captured_payload["callback_url"] == "https://example.com/callback"
    assert json.loads(response)["task_id"] == "test-task-123"
