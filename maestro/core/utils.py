"""Formatting helpers for MCP tool results."""

import json
from typing import Any

POLL_TOOL = "maestro_get_task"
# The API only exposes single-task retrieval, so there is no batch poll tool.
BATCH_POLL_TOOL = None

_POLLING_INTERVAL_SECONDS = 30
_EXPECTED_WAIT_SECONDS = 10800


def _task_outcome(payload: dict[str, Any]) -> tuple[bool, bool, bool]:
    """Return (is_in_flight, is_complete, is_failed) from task timestamps."""
    if payload.get("finished_at") is None:
        return True, False, False

    response = payload.get("response")
    response = response if isinstance(response, dict) else {}
    failed = bool(response.get("error")) or response.get("success") is False
    return False, not failed, failed


def _with_task_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
    if not task_id:
        return payload

    in_flight, is_complete, is_failed = _task_outcome(payload)

    if is_complete:
        next_step = "Task is complete. Stop polling and present the final video URL to the user."
    elif is_failed:
        next_step = "Task failed. Stop polling and report the failure to the user."
    else:
        next_step = (
            f"The task is still running. Wait {_POLLING_INTERVAL_SECONDS} "
            f'seconds, then call {POLL_TOOL}(task_id="{task_id}") again. '
            "Video production may use the full three-hour production window plus queue time — "
            "keep polling and do NOT give up or tell the user it failed."
        )

    payload["mcp_task_polling"] = {
        "task_id": task_id,
        "poll_tool": POLL_TOOL,
        "batch_poll_tool": BATCH_POLL_TOOL,
        "recommended_action": "poll" if in_flight else "stop",
        "should_poll": in_flight,
        "terminal_state_reached": not in_flight,
        "is_complete": is_complete,
        "is_failed": is_failed,
        "polling_interval_seconds": _POLLING_INTERVAL_SECONDS,
        "expected_wait_seconds": _EXPECTED_WAIT_SECONDS,
        "next_step": next_step,
    }
    return payload


def _with_submission_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("task_id") or payload.get("id")
    if not task_id:
        return payload

    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": POLL_TOOL,
        "batch_poll_tool": BATCH_POLL_TOOL,
        "recommended_action": "poll",
        "should_poll": True,
        "terminal_state_reached": False,
        "polling_interval_seconds": _POLLING_INTERVAL_SECONDS,
        "expected_wait_seconds": _EXPECTED_WAIT_SECONDS,
        "next_step": (
            f'Call {POLL_TOOL}(task_id="{task_id}") until it reports a `finished_at` timestamp. '
            "Video production may use the full three-hour production window plus queue time. "
            f"Wait at least {_POLLING_INTERVAL_SECONDS} seconds between polls and keep polling — "
            "do NOT stop early or tell the user it failed while the task is still running."
        ),
    }
    return payload


def format_result(data: dict[str, Any]) -> str:
    """Serialize an API response for MCP clients."""
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_submission_result(data: dict[str, Any]) -> str:
    """Serialize a task-creating response with polling guidance."""
    return json.dumps(_with_submission_guidance(data), ensure_ascii=False, indent=2)


def format_task_result(data: dict[str, Any]) -> str:
    """Serialize a task query response with polling guidance."""
    return json.dumps(_with_task_guidance(data), ensure_ascii=False, indent=2)
