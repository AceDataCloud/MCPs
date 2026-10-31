"""Public model aliases and generated discovery must agree."""

from typing import get_args
from unittest.mock import AsyncMock

import pytest

from core.server import mcp
from core.types import AiChatModel, AiChatV2Model
from tools import chat_tools, info_tools


@pytest.mark.asyncio
async def test_gemini_38_flash_v1_dispatch(monkeypatch):
    request = AsyncMock(return_value={"answer": "hello"})
    monkeypatch.setattr(chat_tools.client, "create_conversation", request)
    await mcp.call_tool(
        "aichat_create_conversation", {"question": "hello", "model": "gemini-3.8-flash"}
    )
    assert request.await_args.kwargs["model"] == "gemini-3.8-flash"


@pytest.mark.asyncio
async def test_discovery_matches_both_endpoint_enums():
    listing = await info_tools.aichat_list_models()
    v1, rest = listing.split("## aichat_create_conversation_v2", 1)
    v2 = rest.split("## Gemini endpoint coverage", 1)[0]
    assert {line[2:] for line in v1.splitlines() if line.startswith("- ")} == set(
        get_args(AiChatModel)
    )
    assert {line[2:] for line in v2.splitlines() if line.startswith("- ")} == set(
        get_args(AiChatV2Model)
    )
    assert "gpt-6-astra" in get_args(AiChatV2Model)
