"""Chat completion tools for Gemini API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import GeminiAPIError, GeminiAuthError
from core.server import mcp
from core.types import DEFAULT_CHAT_MODEL, ChatModel, NativeGeminiModel


@mcp.tool()
async def gemini_chat_completion(
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
                "The model to use for chat completion. Default is gemini-2.5-flash."
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
                "Sampling temperature between 0 and 2. Higher values make output more random, "
                "lower values make it more focused."
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
    """Create a chat completion using Gemini models via AceDataCloud."""
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

    except GeminiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except GeminiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating chat completion", "message": str(e)})


@mcp.tool()
async def gemini_generate_content(
    contents: Annotated[
        list[dict[str, Any]],
        Field(description="A list of content parts for the native Gemini API."),
    ],
    model: Annotated[
        NativeGeminiModel,
        Field(description="The Gemini model to use. Default is gemini-2.5-flash."),
    ] = "gemini-2.5-flash",
    generation_config: Annotated[
        dict[str, Any] | None,
        Field(description="Generation configuration (temperature, maxOutputTokens, etc.)."),
    ] = None,
) -> str:
    """Generate content using the native Gemini API via AceDataCloud."""
    try:
        payload: dict[str, Any] = {"contents": contents}

        if generation_config is not None:
            payload["generationConfig"] = generation_config

        result = await client.generate_content(model=model, **payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except GeminiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except GeminiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error generating content", "message": str(e)})
