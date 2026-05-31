# AiChat MCP

Unified OpenAI-compatible LLM gateway — chat with GPT, Claude, Gemini, Grok, DeepSeek, Kimi and more via a single endpoint.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-aichat?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-aichat) [![PyPI](https://img.shields.io/pypi/v/mcp-aichat.svg?label=PyPI)](https://pypi.org/project/mcp-aichat/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://aichat.mcp.acedata.cloud/mcp)

Connect VS Code's AI agents to the **Unified LLM gateway via Ace Data Cloud** service. Once configured, AI Assistant can chat with 50+ LLM models — GPT, Claude, Gemini, Grok, DeepSeek and more — through a single endpoint.

This extension registers the **aichat** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `aichat` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and call a tool — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://aichat.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

---

## Tool Reference

**4 tools** available via this server.

| Tool | Description |
| --- | --- |
| `aichat_create_conversation` | Create an AI conversation using the AiChat API. |
| `aichat_create_conversation_v2` | Create / manage conversations via the AiChat v2 endpoint. |
| `aichat_list_models` | List all available AI models for the AiChat API. |
| `aichat_get_usage_guide` | Get a comprehensive guide for using the AiChat tools. |

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

```jsonc
{
  "servers": {
    "aichat": {
      "type": "http",
      "url": "https://aichat.mcp.acedata.cloud/mcp",
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
    "aichat": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-aichat"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-aichat`](https://pypi.org/project/mcp-aichat/) on demand.

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://aichat.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-aichat`](https://pypi.org/project/mcp-aichat/)
- **Source repository:** https://github.com/AceDataCloud/AiChatMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
