"""Restricted GPT Image MCP profile backed by the existing image/task implementation.

This is a separate tool surface, not a second name for the general OpenAI server.
The shared API client, errors, billing semantics and task queries stay authoritative.
"""

import inspect
import json
from collections.abc import Callable
from functools import wraps
from typing import Annotated, Any, Literal, get_args

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from core.types import ImageModel
from tools import image_tools, tasks_tools

GPT_IMAGE_MODELS = tuple(
    model
    for model in get_args(ImageModel)
    if model.startswith("gpt-image-") and ":reverse" not in model
)


def image_function(original: Callable[..., Any]) -> Callable[..., Any]:
    """Reuse the full source signature, restricting only the explicit model choice."""
    signature = inspect.signature(original)
    model_type = Annotated[
        Literal[GPT_IMAGE_MODELS],  # type: ignore[valid-type]
        Field(description="Choose a GPT Image model explicitly; check current pricing first."),
    ]
    parameters = [
        parameter.replace(annotation=model_type, default=inspect.Parameter.empty)
        if parameter.name == "model"
        else parameter
        for parameter in signature.parameters.values()
    ]
    restricted = signature.replace(parameters=parameters)

    @wraps(original)
    async def invoke(**arguments: Any) -> Any:
        # Defensive validation also protects callers invoking this Python wrapper.
        bound = restricted.bind(**arguments)
        if bound.arguments["model"] not in GPT_IMAGE_MODELS:
            raise ValueError("This profile supports GPT Image models only")
        return await original(**bound.arguments)

    invoke.__signature__ = restricted  # type: ignore[attr-defined]
    return invoke


async def gpt_image_list_models() -> str:
    """List GPT Image model identifiers without sending an API request."""
    return json.dumps(
        {
            "models": GPT_IMAGE_MODELS,
            "usage": "Generation/editing is billable. Choose a model explicitly; never regenerate to poll.",
        }
    )


def create_server() -> FastMCP:
    server = FastMCP(
        "GPT Image by Ace Data Cloud",
        instructions=(
            "GPT Image generation, editing, and task retrieval through Ace Data Cloud. "
            "Ask before a billable creation. Query the same task ID until terminal. "
            "A pending response is not a finished image."
        ),
    )
    server.add_tool(image_function(image_tools.openai_generate_image), name="gpt_image_generate")
    server.add_tool(image_function(image_tools.openai_edit_image), name="gpt_image_edit")
    server.add_tool(tasks_tools.openai_get_task, name="gpt_image_get_task")
    server.add_tool(tasks_tools.openai_list_tasks, name="gpt_image_list_tasks")
    server.add_tool(gpt_image_list_models)
    return server
