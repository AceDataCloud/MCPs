"""Formatting helpers for MCP WebExtrator server."""

import json
from typing import Any

POLL_TOOL = "webextrator_get_task"
BATCH_POLL_TOOL = "webextrator_get_tasks_batch"

_POLLING_INTERVAL_SECONDS = 10
_MAX_POLL_ATTEMPTS = 30
_EXPECTED_WAIT_SECONDS = 180


def _task_outcome(payload: dict[str, Any]) -> tuple[bool, bool]:
    """Return (is_complete, is_failed) for an async extract/render task.

    The worker stamps `finished_at` once the job settles — on success *and* on
    failure — so it alone decides whether polling should stop. `response.error`
    then tells the two terminal outcomes apart.
    """
    if payload.get("finished_at") is None:
        return False, False

    response = payload.get("response")
    response = response if isinstance(response, dict) else {}
    failed = bool(response.get("error")) or response.get("success") is False
    return not failed, failed


def _with_submission_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("task_id") or payload.get("id")
    if not task_id:
        return payload

    # mode="sync" returns the finished result inline (already carries
    # `finished_at` + `data`). Telling the model to poll that would be wrong.
    is_complete, is_failed = _task_outcome(payload)
    if is_complete or is_failed:
        return payload

    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": POLL_TOOL,
        "batch_poll_tool": BATCH_POLL_TOOL,
        "recommended_action": "poll",
        "should_poll": True,
        "terminal_state_reached": False,
        "polling_interval_seconds": _POLLING_INTERVAL_SECONDS,
        "max_poll_attempts": _MAX_POLL_ATTEMPTS,
        "expected_wait_seconds": _EXPECTED_WAIT_SECONDS,
        "next_step": (
            f'Call {POLL_TOOL}(task_id="{task_id}") until the task reports a '
            f"`finished_at` timestamp, then read the extracted content from its `response`. "
            f"Wait at least {_POLLING_INTERVAL_SECONDS} seconds between polls and keep "
            f"polling for up to {_MAX_POLL_ATTEMPTS} attempts — do NOT stop early or "
            f"tell the user it failed while the task is still running."
        ),
    }
    return payload


def _with_task_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
    if not task_id:
        return payload

    is_complete, is_failed = _task_outcome(payload)
    should_poll = not (is_complete or is_failed)

    if is_complete:
        next_step = "Task is complete. Stop polling and use the extracted content from `response`."
    elif is_failed:
        next_step = (
            "Task failed. Stop polling and report the error to the user. "
            "Polling again will not change the outcome."
        )
    else:
        next_step = (
            f"The task is still running. Wait {_POLLING_INTERVAL_SECONDS} seconds, then call "
            f'{POLL_TOOL}(task_id="{task_id}") again. '
            f"Keep polling — do NOT give up or tell the user it failed."
        )

    payload["mcp_task_polling"] = {
        "task_id": task_id,
        "poll_tool": POLL_TOOL,
        "batch_poll_tool": BATCH_POLL_TOOL,
        "recommended_action": "poll" if should_poll else "stop",
        "should_poll": should_poll,
        "terminal_state_reached": not should_poll,
        "is_complete": is_complete,
        "is_failed": is_failed,
        "polling_interval_seconds": _POLLING_INTERVAL_SECONDS,
        "max_poll_attempts": _MAX_POLL_ATTEMPTS,
        "next_step": next_step,
    }
    return payload


def format_submission_result(data: dict[str, Any]) -> str:
    """Serialize an async submission response with polling guidance."""
    return json.dumps(_with_submission_guidance(data), ensure_ascii=False, indent=2)


def format_task_result(data: dict[str, Any]) -> str:
    """Serialize a task query response with polling guidance."""
    return json.dumps(_with_task_guidance(data), ensure_ascii=False, indent=2)
