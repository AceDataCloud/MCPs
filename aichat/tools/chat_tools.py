"""Chat conversation tools for AiChat API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import AiChatAPIError, AiChatAuthError
from core.server import mcp
from core.types import DEFAULT_MODEL, AiChatAction, AiChatModel, AiChatModelGroup


@mcp.tool()
async def aichat_create_conversation(
    question: Annotated[
        str | None,
        Field(
            description=(
                "Optional legacy plain-text prompt for chat requests. Ignored when `message` "
                "is provided. Leave empty for retrieve, retrieve_batch, update, or delete actions."
            )
        ),
    ] = None,
    model: Annotated[
        AiChatModel,
        Field(
            description=(
                "The model to use for the request. Supports GPT, Claude, Gemini, Grok, "
                "DeepSeek, Kimi, GLM, and reasoning-model variants. Default is gpt-4.1."
            )
        ),
    ] = DEFAULT_MODEL,
    conversation_id: Annotated[
        str | None,
        Field(
            description=(
                "Conversation identifier. Use this to continue a stateful chat or to target "
                "retrieve, update, or delete actions."
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
                "Whether to persist the conversation. When omitted, the API uses its default "
                "stateful behavior."
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
    action: Annotated[
        AiChatAction | None,
        Field(
            description=(
                "Optional conversation action. Use `chat` (default) to generate a response, "
                "`retrieve` to load one conversation, `retrieve_batch` to list conversations, "
                "`update` to patch a conversation, or `delete` to remove one."
            )
        ),
    ] = None,
    message: Annotated[
        str | list[dict[str, Any]] | None,
        Field(
            description=(
                "Optional multimodal user message for chat requests. Provide either a plain "
                "string or an array of content blocks such as "
                "[{'type': 'text', 'text': 'Describe this image'}, "
                "{'type': 'image_url', 'image_url': {'url': 'https://example.com/image.png'}}]."
            )
        ),
    ] = None,
    max_turns: Annotated[
        int | None,
        Field(
            description=(
                "Optional cap on agentic-loop iterations for this request."
            ),
            ge=1,
        ),
    ] = None,
    tool_results: Annotated[
        list[dict[str, Any]] | None,
        Field(
            description=(
                "Optional resume payload for a conversation paused on ask_user_question. "
                "Provide entries with `tool_use_id`, `output`, and optional `is_error`."
            )
        ),
    ] = None,
    messages: Annotated[
        list[dict[str, Any]] | None,
        Field(
            description=(
                "Optional replacement conversation history. Only used for `update` actions."
            )
        ),
    ] = None,
    title: Annotated[
        str | None,
        Field(description="Optional conversation title for `update` actions."),
    ] = None,
    user_id: Annotated[
        str | None,
        Field(description="Optional user filter for `retrieve_batch` actions."),
    ] = None,
    application_id: Annotated[
        str | None,
        Field(description="Optional application filter for `retrieve_batch` actions."),
    ] = None,
    model_group: Annotated[
        AiChatModelGroup | None,
        Field(description="Optional provider bucket filter for `retrieve_batch` actions."),
    ] = None,
    offset: Annotated[
        int | None,
        Field(description="Optional pagination offset for `retrieve_batch` actions.", ge=0),
    ] = None,
    limit: Annotated[
        int | None,
        Field(description="Optional pagination limit for `retrieve_batch` actions.", ge=1, le=100),
    ] = None,
) -> str:
    """Create an AI conversation using the AiChat API.

    Sends a chat request or conversation-management action to the AiChat API.
    Supports legacy question-based chat, multimodal message input, and CRUD-style actions.

    Use this when:
    - You need to ask a question to an AI model
    - You want to send multimodal message content
    - You want to continue, retrieve, list, update, or delete conversations

    Returns:
        JSON response containing the API result.
    """
    if action in (None, "chat") and question is None and message is None and tool_results is None:
        return json.dumps(
            {
                "error": "Validation Error",
                "message": "chat requests require question, message, or tool_results",
            }
        )

    try:
        result = await client.create_conversation(
            question=question,
            model=model,
            conversation_id=conversation_id,
            preset=preset,
            stateful=stateful,
            references=references,
            action=action,
            message=message,
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
