"""Unit tests for video tools."""

import json

import pytest

from core.server import mcp
from tools import video_tools


def test_wan_reference_video_schema_requires_url_array():
    """Reference videos must be represented as an array, not a joined string."""
    tool = next(
        tool
        for tool in mcp._tool_manager.list_tools()
        if tool.name == "wan_generate_video_from_image"
    )
    reference_schema = tool.parameters["properties"]["reference_video_urls"]

    assert reference_schema["anyOf"] == [
        {"items": {"type": "string"}, "minItems": 1, "type": "array"},
        {"type": "null"},
    ]
    assert "never join URLs with commas" in reference_schema["description"]
    assert "never JSON-stringify the array" in reference_schema["description"]


@pytest.mark.asyncio
async def test_wan_forwards_reference_video_array(monkeypatch):
    """Reference video URLs must remain an array in the API payload."""
    captured_payload: dict[str, object] = {}

    async def mock_generate_video(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "task-123"}

    monkeypatch.setattr(video_tools.client, "generate_video", mock_generate_video)
    references = [
        " https://example.com/reference-one.mp4 ",
        "https://example.com/reference-two.mp4",
        " ",
    ]

    response = await video_tools.wan_generate_video_from_image(
        prompt="Keep the same character appearance.",
        image_url="https://example.com/start.png",
        model="wan2.6-r2v",
        reference_video_urls=references,
    )

    assert captured_payload["reference_video_urls"] == [
        "https://example.com/reference-one.mp4",
        "https://example.com/reference-two.mp4",
    ]
    assert json.loads(response)["task_id"] == "task-123"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("legacy_value", "expected"),
    [
        (
            "https://example.com/reference-one.mp4, https://example.com/reference-two.mp4",
            [
                "https://example.com/reference-one.mp4",
                "https://example.com/reference-two.mp4",
            ],
        ),
        (
            "https://example.com/reference.mp4?signature=part-one,part-two",
            ["https://example.com/reference.mp4?signature=part-one,part-two"],
        ),
    ],
)
async def test_wan_normalizes_legacy_comma_separated_references(
    monkeypatch, legacy_value, expected
):
    """FastMCP keeps legacy comma strings compatible but sends API arrays."""
    captured_payload: dict[str, object] = {}

    async def mock_generate_video(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "task-legacy"}

    monkeypatch.setattr(video_tools.client, "generate_video", mock_generate_video)
    tool = next(
        tool
        for tool in mcp._tool_manager.list_tools()
        if tool.name == "wan_generate_video_from_image"
    )

    await tool.run(
        {
            "prompt": "Keep the same character appearance.",
            "image_url": "https://example.com/start.png",
            "model": "wan2.6-r2v",
            "reference_video_urls": legacy_value,
        }
    )

    assert captured_payload["reference_video_urls"] == expected
