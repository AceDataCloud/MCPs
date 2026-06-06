# OpenAI MCP

OpenAI models via Ace Data Cloud — chat completions, embeddings, image generation and editing, Responses API, async tasks.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-openai?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-openai) [![PyPI](https://img.shields.io/pypi/v/mcp-openai.svg?label=PyPI)](https://pypi.org/project/mcp-openai/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://openai.mcp.acedata.cloud/mcp)

Connect VS Code's AI agents to the **OpenAI models via Ace Data Cloud** service. Once configured, AI Assistant can run OpenAI chat completions, generate embeddings, create or edit images, and orchestrate the Responses API — all routed through Ace Data Cloud.

This extension registers the **openai** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `openai` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and call a tool — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://openai.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

## VS Code Setup Guide

For the full VS Code walkthrough, see [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode). It covers token setup, project-level and user-level `mcp.json`, Copilot Agent Mode, and using one Ace Data Cloud token across hosted MCP servers.

---

## Tool Reference

**11 tools** available via this server.

| Tool | Description |
| --- | --- |
| `openai_chat_completion` | Create a chat completion using OpenAI models via AceDataCloud. |
| `openai_create_embedding` | Create text embeddings using OpenAI embedding models via AceDataCloud. |
| `openai_generate_image` | Generate images using OpenAI image models via AceDataCloud. |
| `openai_edit_image` | Edit or modify existing images using OpenAI image models via AceDataCloud. |
| `openai_create_response` | Create a response using the OpenAI Responses API via AceDataCloud. |
| `openai_get_task` | Retrieve a single async image task by its task ID or custom trace ID. |
| `openai_list_tasks` | List async image tasks using batch query filters. |
| `openai_list_chat_models` | List all available chat completion models. |
| `openai_list_image_models` | List all available image generation and editing models. |
| `openai_list_embedding_models` | List all available text embedding models. |
| `openai_get_usage_guide` | Get a comprehensive guide for using the OpenAI tools. |

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

```jsonc
{
  "servers": {
    "openai": {
      "type": "http",
      "url": "https://openai.mcp.acedata.cloud/mcp",
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
    "openai": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-openai"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-openai`](https://pypi.org/project/mcp-openai/) on demand.

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://openai.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-openai`](https://pypi.org/project/mcp-openai/)
- **Source repository:** https://github.com/AceDataCloud/OpenAIMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
