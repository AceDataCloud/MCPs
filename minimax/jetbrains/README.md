# MiniMax H3 MCP — JetBrains Plugin

Configure MiniMax H3 multimodal video generation for JetBrains AI Assistant through MCP.

## Capabilities

- text-to-video
- one to nine reference images
- one to three audio references with optional images
- asynchronous task tracking

## Setup

1. Install the plugin.
2. Open **Settings → Tools → MiniMax MCP**.
3. Enter your AceDataCloud API token.
4. Copy the STDIO or hosted HTTP configuration into AI Assistant MCP settings.

Hosted endpoint: `https://minimax.mcp.acedata.cloud/mcp`

Local command: `uvx mcp-minimax`

Get a token at https://platform.acedata.cloud/console/applications.

## License

MIT
