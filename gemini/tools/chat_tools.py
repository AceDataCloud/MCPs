"""Chat completion tools for Gemini API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import GeminiAPIError, GeminiAuthError
from core.server import mcp
from core.types import (
    DEFAULT_CHAT_MODEL,
    ChatModel,
)


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
                "The model to use for chat completion. "
                "Default is gemini-2.5-pro."
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
    """Create a chat completion using Gemini models via AceDataCloud (OpenAI-compatible endpoint).

    Sends a conversation to the specified model and returns the generated response.

    Use this when:
    - You need to have a conversation with a Gemini model using OpenAI-compatible API
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

    except GeminiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except GeminiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating chat completion", "message": str(e)})


@mcp.tool()
async def gemini_generate_content(
    model: Annotated[
        ChatModel,
        Field(
            description=(
                "The Gemini model to use for content generation. "
                "Default is gemini-2.5-pro."
            )
        ),
    ],
    contents: Annotated[
        list[dict[str, Any]],
        Field(
            description=(
                "The input content for the model. Each item should be a dict with 'role' "
                "and 'parts' fields. Example: [{'role': 'user', 'parts': [{'text': 'Hello'}]}]"
            )
        ),
    ],
    system_instruction: Annotated[
        dict[str, Any] | None,
        Field(
            description=(
                "Optional system instruction as a dict. "
                "Example: {'parts': [{'text': 'You are a helpful assistant.'}]}"
            )
        ),
    ] = None,
    generation_config: Annotated[
        dict[str, Any] | None,
        Field(
            description=(
                "Optional generation configuration dict. "
                "Example: {'temperature': 0.7, 'maxOutputTokens': 1024}"
            )
        ),
    ] = None,
) -> str:
    """Generate content using the Google native Gemini API.

    Uses the /v1beta/models/{model}:generateContent endpoint (Google native format).

    Use this when:
    - You need to use the native Google Gemini API format
    - You want fine-grained control over generation configuration

    Returns:
        JSON response containing the generated content.
    """
    try:
        kwargs: dict[str, Any] = {"contents": contents}

        if system_instruction is not None:
            kwargs["systemInstruction"] = system_instruction
        if generation_config is not None:
            kwargs["generationConfig"] = generation_config

        result = await client.generate_content(model=model, **kwargs)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except GeminiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except GeminiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error generating content", "message": str(e)})
