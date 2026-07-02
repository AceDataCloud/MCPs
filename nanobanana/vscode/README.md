# NanoBanana MCP

Gemini-powered NanoBanana — generate and edit images via natural language.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-nanobanana) [![PyPI](https://img.shields.io/pypi/v/mcp-nanobanana-pro.svg?label=PyPI)](https://pypi.org/project/mcp-nanobanana-pro/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://nanobanana.mcp.acedata.cloud/mcp)

Image generation and edit-by-instruction using NanoBanana, NanoBanana 2, and NanoBanana Pro (built on Gemini).

This extension registers the **nanobanana** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `nanobanana` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a image task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **NanoBanana MCP: Set Ace Data Cloud API Key**
- **NanoBanana MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://nanobanana.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

## VS Code Setup Guide

For screenshots, token setup, project-level and user-level `mcp.json`, and Copilot Agent Mode examples, see:

- [NanoBanana MCP VS Code guide](https://platform.acedata.cloud/documents/promotion_article_mcp_nanobanana_vscode)
- [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode)

### Example prompts

- "Generate a watercolor postcard of Kyoto in cherry-blossom season. Use nanobanana pro."
- "Edit https://example.com/desk.jpg — clear the desk and add a single houseplant."

---

## Tool Reference

**4 tools** available via this server.

| Tool | Description |
| --- | --- |
| `nanobanana_generate_image` | Generate an AI image from a text prompt using Google's Nano Banana model. |
| `nanobanana_edit_image` | Edit or combine images using AI based on a text prompt. |
| `nanobanana_get_task` | Query the status and result of an image generation or edit task. |
| `nanobanana_get_tasks_batch` | Query multiple image generation/edit tasks at once. |

## Supported Models

`nano-banana`, `nano-banana-2`, `nano-banana-pro`

## Pricing

From $0.015 per image. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.nanobanana
Server label: NanoBanana MCP
Server URL  : https://nanobanana.mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or $ACEDATACLOUD_API_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{
  "servers": {
    "nanobanana": {
      "type": "http",
      "url": "https://nanobanana.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
      "description": "Ace Data Cloud API key",
      "password": true
    }
  ]
}
```

### Alternative: local stdio (no network roundtrip)

For offline dev, air-gapped environments, or pinning to a specific PyPI
version, install [`uv`](https://docs.astral.sh/uv/) and use:

```jsonc
{
  "servers": {
    "nanobanana": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-nanobanana-pro"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-nanobanana-pro`](https://pypi.org/project/mcp-nanobanana-pro/) on demand.

---

## Links

- **Hosted endpoint:** https://nanobanana.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-nanobanana-pro`](https://pypi.org/project/mcp-nanobanana-pro/)
- **Source repository:** https://github.com/AceDataCloud/NanoBananaMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
