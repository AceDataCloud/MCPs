"""Polling throttle for maestro task retrieval."""

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_get_task_throttles_while_unfinished(monkeypatch):
    slept: list[float] = []

    async def mock_get_task(_task_id):
        return {"id": "t-1", "finished_at": None}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.maestro_get_task(task_id="t-1")

    assert slept == [5]


@pytest.mark.asyncio
@pytest.mark.parametrize("response", [{}, {"error": "failed"}, {"success": False}])
async def test_get_task_returns_immediately_when_finished(monkeypatch, response):
    slept: list[float] = []

    async def mock_get_task(_task_id):
        return {"id": "t-1", "finished_at": 1, "response": response}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.maestro_get_task(task_id="t-1")

    assert slept == []
