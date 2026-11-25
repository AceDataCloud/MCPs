"""Unit tests for task tools."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from tools.task_tools import suno_get_task, suno_get_tasks_batch


class TestGetTaskTool:
    @pytest.mark.asyncio
    async def test_success_response_without_state_does_not_sleep(self):
        task = {
            "id": "complete-task",
            "state": "",
            "response": {"success": True, "data": [{"id": "audio-1"}]},
        }
        with (
            patch("tools.task_tools.client.query_task", new=AsyncMock(return_value=task)),
            patch("tools.task_tools.asyncio.sleep", new=AsyncMock()) as mock_sleep,
        ):
            result = await suno_get_task(task_id="complete-task")

        mock_sleep.assert_not_awaited()
        assert '"state": "complete"' in result
        assert '"should_poll": false' in result

    @pytest.mark.asyncio
    async def test_failed_response_does_not_sleep(self):
        task = {
            "id": "failed-task",
            "state": "",
            "response": {
                "success": False,
                "error": {"code": "bad_request", "message": "prompt is required"},
            },
        }
        with (
            patch("tools.task_tools.client.query_task", new=AsyncMock(return_value=task)),
            patch("tools.task_tools.asyncio.sleep", new=AsyncMock()) as mock_sleep,
        ):
            result = await suno_get_task(task_id="failed-task")

        mock_sleep.assert_not_awaited()
        assert '"state": "failed"' in result
        assert '"should_poll": false' in result

    @pytest.mark.asyncio
    async def test_batch_marks_response_success_as_complete(self):
        response = {
            "count": 1,
            "items": [
                {
                    "id": "complete-task",
                    "state": "",
                    "response": {
                        "success": True,
                        "data": [{"title": "Done", "audio_url": "https://example.com/a.mp3"}],
                    },
                }
            ],
        }
        with patch(
            "tools.task_tools.client.query_task",
            new=AsyncMock(return_value=response),
        ):
            result = await suno_get_tasks_batch(task_ids=["complete-task"])

        item = json.loads(result)["items"][0]
        assert item["mcp_task_polling"]["is_complete"] is True
        assert item["response"]["data"][0]["audio_url"] == "https://example.com/a.mp3"
        assert item["mcp_task_polling"]["should_poll"] is False

    @pytest.mark.asyncio
    async def test_batch_marks_response_error_as_failed(self):
        response = {
            "count": 1,
            "items": [
                {
                    "id": "failed-task",
                    "state": "",
                    "response": {
                        "success": False,
                        "error": {"code": "bad_request", "message": "prompt is required"},
                    },
                }
            ],
        }
        with patch(
            "tools.task_tools.client.query_task",
            new=AsyncMock(return_value=response),
        ):
            result = await suno_get_tasks_batch(task_ids=["failed-task"])

        item = json.loads(result)["items"][0]
        assert item["mcp_task_polling"]["is_failed"] is True
        assert item["response"]["error"]["code"] == "bad_request"
        assert item["mcp_task_polling"]["should_poll"] is False


async def test_batch_preserves_model_project_and_media_result_shapes():
    data = [
        {
            "id": "model-task",
            "response": {"success": True, "data": {"id": "model", "status": "ready"}},
        },
        {
            "id": "project-task",
            "response": {
                "success": True,
                "data": {"id": "project", "version_id": "new", "candidates": [{"id": "candidate"}]},
            },
        },
        {
            "id": "midi-task",
            "response": {"success": True, "data": [{"midi_url": "https://example.com/song.mid"}]},
        },
    ]
    with patch(
        "tools.task_tools.client.query_task",
        new=AsyncMock(return_value={"items": data, "count": 3}),
    ):
        result = json.loads(await suno_get_tasks_batch([item["id"] for item in data]))
    assert result["count"] == 3
    for original, returned in zip(data, result["items"], strict=True):
        assert returned["response"] == original["response"]
        assert returned["mcp_task_polling"]["should_poll"] is False


@pytest.mark.parametrize("success", [False, True])
async def test_explicit_unfinished_task_keeps_polling(success):
    task = {"id": "running", "finished_at": None, "response": {"success": success, "data": []}}
    with (
        patch("tools.task_tools.client.query_task", new=AsyncMock(return_value=task)),
        patch("tools.task_tools.asyncio.sleep", new=AsyncMock()) as sleep,
    ):
        result = json.loads(await suno_get_task("running"))
    sleep.assert_awaited_once_with(5)
    assert result["mcp_task_polling"]["should_poll"] is True
    assert result["mcp_task_polling"]["terminal_state_reached"] is False


async def test_new_project_task_without_response_keeps_polling():
    task = {"id": "project-task", "finished_at": None, "response": None}
    with (
        patch("tools.task_tools.client.query_task", new=AsyncMock(return_value=task)),
        patch("tools.task_tools.asyncio.sleep", new=AsyncMock()) as sleep,
    ):
        result = json.loads(await suno_get_task("project-task"))
    sleep.assert_awaited_once_with(5)
    assert result["response"] is None
    assert result["mcp_task_polling"]["should_poll"] is True
