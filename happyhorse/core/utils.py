"""Formatting helpers for Happy Horse MCP tool results."""

import json
from typing import Any

POLL_TOOL = "happyhorse_get_task"
BATCH_POLL_TOOL = "happyhorse_get_tasks_batch"


def _with_submission_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("task_id")
    if not task_id:
        return payload
    payload["mcp_async_submission"] = {
        "task_id": task_id,
        "poll_tool": POLL_TOOL,
        "batch_poll_tool": BATCH_POLL_TOOL,
        "should_poll": True,
        "polling_interval_seconds": 15,
        "next_step": (
            f'Wait 15 seconds, then call {POLL_TOOL}(task_id="{task_id}"). '
            "Keep polling until the response contains the final video_url or a terminal error."
        ),
    }
    return payload


def _task_state(data: dict[str, Any]) -> tuple[str, bool, bool]:
    response = data.get("response")
    response_data = response.get("data") if isinstance(response, dict) else None
    items = response_data if isinstance(response_data, list) else []
    item_states = {str(item.get("state", "")).lower() for item in items if isinstance(item, dict)}
    state = str(data.get("state") or data.get("status") or "").lower()
    if "error" in item_states or state in {"failed", "error", "cancelled", "canceled"}:
        return state or "error", False, True
    has_video = any(isinstance(item, dict) and item.get("video_url") for item in items)
    complete = (
        has_video
        or "succeeded" in item_states
        or state
        in {
            "complete",
            "completed",
            "succeeded",
            "success",
        }
    )
    return state or ("succeeded" if complete else "pending"), complete, False


def _with_task_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
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
            "Stop polling and present the final video_url to the user."
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
    """Serialize a video submission with polling guidance."""
    return json.dumps(_with_submission_guidance(data), ensure_ascii=False, indent=2)


def format_task_result(data: dict[str, Any]) -> str:
    """Serialize one task with terminal-state guidance."""
    return json.dumps(_with_task_guidance(data), ensure_ascii=False, indent=2)


def format_batch_task_result(data: dict[str, Any]) -> str:
    """Serialize a batch task response."""
    return json.dumps(data, ensure_ascii=False, indent=2)
