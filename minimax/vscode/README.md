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
3. Open the MCP server picker and enable **MiniMax MCP**.

The extension connects to `https://minimax.mcp.acedata.cloud/mcp`. Get a token at https://platform.acedata.cloud/console/applications.

## Tools

- `minimax_generate_video_from_text`
- `minimax_generate_video_from_images`
- `minimax_generate_video_from_audio`
- `minimax_get_task`
- `minimax_get_tasks_batch`
- `minimax_list_models`
- `minimax_list_actions`

Public pricing is $0.057143/s for 768P and $0.091429/s for 2K. Failed tasks are not charged.
