"""Unit tests for AiChat MCP tool functions."""

import json
from unittest.mock import AsyncMock, patch

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from core.server import mcp
from tools.chat_tools import aichat_create_conversation_v2
from tools.info_tools import aichat_get_usage_guide, aichat_list_models


@pytest.mark.asyncio
async def test_list_models_includes_sol_fast() -> None:
    assert "gpt-5.6-sol-fast" in await aichat_list_models()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "client_method"),
    [
        ("aichat_create_conversation", "create_conversation"),
        ("aichat_create_conversation_v2", "create_conversation_v2"),
    ],
)
async def test_sol_fast_dispatch_preserves_public_alias(
    mock_conversation_response, tool_name, client_method
) -> None:
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    model_schema = tools[tool_name].inputSchema["properties"]["model"]
    assert "gpt-5.6-sol-fast" in model_schema["enum"]
    assert model_schema["default"] == "gpt-4.1"

    with patch(
        f"tools.chat_tools.client.{client_method}",
        new=AsyncMock(return_value=mock_conversation_response),
    ) as mock_request:
        await mcp.call_tool(tool_name, {"question": "hello", "model": "gpt-5.6-sol-fast"})

    assert mock_request.await_args.kwargs["model"] == "gpt-5.6-sol-fast"


@pytest.mark.asyncio
async def test_gemini_argon_discovery_identifies_v2_and_wrapper_limits() -> None:
    listing = await aichat_list_models()
    guide = await aichat_get_usage_guide()
    assert "Gemini endpoint coverage" in listing
    for text in (listing, guide):
        assert "gemini-4-argon" in text
        assert "aichat_create_conversation_v2" in text
        assert "gpt-4.1" in text
    assert "not native Gemini Generate Content or Google" in guide
    assert "does not expose `max_tokens`" in guide


@pytest.mark.asyncio
async def test_gemini_argon_v2_dispatch_preserves_public_model(mock_conversation_response) -> None:
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    properties = tools["aichat_create_conversation_v2"].inputSchema["properties"]
    assert "gemini-4-argon" in properties["model"]["enum"]
    assert properties["model"]["default"] == "gpt-4.1"
    assert not {"max_tokens", "thinking_level", "cached_content"} & properties.keys()
    with patch(
        "tools.chat_tools.client.create_conversation_v2",
        new=AsyncMock(return_value=mock_conversation_response),
    ) as request:
        result = await mcp.call_tool(
            "aichat_create_conversation_v2",
            {"question": "hello", "model": "gemini-4-argon"},
        )
    assert request.await_args.kwargs["model"] == "gemini-4-argon"
    content, _ = result
    assert json.loads(content[0].text) == mock_conversation_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "client_method", "model"),
    [
        ("aichat_create_conversation", "create_conversation", "gemini-4-argon"),
        ("aichat_create_conversation_v2", "create_conversation_v2", "claude-opus-5-5"),
    ],
)
async def test_models_outside_endpoint_contract_fail_before_api(
    tool_name: str, client_method: str, model: str
) -> None:
    with (
        patch(f"tools.chat_tools.client.{client_method}", new=AsyncMock()) as request,
        pytest.raises(ToolError),
    ):
        await mcp.call_tool(tool_name, {"question": "hello", "model": model})
    request.assert_not_awaited()


@pytest.mark.asyncio
async def test_kimi_discovery_identifies_v2_tool_and_keeps_k3_alias() -> None:
    listing = await aichat_list_models()
    guide = await aichat_get_usage_guide()
    assert "Kimi (AiChat v2 only)" in listing
    assert "recommended" not in next(
        line for line in listing.splitlines() if line.startswith("- kimi-k3.1-pro")
    )
    for model in ("kimi-k3.1-pro", "kimi-k3"):
        assert model in listing
        assert model in guide
    assert "aichat_create_conversation_v2" in listing
    assert "does not expose `reasoning_effort`" in guide


@pytest.mark.asyncio
@pytest.mark.parametrize("model", ["kimi-k3.1-pro", "kimi-k3", "kimi-k2.6"])
async def test_kimi_v2_dispatch_preserves_public_alias(model: str) -> None:
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    properties = tools["aichat_create_conversation_v2"].inputSchema["properties"]
    assert model in properties["model"]["enum"]
    assert properties["model"]["default"] == "gpt-4.1"
    assert "reasoning_effort" not in properties
    assert (
        model not in tools["aichat_create_conversation"].inputSchema["properties"]["model"]["enum"]
    )
    with patch(
        "tools.chat_tools.client.create_conversation_v2", new=AsyncMock(return_value={"id": "test"})
    ) as request:
        await mcp.call_tool("aichat_create_conversation_v2", {"question": "hello", "model": model})
    assert request.await_args.kwargs["model"] == model
    assert "reasoning_effort" not in request.await_args.kwargs


@pytest.mark.asyncio
@pytest.mark.parametrize("model", ["kimi-k3.1-pro", "kimi-k2-0905-preview"])
async def test_v1_rejects_kimi_without_api_call(model: str) -> None:
    with (
        patch("tools.chat_tools.client.create_conversation", new=AsyncMock()) as request,
        pytest.raises(ToolError),
    ):
        await mcp.call_tool("aichat_create_conversation", {"question": "hello", "model": model})
    request.assert_not_awaited()


@pytest.mark.asyncio
async def test_v2_rejects_retired_kimi_without_api_call() -> None:
    with (
        patch("tools.chat_tools.client.create_conversation_v2", new=AsyncMock()) as request,
        pytest.raises(ToolError),
    ):
        await mcp.call_tool("aichat_create_conversation_v2", {"model": "kimi-k2-0905-preview"})
    request.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("max_turns", [None, 1, 500])
async def test_v2_agent_turn_limit_dispatch(max_turns: int | None) -> None:
    tool = next(
        tool for tool in await mcp.list_tools() if tool.name == "aichat_create_conversation_v2"
    )
    schema = tool.inputSchema["properties"]["max_turns"]
    integer_schema = next(item for item in schema["anyOf"] if item["type"] == "integer")
    assert integer_schema["minimum"] == 1
    assert integer_schema["maximum"] == 500
    assert "defaults to 500" in schema["description"]
    arguments = {} if max_turns is None else {"max_turns": max_turns}
    with patch(
        "tools.chat_tools.client.create_conversation_v2", new=AsyncMock(return_value={"id": "test"})
    ) as request:
        await mcp.call_tool("aichat_create_conversation_v2", {"question": "hello", **arguments})
    if max_turns is None:
        assert "max_turns" not in request.await_args.kwargs
    else:
        assert request.await_args.kwargs["max_turns"] == max_turns


@pytest.mark.asyncio
@pytest.mark.parametrize("max_turns", [0, 501])
async def test_v2_rejects_out_of_range_turn_limit_without_api_call(max_turns: int) -> None:
    with (
        patch("tools.chat_tools.client.create_conversation_v2", new=AsyncMock()) as request,
        pytest.raises(ToolError),
    ):
        await mcp.call_tool("aichat_create_conversation_v2", {"max_turns": max_turns})
    request.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_conversation_v2_forwards_async_fields() -> None:
    expected = {"id": "conversation-123", "answer": "done"}

    with patch(
        "tools.chat_tools.client.create_conversation_v2",
        new=AsyncMock(return_value=expected),
    ) as mock_create_conversation_v2:
        result = await aichat_create_conversation_v2(
            model="gpt-4.1",
            async_=True,
            callback_url="https://example.com/callback",
            allowed_skills=["web_search"],
            allowed_mcp_servers=["filesystem"],
            unattended_policy={"mode": "auto"},
        )

    assert json.loads(result) == expected
    assert mock_create_conversation_v2.await_args.kwargs["async"] is True
    assert (
        mock_create_conversation_v2.await_args.kwargs["callback_url"]
        == "https://example.com/callback"
    )
    assert mock_create_conversation_v2.await_args.kwargs["allowed_skills"] == ["web_search"]
    assert mock_create_conversation_v2.await_args.kwargs["allowed_mcp_servers"] == ["filesystem"]
    assert mock_create_conversation_v2.await_args.kwargs["unattended_policy"] == {"mode": "auto"}


@pytest.mark.asyncio
@pytest.mark.parametrize(("arguments", "expected"), [({"async": False}, False), ({}, None)])
async def test_fastmcp_dispatch_maps_public_async_parameter(
    arguments: dict[str, bool], expected: bool | None
) -> None:
    expected_response = {"id": "conversation-123", "answer": "done"}
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    properties = tools["aichat_create_conversation_v2"].inputSchema["properties"]

    assert "async" in properties
    assert "async_" not in properties

    with patch(
        "tools.chat_tools.client.create_conversation_v2",
        new=AsyncMock(return_value=expected_response),
    ) as mock_create_conversation_v2:
        result = await mcp.call_tool(
            "aichat_create_conversation_v2",
            {"model": "gpt-4.1", "question": "hello", **arguments},
        )

    assert result
    payload = mock_create_conversation_v2.await_args.kwargs
    if expected is None:
        assert "async" not in payload
    else:
        assert payload["async"] is expected


@pytest.mark.asyncio
async def test_create_conversation_v2_forwards_string_message_payload() -> None:
    expected = {"id": "conversation-123", "answer": "done"}

    with patch(
        "tools.chat_tools.client.create_conversation_v2",
        new=AsyncMock(return_value=expected),
    ) as mock_create_conversation_v2:
        await aichat_create_conversation_v2(
            model="gpt-4.1",
            message="hello",
        )

    assert mock_create_conversation_v2.await_args.kwargs["message"] == "hello"


@pytest.mark.asyncio
async def test_create_conversation_v2_forwards_array_message_payload() -> None:
    expected = {"id": "conversation-123", "answer": "done"}
    message_payload = [{"type": "text", "text": "hello"}]

    with patch(
        "tools.chat_tools.client.create_conversation_v2",
        new=AsyncMock(return_value=expected),
    ) as mock_create_conversation_v2:
        await aichat_create_conversation_v2(
            model="gpt-4.1",
            message=message_payload,
        )

    assert mock_create_conversation_v2.await_args.kwargs["message"] == message_payload
