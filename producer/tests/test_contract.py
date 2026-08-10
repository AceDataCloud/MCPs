"""Guards the Producer MCP surface against the API contract."""

from typing import get_args

from core.client import ProducerClient
from core.server import mcp
from core.types import AudioAction, ProducerModel
from tools import audio_tools  # noqa: F401

SPEC_MODELS = {
    "FUZZ-2.0 Pro",
    "FUZZ-2.0",
    "FUZZ-2.0 Raw",
    "FUZZ-1.1 Pro",
    "FUZZ-1.0 Pro",
    "FUZZ-1.0",
    "FUZZ-1.1",
    "FUZZ-0.8",
}

SPEC_ACTIONS = {
    "generate",
    "cover",
    "extend",
    "variation",
    "swap_vocals",
    "swap_instrumentals",
    "replace_section",
    "stems",
}


def test_models_match_spec():
    assert set(get_args(ProducerModel)) == SPEC_MODELS


def test_actions_match_spec():
    assert set(get_args(AudioAction)) == SPEC_ACTIONS


def test_audio_generation_exposes_async_and_string_seed():
    schema = mcp._tool_manager._tools["producer_generate_music"].parameters
    properties = schema["properties"]

    assert "async" in properties
    assert {"type": "boolean"} in properties["async"]["anyOf"]
    assert {"type": "string"} in properties["seed"]["anyOf"]


def test_async_callback_preserves_explicit_false():
    client = ProducerClient(api_token="test-token", base_url="https://api.test.com")

    assert client._with_async_callback({"async": False})["async"] is False
