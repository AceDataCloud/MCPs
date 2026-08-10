"""Unit tests for NanoBanana image tools."""

import json

import pytest

from tools import image_tools


@pytest.mark.asyncio
async def test_generate_image_forwards_count_and_callback(monkeypatch, mock_image_response):
    captured_payload: dict[str, object] = {}

    async def mock_generate_image_async(**kwargs):
        captured_payload.update(kwargs)
        return mock_image_response

    monkeypatch.setattr(image_tools.client, "generate_image_async", mock_generate_image_async)

    response = await image_tools.nanobanana_generate_image(
        prompt="test",
        count=2,
        callback_url="https://example.com/callback",
    )

    assert captured_payload["count"] == 2
    assert captured_payload["callback_url"] == "https://example.com/callback"
    assert json.loads(response)["task_id"] == "test-task-123"


@pytest.mark.asyncio
async def test_edit_image_forwards_count_and_callback(monkeypatch, mock_image_response):
    captured_payload: dict[str, object] = {}

    async def mock_edit_image_async(**kwargs):
        captured_payload.update(kwargs)
        return mock_image_response

    monkeypatch.setattr(image_tools.client, "edit_image_async", mock_edit_image_async)

    response = await image_tools.nanobanana_edit_image(
        prompt="test",
        image_urls=["https://example.com/image.png"],
        count=2,
        callback_url="https://example.com/callback",
    )

    assert captured_payload["count"] == 2
    assert captured_payload["callback_url"] == "https://example.com/callback"
    assert json.loads(response)["task_id"] == "test-task-123"
