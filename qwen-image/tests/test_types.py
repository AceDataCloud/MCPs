from typing import get_args

from core.types import QwenImageModel


def test_models_are_exact():
    assert set(get_args(QwenImageModel)) == {"qwen-image-3.0", "qwen-image-3.0-pro"}
