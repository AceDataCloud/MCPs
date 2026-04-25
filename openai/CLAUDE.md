# OpenAIMCP

MCP (Model Context Protocol) server for OpenAI API via AceDataCloud.

## Project Structure

```
core/
  config.py     — Settings dataclass (API token, base URL)
  server.py     — FastMCP server singleton
  client.py     — httpx async HTTP client
  types.py      — Literal types (ChatModel, ImageModel, EmbeddingModel, etc.)
  exceptions.py — Error classes (AuthError, APIError, TimeoutError)
  oauth.py      — OAuth 2.1 provider
tools/
  chat_tools.py        — openai_chat_completion
  responses_tools.py   — openai_create_response
  image_tools.py       — openai_generate_image, openai_edit_image
  embedding_tools.py   — openai_create_embedding
  info_tools.py        — list models, usage guide
prompts/           — LLM guidance prompts
tests/             — pytest-asyncio tests
```

## Sync from Docs

When invoked by the sync workflow, the Docs repo is checked out at `_docs/`. Your job:

1. **Source of truth** — `_docs/openapi/openai.json` is the OpenAPI spec for the OpenAI API.
2. **Compare models** — The Literal types in `core/types.py` must match the spec's model enum. Add/remove as needed.
3. **Compare parameters** — Each `@mcp.tool()` function's parameters should match the corresponding OpenAPI endpoint.
4. **Update defaults** — If a new model becomes the recommended default, update the default in `core/types.py`.
5. **Update README** — Keep the model table and feature list current.
