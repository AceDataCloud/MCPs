# Fish Audio MCP

Fish Audio TTS — generate natural speech and browse the Fish voice library.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-fish?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-fish) [![PyPI](https://img.shields.io/pypi/v/mcp-fish.svg?label=PyPI)](https://pypi.org/project/mcp-fish/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://fish.mcp.acedata.cloud/mcp)

Generate natural-sounding speech from text using Fish Audio voices via Ace Data Cloud. Browse and search the voice library, fetch model metadata, submit asynchronous generation tasks, and poll single or batched results.

This extension registers the **fish** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `fish` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a audio task — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://fish.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

## VS Code Setup Guide

For the full VS Code walkthrough, see [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode). It covers token setup, project-level and user-level `mcp.json`, Copilot Agent Mode, and using one Ace Data Cloud token across hosted MCP servers.

### Example prompts

- "Generate audio for "Welcome to Ace Data Cloud" with a Fish voice and give me the URL."
- "List 10 Fish voice models and show their language, gender, and any tags."
- "Check the status of Fish task <id>."

---

## Tool Reference

**6 tools** available via this server.

| Tool | Description |
| --- | --- |
| `fish_generate_audio` | Generate speech from text via a Fish voice model |
| `fish_list_models` | List available Fish voice models |
| `fish_get_model` | Fetch metadata for a specific Fish voice model |
| `fish_get_task` | Get the status / result of a generation task |
| `fish_get_tasks_batch` | Batch-fetch the status / result of multiple tasks |
| `fish_get_usage_guide` | Get the API usage guide |

## Pricing

Per-character billing. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

```jsonc
{
  "servers": {
    "fish": {
      "type": "http",
      "url": "https://fish.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
      "description": "Ace Data Cloud API token",
      "password": true
    }
  ]
}
```

VS Code will prompt for the token on first use and persist it in the OS
secret store (Keychain / Credential Manager / libsecret).

### Alternative: local stdio (no network roundtrip)

If you prefer running the server locally — for offline dev, air-gapped
environments, or to pin to a specific PyPI version — install
[`uv`](https://docs.astral.sh/uv/) and replace your `mcp.json` entry with:

```jsonc
{
  "servers": {
    "fish": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-fish"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-fish`](https://pypi.org/project/mcp-fish/) on demand.

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://fish.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-fish`](https://pypi.org/project/mcp-fish/)
- **Source repository:** https://github.com/AceDataCloud/FishMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
