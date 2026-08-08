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
    ReasoningEffort,
    ServiceTier,
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
    response_format: Annotated[
        dict[str, Any] | None,
        Field(
            description=(
                "Optional response format object, such as {'type': 'text'}, "
                "{'type': 'json_object'}, or {'type': 'json_schema', 'json_schema': {...}}."
            )
        ),
    ] = None,
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Optional tool definitions the model may call."),
    ] = None,
    tool_choice: Annotated[
        str | dict[str, Any] | None,
        Field(
            description=(
                "Controls which tool is called. Use 'none', 'auto', 'required', "
                "or an object selecting a specific function tool."
            )
        ),
    ] = None,
    top_p: Annotated[
        float | None,
        Field(description="Nucleus sampling value between 0 and 1. Default is 1."),
    ] = None,
    frequency_penalty: Annotated[
        float | None,
        Field(description="Penalty between -2 and 2 for repeated tokens. Default is 0."),
    ] = None,
    presence_penalty: Annotated[
        float | None,
        Field(description="Penalty between -2 and 2 for tokens already present. Default is 0."),
    ] = None,
    seed: Annotated[
        int | None,
        Field(description="Optional seed for deterministic sampling where supported."),
    ] = None,
    stop: Annotated[
        str | list[str] | None,
        Field(description="Stop sequence or up to four stop sequences."),
    ] = None,
    max_completion_tokens: Annotated[
        int | None,
        Field(description="Upper bound for generated completion tokens."),
    ] = None,
    logprobs: Annotated[
        bool | None,
        Field(description="Whether to return log probabilities for output tokens."),
    ] = None,
    top_logprobs: Annotated[
        int | None,
        Field(description="Number of most likely tokens to return at each position (0-20)."),
    ] = None,
    stream: Annotated[
        bool | None,
        Field(description="Whether to stream the response. Default is False."),
    ] = None,
    stream_options: Annotated[
        dict[str, Any] | None,
        Field(description="Additional streaming options."),
    ] = None,
    parallel_tool_calls: Annotated[
        bool | None,
        Field(description="Whether to allow parallel tool calls. Default is True."),
    ] = None,
    user: Annotated[
        str | None,
        Field(description="End-user identifier for abuse monitoring."),
    ] = None,
    n: Annotated[
        int | None,
        Field(
            description="How many chat completion choices to generate for each input. Default is 1."
        ),
    ] = None,
    store: Annotated[
        bool | None,
        Field(description="Whether to store the output for later retrieval. Default is False."),
    ] = None,
    metadata: Annotated[
        dict[str, Any] | None,
        Field(description="Optional metadata attached to the request."),
    ] = None,
    logit_bias: Annotated[
        dict[str, Any] | None,
        Field(description="Token bias map to adjust likelihood of selected tokens."),
    ] = None,
    modalities: Annotated[
        list[str] | None,
        Field(description="Output modalities requested from the model."),
    ] = None,
    audio: Annotated[
        dict[str, Any] | None,
        Field(description="Audio output options when requesting audio modalities."),
    ] = None,
    prediction: Annotated[
        dict[str, Any] | None,
        Field(description="Prediction hints for supported models."),
    ] = None,
    web_search_options: Annotated[
        dict[str, Any] | None,
        Field(description="Web search options for models that support web search."),
    ] = None,
    reasoning_effort: Annotated[
        ReasoningEffort | None,
        Field(
            description=(
                "Constrains effort on reasoning for reasoning models. Options: 'minimal', "
                "'low', 'medium', 'high'. Default is 'medium'."
            )
        ),
    ] = None,
    service_tier: Annotated[
        ServiceTier | None,
        Field(
            description=(
                "Specifies the processing tier. Options: 'auto' (default), 'default', "
                "'flex', 'scale', 'priority'."
            )
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
        if response_format is not None:
            payload["response_format"] = response_format
        if tools is not None:
            payload["tools"] = tools
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice
        if top_p is not None:
            payload["top_p"] = top_p
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            payload["presence_penalty"] = presence_penalty
        if seed is not None:
            payload["seed"] = seed
        if stop is not None:
            payload["stop"] = stop
        if max_completion_tokens is not None:
            payload["max_completion_tokens"] = max_completion_tokens
        if logprobs is not None:
            payload["logprobs"] = logprobs
        if top_logprobs is not None:
            payload["top_logprobs"] = top_logprobs
        if stream is not None:
            payload["stream"] = stream
        if stream_options is not None:
            payload["stream_options"] = stream_options
        if parallel_tool_calls is not None:
            payload["parallel_tool_calls"] = parallel_tool_calls
        if user is not None:
            payload["user"] = user
        if n is not None:
            payload["n"] = n
        if store is not None:
            payload["store"] = store
        if metadata is not None:
            payload["metadata"] = metadata
        if logit_bias is not None:
            payload["logit_bias"] = logit_bias
        if modalities is not None:
            payload["modalities"] = modalities
        if audio is not None:
            payload["audio"] = audio
        if prediction is not None:
            payload["prediction"] = prediction
        if web_search_options is not None:
            payload["web_search_options"] = web_search_options
        if reasoning_effort is not None:
            payload["reasoning_effort"] = reasoning_effort
        if service_tier is not None:
            payload["service_tier"] = service_tier

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
