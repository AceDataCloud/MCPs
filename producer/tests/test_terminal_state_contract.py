"""Regression tests for Producer task terminal-state guidance."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from core.utils import format_task_result
from tools.task_tools import producer_get_task, producer_get_tasks_batch


def test_response_success_without_state_is_complete():
    result = json.loads(
        format_task_result({"id": "done", "state": "", "response": {"success": True, "data": []}})
    )
    guidance = result["mcp_task_polling"]
    assert guidance["state"] == "complete"
    assert guidance["is_complete"] is True
    assert guidance["should_poll"] is False


def test_response_failure_without_state_is_failed():
    result = json.loads(
        format_task_result(
            {"id": "failed", "state": "", "response": {"success": False, "error": {"code": "bad"}}}
        )
    )
    guidance = result["mcp_task_polling"]
    assert guidance["state"] == "failed"
    assert guidance["is_failed"] is True
    assert guidance["should_poll"] is False


@pytest.mark.asyncio
async def test_failed_task_does_not_sleep():
    task = {"id": "failed", "state": "", "response": {"success": False}}
    with (
        patch("tools.task_tools.client.query_task", new=AsyncMock(return_value=task)),
        patch("tools.task_tools.asyncio.sleep", new=AsyncMock()) as sleep,
    ):
        await producer_get_task(task_id="failed")
    sleep.assert_not_awaited()


@pytest.mark.asyncio
async def test_batch_normalizes_empty_states():
    response = {
        "count": 2,
        "items": [
            {"id": "done", "state": "", "response": {"success": True, "data": []}},
            {"id": "failed", "state": "", "response": {"success": False, "error": {"code": "bad"}}},
        ],
    }
    with patch("tools.task_tools.client.query_task", new=AsyncMock(return_value=response)):
        result = await producer_get_tasks_batch(task_ids=["done", "failed"])
    assert "State: complete" in result
    assert "State: failed" in result
    assert "keep polling" not in result
