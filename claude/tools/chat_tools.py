"""Chat completion tools for Claude API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import ClaudeAPIError, ClaudeAuthError
from core.server import mcp
from core.types import (
    DEFAULT_CHAT_MODEL,
    ChatModel,
)


@mcp.tool()
async def claude_chat_completion(
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
                "The model to use for chat completion. "
                "Default is claude-sonnet-4-20250514."
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
    """Create a chat completion using Claude models via AceDataCloud (OpenAI-compatible endpoint).

    Sends a conversation to the specified model and returns the generated response.

    Use this when:
    - You need to have a conversation with a Claude model using OpenAI-compatible API
    - You want to generate text responses based on a prompt

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

    except ClaudeAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except ClaudeAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating chat completion", "message": str(e)})


@mcp.tool()
async def claude_create_message(
    messages: Annotated[
        list[dict[str, Any]],
        Field(
            description=(
                "A list of messages for the conversation. Each message must have a "
                "'role' ('user' or 'assistant') and 'content' field. "
                "Example: [{'role': 'user', 'content': 'Hello!'}]"
            )
        ),
    ],
    model: Annotated[
        ChatModel,
        Field(
            description=(
                "The model to use. "
                "Default is claude-sonnet-4-20250514."
            )
        ),
    ],
    max_tokens: Annotated[
        int,
        Field(
            description="The maximum number of tokens to generate in the response."
        ),
    ],
    system: Annotated[
        str | None,
        Field(
            description="Optional system prompt to guide the model's behavior."
        ),
    ] = None,
    temperature: Annotated[
        float | None,
        Field(
            description=(
                "Sampling temperature between 0 and 1. Higher values make output "
                "more random, lower values make it more focused."
            )
        ),
    ] = None,
) -> str:
    """Create a message using the Anthropic native Claude API.

    Uses the /v1/messages endpoint (Anthropic native format).

    Use this when:
    - You need to use the native Anthropic messages API format
    - You want precise control over max_tokens

    Returns:
        JSON response containing the model's reply and usage information.
    """
    try:
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
        }

        if system is not None:
            payload["system"] = system
        if temperature is not None:
            payload["temperature"] = temperature

        result = await client.create_message(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except ClaudeAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except ClaudeAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating message", "message": str(e)})
