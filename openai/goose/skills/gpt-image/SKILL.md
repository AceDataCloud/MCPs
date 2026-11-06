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
- For generation or editing, use `quality: "auto"`, `"low"`, `"medium"` or `"high"` with GPT Image models. Choose `"xhigh"` or `"max"` only for GPT Image 2.5 or 2.6 Flare/Sunburst, including their `:reverse` and `:official` variants; official variants bill actual token usage. Do not silently switch models to obtain a quality setting.
- When the user explicitly selects reverse mode, pass `gpt-image-2.5-flare:reverse` or `gpt-image-2.5-sunburst:reverse` unchanged to generate/edit; each is equivalent to its unsuffixed model. GPT Image 2/2.5 unsuffixed and `:reverse` models bill per successful image (base price 0.19 Credits/image; confirm current account pricing). For 2.0/2.5 requests, the API may use compatible GPT Image 2.5 Flare during recovery without changing the requested model or per-image billing; do not treat recovery as permission to resubmit.
- After one submission, retain the returned task ID. Use `gpt_image_get_task` to query that same ID, with the exact ID argument name from the schema. A pending result is not success; stop at terminal failure and preserve upstream meaning. Do not submit another generation to poll.
- Report complete only with an explicit successful terminal status and returned media URLs. Never fabricate audio/image/video URLs or claim a unique billing record without checking the account's actual usage.
- When using GPT Image, choose a public `gpt-image-*` model explicitly. This image plugin does not offer chat, embeddings, audio or Nano Banana as automatic fallbacks.

The installed server is the canonical published `--profile gpt-image` surface, including `gpt_image_list_tasks` for bounded history lookup. Model must be explicitly supplied for generate/edit; inspect its enum rather than inventing an alias.

For 2.6 generation or URL-based editing, select `gpt-image-2.6-flare` or `gpt-image-2.6-sunburst`, or their complete `:reverse` / `:official` variants; never pass `gpt-image-2.6`, `gpt-image-2.6:reverse` or `gpt-image-2.6:official`. Preserve the exact selected ID. Plain/reverse 2.6 models bill 0.22 Credits per successful output file even if the response reports tokens; official variants use the same actual-token rates as 2.5, not a fixed image price. Confirm current account pricing before submission. For multiple outputs use `n` (1–10) with `response_format: "url"`; `b64_json` requires `n=1`. SVG is not supported. A failed 2.6 request has no cross-model fallback; query the original task and report failure rather than substituting a model.

## GPT Image 2.6 procedure

1. Choose static PNG/JPEG/WebP or native GIF before submitting. For static 4K generation/editing, pass concrete pixel dimensions such as `size: "3840x2160"` or `"2160x3840"`, never `"4K"` or `"4096x4096"`. Static dimensions must be multiples of 16, with a longest side at most 3840, 655,360–8,294,400 total pixels and aspect ratio at most 3:1.
2. For an explicitly requested animation, use `output_format: "gif"` on any of the six complete 2.6 IDs above. Start with `size: "512x512"`, `frame_count: 9`, `frame_duration_ms: 200`; omitted/auto GIF size uses that preview preset. Frame count must be an integer 2–16 and per-frame duration an integer 20–655350 ms, rounded to the nearest 10 ms when encoded. Frame controls are GIF-only; `n` counts GIF files, not frames. Actual dimensions may be adjusted. Size, frames and quantity share a model pixel budget: do not infer general 1K or 4K GIF support from static sizes. Omit mask, markup, output_compression, prompt_rewriter and partial_images for GIF.
3. Set `complexity: "low"`, `"medium"` or `"high"` only for 2.6 when planning control is needed. It is independent of rendering `quality`; omit it for the model default `high`. It has no separate surcharge, but official variants still bill actual tokens.
4. For annotation-guided static editing, prepare a PNG with transparent pixels matching the first reference after orientation. Each image must be at most 16,777,216 pixels, with markup at most 40MB. Pass `markup` as an HTTPS URL, PNG base64 data URL or an object containing only `image_url`; never a local path or `file_id`. Describe the marked change in `prompt`. Do not combine markup with mask, GIF or prompt_rewriter. The MCP edit tool sends JSON references, not multipart file uploads. Omit `input_fidelity` for 2.6.
5. Submit once using `gpt_image_generate` or `gpt_image_edit`, retain the task ID, then query that same ID with `gpt_image_get_task` until terminal. Report only returned results, preserving failure details without another billable submission.
