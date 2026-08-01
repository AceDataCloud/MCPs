"""Polling throttle for Digital Human task retrieval."""

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_get_task_throttles_while_running(monkeypatch) -> None:
    slept: list[float] = []

    async def mock_get_task(_task_id, **_kwargs):
        return {"task_id": "t-1", "state": "processing"}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.digitalhuman_get_task(task_id="t-1")

    assert slept == [5]


@pytest.mark.asyncio
async def test_get_task_returns_immediately_when_complete(monkeypatch) -> None:
    slept: list[float] = []

    async def mock_get_task(_task_id, **_kwargs):
        return {"task_id": "t-1", "state": "succeed", "video_url": "https://example.com/v.mp4"}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(task_tools.client, "get_task", mock_get_task)
    monkeypatch.setattr(task_tools.asyncio, "sleep", fake_sleep)

    await task_tools.digitalhuman_get_task(task_id="t-1")

    assert slept == []
