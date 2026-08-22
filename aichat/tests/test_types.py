"""Contract tests for public MCP input types."""

from typing import get_args

from core.types import AiChatModel, AiChatV2Model


def test_kimi_k3_models_are_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "kimi-k3" in models
    assert "kimi-k2.6" in models


def test_claude_fable_5_is_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "claude-fable-5" in models


def test_flagship_models_are_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "gpt-5.2-pro" in models
    assert "grok-4.5" in models
    assert "gemini-3.1-pro-preview" in models
    assert "glm-5.2" in models


def test_deepseek_v4_pro_is_available_once_in_each_aichat_api() -> None:
    assert get_args(AiChatModel).count("deepseek-v4-pro") == 1
    assert get_args(AiChatV2Model).count("deepseek-v4-pro") == 1
