"""Chat completion tools for Grok API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import GrokAPIError, GrokAuthError
from core.server import mcp
from core.types import DEFAULT_CHAT_MODEL, GrokChatModel, ReasoningEffort, ServiceTier


@mcp.tool()
async def grok_chat_completions(
    messages: Annotated[
        list[dict[str, Any]],
        Field(
            description=(
                "Conversation messages. Each message is a dict with 'role' "
                "('system'/'user'/'assistant'/'tool') and 'content' keys. Content may be a "
                "list of text/image_url parts for image input. Required."
            )
        ),
    ],
    model: Annotated[
        GrokChatModel,
        Field(
            description=(
                "The Grok chat model: grok-4.5 (default, latest flagship), grok-4 or grok-3."
            )
        ),
    ] = DEFAULT_CHAT_MODEL,
    temperature: Annotated[
        float | None,
        Field(description="Sampling temperature between 0 and 2. Higher = more random."),
    ] = None,
    max_tokens: Annotated[
        int | None,
        Field(description="Maximum number of tokens to generate."),
    ] = None,
    top_p: Annotated[
        float | None,
        Field(description="Nucleus sampling probability mass. Default 1."),
    ] = None,
    stream: Annotated[
        bool | None,
        Field(description="Whether to stream partial message deltas. Default False."),
    ] = None,
    stop: Annotated[
        str | list[str] | None,
        Field(description="Stop sequences where the API will stop generating tokens."),
    ] = None,
    frequency_penalty: Annotated[
        float | None,
        Field(description="Frequency penalty between -2.0 and 2.0. Positive decreases repetition."),
    ] = None,
    presence_penalty: Annotated[
        float | None,
        Field(
            description="Presence penalty between -2.0 and 2.0. Positive increases topic variety."
        ),
    ] = None,
    seed: Annotated[
        int | None,
        Field(description="Random seed for (best-effort) deterministic sampling."),
    ] = None,
    response_format: Annotated[
        dict[str, Any] | None,
        Field(description='Response format specification (e.g. {"type": "json_object"}).'),
    ] = None,
    reasoning_effort: Annotated[
        ReasoningEffort | None,
        Field(
            description=(
                "Reasoning effort. Only applies to reasoning-capable models; "
                "ignored by non-reasoning models."
            )
        ),
    ] = None,
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(description="List of tools (functions) the model may call."),
    ] = None,
    tool_choice: Annotated[
        str | dict[str, Any] | None,
        Field(description="Controls tool calling. 'none', 'auto', 'required', or a dict."),
    ] = None,
    user: Annotated[
        str | None,
        Field(description="End-user identifier for abuse monitoring."),
    ] = None,
    service_tier: Annotated[
        ServiceTier | None,
        Field(
            description=(
                "Specifies the processing tier. Options: 'auto' (default), 'default', "
                "'flex' (asynchronous batch-eligible), 'scale', or 'priority'."
            )
        ),
    ] = None,
    n: Annotated[
        int | None,
        Field(description="How many chat completion choices to generate. Default 1."),
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
        Field(description="Whether to enable parallel tool calls. Default true."),
    ] = None,
    store: Annotated[
        bool | None,
        Field(description="Whether to store the output of this chat completion. Default false."),
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
    """Create a Grok (xAI) chat completion via the AceDataCloud Grok API.

    Sends messages to a Grok chat model and returns the generated response in the
    OpenAI-compatible chat completion format.

    Use this when:
    - You want to chat/reason with a Grok model (grok-4 / grok-3 family)
    - You need vision/image understanding
    - You need tool/function calling with Grok

    For generating videos, use grok_text_to_video / grok_image_to_video instead.

    Returns:
        JSON response containing the chat completion result.
    """
    if not messages:
        return json.dumps({"error": "Validation Error", "message": "messages is required"})

    try:
        result = await client.chat_completions(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            stop=stop,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            seed=seed,
            response_format=response_format,
            reasoning_effort=reasoning_effort,
            tools=tools,
            tool_choice=tool_choice,
            user=user,
            service_tier=service_tier,
            n=n,
            max_completion_tokens=max_completion_tokens,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            stream_options=stream_options,
            parallel_tool_calls=parallel_tool_calls,
            store=store,
            metadata=metadata,
            logit_bias=logit_bias,
            modalities=modalities,
            audio=audio,
            prediction=prediction,
            web_search_options=web_search_options,
        )

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except GrokAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except GrokAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating chat completion", "message": str(e)})
