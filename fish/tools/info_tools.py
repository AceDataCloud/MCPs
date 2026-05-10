"""Informational tools for Fish API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import FishAPIError, FishAuthError
from core.server import mcp


@mcp.tool()
async def fish_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Fish TTS tools.

    Provides detailed information on how to use the Fish tools effectively,
    including parameters, examples, and best practices.

    Returns:
        Complete usage guide for Fish TTS tools.
    """
    # Last updated: 2026-05-10
    return """# Fish TTS Tools Usage Guide

## Available Tools

### Audio Generation
**fish_generate_audio** - Convert text to speech using a voice
- text: The text to synthesize (required)
- reference_id: Voice model ID (optional)
- model: `s1` or `s2-pro` (optional, default `s2-pro`)
- format: `mp3`, `wav`, `pcm`, `opus` (optional)
- callback_url: Async callback URL (optional)

### Voice Models
**fish_list_models** - Query available voice models
- page_size: Number of items per page (optional, default 10)
- page_number: Page number (optional, default 1)
- title/tag/language/...: Optional query filters

**fish_get_model** - Query a single voice model detail by model ID
- model_id: Voice model ID (required)

### Task Status
**fish_get_task** - Check status of a single task
- task_id: The task ID from a generation request (required)

**fish_get_tasks_batch** - Check status of multiple tasks
- task_ids: List of task IDs (required)

## Example Usage

### Generate Speech
```
fish_generate_audio(
    text="Hello, welcome to our service!",
    reference_id="d7900c21663f485ab63ebdb7e5905036"
)
```

### Query Models
```
fish_list_models(page_size=10, page_number=1)
```

### Check Task Status
```
fish_get_task(task_id="93f11baf-347b-4bb4-9520-8653cb46d6a3")
```

## Workflow: Async Generation

For long-running tasks, the API may return a task_id immediately.
Poll fish_get_task until the state is 'complete':

1. Call fish_generate_audio → get task_id
2. Call fish_get_task(task_id=...) repeatedly
3. When state='complete', retrieve the audio URL from the response

## Response Structure

### Successful Response
- **success**: `true` - request was successful
- **task_id**: Task ID for polling
- **data**: Array of result items with audio URLs or voice IDs

### Error Response
- **error.code**: Error code (e.g., `bad_request`, `invalid_token`)
- **error.message**: Human-readable error description
- **trace_id**: Request trace ID for debugging
"""


@mcp.tool()
async def fish_list_models(
    page_size: Annotated[
        int | None,
        Field(description="Number of items per page. Default is 10."),
    ] = None,
    page_number: Annotated[
        int | None,
        Field(description="Page number. Default is 1."),
    ] = None,
    title: Annotated[
        str | None,
        Field(description="Filter by model title."),
    ] = None,
    tag: Annotated[
        str | None,
        Field(description="Filter by tag."),
    ] = None,
    self_only: Annotated[
        bool | None,
        Field(
            description=(
                "Filter to current user's models only. "
                "Maps to OpenAPI query parameter `self`."
            )
        ),
    ] = None,
    author_id: Annotated[
        str | None,
        Field(description="Filter by author id."),
    ] = None,
    language: Annotated[
        str | None,
        Field(description="Filter by language."),
    ] = None,
    title_language: Annotated[
        str | None,
        Field(description="Filter by title language."),
    ] = None,
    sort_by: Annotated[
        str | None,
        Field(description="Sort strategy."),
    ] = None,
) -> str:
    """List available Fish voice models from /fish/model."""
    params: dict = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_number is not None:
        params["page_number"] = page_number
    if title is not None:
        params["title"] = title
    if tag is not None:
        params["tag"] = tag
    if self_only is not None:
        params["self"] = self_only
    if author_id is not None:
        params["author_id"] = author_id
    if language is not None:
        params["language"] = language
    if title_language is not None:
        params["title_language"] = title_language
    if sort_by is not None:
        params["sort_by"] = sort_by

    try:
        result = await client.list_models(**params)
        if not result:
            return json.dumps({"error": "No response received from the API."})
        return json.dumps(result, ensure_ascii=False, indent=2)
    except FishAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except FishAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error listing models", "message": str(e)})


@mcp.tool()
async def fish_get_model(
    model_id: Annotated[
        str,
        Field(description="Model ID to retrieve, from /fish/model/{id}."),
    ],
) -> str:
    """Get a single Fish voice model by model id."""
    try:
        result = await client.get_model(model_id)
        if not result:
            return json.dumps({"error": "No response received from the API."})
        return json.dumps(result, ensure_ascii=False, indent=2)
    except FishAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except FishAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error getting model", "message": str(e)})
