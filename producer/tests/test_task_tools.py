"""Unit tests for Producer task tools."""

import json

import pytest

from tools import task_tools


@pytest.mark.asyncio
async def test_producer_get_tasks_batch_returns_api_json(monkeypatch):
    """Batch task lookups should preserve the API response schema."""
    payload = {
        "count": 1,
        "items": [
            {
                "id": "task-123",
                "state": "complete",
                "created_at": 1705788000.0,
                "started_at": "2026-04-05T00:00:05.000Z",
                "finished_at": 1705788060.0,
                "elapsed": 60.0,
                "response": {
                    "success": True,
                    "data": [{"title": "Test Song", "audio_url": "https://cdn.example.com/test.mp3"}],
                },
            }
        ],
    }

    async def fake_query_task(**_kwargs):
        return payload

    monkeypatch.setattr(task_tools.client, "query_task", fake_query_task)

    result = await task_tools.producer_get_tasks_batch(task_ids=["task-123"])

    assert json.loads(result) == payload
