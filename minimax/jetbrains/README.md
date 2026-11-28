# MiniMax H3 MCP — JetBrains Plugin

Configure MiniMax H3 multimodal video generation for JetBrains AI Assistant through MCP.

## Capabilities

- text-to-video
- one to nine reference images
- one to three audio references with required images
- asynchronous task tracking

## Setup

1. Install the plugin.
2. Open **Settings → Tools → MiniMax MCP**.
3. Enter your AceDataCloud API token.
4. Copy the STDIO or hosted HTTP configuration into AI Assistant MCP settings.

Hosted endpoint: `https://minimax.mcp.acedata.cloud/mcp`

Local command: `uvx mcp-minimax`

Get a token at https://platform.acedata.cloud/console/applications.?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button marked **1** beside **API KEY**.

![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

Store the raw key in your client’s credential store or in the environment variable shown below. Add `Bearer ` only when setting an HTTP `Authorization` header yourself. Check access to the required operations, the current pricing, and the application balance. To use a separate key for this integration, open **Manage Keys** to set **Allowed APIs**, expiration, and usage limit.
<!-- END TOKEN ONBOARDING -->

## Documentation

[Documentation](https://platform.acedata.cloud/documents/minimax-videos?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen)

## License

MIT
