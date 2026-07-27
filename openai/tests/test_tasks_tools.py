"""Unit tests for tasks tools."""

import json

import pytest

from tools import tasks_tools


@pytest.mark.asyncio
async def test_openai_list_tasks_accepts_images_type(monkeypatch):
    """openai_list_tasks should forward the 'images' type filter to the API."""
    captured_payload: dict[str, object] = {}

    async def mock_tasks(**kwargs):
        captured_payload.update(kwargs)
        return {"items": [], "count": 0}

    monkeypatch.setattr(tasks_tools.client, "tasks", mock_tasks)

    response = await tasks_tools.openai_list_tasks(type="images")

    assert captured_payload["action"] == "retrieve_batch"
    assert captured_payload["type"] == "images"
    assert json.loads(response) == {"items": [], "count": 0}


@pytest.mark.asyncio
async def test_openai_get_task_throttles_while_running(monkeypatch):
    """An unfinished task should back off so pollers don't spin."""
    slept: list[float] = []

    async def mock_tasks(**_kwargs):
        return {"id": "t-1", "finished_at": None}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(tasks_tools.client, "tasks", mock_tasks)
    monkeypatch.setattr(tasks_tools.asyncio, "sleep", fake_sleep)

    await tasks_tools.openai_get_task(id="t-1")

    assert slept == [5]


@pytest.mark.asyncio
async def test_openai_get_task_returns_immediately_when_finished(monkeypatch):
    """A finished task must not add latency."""
    slept: list[float] = []

    async def mock_tasks(**_kwargs):
        return {"id": "t-1", "finished_at": 1785123456.0, "response": {"data": []}}

    async def fake_sleep(seconds):
        slept.append(seconds)

    monkeypatch.setattr(tasks_tools.client, "tasks", mock_tasks)
    monkeypatch.setattr(tasks_tools.asyncio, "sleep", fake_sleep)

    result = await tasks_tools.openai_get_task(id="t-1")

    assert slept == []
    assert json.loads(result)["finished_at"] == 1785123456.0
