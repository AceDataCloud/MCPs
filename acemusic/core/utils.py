"""Result formatting with explicit, bounded polling guidance."""

import json
from typing import Any

SUCCESS = {"succeeded", "completed", "complete"}
FAILURE = {"failed", "error", "cancelled", "canceled", "partial_failed"}


def task_state(data: dict[str, Any]) -> str:
    """Use group state; an individual audio URL is not completion."""
    state = str(data.get("state") or data.get("status") or "").lower()
    response = data.get("response")
    if not isinstance(response, dict):
        response = data
    if state in SUCCESS | FAILURE:
        return state
    response_state = str(response.get("state") or response.get("status") or "").lower()
    if response_state in SUCCESS | FAILURE:
        return response_state
    if response.get("success") is False:
        return "failed"
    if response.get("success") is True and response.get("data"):
        return "succeeded"
    return state or "pending"


def format_result(data: dict[str, Any], *, submission: bool = False) -> str:
    """Keep the API payload while advising clients to query the same task."""
    result = dict(data)
    state = task_state(result)
    task_id = result.get("task_id") or result.get("id")
    if task_id:
        terminal = state in SUCCESS | FAILURE
        result["mcp_task_polling"] = {
            "task_id": task_id,
            "state": state,
            "terminal_state_reached": terminal,
            "should_poll": not terminal,
            "poll_tool": "acemusic_get_task",
            "polling_interval_seconds": 10,
            "next_step": (
                "Present the terminal result, including partial failure details. Do not generate again."
                if terminal
                else "Save this task ID. Wait 10 seconds, then query the same task. On a client wait timeout, keep this ID for recovery; do not submit a replacement."
            ),
        }
        if submission and not terminal:
            result["mcp_task_polling"]["submission_accepted"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)
