# FaceTransformMCP

MCP (Model Context Protocol) server for the AceDataCloud Face Transform API —
seven face tools covering keypoint detection, beautification, age/gender
transform, face swap, cartoonization, and liveness detection.

## Project Structure

```
core/
  config.py     — Settings dataclass (API token, base URL, timeouts)
  server.py     — FastMCP server singleton + optional OAuth provider
  client.py     — FaceClient: async httpx wrapper for /face/* endpoints
  types.py      — Literal types (FaceAnalyzeMode, FaceModelVersion, ...)
  exceptions.py — Error classes (FaceAuthError, FaceAPIError, FaceTimeoutError)
  oauth.py      — Generic AceDataCloud OAuth 2.1 provider (PKCE)
  utils.py      — Shared response helpers (kept from template; unused by face)
tools/
  face_tools.py — All seven face tools + face_get_usage_guide
prompts/
  __init__.py   — face_guide, face_workflow_examples
tests/
  test_smoke.py — Smoke tests (settings, server import, tool registration)
```

## Adding / updating a face endpoint

1. **Source of truth** — the upstream OpenAPI spec lives at
   `https://docs.acedata.cloud/openapi/face.json` (or the matching file in the
   `Docs/` submodule).
2. **Update client** — add a method to `FaceClient` in `core/client.py`.
3. **Add tool** — register a new `@mcp.tool()` function in
   `tools/face_tools.py`.
4. **Update prompts** — extend `face_guide` and `face_workflow_examples`.
5. **Update server card** — append the tool description to the `server_card`
   payload in `main.py`.
6. **Update README + CHANGELOG**.
7. **Add tests** — at minimum a smoke test that the tool is registered.
8. Run `ruff check .` and `pytest --cov=core --cov=tools` before opening a PR.

## Development

```bash
pip install -e ".[dev,test]"
pytest --cov=core --cov=tools
ruff check .
```

## Local run

```bash
cp .env.example .env
# fill in ACEDATACLOUD_API_TOKEN
python main.py                          # stdio
python main.py --transport http         # HTTP on :8000
```
