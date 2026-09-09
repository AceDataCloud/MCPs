"""Tests for NanoBanana informational tools."""

from typing import get_args

import pytest

from core.types import NanoBananaModel
from tools.info_tools import nanobanana_list_models


@pytest.mark.asyncio
async def test_list_models_covers_the_public_model_literal() -> None:
    result = await nanobanana_list_models()

    for model in get_args(NanoBananaModel):
        assert f"`{model}`" in result
    assert "Review live pricing" in result
