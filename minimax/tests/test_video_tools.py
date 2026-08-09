from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from core.types import MinimaxContent
from tools import video_tools


@pytest.fixture
def generated_response():
    return {"task_id": "task-1", "started_at": 1}


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
    )


@pytest.mark.asyncio
async def test_image_tool_payload(monkeypatch, generated_response):
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
                "role": "first_frame",
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
                "role": "first_frame",
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
    )


def test_content_schema_rejects_extra_fields():
    with pytest.raises(ValidationError):
        MinimaxContent(type="text", text="animate this", unexpected=True)
