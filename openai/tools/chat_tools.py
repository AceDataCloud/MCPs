"""Chat completion tools for OpenAI API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp
from core.types import (
    DEFAULT_CHAT_MODEL,
    ChatModel,
)


@mcp.tool()
async def openai_chat_completion(
    messages: Annotated[
        list[dict[str, Any]],
        Field(
            description=(
                "A list of messages comprising the conversation. Each message must have a "
                "'role' ('system', 'user', or 'assistant') and 'content' field. "
                "Example: [{'role': 'user', 'content': 'Hello!'}]"
            )
        ),
    ],
    model: Annotated[
        ChatModel,
        Field(
            description=(
                "The model to use for chat completion. Options include gpt-4.1, gpt-4o, "
                "gpt-5, o1, o3, o4-mini, and many more. Default is gpt-4.1."
            )
        ),
    ] = DEFAULT_CHAT_MODEL,
    max_tokens: Annotated[
        int | None,
        Field(
            description=(
                "The maximum number of tokens to generate. If not specified, the model uses "
                "its default limit."
            )
        ),
    ] = None,
    temperature: Annotated[
        float | None,
        Field(
            description=(
                "Sampling temperature between 0 and 2. Higher values (e.g. 0.8) make output "
                "more random, lower values (e.g. 0.2) make it more focused. Default is 1."
            )
        ),
    ] = None,
    n: Annotated[
        int | None,
        Field(
            description="How many chat completion choices to generate for each input. Default is 1."
        ),
    ] = None,
) -> str:
    """Create a chat completion using OpenAI models via AceDataCloud.

    Sends a conversation to the specified model and returns the generated response.
    Supports all major GPT and o-series models.

    Use this when:
    - You need to have a conversation with an AI model
    - You want to generate text responses based on a prompt
    - You need structured JSON output from a model

    Returns:
        JSON response containing the model's reply and usage information.
    """
    try:
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if n is not None:
            payload["n"] = n

        result = await client.chat_completions(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating chat completion", "message": str(e)})
