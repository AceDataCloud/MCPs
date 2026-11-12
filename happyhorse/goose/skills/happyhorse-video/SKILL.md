---
name: happyhorse-video
description: Use HappyHorse through Ace Data Cloud in goose for HappyHorse text/image/reference video and editing. Use the installed service MCP tools; query the original task ID after generation. This plugin is maintained by Ace Data Cloud, not the service brand's official plugin.
license: MIT
---

# HappyHorse by Ace Data Cloud

Use the MCP tools installed by this plugin. Match tools by their suffix because goose namespaces them with `happyhorse-by-acedatacloud`.

- Read `../../README.md` for installation and credential setup. The service API key belongs in `ACEDATACLOUD_API_TOKEN` in the environment that starts goose; never ask the user to paste it into chat.
- A free connection/reference check uses `happyhorse_list_models`. Static reference success is not a paid generation or a billing result.
- For an explicitly requested generation/edit, inspect the installed tool schema first. Use `happyhorse_generate_video` as applicable. Do not invent model defaults or silently substitute another model/service.
- For image animation, the output aspect ratio follows the source image. For `happyhorse_edit_video`, duration and aspect ratio follow the source video; do not try to change either with `duration` or `ratio`. Editing is billed on combined input and output video duration, so account for both when checking the user's cap.
- Confirm current account access, balance and price; preserve any user spending cap. Do not generate merely to test installation or check progress.
- For a trial account with no completed paid recharge or administrator-added Credits, submit only one billable request at a time across all API keys and services. Rewards, recharge cards and transferred Credits do not remove this limit. Wait for the original task's terminal result before another paid submission; asynchronous acceptance does not free the slot.
- On HTTP 429 `too_many_requests`, stop new paid submissions and use free task polling on the original task ID. Do not rotate keys, switch services or blindly retry. A disconnect or proxy timeout does not prove the task stopped; if it remains without a terminal result for a long time, contact support with the returned `trace_id`.
- After one submission, retain the returned task ID. Use `happyhorse_get_task` to query that same ID, with the exact ID argument name from the schema. A pending result is not success; stop at terminal failure and preserve upstream meaning. Do not submit another generation to poll.
- Report complete only with an explicit successful terminal status and returned media URLs. Never fabricate audio/image/video URLs or claim a unique billing record without checking the account's actual usage.
