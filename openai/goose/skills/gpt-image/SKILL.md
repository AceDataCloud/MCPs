---
name: gpt-image
description: Use GPT Image through Ace Data Cloud in goose for GPT Image generation and image editing. Use the installed service MCP tools; query the original task ID after generation. This plugin is maintained by Ace Data Cloud, not the service brand's official plugin.
license: MIT
---

# GPT Image by Ace Data Cloud

Use the MCP tools installed by this plugin. Match tools by their suffix because goose namespaces them with `gpt-image-by-acedatacloud`.

- Read `../../README.md` for installation and credential setup. The service API key belongs in `ACEDATACLOUD_API_TOKEN` in the environment that starts goose; never ask the user to paste it into chat.
- A free connection/reference check uses `gpt_image_list_models`. Static reference success is not a paid generation or a billing result.
- For an explicitly requested generation/edit, inspect the installed tool schema first. Use `gpt_image_generate`, `gpt_image_edit` as applicable. Do not invent model defaults or silently substitute another model/service.
- Confirm current account access, balance and price; preserve any user spending cap. The Platform catalog hides OpenAI image API/model entries and companion guides in mainland China (`cn`); a local `gpt_image_list_models` result does not establish regional availability. Check the current Platform catalog before recommending image submission, and do not suggest bypassing regional visibility. This catalog rule does not introduce a client-side API block. Do not generate merely to test installation or check progress.
- For generation or editing, use `quality: "auto"`, `"low"`, `"medium"` or `"high"` with GPT Image models. Choose `"xhigh"` or `"max"` only for `gpt-image-2.5-flare` or `gpt-image-2.5-sunburst`, including their `:official` variants; official variants bill actual token usage. Do not silently switch models to obtain a quality setting.
- After one submission, retain the returned task ID. Use `gpt_image_get_task` to query that same ID, with the exact ID argument name from the schema. A pending result is not success; stop at terminal failure and preserve upstream meaning. Do not submit another generation to poll.
- Report complete only with an explicit successful terminal status and returned media URLs. Never fabricate audio/image/video URLs or claim a unique billing record without checking the account's actual usage.
- When using GPT Image, choose a public `gpt-image-*` model explicitly. This image plugin does not offer chat, embeddings, audio or Nano Banana as automatic fallbacks.

The installed server is the canonical published `--profile gpt-image` surface, including `gpt_image_list_tasks` for bounded history lookup. Model must be explicitly supplied for generate/edit; inspect its enum rather than inventing an alias.
