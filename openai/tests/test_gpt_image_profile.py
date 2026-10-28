"""Exercise the real narrowed MCP dispatch without sending a paid API request."""

import json
from unittest.mock import AsyncMock, patch

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from gpt_image_tools import GPT_IMAGE_MODELS, create_server
from tools import image_tools, tasks_tools


@pytest.mark.asyncio
async def test_profile_only_discovers_image_and_task_tools():
    tools = await create_server().list_tools()
    assert {tool.name for tool in tools} == {
        "gpt_image_generate",
        "gpt_image_edit",
        "gpt_image_get_task",
        "gpt_image_list_tasks",
        "gpt_image_list_models",
    }
    for tool in tools:
        if tool.name in {"gpt_image_generate", "gpt_image_edit"}:
            assert tool.inputSchema["properties"]["model"]["enum"] == list(GPT_IMAGE_MODELS)
            assert "model" in tool.inputSchema["required"]
            assert "async" in tool.inputSchema["properties"]
            assert "async_" not in tool.inputSchema["properties"]


@pytest.mark.asyncio
async def test_dispatch_preserves_model_async_and_task_submission():
    client = image_tools.client
    response = {"task_id": "existing-fixture", "status": "pending"}
    with patch.object(
        client, "images_generations_async", new=AsyncMock(return_value=response)
    ) as call:
        await create_server().call_tool(
            "gpt_image_generate", {"prompt": "fixture", "model": "gpt-image-2", "async": True}
        )
        assert call.call_args.kwargs["model"] == "gpt-image-2"
        assert call.call_args.kwargs["async"] is True


@pytest.mark.asyncio
async def test_other_models_and_missing_model_fail_before_api():
    with patch.object(image_tools.client, "images_generations_async", new=AsyncMock()) as call:
        for arguments in ({"prompt": "fixture", "model": "nano-banana"}, {"prompt": "fixture"}):
            with pytest.raises(ToolError):
                await create_server().call_tool("gpt_image_generate", arguments)
        call.assert_not_awaited()


@pytest.mark.asyncio
async def test_edit_preserves_ordered_image_list_and_public_alias():
    images = ["https://example.test/base.png", "https://example.test/ref.png"]
    with patch.object(
        image_tools.client, "images_edits_async", new=AsyncMock(return_value={"task_id": "same-id"})
    ) as call:
        await create_server().call_tool(
            "gpt_image_edit",
            {"image": images, "prompt": "fixture", "model": "gpt-image-2", "async": True},
        )
        assert call.call_args.kwargs["image"] == images
        assert call.call_args.kwargs["async"] is True


@pytest.mark.asyncio
async def test_static_model_listing_does_not_request_generation():
    with patch.object(image_tools.client, "images_generations_async", new=AsyncMock()) as call:
        content = await create_server().call_tool("gpt_image_list_models", {})
        assert "gpt-image-2" in json.dumps(content, default=str)
        call.assert_not_awaited()


@pytest.mark.asyncio
async def test_task_query_reuses_same_id_and_preserves_terminal_response():
    response = {
        "id": "original-task",
        "finished_at": "2026-10-18T00:00:00Z",
        "response": {"data": []},
    }
    with patch.object(tasks_tools.client, "tasks", new=AsyncMock(return_value=response)) as call:
        result = await create_server().call_tool("gpt_image_get_task", {"id": "original-task"})
        call.assert_awaited_once_with(action="retrieve", id="original-task")
        assert "original-task" in json.dumps(result, default=str)
