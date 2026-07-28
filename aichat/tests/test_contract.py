"""Guards the AiChat MCP contract against the API spec.

The spec enum can lag behind what the gateway actually accepts, so the v2
check is one-directional: everything in the spec must be offered, but the
MCP may legitimately expose more (each extra is verified live before being
added here).
"""

from typing import get_args

from core.server import mcp
from core.types import AiChatModel, AiChatV2Model
from tools import chat_tools

# Models the /aichat/conversations spec enum requires us to offer.
V1_REQUIRED = {
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.6-sol",
    "gpt-5.4-mini",
    "gpt-5.4-nano",
    "grok-4.5",
    "glm-5.2",
    "glm-5",
    "glm-5-turbo",
}

# Verified live on /aichat2/conversations but not yet in that spec's enum.
V2_AHEAD_OF_SPEC = {
    "gemini-3.5-flash",
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.6-sol",
}


def test_v1_offers_the_newest_models():
    missing = V1_REQUIRED - set(get_args(AiChatModel))
    assert not missing, f"AiChatModel is missing {sorted(missing)}"


def test_v2_offers_claude_sonnet_5():
    assert "claude-sonnet-5" in get_args(AiChatV2Model)


def test_v2_keeps_models_the_spec_has_not_caught_up_with():
    missing = V2_AHEAD_OF_SPEC - set(get_args(AiChatV2Model))
    assert not missing, f"AiChatV2Model dropped live models {sorted(missing)}"


def test_v2_exposes_async_request_controls():
    assert hasattr(chat_tools, "aichat_create_conversation_v2")
    schema = mcp._tool_manager._tools["aichat_create_conversation_v2"].parameters
    properties = schema["properties"]

    assert {"type": "boolean"} in properties["async"]["anyOf"]
    assert "callback_url" in properties
    assert "allowed_skills" in properties
    assert "allowed_mcp_servers" in properties
    assert "unattended_policy" in properties
