"""Tool payload tests for Happy Horse MCP."""

import json
from unittest.mock import AsyncMock, patch

from tools.task_tools import happyhorse_get_task, happyhorse_get_tasks_batch
from tools.video_tools import (
    happyhorse_edit_video,
    happyhorse_generate_video,
    happyhorse_generate_video_from_image,
    happyhorse_generate_video_from_references,
)


async def test_text_to_video_payload() -> None:
    with patch("tools.video_tools.client.generate_video", new_callable=AsyncMock) as generate:
        generate.return_value = {"task_id": "task-1"}
        result = await happyhorse_generate_video(
            prompt="A horse crossing a snowy ridge",
            resolution="720P",
            ratio="9:16",
            duration=8,
            seed=42,
        )

    generate.assert_awaited_once_with(
        {
            "action": "generate",
            "model": "happyhorse-1.1-t2v",
            "prompt": "A horse crossing a snowy ridge",
            "ratio": "9:16",
            "resolution": "720P",
            "duration": 8,
            "watermark": False,
            "seed": 42,
        }
    )
    assert json.loads(result)["mcp_async_submission"]["poll_tool"] == "happyhorse_get_task"


async def test_image_to_video_prompt_is_optional() -> None:
    with patch("tools.video_tools.client.generate_video", new_callable=AsyncMock) as generate:
        generate.return_value = {"task_id": "task-2"}
        await happyhorse_generate_video_from_image("https://example.com/frame.jpg")

    generate.assert_awaited_once_with(
        {
            "action": "image_to_video",
            "model": "happyhorse-1.1-i2v",
            "image_url": "https://example.com/frame.jpg",
            "prompt": None,
            "resolution": "1080P",
            "duration": 5,
            "watermark": False,
        }
    )


async def test_reference_generation_validates_image_limit() -> None:
    result = await happyhorse_generate_video_from_references(
        "Use character1",
        [f"https://example.com/{index}.jpg" for index in range(10)],
    )

    assert result == "Error: image_urls must contain between 1 and 9 URLs."


async def test_video_edit_omits_ignored_generation_fields() -> None:
    with patch("tools.video_tools.client.generate_video", new_callable=AsyncMock) as generate:
        generate.return_value = {"task_id": "task-3"}
        await happyhorse_edit_video(
            "Keep the camera motion and change the costume",
            "https://example.com/source.mp4",
            image_urls=["https://example.com/style.jpg"],
            audio_setting="origin",
        )

    generate.assert_awaited_once_with(
        {
            "action": "video_edit",
            "model": "happyhorse-1.0-video-edit",
            "prompt": "Keep the camera motion and change the costume",
            "video_url": "https://example.com/source.mp4",
            "resolution": "1080P",
            "audio_setting": "origin",
            "watermark": False,
            "image_urls": ["https://example.com/style.jpg"],
        }
    )


async def test_task_tools_delegate_to_client() -> None:
    with (
        patch("tools.task_tools.client.get_task", new_callable=AsyncMock) as get_task,
        patch("tools.task_tools.client.get_tasks_batch", new_callable=AsyncMock) as get_batch,
    ):
        get_task.return_value = {"id": "task-1"}
        get_batch.return_value = {"items": [], "count": 0}
        await happyhorse_get_task("task-1")
        await happyhorse_get_tasks_batch(["task-1", "task-2"])

    get_task.assert_awaited_once_with("task-1")
    get_batch.assert_awaited_once_with(["task-1", "task-2"])
