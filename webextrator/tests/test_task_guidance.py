"""Polling-guidance blocks attached to webextrator task responses."""

import json

from core.utils import format_task_result

_RUNNING = {"id": "t-1", "finished_at": None, "response": None}
_DONE = {
    "id": "t-1",
    "started_at": 1785136969.95,
    "finished_at": 1785136982.29,
    "elapsed": 12.34,
    "response": {"success": True},
}
_FAILED = {
    "id": "t-1",
    "finished_at": 1785137086.22,
    "response": {"success": False, "error": {"code": "bad_request", "message": "nope"}},
}


def _guidance(payload):
    return json.loads(format_task_result(payload))["mcp_task_polling"]


def test_running_task_keeps_polling():
    block = _guidance(_RUNNING)
    assert block["should_poll"] is True
    assert block["recommended_action"] == "poll"


def test_completed_task_stops():
    payload = json.loads(format_task_result(_DONE))
    block = payload["mcp_task_polling"]
    assert block["should_poll"] is False
    assert block["is_complete"] is True
    assert payload["started_at"] == 1785136969.95
    assert payload["elapsed"] == 12.34


def test_failed_task_stops_instead_of_polling_forever():
    """A failed task carries `finished_at`; polling it again cannot help."""
    block = _guidance(_FAILED)
    assert block["should_poll"] is False
    assert block["is_failed"] is True


def test_payload_without_id_is_left_untouched():
    assert "mcp_task_polling" not in json.loads(format_task_result({"error": "nope"}))


def test_sync_mode_result_is_not_told_to_poll():
    """mode="sync" returns the finished result inline — it must not advertise polling.

    Shape from the worker's buildSuccess(): task_id is present even though the
    task already settled, so a task_id-only guard would wrongly attach guidance.
    """
    from core.utils import format_submission_result

    sync_payload = {
        "success": True,
        "task_id": "t-1",
        "finished_at": 1785137086.22,
        "elapsed": 3.1,
        "data": {"title": "hello"},
    }
    assert "mcp_async_submission" not in json.loads(format_submission_result(sync_payload))


def test_async_submission_still_gets_guidance():
    from core.utils import format_submission_result

    payload = json.loads(format_submission_result({"task_id": "t-2"}))
    assert payload["mcp_async_submission"]["should_poll"] is True
