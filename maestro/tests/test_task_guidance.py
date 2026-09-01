"""Polling-guidance blocks attached to Maestro task responses."""

import json

import pytest

from core.utils import format_submission_result, format_task_result


def _guidance(payload):
    return json.loads(format_task_result(payload))["mcp_task_polling"]


def test_unfinished_task_keeps_polling():
    block = _guidance({"id": "t-1", "finished_at": None})
    assert block["should_poll"] is True
    assert block["recommended_action"] == "poll"


def test_finished_task_stops():
    block = _guidance({"id": "t-1", "finished_at": 1, "response": {}})
    assert block["should_poll"] is False
    assert block["is_complete"] is True


@pytest.mark.parametrize("response", [{"error": "failed"}, {"success": False}])
def test_finished_task_failures_stop(response):
    block = _guidance({"id": "t-1", "finished_at": 1, "response": response})
    assert block["should_poll"] is False
    assert block["is_failed"] is True


def test_submission_carries_polling_instructions():
    block = json.loads(format_submission_result({"task_id": "t-9"}))["mcp_async_submission"]
    assert block["poll_tool"] == "maestro_get_task"
    assert block["should_poll"] is True


def test_payload_without_id_is_left_untouched():
    assert "mcp_task_polling" not in json.loads(format_task_result({"error": "nope"}))


def test_batch_poll_tool_is_not_advertised():
    """Maestro has no documented batch-retrieval task API."""
    block = _guidance({"id": "t-1", "finished_at": None})
    assert block["batch_poll_tool"] is None


def test_polling_has_no_fixed_attempt_budget():
    block = _guidance({"id": "t-1", "finished_at": None})
    assert "max_poll_attempts" not in block
    assert block["expected_wait_seconds"] == 10800
