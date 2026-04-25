"""Chat tools for AIChat API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import AIChatAPIError, AIChatAuthError
from core.server import mcp
from core.types import (
    DEFAULT_CHAT_MODEL,
    ChatModel,
)


@mcp.tool()
async def aichat_conversation(
    question: Annotated[
        str,
        Field(description="The prompt or question to be answered. Required."),
    ],
    model: Annotated[
        ChatModel,
        Field(
            description=(
                "The model to use for answering the prompt. Options include gpt-4.1, gpt-4o, "
                "gpt-5, o1, o3, o4-mini, deepseek-r1, deepseek-v3, grok-3, glm-4.6, and many "
                "more. Default is gpt-4.1."
            )
        ),
    ] = DEFAULT_CHAT_MODEL,
    conversation_id: Annotated[
        str | None,
        Field(
            description=(
                "The unique identifier of an existing conversation. Provide this to continue "
                "a previous conversation when stateful is True."
            )
        ),
    ] = None,
    stateful: Annotated[
        bool | None,
        Field(
            description=(
                "Whether to use stateful conversation mode. When True, the conversation "
                "history is maintained across requests using the conversation id."
            )
        ),
    ] = None,
    preset: Annotated[
        str | None,
        Field(description="The preset model configuration to use for answering the prompt."),
    ] = None,
    references: Annotated[
        list[str] | None,
        Field(
            description=(
                "A list of reference URLs or sources to be used as context when "
                "answering the prompt."
            )
        ),
    ] = None,
) -> str:
    """Send a question to an AI model and get an answer via AceDataCloud AIChat API.

    Supports a wide range of models including GPT, o-series, DeepSeek, Grok, and GLM.
    Optionally supports stateful conversations to maintain context across multiple turns.

    Use this when:
    - You need to ask a question to an AI model
    - You want to have a multi-turn conversation (use stateful=True and pass conversation_id)
    - You need to use a specific model like DeepSeek, Grok, or GLM

    Returns:
        JSON response containing the answer and conversation id.
    """
    try:
        payload: dict = {
            "question": question,
            "model": model,
        }

        if conversation_id is not None:
            payload["id"] = conversation_id
        if stateful is not None:
            payload["stateful"] = stateful
        if preset is not None:
            payload["preset"] = preset
        if references is not None:
            payload["references"] = references

        result = await client.conversations(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except AIChatAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except AIChatAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating conversation", "message": str(e)})
