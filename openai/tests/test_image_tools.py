"""Unit tests for image tools."""

import json
from typing import Any

import pytest

from core.server import mcp
from tools import image_tools


def test_openai_edit_image_schema_accepts_single_or_multiple_images():
    """The MCP schema must expose the API's string-or-array contract."""
    tool = next(tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_edit_image")
    image_schema = tool.parameters["properties"]["image"]

    assert image_schema["anyOf"] == [
        {"type": "string"},
        {
            "items": {"type": "string"},
            "maxItems": 16,
            "minItems": 1,
            "type": "array",
        },
    ]
    assert "Never join multiple URLs with commas" in image_schema["description"]
    assert "never JSON-stringify the array" in image_schema["description"]


@pytest.mark.asyncio
async def test_openai_edit_image_forwards_image_array(monkeypatch):
    """Multiple image URLs must remain an array in the API payload."""
    captured_payload: dict[str, object] = {}

    async def mock_images_edits(**kwargs):
        captured_payload.update(kwargs)
        return {"data": [{"url": "https://example.com/edited.png"}]}

    monkeypatch.setattr(image_tools.client, "images_edits", mock_images_edits)
    images = [
        "https://example.com/base.png",
        "https://example.com/logo.png",
    ]

    response = await image_tools.openai_edit_image(
        image=images,
        prompt="Replace the base image logo with the reference logo.",
        model="gpt-image-2",
    )

    assert captured_payload["image"] == images
    assert json.loads(response) == {"data": [{"url": "https://example.com/edited.png"}]}


@pytest.mark.asyncio
async def test_openai_edit_image_uses_auto_size_by_default(monkeypatch):
    """Image editing should preserve the reference image aspect ratio by default."""
    captured_payload: dict[str, object] = {}

    async def mock_images_edits(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-0"}

    monkeypatch.setattr(image_tools.client, "images_edits", mock_images_edits)

    await image_tools.openai_edit_image(
        image="https://example.com/base.png",
        prompt="Remove the background.",
        model="gpt-image-2",
    )

    assert captured_payload["size"] == "auto"


@pytest.mark.asyncio
async def test_openai_generate_image_submits_async(monkeypatch):
    """Generation must be submitted asynchronously so slow models don't time out."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-1"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(prompt="a panda", model="gpt-image-1")

    assert captured_payload["async"] is True


@pytest.mark.asyncio
async def test_openai_generate_image_uses_auto_size_by_default(monkeypatch):
    """Generation should let the model choose dimensions by default, as the API does."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-3"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(prompt="a panda", model="gpt-image-1")

    assert captured_payload["size"] == "auto"


def test_openai_edit_image_schema_omits_partial_images():
    """JSON edits endpoint doesn't accept partial_images; tool schema must not expose it."""
    tool = next(tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_edit_image")
    assert "partial_images" not in tool.parameters["properties"]


@pytest.mark.asyncio
async def test_openai_generate_image_defers_to_explicit_callback_url(monkeypatch):
    """An explicit callback_url already implies async upstream — don't double-flag it."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-2"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(
        prompt="a panda",
        model="gpt-image-1",
        callback_url="https://example.com/hook",
    )

    assert "async" not in captured_payload
    assert captured_payload["callback_url"] == "https://example.com/hook"


def test_openai_image_tools_expose_async_parameter():
    """The MCP schema should expose the API's async request-body parameter."""
    tools = {tool.name: tool for tool in mcp._tool_manager.list_tools()}

    assert "async" in tools["openai_generate_image"].parameters["properties"]
    assert "async" in tools["openai_edit_image"].parameters["properties"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "arguments", "client_method"),
    [
        (
            "openai_generate_image",
            {"prompt": "a panda", "model": "gpt-image-1"},
            "images_generations_async",
        ),
        (
            "openai_edit_image",
            {
                "image": "https://example.com/base.png",
                "prompt": "Remove the background.",
                "model": "gpt-image-2",
            },
            "images_edits_async",
        ),
    ],
)
async def test_fastmcp_dispatch_maps_public_async_parameter(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    arguments: dict[str, object],
    client_method: str,
) -> None:
    captured_payload: dict[str, object] = {}

    async def mock_request(**kwargs: Any) -> dict[str, list[dict[str, str]]]:
        captured_payload.update(kwargs)
        return {"data": [{"url": "https://example.com/image.png"}]}

    monkeypatch.setattr(image_tools.client, client_method, mock_request)
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    properties = tools[tool_name].inputSchema["properties"]

    assert "async" in properties
    assert "async_" not in properties

    result = await mcp.call_tool(tool_name, {**arguments, "async": False})

    assert result
    assert captured_payload["async"] is False


@pytest.mark.asyncio
async def test_openai_generate_image_preserves_explicit_sync(monkeypatch):
    """Callers can opt out of the default async submission when the API supports it."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"data": [{"url": "https://example.com/image.png"}]}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(
        prompt="a panda",
        model="gpt-image-1",
        async_=False,
    )

    assert captured_payload["async"] is False


def test_openai_image_tool_schemas_expose_exact_gpt_image_2_5_models():
    tools = {tool.name: tool for tool in mcp._tool_manager.list_tools()}
    expected = {
        "gpt-image-2.5-flare",
        "gpt-image-2.5-flare:official",
        "gpt-image-2.5-sunburst",
        "gpt-image-2.5-sunburst:official",
    }
    for name in ("openai_generate_image", "openai_edit_image"):
        model_schema = tools[name].parameters["properties"]["model"]
        models = set(model_schema["enum"])
        assert expected <= models
        assert "gpt-image-2.5" not in models
        assert "gpt-image-2.5:official" not in models
        assert "gpt-image-2.5:reverse" not in models


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model",
    [
        "gpt-image-2.5-flare",
        "gpt-image-2.5-flare:official",
        "gpt-image-2.5-sunburst",
        "gpt-image-2.5-sunburst:official",
    ],
)
async def test_openai_image_tools_forward_gpt_image_2_5_models(monkeypatch, model):
    generated: dict[str, object] = {}
    edited: dict[str, object] = {}

    async def mock_generate(**kwargs):
        generated.update(kwargs)
        return {"task_id": "generated"}

    async def mock_edit(**kwargs):
        edited.update(kwargs)
        return {"task_id": "edited"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_generate)
    monkeypatch.setattr(image_tools.client, "images_edits", mock_edit)
    await image_tools.openai_generate_image(prompt="a circle", model=model)
    await image_tools.openai_edit_image(
        image="https://example.com/source.png", prompt="make it red", model=model
    )
    assert generated["model"] == model
    assert edited["model"] == model
