# MiniMax H3 MCP for VS Code

Connect VS Code MCP clients to MiniMax H3 video generation through AceDataCloud.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-minimax)

## Capabilities

- text-to-video
- one to nine reference images
- one to three audio references with required images
- 4–15 second output in 768P or 2K, with 16:9 or 9:16
- asynchronous task retrieval

## Setup

1. Install the extension.
2. Run **MiniMax MCP: Set Ace Data Cloud API Key**.
3. **Select a model with tool calling in VS Code Chat.** You can use your existing model, or install [Ace Data Cloud Chat Models](https://marketplace.visualstudio.com/items?itemName=acedatacloud.chat-models). For the Ace model, first follow its [setup guide](https://github.com/AceDataCloud/VSCodeModelProvider#4-show-the-model-in-chat), open **Chat: Manage Language Models**, make the model visible, and select it in Chat. BYOK Chat does not require GitHub sign-in or a Copilot plan; organization policies still apply.
4. **Enable this server's tools.** Open **Chat → Agent → Configure Tools** and select only the tools you need under **MiniMax MCP**. If the list is empty, choose **Update Tools**. The extension prompts for the API key on first use and saves it in VS Code's `SecretStorage`. Disable another copy of the same server from the Ace MCP bundle or manual `mcp.json` to avoid duplicate tools.
5. **Verify one result.** Check the Tool Reference below and current pricing before running a request. If you already have a task ID, enable its task-query tool and query that same ID first. An accepted generation is not a completed result: poll the original task until it reaches a successful terminal state, open the returned media, and match the task ID in [Usage](https://platform.acedata.cloud/console/usage?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen). Do not resubmit generation to poll. Model Chat and background utility calls can add separate charges to the service request.

The extension connects to `https://minimax.mcp.acedata.cloud/mcp`. Get an application API key using the instructions below.

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button marked **1** beside **API KEY**.

![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

Store the raw key in your client’s credential store or in the environment variable shown below. Add `Bearer ` only when setting an HTTP `Authorization` header yourself. Check access to the required operations, the current pricing, and the application balance. To use a separate key for this integration, open **Manage Keys** to set **Allowed APIs**, expiration, and usage limit.
<!-- END TOKEN ONBOARDING -->

## Tools

- `minimax_generate_video_from_text`
- `minimax_generate_video_from_images`
- `minimax_generate_video_from_audio`
- `minimax_get_task`
- `minimax_get_tasks_batch`
- `minimax_list_models`
- `minimax_list_actions`

Public pricing is $0.057143/s for 768P and $0.091429/s for 2K. Failed tasks are not charged.

## Documentation

[Documentation](https://platform.acedata.cloud/documents/minimax-videos?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen)
