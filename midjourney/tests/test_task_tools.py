"""Unit tests for Midjourney task tools."""

import json

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_midjourney_get_tasks_batch_returns_api_json(monkeypatch):
    """Batch task lookups should preserve the API response schema."""
    payload = {
        "count": 1,
        "items": [
            {
                "id": "task-123",
                "created_at": "2025-01-21T00:00:00.000Z",
                "started_at": "2025-01-21T00:00:05.000Z",
                "finished_at": 1737417660.0,
                "elapsed": 55.0,
                "response": {"success": True, "image_url": "https://cdn.midjourney.com/test.png"},
            }
        ],
    }

    async def fake_query_task(**_kwargs):
        return payload

    monkeypatch.setattr(task_tools.client, "query_task", fake_query_task)

    result = await task_tools.midjourney_get_tasks_batch(task_ids=["task-123"])

    assert json.loads(result) == payload
