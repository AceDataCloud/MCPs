"""Tests for Seedream API type definitions."""

from typing import get_args

from core.types import Background, SeedreamModel, SeedreamSize


def test_seedream_model_matches_api_contract() -> None:
    """All Seedream models from the API contract are exposed."""
    assert get_args(SeedreamModel) == (
        "doubao-seedream-5-0-pro-260628",
        "doubao-seedream-5-0-260128",
        "doubao-seedream-5-0-lite-260128",
        "doubao-seedream-4-0-250828",
        "doubao-seedream-4-5-251128",
    )


def test_seedream_size_matches_api_contract() -> None:
    """The API contract accepts arbitrary size strings."""
    assert SeedreamSize is str


def test_seedream_background_matches_api_contract() -> None:
    """Only supported background opacity options are exposed."""
    assert get_args(Background) == ("transparent", "opaque")
