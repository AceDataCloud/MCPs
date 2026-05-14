"""Chat completion tools for GLM API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import GlmAPIError, GlmAuthError
from core.server import mcp
from core.types import DEFAULT_MODEL, GlmModel, ReasoningEffort, ServiceTier


@mcp.tool()
async def glm_chat_completions(
    messages: Annotated[
        list[dict[str, Any]],
        Field(
            description=(
                "Conversation messages. Each message is a dict with 'role' and 'content' keys. "
                "Required."
            )
        ),
    ],
    model: Annotated[
        GlmModel,
        Field(
            description=(
                "The GLM model to use. Options: glm-5.1, glm-4.7, glm-4.6, glm-4.5-air, "
                "glm-3-turbo. Default is glm-4.7."
            )
        ),
    ] = DEFAULT_MODEL,
    temperature: Annotated[
        float | None,
        Field(description="Sampling temperature between 0 and 2. Higher = more random. Default 1."),
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
    n: Annotated[
        int | None,
        Field(description="How many chat completion choices to generate. Default 1."),
    ] = None,
    stop: Annotated[
        str | list[str] | None,
        Field(description="Stop sequences where the API will stop generating tokens."),
    ] = None,
    frequency_penalty: Annotated[
        float | None,
        Field(
            description=(
                "Frequency penalty between -2.0 and 2.0. Positive values decrease repetition. "
                "Default 0."
            )
        ),
    ] = None,
    presence_penalty: Annotated[
        float | None,
        Field(
            description=(
                "Presence penalty between -2.0 and 2.0. Positive values increase topic variety. "
                "Default 0."
            )
        ),
    ] = None,
    seed: Annotated[
        int | None,
        Field(description="Random seed for deterministic sampling."),
    ] = None,
    response_format: Annotated[
        dict[str, Any] | None,
        Field(description='Response format specification (e.g. {"type": "json_object"}).'),
    ] = None,
    reasoning_effort: Annotated[
        ReasoningEffort | None,
        Field(description=("Reasoning effort level: minimal, low, medium, high. Default medium.")),
    ] = None,
    service_tier: Annotated[
        ServiceTier | None,
        Field(description=("Service tier: auto, default, flex, scale, priority. Default auto.")),
    ] = None,
    user: Annotated[
        str | None,
        Field(description="End-user identifier for abuse monitoring."),
    ] = None,
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(description="List of tools the model may call."),
    ] = None,
    tool_choice: Annotated[
        str | dict[str, Any] | None,
        Field(description="Controls which tool is called. Can be 'none', 'auto', or a dict."),
    ] = None,
    parallel_tool_calls: Annotated[
        bool | None,
        Field(description="Enable parallel function calling. Default True."),
    ] = None,
    max_completion_tokens: Annotated[
        int | None,
        Field(description="Upper bound for tokens that can be generated for a completion."),
    ] = None,
    logprobs: Annotated[
        bool | None,
        Field(description="Whether to return log probabilities of output tokens. Default False."),
    ] = None,
    top_logprobs: Annotated[
        int | None,
        Field(description="Number of most likely tokens to return at each token position."),
    ] = None,
    store: Annotated[
        bool | None,
        Field(description="Whether to store the output of this request. Default False."),
    ] = None,
    metadata: Annotated[
        dict[str, Any] | None,
        Field(description="Key-value pairs for storing additional information."),
    ] = None,
    logit_bias: Annotated[
        dict[str, Any] | None,
        Field(description="Modify the likelihood of specified tokens appearing in the completion."),
    ] = None,
    modalities: Annotated[
        list[str] | None,
        Field(description="Output types to generate (e.g. ['text', 'audio'])."),
    ] = None,
    audio: Annotated[
        dict[str, Any] | None,
        Field(description="Parameters for audio output."),
    ] = None,
    prediction: Annotated[
        dict[str, Any] | None,
        Field(description="Static predicted output content for latency reduction."),
    ] = None,
    web_search_options: Annotated[
        dict[str, Any] | None,
        Field(description="Options for web search tool."),
    ] = None,
    stream_options: Annotated[
        dict[str, Any] | None,
        Field(description="Options for streaming response."),
    ] = None,
) -> str:
    """Create a GLM chat completion using the AceDataCloud GLM API.

    Sends messages to the specified GLM model and returns the generated response.
    Supports all GLM models: glm-5.1, glm-4.7, glm-4.6, glm-4.5-air, glm-3-turbo.

    Use this when:
    - You need to chat with a Zhipu GLM model
    - You need Chinese language understanding or generation
    - You want to use GLM's reasoning capabilities

    Returns:
        JSON response containing the chat completion result.
    """
    if not messages:
        return json.dumps({"error": "Validation Error", "message": "messages is required"})

    try:
        result = await client.chat_completions(
            messages=messages,
            model=model,
            n=n,
            stream=stream,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            seed=seed,
            stop=stop,
            max_completion_tokens=max_completion_tokens,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
            stream_options=stream_options,
            parallel_tool_calls=parallel_tool_calls,
            user=user,
            reasoning_effort=reasoning_effort,
            service_tier=service_tier,
            store=store,
            metadata=metadata,
            logit_bias=logit_bias,
            modalities=modalities,
            audio=audio,
            prediction=prediction,
            web_search_options=web_search_options,
            tools=tools,
            tool_choice=tool_choice,
        )

        if not result:
            return json.dumps({"error": "No response received from the API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except GlmAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except GlmAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating chat completion", "message": str(e)})
