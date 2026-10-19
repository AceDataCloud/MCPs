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
2. **Get an application API key** using the detailed steps below. Check service access and your current balance before the first request.
3. **Select a model with tool calling in VS Code Chat.** You can use your existing model, or install [Ace Data Cloud Chat Models](https://marketplace.visualstudio.com/items?itemName=acedatacloud.chat-models). For the Ace model, first follow its [setup guide](https://github.com/AceDataCloud/VSCodeModelProvider#4-show-the-model-in-chat), open **Chat: Manage Language Models**, make the model visible, and select it in Chat. BYOK Chat does not require GitHub sign-in or a Copilot plan; organization policies still apply.
4. **Enable this server's tools.** Open **Chat → Agent → Configure Tools** and select only the tools you need under **Fish Audio MCP**. If the list is empty, choose **Update Tools**. The extension prompts for the API key on first use and saves it in VS Code's `SecretStorage`. Disable another copy of the same server from the Ace MCP bundle or manual `mcp.json` to avoid duplicate tools.
5. **Verify one result.** Check the Tool Reference below and current pricing before running a request. If you already have a task ID, enable its task-query tool and query that same ID first. An accepted generation is not a completed result: poll the original task until it reaches a successful terminal state, open the returned media, and match the task ID in [Usage](https://platform.acedata.cloud/console/usage?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_mcp_vscode_console_usage). Do not resubmit generation to poll. Model Chat and background utility calls can add separate charges to the service request.

You can rotate or remove the API key any time from the command palette:

- **Fish Audio MCP: Set Ace Data Cloud API Key**
- **Fish Audio MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://fish.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_mcp_vscode_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_mcp_vscode_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

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

Per-character billing. Free trial credit on sign-up. See [Documentation](https://platform.acedata.cloud/documents/fish?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_mcp_vscode_quick_start).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.fish
Server label: Fish Audio MCP
Server URL  : https://fish.mcp.acedata.cloud/mcp
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

---

## Links

- **Hosted endpoint:** https://fish.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-fish`](https://pypi.org/project/mcp-fish/)
- **Source repository:** https://github.com/AceDataCloud/FishMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_mcp_vscode_platform
- **Documentation:** https://platform.acedata.cloud/documents/fish?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=fish_mcp_vscode_quick_start

## License

MIT — see [LICENSE](LICENSE).
