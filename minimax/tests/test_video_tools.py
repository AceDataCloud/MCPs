from unittest.mock import AsyncMock

import pytest

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
        model="minimax-h3",
        prompt="fox",
        resolution="2K",
        ratio="16:9",
        duration=6,
        aigc_watermark=False,
    )


@pytest.mark.asyncio
async def test_image_tool_payload(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    await video_tools.minimax_generate_video_from_images(
        ["https://cdn.test/one.png", "https://cdn.test/two.png"], prompt="move"
    )

    generate.assert_awaited_once_with(
        model="minimax-h3",
        prompt="move",
        resolution="2K",
        ratio="16:9",
        duration=4,
        aigc_watermark=False,
        image_urls=["https://cdn.test/one.png", "https://cdn.test/two.png"],
    )


@pytest.mark.asyncio
async def test_audio_tool_payload(monkeypatch, generated_response):
    generate = AsyncMock(return_value=generated_response)
    monkeypatch.setattr(video_tools.client, "generate_video", generate)

    await video_tools.minimax_generate_video_from_audio(
        ["https://cdn.test/beat.mp3"], ["https://cdn.test/one.png"], "dance"
    )

    generate.assert_awaited_once_with(
        model="minimax-h3",
        prompt="dance",
        resolution="2K",
        ratio="16:9",
        duration=4,
        aigc_watermark=False,
        audio_urls=["https://cdn.test/beat.mp3"],
        image_urls=["https://cdn.test/one.png"],
    )
