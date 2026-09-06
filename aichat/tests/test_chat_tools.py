"""Unit tests for AiChat MCP tool functions."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from core.server import mcp
from tools.chat_tools import aichat_create_conversation_v2


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
