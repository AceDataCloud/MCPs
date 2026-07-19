"""Contract tests for public MCP input types."""

from typing import get_args

from core.types import AiChatV2Model


def test_kimi_k3_models_are_available_in_aichat_v2() -> None:
    models = set(get_args(AiChatV2Model))

    assert "kimi-k3" in models
    assert "kimi-k2.6" in models
