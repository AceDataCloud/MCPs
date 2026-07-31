"""Guards against re-introducing models the API no longer accepts."""

from typing import get_args

from core.types import DEFAULT_CHAT_MODEL, GrokChatModel, ReasoningEffort, ServiceTier

# Mirrors the `model` / `reasoning_effort` / `service_tier` enums in the Grok chat OpenAPI spec.
SPEC_CHAT_MODELS = {"grok-4.5", "grok-4", "grok-3"}
SPEC_REASONING_EFFORT = {"minimal", "low", "medium", "high"}
SPEC_SERVICE_TIER = {"auto", "default", "flex", "scale", "priority"}


def test_chat_models_match_spec():
    assert set(get_args(GrokChatModel)) == SPEC_CHAT_MODELS


def test_unsupported_models_are_gone():
    # These all return 400 "is not supported".
    for retired in ("grok-4-1-fast", "grok-4-1-fast-non-reasoning", "grok-3-mini", "grok-2-vision"):
        assert retired not in get_args(GrokChatModel)


def test_reasoning_effort_matches_spec():
    assert set(get_args(ReasoningEffort)) == SPEC_REASONING_EFFORT


def test_service_tier_matches_spec():
    assert set(get_args(ServiceTier)) == SPEC_SERVICE_TIER


def test_default_chat_model_is_selectable():
    assert DEFAULT_CHAT_MODEL in get_args(GrokChatModel)
