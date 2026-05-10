"""Chat conversation tools for AiChat API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import AiChatAPIError, AiChatAuthError
from core.server import mcp
from core.types import DEFAULT_MODEL, AiChatModel


@mcp.tool()
async def aichat_create_conversation(
    question: Annotated[
        str | None,
        Field(description=("The prompt or question to be answered by the AI model. Required.")),
    ] = None,
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
    action: Annotated[
        str | None,
        Field(
            description=(
                "Operation to perform: chat, retrieve, retrieve_batch, update, or delete. "
                "Defaults to chat."
            )
        ),
    ] = None,
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
    message: Annotated[
        str | list[dict[str, Any]] | None,
        Field(
            description=(
                "Optional multimodal user content for this turn, as a string or content blocks."
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
    max_turns: Annotated[
        int | None,
        Field(description="Optional max number of turns for agentic mode."),
    ] = None,
    tool_results: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Optional prior tool outputs to inject into this turn."),
    ] = None,
    messages: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Optional full message list for update operations."),
    ] = None,
    title: Annotated[
        str | None,
        Field(description="Optional conversation title (mainly for update)."),
    ] = None,
    user_id: Annotated[
        str | None,
        Field(description="Optional user ID for list/retrieve_batch filtering."),
    ] = None,
    application_id: Annotated[
        str | None,
        Field(description="Optional application ID for retrieve_batch filtering."),
    ] = None,
    model_group: Annotated[
        str | None,
        Field(description="Optional model group filter for retrieve_batch."),
    ] = None,
    offset: Annotated[
        int | None,
        Field(description="Optional pagination offset for retrieve_batch."),
    ] = None,
    limit: Annotated[
        int | None,
        Field(description="Optional pagination limit for retrieve_batch."),
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
    if action in (None, "chat") and not question and not message:
        return json.dumps(
            {"error": "Validation Error", "message": "question or message is required for chat"}
        )

    try:
        result = await client.create_conversation(
            question=question,
            model=model,
            action=action,
            conversation_id=conversation_id,
            message=message,
            preset=preset,
            stateful=stateful,
            references=references,
            max_turns=max_turns,
            tool_results=tool_results,
            messages=messages,
            title=title,
            user_id=user_id,
            application_id=application_id,
            model_group=model_group,
            offset=offset,
            limit=limit,
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
