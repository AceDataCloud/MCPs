"""Unit tests for chat conversation tools."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from tools.chat_tools import aichat_create_conversation


class TestAiChatCreateConversation:
    """Tests for aichat_create_conversation tool."""

    @pytest.mark.asyncio
    async def test_chat_requires_question_message_or_tool_results(self) -> None:
        """Test that chat requests still require some user input."""
        result = await aichat_create_conversation(
            question=None,
            model="gpt-4.1",
        )

        payload = json.loads(result)
        assert payload["error"] == "Validation Error"
        assert "require question, message, or tool_results" in payload["message"]

    @pytest.mark.asyncio
    async def test_accepts_multimodal_message_without_question(self) -> None:
        """Test that multimodal chat requests do not require the legacy question field."""
        expected = {"id": "conversation-1", "answer": "Done"}

        with patch("tools.chat_tools.client") as mock_client:
            mock_client.create_conversation = AsyncMock(return_value=expected)

            result = await aichat_create_conversation(
                question=None,
                model="gpt-4o-image",
                message=[
                    {"type": "text", "text": "Describe this image."},
                    {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
                ],
            )

            assert json.loads(result) == expected
            call_kwargs = mock_client.create_conversation.call_args[1]
            assert call_kwargs["question"] is None
            assert call_kwargs["model"] == "gpt-4o-image"
            assert call_kwargs["message"][0]["type"] == "text"

    @pytest.mark.asyncio
    async def test_accepts_retrieve_batch_without_question(self) -> None:
        """Test that non-chat actions can be called without a question."""
        expected = {"items": [], "total": 0}

        with patch("tools.chat_tools.client") as mock_client:
            mock_client.create_conversation = AsyncMock(return_value=expected)

            result = await aichat_create_conversation(
                question=None,
                model="claude-sonnet-4-6",
                action="retrieve_batch",
                model_group="claude",
                limit=10,
            )

            assert json.loads(result) == expected
            call_kwargs = mock_client.create_conversation.call_args[1]
            assert call_kwargs["action"] == "retrieve_batch"
            assert call_kwargs["model_group"] == "claude"
            assert call_kwargs["limit"] == 10
