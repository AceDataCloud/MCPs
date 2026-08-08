"""Unit tests for MiniMax task tools."""

import asyncio
import json
from unittest.mock import AsyncMock

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_list_tasks_passes_documented_filters(monkeypatch):
    query = AsyncMock(return_value={"items": [], "total": 0})
    monkeypatch.setattr(task_tools.client, "query_task", query)

    result = await task_tools.minimax_list_tasks(
        limit=10, offset=5, created_at_min=1000, created_at_max=2000
    )

    assert json.loads(result) == {"items": [], "total": 0}
    query.assert_awaited_once_with(
        action="retrieve", limit=10, offset=5, created_at_min=1000, created_at_max=2000
    )


@pytest.mark.asyncio
async def test_get_succeeded_task_does_not_sleep(monkeypatch):
    query = AsyncMock(return_value={"task": {"id": "task-1", "status": "succeeded"}})
    sleep = AsyncMock()
    monkeypatch.setattr(task_tools.client, "query_task", query)
    monkeypatch.setattr(asyncio, "sleep", sleep)

    await task_tools.minimax_get_task("task-1")

    sleep.assert_not_awaited()
