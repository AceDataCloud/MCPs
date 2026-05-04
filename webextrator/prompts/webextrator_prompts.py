"""Prompt templates for WebExtrator MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def webextrator_guide() -> str:
    """Guide for choosing the right WebExtrator tool for web extraction and rendering tasks."""
    return """# WebExtrator Guide

When the user wants to extract data or render content from a web page, use the appropriate tool:

## Structured Content Extraction
**Tool:** `webextrator_extract`
**Use when:**
- User wants to extract product details, prices, or specifications from an e-commerce page
- User wants to extract article text, title, or metadata from a news/blog page
- User needs structured data from any web page

**Example:** "Extract the product details from this URL: https://example.com/product/123"
→ Call `webextrator_extract` with url="https://example.com/product/123", expected_type="product"

## Page Rendering
**Tool:** `webextrator_render`
**Use when:**
- User wants the full HTML source after JavaScript execution
- User needs the rendered DOM of a single-page application (SPA)
- User wants to inspect what a page looks like after dynamic content loads

**Example:** "Get the rendered HTML of https://example.com/app"
→ Call `webextrator_render` with url="https://example.com/app"

## Task Retrieval
**Tool:** `webextrator_get_task`
**Use when:**
- User submitted an async request (with callback_url) and wants the result
- User has a task ID and wants to check its status

**Tool:** `webextrator_get_tasks_batch`
**Use when:**
- User wants results for multiple tasks at once

## Performance Tips

### For faster extraction
Use `block_resources=["image", "font", "media"]` to skip loading heavy assets.

### For dynamic pages
Use `wait_for_selector="#content"` to wait for specific elements before extracting.

### For slow pages
Increase `timeout` (default: 30s) or add `delay` for extra wait time.

### For async workflows
Provide `callback_url` to process asynchronously and use `webextrator_get_task` to retrieve results.

## Important Notes:
1. The `url` field is required for both extract and render
2. Use `expected_type` to help the extractor understand the content structure
3. Use `enable_llm=True` for richer semantic normalization
4. Bearer token authentication is required
5. Use `webextrator_get_usage_guide` for full parameter documentation
"""


@mcp.prompt()
def webextrator_workflow_examples() -> str:
    """Common workflow examples for WebExtrator tasks."""
    return """# WebExtrator Workflow Examples

## Workflow 1: Extract Product Data
1. User: "Get the product details from https://shop.example.com/item/42"
2. Call `webextrator_extract(url="https://shop.example.com/item/42", expected_type="product", enable_llm=True)`
3. Return the structured product data (name, price, description, images, etc.)

## Workflow 2: Extract Article Content
1. User: "Summarize the article at https://news.example.com/story/456"
2. Call `webextrator_extract(url="https://news.example.com/story/456", expected_type="article")`
3. Use the extracted title, body, and metadata to provide a summary

## Workflow 3: Render a JavaScript App
1. User: "Get the HTML of https://app.example.com after it loads"
2. Call `webextrator_render(url="https://app.example.com", wait_until="networkidle", wait_for_selector="#app")`
3. Return the rendered HTML

## Workflow 4: Fast Render (block heavy resources)
1. User: "Quickly render https://example.com/page"
2. Call `webextrator_render(url="https://example.com/page", block_resources=["image", "font", "media", "stylesheet"])`
3. Return the lightweight HTML

## Workflow 5: Async Extraction
1. User: "Extract content from https://example.com/large-page (async)"
2. Call `webextrator_extract(url="...", callback_url="https://my-server.com/hook")`
3. Receive task_id from response
4. Later: `webextrator_get_task(task_id="<task-id>")` to get the result

## Workflow 6: Batch Task Retrieval
1. Multiple async tasks were submitted
2. Call `webextrator_get_tasks_batch(ids=["id1", "id2", "id3"])`
3. Return all results in one response

## Tips:
- Use `expected_type` to improve extraction accuracy
- Combine `wait_for_selector` with SPAs to ensure the content has rendered
- Block unnecessary resources with `block_resources` for faster results
"""
