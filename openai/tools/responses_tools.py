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
        str | list[dict[str, Any]],
        Field(
            description=(
                "A text prompt or a list of messages comprising the conversation. Each message "
                "must have a 'role' ('system', 'user', or 'assistant') and 'content' field. "
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
        Field(description="Number of response choices to generate. Default is 1."),
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
    response_format: Annotated[
        dict[str, Any] | None,
        Field(description='Response format specification, such as {"type": "json_object"}.'),
    ] = None,
    stream: Annotated[
        bool | None,
        Field(description="Whether to stream partial response output. Default is false."),
    ] = None,
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Tools the model may call while creating the response."),
    ] = None,
    tool_choice: Annotated[
        str | dict[str, Any] | None,
        Field(description="Controls tool calling: 'none', 'auto', 'required', or a tool object."),
    ] = None,
    parallel_tool_calls: Annotated[
        bool | None,
        Field(description="Whether to enable parallel tool calls. Default is true."),
    ] = None,
    include: Annotated[
        list[str] | None,
        Field(description="Additional response payload sections to include."),
    ] = None,
    reasoning: Annotated[
        dict[str, Any] | None,
        Field(description="Reasoning configuration options."),
    ] = None,
    text: Annotated[
        dict[str, Any] | None,
        Field(description="Text output configuration options."),
    ] = None,
    max_output_tokens: Annotated[
        int | None,
        Field(description="Upper bound for tokens generated in the response output."),
    ] = None,
    store: Annotated[
        bool | None,
        Field(description="Whether to store the output of this response."),
    ] = None,
    stream_options: Annotated[
        dict[str, Any] | None,
        Field(description="Options for streaming responses."),
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
        if response_format is not None:
            payload["response_format"] = response_format
        if stream is not None:
            payload["stream"] = stream
        if tools is not None:
            payload["tools"] = tools
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice
        if parallel_tool_calls is not None:
            payload["parallel_tool_calls"] = parallel_tool_calls
        if include is not None:
            payload["include"] = include
        if reasoning is not None:
            payload["reasoning"] = reasoning
        if text is not None:
            payload["text"] = text
        if max_output_tokens is not None:
            payload["max_output_tokens"] = max_output_tokens
        if store is not None:
            payload["store"] = store
        if stream_options is not None:
            payload["stream_options"] = stream_options

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
