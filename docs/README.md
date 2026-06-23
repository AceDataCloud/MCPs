# AceDataCloud Docs MCP

A **public, zero-install** [Model Context Protocol](https://modelcontextprotocol.io) server that
exposes the entire [AceData Cloud](https://platform.acedata.cloud) catalog — documentation, API
specs (OpenAPI), models, pricing, and runnable code examples — as tools any agent or IDE can call.

No API token required. It only reads AceData Cloud's public, read-only endpoints.

## Use it (remote — recommended)

Add one URL to your MCP client:

```json
{
  "mcpServers": {
    "acedatacloud-docs": {
      "url": "https://docs.mcp.acedata.cloud/mcp"
    }
  }
}
```

Claude Code:

```bash
claude mcp add --transport http acedatacloud-docs https://docs.mcp.acedata.cloud/mcp
```

## Use it (local — stdio via PyPI)

```bash
uvx mcp-docs            # or: pip install mcp-docs && mcp-docs
```

## Tools

| Tool | What it does |
|---|---|
| `acedatacloud_search_docs` | Search the docs by keyword/question → snippets + URLs |
| `acedatacloud_list_docs` / `acedatacloud_fetch_doc` | Browse and read full documentation pages |
| `acedatacloud_list_services` | List services (logical API groupings) |
| `acedatacloud_list_apis` | List public API endpoints (optionally per service) |
| `acedatacloud_get_spec` | Get the OpenAPI spec for an API (filtered by path/service) |
| `acedatacloud_list_models` / `acedatacloud_get_model` | Model catalog + USD pricing |
| `acedatacloud_get_pricing` | Display pricing for a service |
| `acedatacloud_get_code_example` | A runnable curl / python / javascript snippet |
| `acedatacloud_list_mcp_servers` | AceData Cloud's other MCP servers + how to connect |

## Development

```bash
pip install -e ".[dev,test]"
python main.py                  # stdio
python main.py --transport http # remote (port 8000)
pytest
```

`acedatacloud_list_mcp_servers` is backed by `core/data/mcp_servers.json`, generated from the sibling
`MCPs/*/server.json` files via `python scripts/gen_mcp_servers.py`.

## License

MIT
