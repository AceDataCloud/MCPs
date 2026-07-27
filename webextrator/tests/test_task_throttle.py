"""Polling throttle for webextrator task retrieval."""

import json

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_get_task_throttles_while_running(monkeypatch):
    """An unfinished task backs off so pollers don't spin."""
    slept: list[float] = []

    async def mock_query(**_kwargs):
        return {"id": "t-1", "finished_at": None}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "query_tasks", mock_query)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.webextrator_get_task(task_id="t-1")

    assert slept == [5]


@pytest.mark.asyncio
async def test_get_task_returns_immediately_when_finished(monkeypatch):
    """A settled task must not add latency."""
    slept: list[float] = []

    async def mock_query(**_kwargs):
        return {"id": "t-1", "finished_at": "2026-07-27T00:00:00Z", "response": {}}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "query_tasks", mock_query)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    result = await task_tools.webextrator_get_task(task_id="t-1")

    assert slept == []
    assert json.loads(result)["finished_at"] == "2026-07-27T00:00:00Z"


@pytest.mark.asyncio
async def test_get_task_reports_missing_task(monkeypatch):
    """An unknown id reads as 'not found', not as a transport failure."""

    async def mock_query(**_kwargs):
        return {}

    monkeypatch.setattr(task_tools.client, "query_tasks", mock_query)

    result = json.loads(await task_tools.webextrator_get_task(task_id="nope"))

    assert result["error"] == "Task not found"
