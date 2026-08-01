"""Tool payload tests for Digital Human MCP."""

import json
from unittest.mock import AsyncMock, patch

from tools.task_tools import (
    digitalhuman_delete_task,
    digitalhuman_get_task,
    digitalhuman_get_tasks_batch,
)
from tools.video_tools import digitalhuman_create_video
from tools.voice_tools import digitalhuman_clone_voice


async def test_create_video_payload() -> None:
    with patch("tools.video_tools.client.create_video", new_callable=AsyncMock) as create_video:
        create_video.return_value = {"task_id": "task-1"}
        result = await digitalhuman_create_video(
            video_url="https://example.com/face.mp4",
            audio_url="https://example.com/voice.mp3",
            guidance=1.5,
            steps=30,
            seam_fix=False,
            speed=1.2,
        )

    create_video.assert_awaited_once_with(
        {
            "video_url": "https://example.com/face.mp4",
            "image_url": None,
            "audio_url": "https://example.com/voice.mp3",
            "text": None,
            "voice_id": None,
            "engine": "latentsync",
            "guidance": 1.5,
            "steps": 30,
            "seam_fix": False,
            "speed": 1.2,
            "resolution": "720p",
            "callback_url": None,
            "async": None,
        }
    )
    assert json.loads(result)["mcp_async_submission"]["poll_tool"] == "digitalhuman_get_task"


async def test_create_video_requires_exactly_one_face_source() -> None:
    result = await digitalhuman_create_video(
        video_url="https://example.com/face.mp4",
        image_url="https://example.com/face.jpg",
        audio_url="https://example.com/voice.mp3",
    )

    assert "exactly one of video_url or image_url" in result


async def test_create_video_requires_voice_id_with_text() -> None:
    result = await digitalhuman_create_video(
        image_url="https://example.com/face.jpg",
        text="Hello world",
    )

    assert "voice_id is required" in result


async def test_clone_voice_payload() -> None:
    with patch("tools.voice_tools.client.clone_voice", new_callable=AsyncMock) as clone_voice:
        clone_voice.return_value = {"voice_id": "voice-1", "state": "succeed"}
        result = await digitalhuman_clone_voice(
            audio_url="https://example.com/sample.wav",
            lang="en",
            async_=True,
        )

    clone_voice.assert_awaited_once_with(
        {
            "audio_url": "https://example.com/sample.wav",
            "lang": "en",
            "name": None,
            "async": True,
        }
    )
    assert json.loads(result)["voice_id"] == "voice-1"


async def test_task_tools_delegate_to_client() -> None:
    with (
        patch("tools.task_tools.client.get_task", new_callable=AsyncMock) as get_task,
        patch("tools.task_tools.client.get_tasks_batch", new_callable=AsyncMock) as get_batch,
        patch("tools.task_tools.client.delete_task", new_callable=AsyncMock) as delete_task,
    ):
        get_task.return_value = {"task_id": "task-1", "state": "succeed", "video_url": "url"}
        get_batch.return_value = {"items": [], "count": 0}
        delete_task.return_value = {"success": True}
        await digitalhuman_get_task("task-1", action="retrieve")
        await digitalhuman_get_tasks_batch(["task-1", "task-2"])
        await digitalhuman_delete_task("task-3")

    get_task.assert_awaited_once_with("task-1", action="retrieve")
    get_batch.assert_awaited_once_with(["task-1", "task-2"])
    delete_task.assert_awaited_once_with("task-3")
