"""Formatting helpers for Digital Human MCP tool results."""

import json
from typing import Any

POLL_TOOL = "digitalhuman_get_task"
BATCH_POLL_TOOL = "digitalhuman_get_tasks_batch"


def _is_video_complete(data: dict[str, Any]) -> bool:
    state = str(data.get("state", "")).lower()
    return bool(data.get("video_url")) or state in {"succeed", "succeeded", "success", "completed"}


def _is_voice_complete(data: dict[str, Any]) -> bool:
    state = str(data.get("state", "")).lower()
    return bool(data.get("voice_id")) or state in {"succeed", "succeeded", "success", "completed"}


def _with_submission_guidance(
    data: dict[str, Any],
    *,
    complete_predicate: Any,
) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("task_id")
    if not task_id or complete_predicate(payload):
        return payload
    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": POLL_TOOL,
        "batch_poll_tool": BATCH_POLL_TOOL,
        "should_poll": True,
        "polling_interval_seconds": 15,
        "next_step": (
            f'Wait 15 seconds, then call {POLL_TOOL}(task_id="{task_id}"). '
            "Keep polling until the task reaches a terminal state."
        ),
    }
    return payload


def _task_state(data: dict[str, Any]) -> tuple[str, bool, bool]:
    state = str(data.get("state", "")).lower()
    if state in {"failed", "error", "cancelled", "canceled"}:
        return state, False, True
    complete = _is_video_complete(data) or _is_voice_complete(data)
    if complete:
        return state or "succeed", True, False
    return state or "pending", False, False


def is_task_settled(data: dict[str, Any]) -> bool:
    """True once the task reached a terminal state."""
    _, complete, failed = _task_state(data)
    return complete or failed


def _with_task_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("task_id")
    if not task_id:
        return payload
    state, complete, failed = _task_state(payload)
    should_poll = not (complete or failed)
    payload["mcp_task_polling"] = {
        "task_id": task_id,
        "poll_tool": POLL_TOOL,
        "batch_poll_tool": BATCH_POLL_TOOL,
        "state": state,
        "should_poll": should_poll,
        "terminal_state_reached": not should_poll,
        "is_complete": complete,
        "is_failed": failed,
        "polling_interval_seconds": 15,
        "next_step": (
            "Stop polling and present the final result to the user."
            if complete
            else (
                "Stop polling and report the task failure."
                if failed
                else f'Wait 15 seconds, then call {POLL_TOOL}(task_id="{task_id}") again.'
            )
        ),
    }
    return payload


def format_video_result(data: dict[str, Any]) -> str:
    """Serialize a video submission with polling guidance when needed."""
    return json.dumps(
        _with_submission_guidance(data, complete_predicate=_is_video_complete),
        ensure_ascii=False,
        indent=2,
    )


def format_voice_result(data: dict[str, Any]) -> str:
    """Serialize a voice-clone submission with polling guidance when needed."""
    return json.dumps(
        _with_submission_guidance(data, complete_predicate=_is_voice_complete),
        ensure_ascii=False,
        indent=2,
    )


def format_task_result(data: dict[str, Any]) -> str:
    """Serialize one task with terminal-state guidance."""
    return json.dumps(_with_task_guidance(data), ensure_ascii=False, indent=2)


def format_batch_task_result(data: dict[str, Any]) -> str:
    """Serialize a batch task response."""
    return json.dumps(data, ensure_ascii=False, indent=2)
