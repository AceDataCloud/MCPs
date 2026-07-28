"""Unit tests for AiChat MCP tool functions."""

import json
from unittest.mock import AsyncMock, patch

import pytest

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
