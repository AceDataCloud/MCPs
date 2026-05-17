"""Chat conversation tools for AiChat API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import AiChatAPIError, AiChatAuthError
from core.server import mcp
from core.types import (
    DEFAULT_MODEL,
    DEFAULT_V2_MODEL,
    AiChatModel,
    AiChatV2Action,
    AiChatV2Model,
    AiChatV2ModelGroup,
)


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
        Field(description="Model to use for the request."),
    ] = DEFAULT_V2_MODEL,
    action: Annotated[
        AiChatV2Action,
        Field(
            description="Operation to perform: chat (default), retrieve, retrieve_batch, update, or delete."
        ),
    ] = "chat",
    id: Annotated[
        str | None,
        Field(description="Conversation ID. Required for retrieve/update/delete actions."),
    ] = None,
    question: Annotated[
        str | None,
        Field(description="Question text for chat action."),
    ] = None,
    message: Annotated[
        dict[str, Any] | None,
        Field(description="Single message object to include in the request."),
    ] = None,
    stateful: Annotated[
        bool | None,
        Field(description="Whether to use stateful conversation mode."),
    ] = True,
    references: Annotated[
        list[str] | None,
        Field(description="Optional list of reference sources."),
    ] = None,
    preset: Annotated[
        str | None,
        Field(description="Optional preset model configuration."),
    ] = None,
    max_turns: Annotated[
        int | None,
        Field(description="Maximum number of turns for conversation history."),
    ] = None,
    tool_results: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Tool call results for follow-up turns."),
    ] = None,
    messages: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Conversation messages for update/action workflows."),
    ] = None,
    title: Annotated[
        str | None,
        Field(description="Conversation title."),
    ] = None,
    user_id: Annotated[
        str | None,
        Field(description="Filter or associate by user ID."),
    ] = None,
    application_id: Annotated[
        str | None,
        Field(description="Filter or associate by application ID."),
    ] = None,
    model_group: Annotated[
        AiChatV2ModelGroup | None,
        Field(description="Provider group filter for retrieve_batch."),
    ] = None,
    offset: Annotated[
        int | None,
        Field(description="Pagination offset for retrieve_batch."),
    ] = 0,
    limit: Annotated[
        int | None,
        Field(description="Pagination limit for retrieve_batch."),
    ] = 100,
) -> str:
    """Create/manage conversations via AiChat v2 endpoint."""
    payload: dict[str, Any] = {
        "model": model,
        "action": action,
    }
    optional_fields = {
        "id": id,
        "question": question,
        "message": message,
        "stateful": stateful,
        "references": references,
        "preset": preset,
        "max_turns": max_turns,
        "tool_results": tool_results,
        "messages": messages,
        "title": title,
        "user_id": user_id,
        "application_id": application_id,
        "model_group": model_group,
        "offset": offset,
        "limit": limit,
    }
    payload.update({k: v for k, v in optional_fields.items() if v is not None})

    try:
        result = await client.create_conversation_v2(**payload)
        if not result:
            return json.dumps({"error": "No response received from the API."})
        return json.dumps(result, ensure_ascii=False, indent=2)
    except AiChatAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except AiChatAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating conversation", "message": str(e)})
