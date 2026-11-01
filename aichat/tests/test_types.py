"""Contract tests for public MCP input types."""

from typing import get_args

from core.types import AiChatModel, AiChatV2Model, AiChatV2ModelGroup


def test_kimi_models_are_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "kimi-k3.1-pro" in models
    assert "kimi-k3" in models
    assert "kimi-k2.6" in models


def test_claude_fable_models_are_available_once_in_aichat_v2() -> None:
    models = get_args(AiChatV2Model)

    assert models.count("claude-fable-5-1") == 1
    assert models.count("claude-fable-5") == 1


def test_flagship_models_are_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "gpt-5.6-sol-fast" in models
    assert "gpt-5.2-pro" in models
    assert {
        "gpt-6.1-sol",
        "gpt-6.1-terra",
        "gpt-6-sol",
        "gpt-6-luna",
        "grok-4.7",
        "gemini-4-argon",
        "gemini-3.8-flash",
    } <= models
    assert "grok-4.5" in models
    assert "glm-5.3" in models
    assert "gemini-3.1-pro-preview" in models
    assert "glm-5.2" in models


def test_deepseek_v4_pro_is_available_once_in_each_aichat_api() -> None:
    assert get_args(AiChatModel).count("deepseek-v4-pro") == 1
    assert get_args(AiChatV2Model).count("deepseek-v4-pro") == 1


def test_mimo_identifiers_are_available_without_duplicate_aliases() -> None:
    for model in ("mimo-v2.6-pro", "mimo-v2.6-flash"):
        assert get_args(AiChatModel).count(model) == 1
        assert get_args(AiChatV2Model).count(model) == 1
    assert "mimo" in get_args(AiChatV2ModelGroup)
