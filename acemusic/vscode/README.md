# ACE Music by Ace Data Cloud

ACE Music songs and lyrics with Ace Data Cloud; retrieve original task results.


[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-acemusic?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-acemusic) [![PyPI](https://img.shields.io/pypi/v/mcp-acemusic.svg?label=PyPI)](https://pypi.org/project/mcp-acemusic/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://acemusic.mcp.acedata.cloud/mcp)

Create songs from an idea or custom lyrics and musical style, write lyrics, and retrieve your original ACE Music task. One task targets two MP3 candidates. Package publication and hosted deployment are release prerequisites.

This extension registers the **acemusic** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `acemusic` MCP server automatically.
2. **Get an application API key** using the detailed steps below. Check service access and your current balance before the first request.
3. **Select a model with tool calling in VS Code Chat.** You can use your existing model, or install [Ace Data Cloud Chat Models](https://marketplace.visualstudio.com/items?itemName=acedatacloud.chat-models). For the Ace model, first follow its [setup guide](https://github.com/AceDataCloud/VSCodeModelProvider#4-show-the-model-in-chat), open **Chat: Manage Language Models**, make the model visible, and select it in Chat. BYOK Chat does not require GitHub sign-in or a Copilot plan; organization policies still apply.
4. **Enable this server's tools.** Open **Chat → Agent → Configure Tools** and select only the tools you need under **ACE Music by Ace Data Cloud**. If the list is empty, choose **Update Tools**. The extension prompts for the API key on first use and saves it in VS Code's `SecretStorage`. Disable another copy of the same server from the Ace MCP bundle or manual `mcp.json` to avoid duplicate tools.
5. **Verify one result.** Check the Tool Reference below and current pricing before running a request. If you already have a task ID, enable its task-query tool and query that same ID first. An accepted generation is not a completed result: poll the original task until it reaches a successful terminal state, open the returned media, and match the task ID in [Usage](https://platform.acedata.cloud/console/usage?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_vscode_console_usage). Do not resubmit generation to poll. Model Chat and background utility calls can add separate charges to the service request.

You can rotate or remove the API key any time from the command palette:

- **ACE Music by Ace Data Cloud: Set Ace Data Cloud API Key**
- **ACE Music by Ace Data Cloud: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://acemusic.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Get your credential

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_vscode_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_vscode_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

### Example prompts

- "Create a warm folk song about returning home using ACE Music."
- "Use these lyrics and a jazz style to create an ACE Music song."
- "Check the original ACE Music task and return the final MP3 URLs."

---

## Tool Reference

**11 tools** available via this server.

| Tool | Description |
| --- | --- |
| `acemusic_generate_music` | One paid idea-to-song submission |
| `acemusic_generate_custom_music` | One paid submission with lyrics, style and title |
| `acemusic_upload_audio` | Separate priced single-track import from a public HTTPS MP3 URL |
| `acemusic_cover_audio` | One paid cover submission using an owned platform audio ID |
| `acemusic_mashup_audio` | One paid submission using exactly two compatible owned platform audio IDs |
| `acemusic_generate_lyrics` | Separately priced title/lyrics assistant |
| `acemusic_get_task` | Free authenticated lookup of the original task |
| `acemusic_get_tasks_batch` | Query up to 50 original tasks |
| `acemusic_list_tasks` | Paginated caller history |
| `acemusic_list_models` | Local model discovery |
| `acemusic_get_capabilities` | Supported workflows and recovery boundaries |

## Supported Models

`acemusic-v1.1`, `acemusic-v1`

## Pricing

Generation and lyrics are priced separately. Check current package pricing; task lookup is authenticated and free. See [Documentation](https://platform.acedata.cloud/documents/mcp-acemusic?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_vscode_quick_start).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.acemusic
Server label: ACE Music by Ace Data Cloud
Server URL  : https://acemusic.mcp.acedata.cloud/mcp
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
    "acemusic": {
      "type": "http",
      "url": "https://acemusic.mcp.acedata.cloud/mcp",
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
    "acemusic": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-acemusic"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-acemusic`](https://pypi.org/project/mcp-acemusic/) on demand.

---

## Links

- **Hosted endpoint:** https://acemusic.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-acemusic`](https://pypi.org/project/mcp-acemusic/)
- **Source repository:** https://github.com/AceDataCloud/AceMusicMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_vscode_platform
- **Documentation:** https://platform.acedata.cloud/documents/mcp-acemusic?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_vscode_quick_start

## License

MIT — see [LICENSE](LICENSE).
