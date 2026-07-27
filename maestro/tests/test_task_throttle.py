"""Polling throttle for maestro task retrieval."""

import pytest

from tools import task_tools


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["queued", "planning", "producing"])
async def test_get_task_throttles_while_running(monkeypatch, status):
    slept: list[float] = []

    async def mock_get_task(_task_id):
        return {"id": "t-1", "status": status}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.maestro_get_task(task_id="t-1")

    assert slept == [5]


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["succeeded", "failed", "dead", "brand-new-state"])
async def test_get_task_returns_immediately_when_settled(monkeypatch, status):
    """Terminal AND unknown states return now — never strand the caller."""
    slept: list[float] = []

    async def mock_get_task(_task_id):
        return {"id": "t-1", "status": status}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.maestro_get_task(task_id="t-1")

    assert slept == []
