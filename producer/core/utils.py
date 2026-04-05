"""Utility functions for MCP Producer server."""

import json
from typing import Any


def _with_submission_guidance(
    data: dict[str, Any],
    poll_tool: str,
    batch_poll_tool: str | None = None,
) -> dict[str, Any]:
    """Attach MCP polling guidance to async submission responses."""
    payload = dict(data)
    task_id = payload.get("task_id")
    if not task_id:
        return payload

    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": poll_tool,
        "batch_poll_tool": batch_poll_tool,
        "next_step": (
            f'Call {poll_tool}(task_id="{task_id}") to poll until '
            f"the task completes and the final media URLs are available."
        ),
    }
    return payload


def _with_task_guidance(
    data: dict[str, Any],
    poll_tool: str,
    batch_poll_tool: str | None = None,
) -> dict[str, Any]:
    """Attach MCP polling guidance to task lookup responses."""
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
    if not task_id:
        return payload

    payload["mcp_task_polling"] = {
        "task_id": task_id,
        "poll_tool": poll_tool,
        "batch_poll_tool": batch_poll_tool,
        "next_step": (
            f"If the task is still pending or processing, call "
            f'{poll_tool}(task_id="{task_id}") again later.'
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
        _with_submission_guidance(data, "producer_get_task", "producer_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_lyrics_result(data: dict[str, Any]) -> str:
    """Format lyrics generation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "producer_get_task", "producer_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_upload_result(data: dict[str, Any]) -> str:
    """Format upload result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "producer_get_task", "producer_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_video_result(data: dict[str, Any]) -> str:
    """Format video generation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "producer_get_task", "producer_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )


def format_wav_result(data: dict[str, Any]) -> str:
    """Format WAV generation result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_submission_guidance(data, "producer_get_task", "producer_get_tasks_batch"),
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


def format_task_result(data: dict[str, Any]) -> str:
    """Format task query result as JSON.

    Args:
        data: API response dictionary

    Returns:
        JSON string representation of the result
    """
    return json.dumps(
        _with_task_guidance(data, "producer_get_task", "producer_get_tasks_batch"),
        ensure_ascii=False,
        indent=2,
    )
