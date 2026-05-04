"""Informational tools for WebExtrator API."""

from core.server import mcp


@mcp.tool()
async def webextrator_get_usage_guide() -> str:
    """Get a comprehensive guide for using the WebExtrator tools.

    Provides detailed information on how to use the WebExtrator tools effectively,
    including parameters, examples, and best practices for web extraction and rendering.

    Returns:
        Complete usage guide for WebExtrator tools.
    """
    return """# WebExtrator Tools Usage Guide

## Available Tools

### webextrator_extract
Extract structured content from a web page.

**Parameters:**
- `url` (required): The URL of the web page to extract content from.
- `expected_type` (optional): Hint about expected content type — 'product', 'article', or 'general'.
- `enable_llm` (optional): Enable LLM-based semantic normalization (boolean). Default: false.
- `wait_until` (optional): Page load condition — 'load', 'domcontentloaded', 'networkidle', 'commit'. Default: 'networkidle'.
- `timeout` (optional): Total timeout in seconds. Default: 30.
- `delay` (optional): Extra delay in seconds after page load.
- `wait_for_selector` (optional): CSS selector to wait for before extracting.
- `block_resources` (optional): List of resource types to block — 'image', 'font', 'media', 'stylesheet', 'xhr', 'fetch'.
- `headers` (optional): Extra HTTP headers as key-value pairs.
- `user_agent` (optional): Override the User-Agent header.
- `callback_url` (optional): Async callback URL — triggers async processing.

### webextrator_render
Render a web page with a headless browser and return the rendered HTML.

**Parameters:**
- `url` (required): The URL of the web page to render.
- `wait_until` (optional): Page load condition. Default: 'networkidle'.
- `timeout` (optional): Total timeout in seconds. Default: 30.
- `delay` (optional): Extra delay in seconds after page load.
- `wait_for_selector` (optional): CSS selector to wait for before capturing HTML.
- `block_resources` (optional): Resource types to block.
- `headers` (optional): Extra HTTP headers.
- `user_agent` (optional): Override User-Agent.
- `callback_url` (optional): Async callback URL.

### webextrator_get_task
Retrieve the result of a single previously created task.

**Parameters:**
- `task_id` (optional): Task UUID to look up.
- `trace_id` (optional): Trace UUID as an alternative lookup. Either task_id or trace_id required.

### webextrator_get_tasks_batch
Retrieve results for multiple tasks in one call.

**Parameters:**
- `ids` (optional): List of task UUIDs.
- `trace_ids` (optional): List of trace UUIDs. Either ids or trace_ids required.
- `offset` (optional): Pagination offset. Default: 0.
- `limit` (optional): Pagination limit. Default: 12.

### webextrator_get_usage_guide
Show this usage guide.

## Example Usage

### Extract Product Information
```
webextrator_extract(
    url="https://example.com/product/123",
    expected_type="product",
    enable_llm=True
)
```

### Extract Article Content
```
webextrator_extract(
    url="https://example.com/blog/my-article",
    expected_type="article",
    wait_until="networkidle"
)
```

### Render a JavaScript SPA
```
webextrator_render(
    url="https://example.com/app",
    wait_until="networkidle",
    wait_for_selector="#main-content"
)
```

### Block Heavy Resources for Speed
```
webextrator_render(
    url="https://example.com/page",
    block_resources=["image", "font", "media"],
    timeout=15
)
```

### Async Extraction with Callback
```
webextrator_extract(
    url="https://example.com/large-page",
    callback_url="https://your-server.com/webhook"
)
# Then poll for the result:
webextrator_get_task(task_id="<returned-task-id>")
```

### Retrieve Multiple Task Results
```
webextrator_get_tasks_batch(
    ids=["task-uuid-1", "task-uuid-2", "task-uuid-3"]
)
```

## Response Structure

### Extract Response
- **id**: Task identifier
- **data**: Extracted structured content (product/article/general fields)
- **status**: Task status ('success', 'pending', 'failed')

### Render Response
- **id**: Task identifier
- **html**: The fully rendered HTML source
- **status**: Task status

### Error Response
- **error**: Error type description
- **message**: Human-readable error description

## Notes
- Use `block_resources` to speed up rendering when you don't need images or styles
- Use `wait_for_selector` to ensure dynamic content has loaded before extraction
- Use `callback_url` for large pages or when you don't want to wait synchronously
- Bearer token authentication is required
"""
