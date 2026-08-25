"""Unit tests for video tools."""

import json

import pytest

from core.server import mcp
from core.types import MediaItem
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


@pytest.mark.asyncio
async def test_wan3_media_parameters_are_forwarded(monkeypatch):
    """Wan 3 parameters must be represented in the API payload."""
    captured_payload: dict[str, object] = {}

    async def mock_generate_video(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "task-wan3"}

    monkeypatch.setattr(video_tools.client, "generate_video", mock_generate_video)

    await video_tools.wan_generate_video(
        model="wan3.0-video",
        prompt="Animate the supplied first frame.",
        duration=30,
        media=[MediaItem(type="first_frame", url="https://example.com/frame.png")],
        ratio="16:9",
        seed=42,
        watermark=True,
    )

    assert captured_payload == {
        "action": "text2video",
        "model": "wan3.0-video",
        "prompt": "Animate the supplied first frame.",
        "resolution": "720P",
        "audio": False,
        "prompt_extend": False,
        "duration": 30,
        "media": [{"type": "first_frame", "url": "https://example.com/frame.png"}],
        "ratio": "16:9",
        "seed": 42,
        "watermark": True,
    }


@pytest.mark.asyncio
async def test_wan3_all_in_one_omits_absent_media(monkeypatch):
    """Optional media should be omitted from the API payload when absent."""
    captured_payload: dict[str, object] = {}

    async def mock_generate_video(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "task-wan3"}

    monkeypatch.setattr(video_tools.client, "generate_video", mock_generate_video)

    await video_tools.wan_generate_video_all_in_one(prompt="Generate from text only.", media=None)

    assert "media" not in captured_payload
