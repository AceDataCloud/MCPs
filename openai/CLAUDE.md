# OpenAIMCP

MCP (Model Context Protocol) server for OpenAI API (chat completions, embeddings, image generation, responses, and image editing) via AceDataCloud API.

## Project Structure

```
core/
  config.py     — Settings dataclass (API token, base URL)
  server.py     — FastMCP server singleton
  client.py     — httpx async HTTP client
  exceptions.py — Error classes (AuthError, APIError, TimeoutError)
tools/
  openai_tools.py  — chat completion, embeddings, image generate, responses, image edit
  info_tools.py    — list models
prompts/           — LLM guidance prompts
tests/             — pytest-asyncio + respx tests
```

## Sync from Docs

When invoked by the sync workflow, the Docs repo is checked out at `_docs/`. Your job:

1. **Source of truth** — `_docs/openapi/openai.json` is the OpenAPI spec for the OpenAI MCP API.
2. **Compare models** — The Literal types in `tools/openai_tools.py` must match the spec's model enum. Add/remove as needed.
3. **Compare parameters** — Each `@mcp.tool()` function's parameters should match the corresponding OpenAPI endpoint.
4. **Update defaults** — If a new model becomes the recommended default, update the default in the tool function.
5. **Update README** — Keep the model table and feature list current.
6. **Add tests** — For new tools or parameters, add test cases in `tests/`.
7. **PR title** — Use format: `sync: <description> [auto-sync]`

## Development

```bash
pip install -e ".[dev]"
pytest --cov=core --cov=tools
ruff check .
```
