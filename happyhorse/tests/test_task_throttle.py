"""Polling throttle for happyhorse task retrieval."""

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_get_task_throttles_while_running(monkeypatch):
    slept: list[float] = []

    async def mock_get_task(_task_id):
        return {"id": "t-1", "state": "processing", "response": {"data": []}}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.happyhorse_get_task(task_id="t-1")

    assert slept == [5]


@pytest.mark.asyncio
async def test_get_task_returns_immediately_when_complete(monkeypatch):
    slept: list[float] = []

    async def mock_get_task(_task_id):
        return {
            "id": "t-1",
            "state": "succeeded",
            "response": {"data": [{"video_url": "https://example.com/v.mp4"}]},
        }

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.happyhorse_get_task(task_id="t-1")

    assert slept == []


@pytest.mark.asyncio
async def test_get_task_returns_immediately_when_failed(monkeypatch):
    """A failed task is terminal — don't keep sleeping on it."""
    slept: list[float] = []

    async def mock_get_task(_task_id):
        return {"id": "t-1", "state": "failed", "response": {"data": []}}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.happyhorse_get_task(task_id="t-1")

    assert slept == []
