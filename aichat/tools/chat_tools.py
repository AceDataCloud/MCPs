"""Chat conversation tools for AiChat API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import AiChatAPIError, AiChatAuthError
from core.server import mcp
from core.types import DEFAULT_MODEL, DEFAULT_V2_MODEL, AiChatModel, AiChatV2Model


@mcp.tool()
async def aichat_create_conversation(
    question: Annotated[
        str,
        Field(description=("The prompt or question to be answered by the AI model. Required.")),
    ],
    model: Annotated[
        AiChatModel,
        Field(
            description=(
                "The model to use for generating the answer. Options include gpt-4.1, gpt-4o, "
                "gpt-5, o1, o3, o4-mini, deepseek-r1, deepseek-v3, grok-3, glm-4.7, and many "
                "more. Default is gpt-4.1."
            )
        ),
    ] = DEFAULT_MODEL,
    conversation_id: Annotated[
        str | None,
        Field(
            description=(
                "The unique identifier of an existing conversation to continue. "
                "If provided, the AI will respond in the context of the prior conversation. "
                "Leave empty to start a new conversation."
            )
        ),
    ] = None,
    preset: Annotated[
        str | None,
        Field(
            description=("An optional preset model configuration to apply for this conversation.")
        ),
    ] = None,
    stateful: Annotated[
        bool | None,
        Field(
            description=(
                "Whether to use stateful conversation mode. When True, the server tracks "
                "conversation history. Default is False (stateless)."
            )
        ),
    ] = None,
    references: Annotated[
        list[str] | None,
        Field(
            description=(
                "Optional list of reference sources or context to include when generating "
                "the answer."
            )
        ),
    ] = None,
) -> str:
    """Create an AI conversation using the AiChat API.

    Sends a question to the specified AI model and returns the generated answer.
    Supports a wide range of models including GPT-4, GPT-5, o-series, DeepSeek, Grok, and GLM.

    Use this when:
    - You need to ask a question to an AI model
    - You want to continue an existing conversation (provide conversation_id)
    - You need answers from specific AI models like DeepSeek, Grok, or GLM

    Returns:
        JSON response containing the conversation ID and the generated answer.
    """
    if not question:
        return json.dumps({"error": "Validation Error", "message": "question is required"})

    try:
        result = await client.create_conversation(
            question=question,
            model=model,
            conversation_id=conversation_id,
            preset=preset,
            stateful=stateful,
            references=references,
        )

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except AiChatAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except AiChatAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating conversation", "message": str(e)})


@mcp.tool()
async def aichat_create_conversation_v2(
    model: Annotated[
        AiChatV2Model,
        Field(
            description=(
                "The model to use for generating the answer. Options include gpt-4.1, gpt-4o, "
                "claude-opus-4-7, claude-sonnet-4-6, gemini-3.1-pro, grok-4, kimi-k2.5, "
                "deepseek-r1, glm-5.1, o3, o4-mini, and many more. Default is gpt-4.1."
            )
        ),
    ] = DEFAULT_V2_MODEL,
    question: Annotated[
        str | None,
        Field(
            description=(
                "The prompt or question to be answered by the AI model. "
                "Plain-text user prompt (v1-compatible)."
            )
        ),
    ] = None,
    conversation_id: Annotated[
        str | None,
        Field(
            description=(
                "The unique identifier of an existing conversation to continue. "
                "If provided with stateful=True, the conversation is resumed. "
                "Leave empty to start a new conversation."
            )
        ),
    ] = None,
    preset: Annotated[
        str | None,
        Field(
            description=("An optional preset model configuration to apply for this conversation.")
        ),
    ] = None,
    stateful: Annotated[
        bool | None,
        Field(
            description=(
                "Whether to persist the conversation. When True (default in v2), the new turn "
                "is stored and can be resumed by later calls. Set to False for one-shot requests."
            )
        ),
    ] = None,
    references: Annotated[
        list[str] | None,
        Field(
            description=(
                "Optional list of reference URLs to attach to this turn. URLs ending in image "
                "extensions are auto-converted to image_url blocks; everything else becomes a "
                "file_url block."
            )
        ),
    ] = None,
) -> str:
    """Create an AI conversation using the AiChat v2 API.

    Sends a question to the specified AI model via the v2 endpoint and returns the generated
    answer. Supports a wider range of models including Claude, Gemini, Grok-4, Kimi, and more.

    Use this when:
    - You need Claude, Gemini, Grok-4, or Kimi models
    - You want access to the latest multi-provider model selection
    - You need to continue an existing v2 conversation (provide conversation_id)

    Returns:
        JSON response containing the conversation ID and the generated answer.
    """
    if not question:
        return json.dumps({"error": "Validation Error", "message": "question is required"})

    try:
        result = await client.create_conversation_v2(
            model=model,
            question=question,
            conversation_id=conversation_id,
            preset=preset,
            stateful=stateful,
            references=references,
        )

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except AiChatAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except AiChatAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating conversation", "message": str(e)})
