"""Polling-guidance blocks attached to submission and task responses."""

import json

from core.utils import format_submission_result, format_task_result

# Shape taken from a real production task (id cb4faeda…): the worker stamps
# `finished_at` on success *and* on failure, so the failure case must stop.
_RUNNING = {"id": "t-1", "finished_at": None, "response": None}
_DONE = {
    "id": "t-1",
    "finished_at": 1785136982.296123,
    "response": {"success": True, "data": [{"url": "https://cdn.example/img.png"}]},
}
_FAILED = {
    "id": "t-1",
    "finished_at": 1785137086.2247078,
    "response": {
        "success": False,
        "error": {
            "code": "bad_request",
            "message": "size width and height must be multiples of 16",
        },
    },
}


def _guidance(payload):
    return json.loads(format_task_result(payload))["mcp_task_polling"]


def test_running_task_tells_the_model_to_keep_polling():
    block = _guidance(_RUNNING)
    assert block["should_poll"] is True
    assert block["terminal_state_reached"] is False
    assert block["recommended_action"] == "poll"
    assert block["polling_interval_seconds"] == 15


def test_completed_task_tells_the_model_to_stop():
    block = _guidance(_DONE)
    assert block["should_poll"] is False
    assert block["is_complete"] is True
    assert block["is_failed"] is False
    assert block["recommended_action"] == "stop"


def test_failed_task_stops_instead_of_polling_forever():
    """A failed task carries `finished_at`; polling it again cannot help."""
    block = _guidance(_FAILED)
    assert block["should_poll"] is False
    assert block["is_failed"] is True
    assert block["is_complete"] is False
    assert "will not change the outcome" in block["next_step"]


def test_submission_response_carries_polling_instructions():
    payload = json.loads(format_submission_result({"task_id": "t-9"}))
    block = payload["mcp_async_submission"]
    assert block["task_id"] == "t-9"
    assert block["poll_tool"] == "openai_get_task"
    assert block["should_poll"] is True


def test_response_without_task_id_is_left_untouched():
    """Sync/error responses must not grow a bogus polling block."""
    payload = json.loads(format_submission_result({"error": "nope"}))
    assert "mcp_async_submission" not in payload


async def test_throttle_and_guidance_never_disagree(monkeypatch):
    """The 5s sleep and the advertised `should_poll` share one predicate.

    suno/producer drifted by computing these two independently; assert the
    failed task neither sleeps nor advertises further polling.
    """
    from tools import tasks_tools

    slept = []

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(tasks_tools.asyncio, "sleep", fake_sleep)

    for payload, expect_sleep in ((_RUNNING, True), (_DONE, False), (_FAILED, False)):
        slept.clear()

        async def fake_tasks(_bound=payload, **_kwargs):
            return _bound

        monkeypatch.setattr(tasks_tools.client, "tasks", fake_tasks)
        block = json.loads(await tasks_tools.openai_get_task(id="t-1"))["mcp_task_polling"]
        assert bool(slept) is expect_sleep
        assert block["should_poll"] is expect_sleep
