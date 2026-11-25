"""Native Messages tools for models with a published Anthropic-compatible contract."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.messages_models import MessagesModel
from core.server import mcp


@mcp.tool()
async def aichat_create_message(
    model: Annotated[
        MessagesModel,
        Field(description="Choose a model from the native Messages list in aichat_list_models."),
    ],
    messages: Annotated[
        list[dict[str, Any]],
        Field(
            min_length=1,
            description="Native Messages history with user/assistant roles and string or content-block content.",
        ),
    ],
    max_tokens: Annotated[
        int,
        Field(
            gt=0,
            description="Required output token budget for this request. This is not the model's maximum context size.",
        ),
    ],
    system: str | list[dict[str, Any]] | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    top_k: int | None = None,
    stop_sequences: list[str] | None = None,
    tools: list[dict[str, Any]] | None = None,
    tool_choice: dict[str, Any] | None = None,
    thinking: dict[str, Any] | None = None,
    output_config: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    cache_control: dict[str, Any] | None = None,
) -> str:
    """Send one native /v1/messages request and return its unmodified response.

    Use this for Claude 5.5 and other models listed for native Messages.
    Supply a General application API token with access to the Claude Messages API.
    Generation uses the application's existing balance. There is no automatic retry.
    """
    result = await client.create_message(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        system=system,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        stop_sequences=stop_sequences,
        tools=tools,
        tool_choice=tool_choice,
        thinking=thinking,
        output_config=output_config,
        metadata=metadata,
        cache_control=cache_control,
    )
    return json.dumps(result, ensure_ascii=False)
