---
name: ace-music
description: Create ACE Music songs, lyrics, covers or mashups and retrieve tasks using the ACE Music MCP in goose.
license: MIT
---

Use the plugin's `acemusic_list_models` or `acemusic_get_capabilities` for a free first check. Get the private application key from the environment that starts goose. For a new song submit once using `acemusic_generate_music` or `acemusic_generate_custom_music`. For a cover or mashup use caller-owned audio IDs. These differ from task IDs. Save the task ID and use `acemusic_get_task` until terminal. If the group partially fails, report that status and any tracks actually returned by the service.

Trial accounts have one billable request at a time across all API keys and services. Asynchronous processing retains that slot: asynchronous acceptance does not free the slot. After HTTP 429 `too_many_requests`, wait for the existing job and use free task polling on the original task ID. A disconnect or proxy timeout does not prove a submission failed. Keep the `trace_id` and reconcile the original request before another paid operation.
