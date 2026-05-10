"""Utility functions for MCP Fish server."""

import json
from typing import Any


def _with_submission_guidance(
    data: dict[str, Any], poll_tool: str, batch_poll_tool: str | None = None
) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("task_id")
    if not task_id:
        return payload

    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": poll_tool,
        "batch_poll_tool": batch_poll_tool,
        "polling_interval_seconds": 5,
        "max_poll_attempts": 100,
        "expected_wait_seconds": 60,
        "next_step": (
            f'Call {poll_tool}(task_id="{task_id}") to poll until the task completes '
            f"and the final audio URL is available. "
            f"IMPORTANT: Audio generation typically takes a few seconds to a minute. "
            f"Wait at least 5 seconds between each poll. "
            f"Keep polling for up to 100 attempts. Do NOT stop early — the task is still running."
        ),
    }
    return payload


def _with_task_guidance(
    data: dict[str, Any], poll_tool: str, batch_poll_tool: str | None = None
) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
    if not task_id:
        return payload

    payload["mcp_task_polling"] = {
        "task_id": task_id,
        "poll_tool": poll_tool,
        "batch_poll_tool": batch_poll_tool,
        "polling_interval_seconds": 5,
        "max_poll_attempts": 100,
        "next_step": (
            f"The task is still pending or processing. "
            f'Wait 5 seconds, then call {poll_tool}(task_id="{task_id}") again. '
            f"IMPORTANT: Audio generation typically takes a few seconds to a minute. "
            f"Keep polling — do NOT give up or tell the user it failed. "
            f"You should poll at least 100 times before considering the task stuck."
        ),
    }
    return payload


def format_audio_result(data: dict[str, Any]) -> str:
    """Format audio generation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "fish_get_task", "fish_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_voice_result(data: dict[str, Any]) -> str:
    """Format voice creation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "fish_get_task", "fish_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_task_result(data: dict[str, Any]) -> str:
    """Format task query result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_task_guidance(data, "fish_get_task", "fish_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_batch_task_result(data: dict[str, Any]) -> str:
    """Format batch task query result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(data, ensure_ascii=False, indent=2)
