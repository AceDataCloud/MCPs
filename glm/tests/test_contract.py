"""Guards the GLM model list against the API contract."""

from typing import get_args

from core.types import DEFAULT_MODEL, GlmModel

# Mirrors the `model` enum in the GLM chat OpenAPI spec.
SPEC_MODELS = {
    "glm-5.3",
    "glm-5.2",
    "glm-5",
    "glm-5-turbo",
    "glm-5.1",
    "glm-4.7",
    "glm-4.6",
    "glm-3-turbo",
}


def test_models_match_spec():
    assert set(get_args(GlmModel)) == SPEC_MODELS


def test_default_model_is_selectable():
    assert DEFAULT_MODEL in get_args(GlmModel)
