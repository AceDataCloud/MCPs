"""Polling guidance tests for Happy Horse MCP."""

import json

from core.utils import format_task_result


def test_pending_task_requests_another_poll() -> None:
    result = json.loads(format_task_result({"id": "task-1", "request": {}}))

    assert result["mcp_task_polling"]["should_poll"] is True
    assert result["mcp_task_polling"]["state"] == "pending"


def test_completed_task_stops_polling() -> None:
    result = json.loads(
        format_task_result(
            {
                "id": "task-1",
                "response": {
                    "success": True,
                    "data": [
                        {
                            "state": "succeeded",
                            "video_url": "https://cdn.example.com/video.mp4",
                        }
                    ],
                },
            }
        )
    )

    assert result["mcp_task_polling"]["should_poll"] is False
    assert result["mcp_task_polling"]["is_complete"] is True


def test_transport_success_does_not_finish_processing_task() -> None:
    result = json.loads(
        format_task_result(
            {
                "id": "task-1",
                "response": {"success": True, "data": [{"state": "processing"}]},
            }
        )
    )

    assert result["mcp_task_polling"]["should_poll"] is True
    assert result["mcp_task_polling"]["is_complete"] is False


def test_failed_task_stops_polling() -> None:
    result = json.loads(
        format_task_result({"id": "task-1", "response": {"data": [{"state": "error"}]}})
    )

    assert result["mcp_task_polling"]["should_poll"] is False
    assert result["mcp_task_polling"]["is_failed"] is True
