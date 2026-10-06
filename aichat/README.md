# MCP AiChat Server

<!-- mcp-name: io.github.AceDataCloud/mcp-aichat -->

A Model Context Protocol (MCP) server for AI dialogue via the AceDataCloud platform.
Supports a wide range of models including GPT-4/5, o-series, DeepSeek, Grok, and GLM.

## Features

- **Multi-model support**: GPT-4.1, GPT-4o, GPT-5, o1, o3, o4-mini, DeepSeek, Grok, GLM, and more
- **Multi-turn conversations**: Continue conversations using conversation IDs
- **Stateful mode**: Optional server-side conversation state management
- **Reference sources**: Include external references for context-aware responses

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://aichat.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-aichat` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/documents/aichat?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://aichat.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user aichat https://aichat.mcp.acedata.cloud/mcp`, then `claude mcp login aichat`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://aichat.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://aichat.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add aichat --url https://aichat.mcp.acedata.cloud/mcp`, then `codex mcp login aichat`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "aichat": {"url": "https://aichat.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "aichat": {"type": "http", "url": "https://aichat.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/documents/aichat?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user aichat https://aichat.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "aichat": {
      "type": "http",
      "url": "https://aichat.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "aichat": {
      "url": "https://aichat.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-aichat-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "aichat": {
      "type": "http",
      "url": "https://aichat.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-aichat-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-aichat
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-aichat
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "aichat": {
      "command": "uvx",
      "args": ["mcp-aichat"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-aichat --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://aichat.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. `aichat_list_models` is a reference tool; it does not verify downstream API access or balance.
3. If you need a full API check, call `aichat_create_conversation` with your own valid input after reviewing [current service documentation](https://platform.acedata.cloud/documents/aichat?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_readme_quick_start) and displayed pricing.

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Available Tools

| Tool | Description |
|------|-------------|
| `aichat_create_conversation` | Create an AI conversation with any supported model |
| `aichat_create_conversation_v2` | Create/manage conversations via `/aichat2/conversations` |
| `aichat_list_models` | List all available AI models |
| `aichat_get_usage_guide` | Get API usage guide |

## Supported Models

### OpenAI
- GPT-5.6 Sol Fast: `gpt-5.6-sol-fast`, supported by both `aichat_create_conversation` and `aichat_create_conversation_v2`. Existing defaults are unchanged.
- GPT-5 series: gpt-5.5, gpt-5.4, gpt-5.2, gpt-5.1, gpt-5, gpt-5-mini, gpt-5-nano
- GPT-4.1 series: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano
- GPT-4o series: gpt-4o, gpt-4o-mini, gpt-4o-all, gpt-4o-image
- GPT-4 series: gpt-4, gpt-4-turbo, gpt-4-vision-preview
- o-series: o1, o1-mini, o1-pro, o3, o3-mini, o3-pro, o4-mini

### DeepSeek
- deepseek-r1, deepseek-r1-0528, deepseek-v3, deepseek-v3-250324, deepseek-v4-flash, deepseek-v4-pro

### xAI
- grok-3

### Zhipu AI
- glm-5.1, glm-4.7, glm-4.6, glm-3-turbo

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/aichat?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_readme_quick_start)

## License

MIT
