# Ace Data Cloud MCP

One VS Code extension for AI chat, images, video, music, search, web extraction,
and account management. Choose from **26 hosted MCP services** and use them in
Copilot Chat without installing Python or running local servers.

## Get started

1. Install **Ace Data Cloud MCP** from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-toolbox).
2. Open the Command Palette and run **Ace Data Cloud: Choose MCP Services**.
3. Run **Ace Data Cloud: Set Shared API Key**, using an API key with access to your selected services from the
   [Ace Data Cloud console](https://platform.acedata.cloud/console/credentials).
4. Open Copilot Chat in Agent mode, enable the tools you need, and ask a question.

VS Code **1.101 or newer** and a chat client with MCP tool support are required.
VS Code asks you to trust an MCP server before starting it. API requests use your
Ace Data Cloud account and are billed according to the selected service.

The default selection includes common creation and search services. Add or
remove services at any time with the picker. The extension exposes server definitions; VS Code controls
when each selected server starts.

## Services

<!-- BEGIN GENERATED SERVICES -->
| Service | Credential |
| --- | --- |
| Ace Data Cloud Account | Platform token |
| AI Chat | API key |
| Face Transform | API key |
| Fish Audio | API key |
| Flux | API key |
| GLM | API key |
| Grok Imagine | API key |
| Hailuo | API key |
| HappyHorse | API key |
| Kling | API key |
| Luma | API key |
| Maestro | API key |
| Midjourney | API key |
| MiniMax | API key |
| NanoBanana | API key |
| OpenAI | API key |
| Producer | API key |
| Qwen Image | API key |
| Seedance | API key |
| Seedream | API key |
| Google Search | API key |
| Short URL | API key |
| Suno | API key |
| Veo | API key |
| Wan | API key |
| Web Extractor | API key |
<!-- END GENERATED SERVICES -->

Account management is optional and requires its own platform token from
[Platform tokens](https://platform.acedata.cloud/console/platform-tokens).
Run **Ace Data Cloud: Set Account Platform Token** to save it. API keys are never
sent to the account-management server, and platform tokens are never sent to
API-service servers.

## Credentials and configuration

Credentials are stored in VS Code **SecretStorage**, not in `settings.json`.
Use **Set Service API Key** when one service needs a different key. Saved service
keys take precedence over the shared key. Environment variables
`ACEDATACLOUD_API_TOKEN` and `ACEDATACLOUD_PLATFORM_TOKEN` are used only when the
corresponding saved credential is absent.

**Clear Saved Credentials** removes keys saved by this extension. It does not
change environment variables. To stop exposing a service, deselect it with
**Choose MCP Services**. To stop all services, select none.

You can also set `acedatacloud.bundle.services` in VS Code settings:

```json
{
  "acedatacloud.bundle.services": ["suno", "kling", "qwen-image", "serp"]
}
```

The new extension ID is `acedatacloud.mcp-toolbox`; the deleted March bundle
ID cannot be reused. Install this extension explicitly, save your key using the command above
and remove the old `acedatacloud.apiToken` plaintext setting. It is no longer read.
The retired Sora service is no longer included. Individual Ace Data Cloud service
extensions remain available; disable duplicate entries if you also use this bundle.

## Examples

- “Use Suno to create a short instrumental track for a product demo.”
- “Use Qwen Image to make a watercolor illustration of a mountain village.”
- “Use Google Search to find the latest developments in battery recycling.”

For generation tasks, continue tracking the task until it completes before
using the output.

## Development

```bash
npm ci
npm test
npm run check
npm run package
```

The source of truth is [`MCPs/vscode-bundle`](https://github.com/AceDataCloud/MCPs/tree/main/vscode-bundle).
This repository receives reviewed source changes through the MCPs sync pipeline;
do not edit its generated service list or source independently.

In MCPs, opt verified services into `scripts/mcp_catalog.json` using
`vscode_bundle`. Endpoints and credential kinds come from each service's
`server.json`. Run `python3 scripts/build_vscode_bundle.py` after catalog changes;
CI checks the generated list, package settings and README together. A retired
service is automatically omitted. Publish runs tests, packages a VSIX and reads
back the public Marketplace version.

[API documentation](https://platform.acedata.cloud/documents) ·
[MCP server source](https://github.com/AceDataCloud/MCPs) ·
[Issues](https://github.com/AceDataCloud/VSCodeMCP/issues)

MIT licensed.
