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
