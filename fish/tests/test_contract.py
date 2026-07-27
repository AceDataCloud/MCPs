"""Guards the Fish TTS model list against the API contract."""

from typing import get_args

from core.types import DEFAULT_MODEL, FishModel

# Mirrors the `model` header-param enum in the Fish TTS OpenAPI spec.
SPEC_MODELS = {"s1", "s2-pro", "s2.1-pro"}


def test_models_match_spec():
    assert set(get_args(FishModel)) == SPEC_MODELS


def test_default_model_is_selectable():
    assert DEFAULT_MODEL in get_args(FishModel)
