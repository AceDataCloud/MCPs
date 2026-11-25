import json
from unittest.mock import AsyncMock, patch

import pytest

from core.server import mcp
from core.utils import format_task_result
from tools import task_tools
from tools.image_tools import qwen_image_edit, qwen_image_generate


def test_generate_schema_matches_openapi_constraints() -> None:
    tool = next(
        tool for tool in mcp._tool_manager.list_tools() if tool.name == "qwen_image_generate"
    )
    properties = tool.parameters["properties"]

    assert properties["prompt"]["minLength"] == 1
    assert properties["prompt"]["maxLength"] == 18000
    assert properties["size"]["anyOf"][0]["pattern"] == r"^[0-9]+\*[0-9]+$"
    assert properties["callback_url"]["anyOf"][0]["format"] == "uri"


@pytest.mark.asyncio
async def test_generate_payload() -> None:
    with patch(
        "tools.image_tools.client.generate_image", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await qwen_image_generate("cat", n=2, size="1024*1024", seed=7)
        payload = call.call_args.kwargs
        assert payload["model"] == "qwen-image-3.0" and payload["n"] == 2 and payload["seed"] == 7


@pytest.mark.asyncio
async def test_edit_payload() -> None:
    with patch(
        "tools.image_tools.client.generate_image", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await qwen_image_edit(
            "restyle",
            ["https://example.com/a.png"],
            model="qwen-image-3.0-pro",
            prompt_extend_mode="agent",
        )
        assert call.call_args.kwargs["image_urls"] == ["https://example.com/a.png"]
        assert call.call_args.kwargs["prompt_extend_mode"] == "agent"


@pytest.mark.asyncio
async def test_batch_task_result_preserves_json_shape(monkeypatch) -> None:
    async def mock_query_task(**_kwargs):
        return {
            "items": [{"id": "task-1", "response": {"success": True}}],
            "count": 1,
            "extra": "preserved",
        }

    monkeypatch.setattr(task_tools.client, "query_task", mock_query_task)

    result = await task_tools.qwen_image_get_tasks_batch(["task-1"])

    assert '"items"' in result
    assert '"count": 1' in result
    assert '"extra": "preserved"' in result


@pytest.mark.parametrize(
    ("finished_at", "should_poll", "is_failed"),
    [(None, True, False), (1234567890, False, True)],
)
def test_false_success_needs_finished_at_for_terminal_failure(
    finished_at: int | None, should_poll: bool, is_failed: bool
) -> None:
    result = json.loads(
        format_task_result(
            {"id": "task-1", "finished_at": finished_at, "response": {"success": False}}
        )
    )
    guidance = result["mcp_task_polling"]
    assert guidance["should_poll"] is should_poll
    assert guidance["is_failed"] is is_failed
    assert guidance["terminal_state_reached"] is not should_poll


@pytest.mark.asyncio
async def test_pending_false_success_throttles_polling(monkeypatch) -> None:
    result = {"id": "task-1", "finished_at": None, "response": {"success": False}}
    query = AsyncMock(return_value=result)
    sleep = AsyncMock()
    monkeypatch.setattr(task_tools.client, "query_task", query)
    monkeypatch.setattr(task_tools.asyncio, "sleep", sleep)

    formatted = json.loads(await task_tools.qwen_image_get_task("task-1"))

    sleep.assert_awaited_once_with(5)
    assert formatted["mcp_task_polling"]["recommended_action"] == "poll"
