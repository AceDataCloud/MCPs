"""Polling-guidance blocks attached to Maestro task responses."""

import json

import pytest

from core.utils import format_submission_result, format_task_result


def _guidance(payload):
    return json.loads(format_task_result(payload))["mcp_task_polling"]


@pytest.mark.parametrize("status", ["queued", "pending", "planning", "producing", "running"])
def test_in_flight_states_keep_polling(status):
    block = _guidance({"id": "t-1", "status": status})
    assert block["should_poll"] is True
    assert block["recommended_action"] == "poll"


def test_succeeded_stops():
    block = _guidance({"id": "t-1", "status": "succeeded"})
    assert block["should_poll"] is False
    assert block["is_complete"] is True


@pytest.mark.parametrize("status", ["failed", "dead", "cancelled"])
def test_terminal_failures_stop(status):
    block = _guidance({"id": "t-1", "status": status})
    assert block["should_poll"] is False
    assert block["is_failed"] is True


def test_unknown_status_stops_rather_than_looping():
    """An unrecognized status must not strand the model in an endless poll."""
    block = _guidance({"id": "t-1", "status": "brand-new-state"})
    assert block["should_poll"] is False
    assert block["is_complete"] is False
    assert block["is_failed"] is False
    assert "unrecognized status" in block["next_step"]


def test_submission_carries_polling_instructions():
    block = json.loads(format_submission_result({"task_id": "t-9"}))["mcp_async_submission"]
    assert block["poll_tool"] == "maestro_get_task"
    assert block["should_poll"] is True


def test_payload_without_id_is_left_untouched():
    assert "mcp_task_polling" not in json.loads(format_task_result({"error": "nope"}))


def test_batch_poll_tool_is_not_advertised():
    """Maestro has no documented batch-retrieval task API."""
    block = _guidance({"id": "t-1", "status": "running"})
    assert block["batch_poll_tool"] is None


def test_poll_budget_covers_the_worker_timeout():
    """AGENT_TIMEOUT is 5400s; the advertised budget must not give up sooner."""
    block = _guidance({"id": "t-1", "status": "running"})
    assert block["max_poll_attempts"] * block["polling_interval_seconds"] >= 5400
