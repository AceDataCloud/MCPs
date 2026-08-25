"""Guards the AiChat MCP contract against the API spec."""

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
    "deepseek-v4-pro",
    "grok-4.5",
    "glm-5.3",
    "glm-5.2",
    "glm-5",
    "glm-5-turbo",
}

# Kimi models the spec removed; they must stay out of the MCP surface.
V2_RETIRED_KIMI = {
    "kimi-k2-0711-preview",
    "kimi-k2-0905-preview",
    "kimi-k2-instruct-0905",
    "kimi-k2-turbo-preview",
}

# Models removed from the current /aichat2/conversations spec enum.
V2_REMOVED_FROM_SPEC = {
    "gpt-5.6-luna",
    "gpt-5.6-terra",
    "gpt-5.6-sol",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-3.0-pro",
    "gemini-3.6-flash",
    "gemini-3-flash-preview",
    "gemini-3.5-flash",
}


def test_v1_offers_the_newest_models():
    missing = V1_REQUIRED - set(get_args(AiChatModel))
    assert not missing, f"AiChatModel is missing {sorted(missing)}"


def test_v2_offers_claude_sonnet_5():
    assert "claude-sonnet-5" in get_args(AiChatV2Model)


def test_v2_offers_claude_spec_models():
    spec_models = {
        "claude-fable-5",
        "claude-opus-5",
        "claude-opus-4-8",
        "claude-sonnet-5",
        "claude-sonnet-4-6",
        "claude-opus-4-7",
        "claude-opus-4-6",
        "claude-opus-4-5-20251101",
        "claude-haiku-4-5-20251001",
        "claude-sonnet-4-5-20250929",
        "claude-opus-4-1-20250805",
        "claude-sonnet-4-20250514",
        "claude-opus-4-20250514",
        "claude-3-7-sonnet-20250219",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307",
        "claude-3-sonnet-20240229",
    }
    missing = spec_models - set(get_args(AiChatV2Model))
    assert not missing, f"AiChatV2Model is missing Claude spec models {sorted(missing)}"


def test_v2_offers_gemini_spec_models():
    spec_models = {
        "gemini-3.1-pro",
        "gemini-2.5-flash-lite",
        "gemini-3.1-flash-lite-preview",
        "gemini-3.1-flash-image-preview",
        "gemini-3.1-pro-preview",
        "gemini-3-pro-preview",
        "gemini-2.0-flash-lite",
    }
    missing = spec_models - set(get_args(AiChatV2Model))
    assert not missing, f"AiChatV2Model is missing Gemini spec models {sorted(missing)}"


def test_v2_offers_deepseek_spec_models():
    spec_models = {
        "deepseek-chat",
        "deepseek-r1",
        "deepseek-r1-0528",
        "deepseek-reasoner",
        "deepseek-v3",
        "deepseek-v3-250324",
        "deepseek-v3.2-exp",
        "deepseek-v4-flash",
        "deepseek-v4-pro",
    }
    missing = spec_models - set(get_args(AiChatV2Model))
    assert not missing, f"AiChatV2Model is missing DeepSeek spec models {sorted(missing)}"


def test_v2_offers_glm_spec_models():
    spec_models = {
        "glm-5.3",
        "glm-5.2",
        "glm-5",
        "glm-5-turbo",
        "glm-5.1",
        "glm-4.7",
        "glm-4.6",
        "glm-3-turbo",
    }
    missing = spec_models - set(get_args(AiChatV2Model))
    assert not missing, f"AiChatV2Model is missing GLM spec models {sorted(missing)}"


def test_v2_excludes_retired_kimi_models():
    lingering = V2_RETIRED_KIMI & set(get_args(AiChatV2Model))
    assert not lingering, f"AiChatV2Model still offers retired models {sorted(lingering)}"


def test_v2_excludes_models_removed_from_spec():
    lingering = V2_REMOVED_FROM_SPEC & set(get_args(AiChatV2Model))
    assert not lingering, f"AiChatV2Model still offers removed models {sorted(lingering)}"


def test_v2_exposes_async_request_controls():
    assert hasattr(chat_tools, "aichat_create_conversation_v2")
    schema = mcp._tool_manager._tools["aichat_create_conversation_v2"].parameters
    properties = schema["properties"]

    assert {"type": "boolean"} in properties["async"]["anyOf"]
    assert "callback_url" in properties
    assert "allowed_skills" in properties
    assert "allowed_mcp_servers" in properties
    assert "unattended_policy" in properties


def test_v2_retrieve_batch_limit_matches_spec_maximum():
    schema = mcp._tool_manager._tools["aichat_create_conversation_v2"].parameters
    properties = schema["properties"]

    assert {"type": "integer", "minimum": 1, "maximum": 100} in properties["limit"]["anyOf"]
