"""Unit tests for image tools."""

import json

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
