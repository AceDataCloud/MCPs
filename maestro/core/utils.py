"""Formatting helpers for MCP tool results."""

import json
from typing import Any

POLL_TOOL = "maestro_get_task"
# maestro_list_tasks takes no ids filter, so it cannot poll one task — advertise none.
BATCH_POLL_TOOL = None

# States that mean "still working". Anything else (succeeded, failed, dead, or
# a status we don't know yet) is treated as terminal — an unknown state must
# not strand the caller in an endless poll loop.
IN_FLIGHT_STATES = {"queued", "pending", "planning", "producing", "running", "processing"}
_FAILED_STATES = {"failed", "dead", "cancelled", "canceled", "error"}

_POLLING_INTERVAL_SECONDS = 30
# Cover the worker's own ceiling: AGENT_TIMEOUT=5400s plus queue wait before it
# starts. Giving up at 60 min would abandon renders that are still alive.
_MAX_POLL_ATTEMPTS = 220
_EXPECTED_WAIT_SECONDS = 5400


def _task_outcome(payload: dict[str, Any]) -> tuple[bool, bool, bool]:
    """Return (is_in_flight, is_complete, is_failed) from the task `status`."""
    status = str(payload.get("status", "")).lower()
    if status in IN_FLIGHT_STATES:
        return True, False, False
    return False, status == "succeeded", status in _FAILED_STATES


def _with_task_guidance(data: dict[str, Any]) -> dict[str, Any]:
    payload = dict(data)
    task_id = payload.get("id") or payload.get("task_id")
    if not task_id:
        return payload

    in_flight, is_complete, is_failed = _task_outcome(payload)
    status = str(payload.get("status", "")).lower()

    if is_complete:
        next_step = "Task is complete. Stop polling and present the final video URL to the user."
    elif is_failed:
        next_step = (
            f"Task reached terminal state '{status}'. Stop polling and report the failure "
            f"to the user. Polling again will not change the outcome."
        )
    elif in_flight:
        next_step = (
            f"The task is still running (status '{status}'). Wait {_POLLING_INTERVAL_SECONDS} "
            f'seconds, then call {POLL_TOOL}(task_id="{task_id}") again. '
            f"Video production commonly takes 10-90 minutes — keep polling and do NOT "
            f"give up or tell the user it failed."
        )
    else:
        # Unknown status: stop rather than loop on a state we can't interpret.
        next_step = (
            f"Task reports an unrecognized status '{status}'. Stop polling and surface the "
            f"raw task payload to the user instead of guessing."
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
        "status": status,
        "polling_interval_seconds": _POLLING_INTERVAL_SECONDS,
        "max_poll_attempts": _MAX_POLL_ATTEMPTS,
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
        "max_poll_attempts": _MAX_POLL_ATTEMPTS,
        "expected_wait_seconds": _EXPECTED_WAIT_SECONDS,
        "next_step": (
            f'Call {POLL_TOOL}(task_id="{task_id}") until its status leaves the in-flight set '
            f"({', '.join(sorted(IN_FLIGHT_STATES))}). "
            f"Video production commonly takes 10-90 minutes. "
            f"Wait at least {_POLLING_INTERVAL_SECONDS} seconds between polls and keep polling "
            f"for up to {_MAX_POLL_ATTEMPTS} attempts — do NOT stop early or tell the user it "
            f"failed while the task is still running."
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
