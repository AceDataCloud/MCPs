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
- text: The text to convert to speech (required)
- reference_id: Voice model ID to condition speech (optional)
- model: "s1" or "s2-pro" (optional, default: s2-pro)
- format: "mp3" | "wav" | "pcm" | "opus" (optional, default: mp3)
- callback_url: Async callback URL (optional)

### Model Discovery
**fish_list_models** - List available voice models
- page_size, page_number: Pagination controls (optional)
- title, tag, language, title_language: Filters (optional)
- self_only, author_id, sort_by: Ownership and sort filters (optional)

**fish_get_model** - Get details of a single model
- model_id: The model ID from fish_list_models (required)

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

### List Models
```
fish_list_models(language="en", page_size=10)
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
- **data**: Result payload from the API (task detail, model list, or model detail)

### Error Response
- **error.code**: Error code (e.g., `bad_request`, `invalid_token`)
- **error.message**: Human-readable error description
- **trace_id**: Request trace ID for debugging
"""


@mcp.tool()
async def fish_list_models(
    page_size: Annotated[
        int | None,
        Field(description="Number of items per page. Defaults to 10."),
    ] = None,
    page_number: Annotated[
        int | None,
        Field(description="1-based page number. Defaults to 1."),
    ] = None,
    title: Annotated[
        str | None,
        Field(description="Filter by partial title match."),
    ] = None,
    tag: Annotated[
        str | None,
        Field(description="Filter by a single tag."),
    ] = None,
    self_only: Annotated[
        bool | None,
        Field(description="When true, only return models owned by the calling account."),
    ] = None,
    author_id: Annotated[
        str | None,
        Field(description="Filter by author id."),
    ] = None,
    language: Annotated[
        str | None,
        Field(description="Filter by language code (e.g. en, zh)."),
    ] = None,
    title_language: Annotated[
        str | None,
        Field(description="Filter by title language."),
    ] = None,
    sort_by: Annotated[
        str | None,
        Field(description="Sort by field accepted by upstream (e.g. created_at, task_count)."),
    ] = None,
) -> str:
    """List available Fish voice models from the API.

    Returns:
        JSON response from /fish/model.
    """
    try:
        params: dict[str, int | str | bool] = {}
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
        Field(description="The unique identifier of the voice model to fetch."),
    ],
) -> str:
    """Get a Fish voice model by ID.

    Returns:
        JSON response from /fish/model/{id}.
    """
    if not model_id:
        return json.dumps({"error": "Validation Error", "message": "model_id is required"})
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
