---
name: gpt-image
description: Use GPT Image through Ace Data Cloud in goose for GPT Image generation and image editing. Use the installed service MCP tools; query the original task ID after generation. This plugin is maintained by Ace Data Cloud, not the service brand's official plugin.
license: MIT
---

# GPT Image by Ace Data Cloud

Use the MCP tools installed by this plugin. Match tools by their suffix because goose namespaces them with `gpt-image-by-acedatacloud`.

- Read `../../README.md` for installation and credential setup. The service API key belongs in `ACEDATACLOUD_API_TOKEN` in the environment that starts goose; never ask the user to paste it into chat.
- A free connection/reference check uses `openai_list_image_models`. Static reference success is not a paid generation or a billing result. For Nano Banana, tool-schema discovery is the free check.
- For an explicitly requested generation/edit, inspect the installed tool schema first. Use `openai_generate_image`, `openai_edit_image` as applicable. Do not invent model defaults or silently substitute another model/service.
- Confirm current account access, balance and price; preserve any user spending cap. Do not generate merely to test installation or check progress.
- After one submission, retain the returned task ID. Use `openai_get_task` to query that same ID, with the exact ID argument name from the schema. A pending result is not success; stop at terminal failure and preserve upstream meaning. Do not submit another generation to poll.
- Report complete only with an explicit successful terminal status and returned media URLs. Never fabricate audio/image/video URLs or claim a unique billing record without checking the account's actual usage.
- When using GPT Image, choose a public `gpt-image-*` model explicitly. This image plugin does not offer chat, embeddings, audio or Nano Banana as automatic fallbacks.
