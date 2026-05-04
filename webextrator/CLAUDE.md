# WebExtraterMCP

MCP (Model Context Protocol) server for web extraction and rendering via AceDataCloud WebExtrator API.

## Project Structure

```
core/
  config.py     — Settings dataclass (API token, base URL)
  server.py     — FastMCP server singleton
  client.py     — httpx async HTTP client
  types.py      — Literal types (WaitUntil, BlockResource, ExpectedType, TaskAction)
  exceptions.py — Error classes (AuthError, APIError, TimeoutError)
tools/
  extract_tools.py  — webextrator_extract, webextrator_render
  task_tools.py     — webextrator_get_task, webextrator_get_tasks_batch
  info_tools.py     — webextrator_get_usage_guide
prompts/              — LLM guidance prompts
tests/                — pytest-asyncio tests
```

## Sync from Docs

When invoked by the sync workflow, the Docs repo is checked out at `_docs/`. Your job:

1. **Source of truth** — `_docs/openapi/webextrator.json` is the OpenAPI spec for the WebExtrator API.
2. **Compare parameters** — Each `@mcp.tool()` function's parameters should match the corresponding OpenAPI endpoint.
3. **Update types** — Keep `core/types.py` Literals in sync with enum values in the spec.
4. **Update defaults** — If default values change, update them in the tool signatures.
5. **PR title** — Use format: `sync: <description> [auto-sync]`

## Development

```bash
pip install -e ".[dev]"
pytest --cov=core --cov=tools
ruff check .
```
