"""Polling guidance tests for Digital Human MCP."""

import json

from core.utils import format_task_result, format_video_result, format_voice_result


def test_pending_video_submission_requests_poll() -> None:
    result = json.loads(format_video_result({"task_id": "task-1", "state": "processing"}))

    assert result["mcp_async_submission"]["should_poll"] is True


def test_completed_voice_submission_skips_poll_guidance() -> None:
    result = json.loads(
        format_voice_result({"task_id": "task-1", "voice_id": "voice-1", "state": "succeed"})
    )

    assert "mcp_async_submission" not in result


def test_pending_task_requests_another_poll() -> None:
    result = json.loads(format_task_result({"task_id": "task-1"}))

    assert result["mcp_task_polling"]["should_poll"] is True
    assert result["mcp_task_polling"]["state"] == "pending"


def test_completed_task_stops_polling() -> None:
    result = json.loads(
        format_task_result(
            {
                "task_id": "task-1",
                "state": "succeed",
                "video_url": "https://cdn.example.com/video.mp4",
            }
        )
    )

    assert result["mcp_task_polling"]["should_poll"] is False
    assert result["mcp_task_polling"]["is_complete"] is True


def test_failed_task_stops_polling() -> None:
    result = json.loads(format_task_result({"task_id": "task-1", "state": "failed"}))

    assert result["mcp_task_polling"]["should_poll"] is False
    assert result["mcp_task_polling"]["is_failed"] is True
