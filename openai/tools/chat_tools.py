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
    n: Annotated[
        int | None,
        Field(
            description="How many chat completion choices to generate for each input. Default is 1."
        ),
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
    stream: Annotated[
        bool | None,
        Field(description="Whether to stream partial message deltas. Default is false."),
    ] = None,
    response_format: Annotated[
        dict[str, Any] | None,
        Field(description='Response format specification, such as {"type": "json_object"}.'),
    ] = None,
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(description="Tools/functions the model may call."),
    ] = None,
    tool_choice: Annotated[
        str | dict[str, Any] | None,
        Field(
            description="Controls tool calling: 'none', 'auto', 'required', or a tool choice object."
        ),
    ] = None,
    top_p: Annotated[
        float | None,
        Field(description="Nucleus sampling probability mass. Default is 1."),
    ] = None,
    frequency_penalty: Annotated[
        float | None,
        Field(description="Frequency penalty between -2.0 and 2.0."),
    ] = None,
    presence_penalty: Annotated[
        float | None,
        Field(description="Presence penalty between -2.0 and 2.0."),
    ] = None,
    seed: Annotated[
        int | None,
        Field(description="Random seed for best-effort deterministic sampling."),
    ] = None,
    stop: Annotated[
        str | list[str] | None,
        Field(description="Stop sequences where the API will stop generating tokens."),
    ] = None,
    max_completion_tokens: Annotated[
        int | None,
        Field(description="Upper bound for tokens generated for a completion."),
    ] = None,
    logprobs: Annotated[
        bool | None,
        Field(description="Whether to return log probabilities of output tokens."),
    ] = None,
    top_logprobs: Annotated[
        int | None,
        Field(description="Number of most likely tokens to return at each token position."),
    ] = None,
    stream_options: Annotated[
        dict[str, Any] | None,
        Field(description="Options for streaming responses."),
    ] = None,
    parallel_tool_calls: Annotated[
        bool | None,
        Field(description="Whether to enable parallel tool calls. Default is true."),
    ] = None,
    user: Annotated[
        str | None,
        Field(description="End-user identifier for abuse monitoring."),
    ] = None,
    store: Annotated[
        bool | None,
        Field(description="Whether to store the output of this chat completion. Default is false."),
    ] = None,
    metadata: Annotated[
        dict[str, Any] | None,
        Field(description="Developer-defined metadata attached to the request."),
    ] = None,
    logit_bias: Annotated[
        dict[str, int] | None,
        Field(description="Token logit bias map."),
    ] = None,
    modalities: Annotated[
        list[str] | None,
        Field(description="Output modalities requested for this response."),
    ] = None,
    audio: Annotated[
        dict[str, Any] | None,
        Field(description="Audio output configuration when requesting audio modality."),
    ] = None,
    prediction: Annotated[
        dict[str, Any] | None,
        Field(description="Static predicted output content to improve latency."),
    ] = None,
    web_search_options: Annotated[
        dict[str, Any] | None,
        Field(description="Web search configuration for search-capable models."),
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
        if reasoning_effort is not None:
            payload["reasoning_effort"] = reasoning_effort
        if service_tier is not None:
            payload["service_tier"] = service_tier
        optional_params = {
            "stream": stream,
            "response_format": response_format,
            "tools": tools,
            "tool_choice": tool_choice,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "seed": seed,
            "stop": stop,
            "max_completion_tokens": max_completion_tokens,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
            "stream_options": stream_options,
            "parallel_tool_calls": parallel_tool_calls,
            "user": user,
            "store": store,
            "metadata": metadata,
            "logit_bias": logit_bias,
            "modalities": modalities,
            "audio": audio,
            "prediction": prediction,
            "web_search_options": web_search_options,
        }
        payload.update({key: value for key, value in optional_params.items() if value is not None})

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
