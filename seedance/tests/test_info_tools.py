"""Tests for Seedance informational tools and onboarding metadata."""

from pathlib import Path
from typing import get_args

import pytest

from core.types import DEFAULT_MODEL, SeedanceModel
from tools.info_tools import seedance_list_models


@pytest.mark.asyncio
async def test_list_models_uses_one_pricing_semantic() -> None:
    result = await seedance_list_models()

    for model in get_args(SeedanceModel):
        assert model in result
    assert "| Pricing |" in result
    assert "See live pricing" in result
    assert "$" not in result
    assert "Credits (720p/sec)" not in result


def test_readme_lists_the_runtime_default_model() -> None:
    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text()

    assert f"| `{DEFAULT_MODEL}`" in readme
    assert "2.0 (default)" in readme
