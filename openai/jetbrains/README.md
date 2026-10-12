# OpenAI MCP — JetBrains Plugin

OpenAI models via Ace Data Cloud via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the OpenAI MCP server with JetBrains AI Assistant.
Once configured, AI Assistant can run OpenAI chat completions, generate embeddings, create or edit images, and orchestrate the Responses API — all routed through Ace Data Cloud.

**11 AI Tools** — OpenAI models via Ace Data Cloud.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.openai)
2. Open **Settings → Tools → OpenAI MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_jetbrains_platform) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_jetbrains_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_jetbrains_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

### HTTP Mode (Remote, recommended)

Connects to the hosted MCP server at `openai.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "openai": {
      "url": "https://openai.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "openai": {
      "command": "uvx",
      "args": ["mcp-openai-pro"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

## Tool Reference

| Tool | Description |
| --- | --- |
| `openai_chat_completion` | Create a chat completion using OpenAI models via AceDataCloud. |
| `openai_create_embedding` | Create text embeddings using OpenAI embedding models via AceDataCloud. |
| `openai_generate_image` | Generate images using OpenAI image models via AceDataCloud. |
| `openai_edit_image` | Edit or modify existing images using OpenAI image models via AceDataCloud. |
| `openai_create_response` | Create a response using the OpenAI Responses API via AceDataCloud. |
| `openai_get_task` | Retrieve a single async image task by its task ID or custom trace ID. |
| `openai_list_tasks` | List async image tasks using batch query filters. |
| `openai_list_chat_models` | List all available chat completion models. |
| `openai_list_image_models` | List all available image generation and editing models. |
| `openai_list_embedding_models` | List all available text embedding models. |
| `openai_get_usage_guide` | Get a comprehensive guide for using the OpenAI tools. |

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_jetbrains_platform)
- [Documentation](https://platform.acedata.cloud/documents/openai?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_jetbrains_quick_start)
- [PyPI Package](https://pypi.org/project/mcp-openai-pro/)
- [Source Code](https://github.com/AceDataCloud/OpenAIMCP)

## License

MIT
