from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from core.server import mcp
from core.types import MinimaxContent
from tools import video_tools


@pytest.fixture
def generated_response():
    return {"task_id": "task-1", "started_at": 1}


@pytest.mark.asyncio
async def test_generation_tool_schemas_expose_async_default():
    tools = {tool.name: tool for tool in await mcp.list_tools()}

    for name in (
        "minimax_generate_video_from_text",
        "minimax_generate_video_from_images",
        "minimax_generate_video_from_audio",
        "minimax_generate_video",
    ):
        properties = tools[name].inputSchema["properties"]
        assert properties["async"]["default"] is True
        assert "async_" not in properties


@pytest.mark.asyncio
async def test_fastmcp_dispatch_maps_public_async_parameter(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    result = await mcp.call_tool(
        "minimax_generate_video_from_text",
        {"prompt": "fox", "async": False},
    )

    assert result
    assert generate.await_args.kwargs["async"] is False


@pytest.mark.asyncio
async def test_fastmcp_dispatch_applies_async_default(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    result = await mcp.call_tool("minimax_generate_video_from_text", {"prompt": "fox"})

    assert result
    assert generate.await_args.kwargs["async"] is True


@pytest.mark.asyncio
async def test_text_tool_payload(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    result = await video_tools.minimax_generate_video_from_text("fox", duration=6)

    assert "task-1" in result
    generate.assert_awaited_once_with(
        model="MiniMax-H3",
        content=[{"type": "text", "text": "fox"}],
        resolution="2K",
        ratio="16:9",
        duration=6,
        **{"async": True},
    )


@pytest.mark.asyncio
async def test_text_tool_can_request_synchronous_response(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    await video_tools.minimax_generate_video_from_text("fox", async_=False)

    generate.assert_awaited_once_with(
        model="MiniMax-H3",
        content=[{"type": "text", "text": "fox"}],
        resolution="2K",
        ratio="16:9",
        duration=4,
        **{"async": False},
    )


@pytest.mark.asyncio
async def test_image_tool_single_image_uses_first_frame(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    await video_tools.minimax_generate_video_from_images(
        ["https://cdn.test/one.png"], prompt="move"
    )

    generate.assert_awaited_once_with(
        model="MiniMax-H3",
        content=[
            {"type": "text", "text": "move"},
            {
                "type": "image_url",
                "image_url": {"url": "https://cdn.test/one.png"},
                "role": "first_frame",
            },
        ],
        resolution="2K",
        ratio="16:9",
        duration=4,
        **{"async": True},
    )


@pytest.mark.asyncio
async def test_image_tool_multiple_images_uses_reference(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    await video_tools.minimax_generate_video_from_images(
        ["https://cdn.test/one.png", "https://cdn.test/two.png"], prompt="move"
    )

    generate.assert_awaited_once_with(
        model="MiniMax-H3",
        content=[
            {"type": "text", "text": "move"},
            {
                "type": "image_url",
                "image_url": {"url": "https://cdn.test/one.png"},
                "role": "reference_image",
            },
            {
                "type": "image_url",
                "image_url": {"url": "https://cdn.test/two.png"},
                "role": "reference_image",
            },
        ],
        resolution="2K",
        ratio="16:9",
        duration=4,
        **{"async": True},
    )


@pytest.mark.asyncio
async def test_audio_tool_payload(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    await video_tools.minimax_generate_video_from_audio(
        ["https://cdn.test/beat.mp3"], ["https://cdn.test/one.png"], "dance"
    )

    generate.assert_awaited_once_with(
        model="MiniMax-H3",
        content=[
            {"type": "text", "text": "dance"},
            {
                "type": "image_url",
                "image_url": {"url": "https://cdn.test/one.png"},
                "role": "reference_image",
            },
            {
                "type": "audio_url",
                "audio_url": {"url": "https://cdn.test/beat.mp3"},
                "role": "reference_audio",
            },
        ],
        resolution="2K",
        ratio="16:9",
        duration=4,
        **{"async": True},
    )


@pytest.mark.asyncio
async def test_full_schema_tool_payload(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    await video_tools.minimax_generate_video(
        [
            MinimaxContent(type="text", text="animate this"),
            MinimaxContent(
                type="video_url",
                video_url={"url": "https://cdn.test/source.mp4"},
                role="reference_video",
            ),
        ],
        ratio="adaptive",
    )

    generate.assert_awaited_once_with(
        model="MiniMax-H3",
        content=[
            {"type": "text", "text": "animate this"},
            {
                "type": "video_url",
                "video_url": {"url": "https://cdn.test/source.mp4"},
                "role": "reference_video",
            },
        ],
        resolution="2K",
        ratio="adaptive",
        duration=4,
        **{"async": True},
    )


def test_content_schema_rejects_extra_fields():
    with pytest.raises(ValidationError):
        MinimaxContent(type="text", text="animate this", unexpected=True)


@pytest.mark.parametrize(
    ("kwargs", "error_match"),
    [
        ({"type": "text"}, "text is required"),
        ({"type": "image_url"}, "image_url is required"),
        (
            {"type": "video_url", "video_url": {"url": "https://cdn.test/source.mp4"}},
            "role is required and must be 'reference_video'",
        ),
        (
            {"type": "audio_url", "audio_url": {"url": "https://cdn.test/source.mp3"}},
            "role is required and must be 'reference_audio'",
        ),
    ],
)
def test_content_schema_enforces_openapi_required_fields(kwargs, error_match):
    with pytest.raises(ValidationError, match=error_match):
        MinimaxContent(**kwargs)
