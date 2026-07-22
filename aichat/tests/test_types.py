"""Contract tests for public MCP input types."""

from typing import get_args

from core.types import AiChatV2Model


def test_kimi_k3_models_are_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "kimi-k3" in models
    assert "kimi-k2.6" in models


def test_claude_fable_5_is_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "claude-fable-5" in models


def test_flagship_models_are_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "gpt-5.6-luna" in models
    assert "gpt-5.6-terra" in models
    assert "gpt-5.6-sol" in models
    assert "grok-4.5" in models
    assert "gemini-3.5-flash" in models
    assert "glm-5.2" in models
