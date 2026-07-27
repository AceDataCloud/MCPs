"""Polling throttle for fish task retrieval."""

import json

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_get_task_throttles_while_running(monkeypatch):
    """The worker only stamps finished_at once the job settles."""
    slept: list[float] = []

    async def mock_query(**_kwargs):
        return {"id": "t-1", "finished_at": None}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "query_task", mock_query)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.fish_get_task(task_id="t-1")

    assert slept == [5]


@pytest.mark.asyncio
async def test_get_task_returns_immediately_when_finished(monkeypatch):
    slept: list[float] = []

    async def mock_query(**_kwargs):
        return {"id": "t-1", "finished_at": 1785131515.0, "response": {}}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "query_task", mock_query)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    result = json.loads(await task_tools.fish_get_task(task_id="t-1"))

    assert slept == []
    assert result["finished_at"] == 1785131515.0


@pytest.mark.asyncio
async def test_get_task_reports_missing_task(monkeypatch):
    async def mock_query(**_kwargs):
        return {}

    monkeypatch.setattr(task_tools.client, "query_task", mock_query)

    result = json.loads(await task_tools.fish_get_task(task_id="nope"))

    assert result["error"] == "Task not found"
