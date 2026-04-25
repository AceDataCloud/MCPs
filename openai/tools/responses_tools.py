"""Responses API tools for OpenAI."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp
from core.types import (
    DEFAULT_RESPONSES_MODEL,
    ResponsesModel,
)


@mcp.tool()
async def openai_create_response(
    input: Annotated[
        list[dict[str, Any]],
        Field(
            description=(
                "A list of messages comprising the conversation. Each message must have a "
                "'role' ('system', 'user', or 'assistant') and 'content' field. "
                "Example: [{'role': 'user', 'content': 'Explain quantum computing'}]"
            )
        ),
    ],
    model: Annotated[
        ResponsesModel,
        Field(
            description=(
                "The model to use. Supports a wide range of GPT-4, GPT-4o, GPT-5, and "
                "o-series models including their dated variants. Default is gpt-4.1."
            )
        ),
    ] = DEFAULT_RESPONSES_MODEL,
    max_tokens: Annotated[
        int | None,
        Field(
            description=(
                "The maximum number of tokens to generate in the response. "
                "If not specified, the model uses its default limit."
            )
        ),
    ] = None,
    temperature: Annotated[
        float | None,
        Field(
            description=(
                "Sampling temperature between 0 and 2. Higher values produce more creative "
                "output; lower values produce more deterministic output. Default is 1."
            )
        ),
    ] = None,
    n: Annotated[
        int | None,
        Field(
            description="Number of response choices to generate. Default is 1."
        ),
    ] = None,
    background: Annotated[
        bool | None,
        Field(
            description=(
                "Whether to run the model response in the background. "
                "When True, returns immediately with a task ID."
            )
        ),
    ] = None,
) -> str:
    """Create a response using the OpenAI Responses API via AceDataCloud.

    The Responses API is an alternative to the Chat Completions API with support
    for a wider range of model variants and additional features like background processing.

    Use this when:
    - You need access to model-specific dated variants (e.g., o3-2025-04-16)
    - You want background processing with a task ID
    - You need access to search-preview models

    Returns:
        JSON response containing the model's output and usage information.
    """
    try:
        payload: dict[str, Any] = {
            "model": model,
            "input": input,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if n is not None:
            payload["n"] = n
        if background is not None:
            payload["background"] = background

        result = await client.responses(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating response", "message": str(e)})
