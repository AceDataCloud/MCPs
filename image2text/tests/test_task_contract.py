"""Authenticated task polling keeps processing and terminal result contracts."""

import json
from unittest.mock import AsyncMock

import httpx
import pytest

import tools  # noqa: F401
from core.client import Image2TextClient, set_request_api_token
from core.server import mcp
from tools import task_tools


@pytest.mark.asyncio
@pytest.mark.parametrize("context_token", [None, "request-token"])
async def test_task_http_uses_bearer_and_keeps_timeout_result(monkeypatch, context_token):
    captured = {}
    terminal = {
        "success": False,
        "task_id": "task-1",
        "status": "failed",
        "error": {"code": "timeout", "message": "Task timed out"},
    }

    async def request(_client, method, url, **kwargs):
        captured.update(kwargs)
        captured["method"] = method
        captured["url"] = url
        return httpx.Response(504, json=terminal, request=httpx.Request(method, url))

    monkeypatch.setattr(httpx.AsyncClient, "request", request)
    set_request_api_token(context_token)
    try:
        result = await Image2TextClient(api_token="configured-token").get_task("task-1")
    finally:
        set_request_api_token(None)
    assert result == terminal
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/captcha/tasks")
    assert captured["json"] == {"task_id": "task-1"}
    assert captured["headers"]["authorization"] == f"Bearer {context_token or 'configured-token'}"


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["processing", "ready", "failed"])
async def test_task_tool_returns_state_and_throttles_only_processing(monkeypatch, status):
    response = {"task_id": "task-1", "status": status, "text": "result"}
    request = AsyncMock(return_value=response)
    sleep = AsyncMock()
    monkeypatch.setattr(task_tools.client, "get_task", request)
    monkeypatch.setattr(task_tools.asyncio, "sleep", sleep)
    content, _ = await mcp.call_tool("image2text_get_task", {"task_id": "task-1"})
    assert json.loads(content[0].text) == response
    request.assert_awaited_once_with(task_id="task-1")
    if status == "processing":
        sleep.assert_awaited_once_with(3)
    else:
        sleep.assert_not_awaited()
