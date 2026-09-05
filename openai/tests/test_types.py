"""Guards public OpenAI model input types against the API spec."""

from typing import get_args

from core.types import ChatModel, ResponsesModel


def test_gpt_6_astra_is_available_for_chat_and_responses() -> None:
    assert "gpt-6-astra" in get_args(ChatModel)
    assert "gpt-6-astra" in get_args(ResponsesModel)
