# MCP Face Transform Server

<!-- mcp-name: io.github.AceDataCloud/mcp-face-transform -->

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that
exposes the AceDataCloud Face Transform API — face keypoint detection,
beautification, age/gender transform, face swap, cartoonization, and liveness
detection.

> **Status:** All Face APIs are currently in **Alpha**. Interfaces may evolve.

## Features

- **Keypoint detection** — 90+ landmarks per face, multi-face supported
- **Beautification** — smoothing, whitening, face slimming, eye enlarging
- **Age transform** — age or de-age a portrait
- **Gender transform** — swap perceived facial gender characteristics
- **Face swap** — move a source face onto a target image (with optional async webhook)
- **Cartoonize** — render a portrait in animated / cartoon style
- **Liveness detection** — distinguish live captures from printed / screen photos

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://face.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-face-transform` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://face.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user face https://face.mcp.acedata.cloud/mcp`, then `claude mcp login face`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://face.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://face.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add face --url https://face.mcp.acedata.cloud/mcp`, then `codex mcp login face`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "face": {"url": "https://face.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "face": {"type": "http", "url": "https://face.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user face https://face.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "face": {
      "type": "http",
      "url": "https://face.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "face": {
      "url": "https://face.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-face-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "face": {
      "type": "http",
      "url": "https://face.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-face-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-face-transform
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-face-transform
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "face": {
      "command": "uvx",
      "args": ["mcp-face-transform"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-face-transform --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://face.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. `face_get_usage_guide` is a reference tool; it does not verify downstream API access or balance.
3. Use a documented service operation for an end-to-end check after reviewing [current service documentation](https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_readme_quick_start).

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Tool Reference

| Tool | Description |
|------|-------------|
| `face_detect_keypoints` | Detect 90+ keypoints per face (multi-face supported). |
| `face_beautify` | Smoothing, whitening, face slimming, and eye enlarging. |
| `face_change_age` | Age or de-age a portrait. |
| `face_change_gender` | Swap perceived facial gender characteristics. |
| `face_swap` | Move a source face onto a target image (with optional async webhook). |
| `face_cartoonize` | Render a portrait in cartoon / animated style. |
| `face_detect_liveness` | Distinguish a live capture from a printed / screen photo. |
| `face_get_usage_guide` | Concise client-side tool usage reference. |

## Example

```text
"Detect all faces in https://example.com/group.jpg and return their keypoints."
→ face_detect_keypoints(image_url="https://example.com/group.jpg")

"Lighten and smooth my portrait."
→ face_beautify(image_url="https://example.com/me.jpg", smoothing=15, whitening=25)

"Replace the face in the scene with the headshot."
→ face_swap(
    source_image_url="https://example.com/headshot.jpg",
    target_image_url="https://example.com/scene.jpg",
  )
```

## Configuration in Claude Desktop / Claude Code

```json
{
  "mcpServers": {
    "face-transform": {
      "command": "uvx",
      "args": ["mcp-face-transform"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Or use the hosted endpoint with bearer auth:

```json
{
  "mcpServers": {
    "face-transform": {
      "url": "https://face.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your_api_token_here"
      }
    }
  }
}
```

## Development

```bash
pip install -e ".[dev,test]"
pytest --cov=core --cov=tools
ruff check .
```

## Service details

<!-- canonical-documentation -->
[Service details](https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_readme_quick_start)

## License

MIT — see [LICENSE](LICENSE).
