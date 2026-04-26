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
    top_p: Annotated[
        float | None,
        Field(
            description=(
                "Nucleus sampling probability mass. The model considers only the tokens with "
                "top_p probability mass. 0.1 means only the tokens comprising the top 10% "
                "probability mass are considered. Default is 1."
            )
        ),
    ] = None,
    frequency_penalty: Annotated[
        float | None,
        Field(
            description=(
                "Number between -2.0 and 2.0. Positive values penalize new tokens based on "
                "their existing frequency in the text so far, decreasing the model's likelihood "
                "to repeat the same line verbatim. Default is 0."
            )
        ),
    ] = None,
    presence_penalty: Annotated[
        float | None,
        Field(
            description=(
                "Number between -2.0 and 2.0. Positive values penalize new tokens based on "
                "whether they appear in the text so far, increasing the model's likelihood to "
                "talk about new topics. Default is 0."
            )
        ),
    ] = None,
    seed: Annotated[
        int | None,
        Field(
            description=(
                "If specified, the system will make a best effort to sample deterministically "
                "such that repeated requests with the same seed and parameters return the same "
                "result."
            )
        ),
    ] = None,
    max_completion_tokens: Annotated[
        int | None,
        Field(
            description=(
                "An upper bound for the number of tokens that can be generated for a completion, "
                "including visible output tokens and reasoning tokens."
            )
        ),
    ] = None,
    stop: Annotated[
        str | list[str] | None,
        Field(
            description=(
                "Up to 4 sequences where the API will stop generating further tokens. "
                "Can be a string or an array of strings."
            )
        ),
    ] = None,
    user: Annotated[
        str | None,
        Field(
            description=(
                "A unique identifier representing your end-user, which can help monitor "
                "and detect abuse."
            )
        ),
    ] = None,
    service_tier: Annotated[
        ServiceTier | None,
        Field(
            description=(
                "Specifies the latency tier to use for processing the request. "
                "Options: 'auto', 'default', 'flex', 'scale', 'priority'."
            )
        ),
    ] = None,
    reasoning_effort: Annotated[
        ReasoningEffort | None,
        Field(
            description=(
                "Controls the effort level of reasoning for o-series models. "
                "Options: 'minimal', 'low', 'medium', 'high'. "
                "The API default is 'medium' when not specified."
            )
        ),
    ] = None,
    store: Annotated[
        bool | None,
        Field(
            description=(
                "Whether to store the output of this chat completion request. "
                "Default is False."
            )
        ),
    ] = None,
    logprobs: Annotated[
        bool | None,
        Field(
            description=(
                "Whether to return log probabilities of the output tokens. "
                "Default is False."
            )
        ),
    ] = None,
    top_logprobs: Annotated[
        int | None,
        Field(
            description=(
                "An integer between 0 and 20 specifying the number of most likely tokens "
                "to return at each position. Requires logprobs=True."
            )
        ),
    ] = None,
    parallel_tool_calls: Annotated[
        bool | None,
        Field(
            description=(
                "Whether to enable parallel function calling during tool use. "
                "Default is True."
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
        if n is not None:
            payload["n"] = n
        if top_p is not None:
            payload["top_p"] = top_p
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            payload["presence_penalty"] = presence_penalty
        if seed is not None:
            payload["seed"] = seed
        if max_completion_tokens is not None:
            payload["max_completion_tokens"] = max_completion_tokens
        if stop is not None:
            payload["stop"] = stop
        if user is not None:
            payload["user"] = user
        if service_tier is not None:
            payload["service_tier"] = service_tier
        if reasoning_effort is not None:
            payload["reasoning_effort"] = reasoning_effort
        if store is not None:
            payload["store"] = store
        if logprobs is not None:
            payload["logprobs"] = logprobs
        if top_logprobs is not None:
            payload["top_logprobs"] = top_logprobs
        if parallel_tool_calls is not None:
            payload["parallel_tool_calls"] = parallel_tool_calls

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
