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

Get a token at https://platform.acedata.cloud/console/applications.?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=minimax_mcp_jetbrains_api_key

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=minimax_mcp_jetbrains_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=minimax_mcp_jetbrains_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

## Documentation

[Documentation](https://platform.acedata.cloud/documents/minimax-videos?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=minimax_mcp_jetbrains_quick_start)

## License

MIT
