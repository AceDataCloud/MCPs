# FishMCP

MCP (Model Context Protocol) server for the AceDataCloud Fish Audio API —
text-to-speech with voice conditioning powered by Fish Audio models.

## Project Structure

```
core/
  config.py     — Settings dataclass (API token, base URL, timeouts)
  server.py     — FastMCP server singleton + optional OAuth provider
  client.py     — FishClient: async httpx wrapper for /fish/* endpoints
  types.py      — Literal types (FishModel, etc.)
  exceptions.py — Error classes (FishAuthError, FishAPIError, FishTimeoutError)
  oauth.py      — Generic AceDataCloud OAuth 2.1 provider (PKCE)
tools/
  audio_tools.py — fish_generate_audio (submit a TTS task)
  task_tools.py  — fish_get_task, fish_get_tasks_batch
  info_tools.py  — fish_list_models, fish_get_model, fish_get_usage_guide
prompts/
  __init__.py    — fish_guide, fish_workflow_examples
tests/
  test_smoke.py  — Smoke tests (settings, server import, tool registration)
```

## TTS workflow

1. Pick a voice model (`fish_list_models` → `fish_get_model`).
2. Submit text (`fish_generate_audio(text=..., model="s2-pro", reference_id=...)`).
3. Poll status until terminal (`fish_get_task(task_id=...)`).
4. Read the final `audio_url` from the task payload and play / download it.

## Sync from Docs

When invoked by the sync workflow, the Docs repo is checked out at `_docs/`. Your job:

1. **Source of truth** — `_docs/openapi/fish.json` is the OpenAPI spec for the Fish Audio API.
2. **Compare models** — The Literal types in `core/types.py` must match the spec's voice model enum. Add/remove as needed.
3. **Compare parameters** — Each `@mcp.tool()` function's parameters should match the corresponding OpenAPI endpoint.
4. **Update defaults** — If a new model becomes the recommended default, update the default in `core/types.py`.
5. **Update README** — Keep the model table and feature list current.
6. **Add tests** — For new tools or parameters, add test cases in `tests/`.
7. **PR title** — Use format: `sync: <description> [auto-sync]`

## Development

```bash
pip install -e ".[dev,test]"
pytest --cov=core --cov=tools
ruff check .
```
