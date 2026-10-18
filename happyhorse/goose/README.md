# HappyHorse by Ace Data Cloud for goose

An independent **HappyHorse** plugin maintained by **Ace Data Cloud**. It installs the existing published `mcp-happyhorse` MCP server and the `happyhorse-by-acedatacloud:happyhorse-video` workflow through goose's native Open Plugins support. It is not made or endorsed by the HappyHorse brand, is not bundled with goose, and is not a listing in goose's retired extension directory.

[简体中文](README_zh_Hans.md) · [Current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_goose_pricing) · [Official goose plugin installation](https://goose-docs.ai/docs/guides/context-engineering/plugins/#install-a-plugin)

## 1. Install the independent plugin

Requirements: goose **1.55.0+**, Python 3.10+ (3.11 for the filtered GPT Image launcher), and [uv](https://docs.astral.sh/uv/) on PATH. Close any duplicate manual configuration of the same MCP server so tools do not appear twice.

```sh
goose plugin install https://github.com/AceDataCloud/HappyHorseMCP.git
```

The command installs only this service plugin, not a media bundle. Its MCP configuration loads automatically in new sessions; no hand-written `config.yaml` or custom MCP address is needed. This repository's default branch must contain the plugin before the public install command works. Until the source PR is merged and synced, this is a review candidate, not a released install.

## 2. Register, sign in and get your service API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_goose_api_key); register/sign in. If needed select **Initialize General Application**, then open **General application**.
2. Check **HappyHorse** access, available balance, current pricing and any account quota. A trial allowance is whatever your account displays now.
3. Copy the API Key on the card, or **Manage Keys → Create** a dedicated key named `goose HappyHorse`. For restrictions, allow the generation/edit and task-query APIs you will use: `/happyhorse/videos, /happyhorse/tasks`. Further operations may need other routes.
4. Copy the raw key value without `Bearer `, quotes or spaces. A `platform-...` management token is not this service API key. Never paste the key into a prompt, shared JSON, screenshot or Git.

![Actual Ace Applications screenshot: copy API Key or Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Actual Ace key creation screenshot: optional restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These redacted Ace console screenshots are reused from the SunoDify tutorial fixed at commit `8d3d035`; retrieved 2026-10-18. They explain the shared account UI, not a HappyHorse/goose generation result.

## 3. Give goose the key

macOS/Linux terminal launch (the prompt hides input; the key is not typed into shell history):

```sh
read -r -s -p 'Ace service API Token: ' ACEDATACLOUD_API_TOKEN
printf '\n'
export ACEDATACLOUD_API_TOKEN
goose session
```

Use a Bash terminal for the snippet. For the desktop app, the variable must be in the environment of the process that launches goose. Restart goose after setting it. Do not assume a terminal export is inherited by an already-open desktop app. This plugin does not add a fake Key dialog and does not read `.env` files on its own. The underlying MCP's normal configuration remains authoritative.

## 4. First connection and workflow

Ask goose to list available tools. The plugin's tools are namespaced under `happyhorse-by-acedatacloud`. Then ask it to call `happyhorse_list_models` only: this is a local reference check, not media generation.

![Official goose UI reference: asking for available extension tools](https://raw.githubusercontent.com/aaif-goose/goose/cd643d2126fffab4c6a6186905211ba868d6a657/documentation/docs/assets/guides/custom-extension-tools.png)

Official original screenshot from the goose 1.54.0 documentation snapshot; original capture date and actual client version are not stated. It shows **wiki/developer**, not an Ace run. It illustrates where tools are discussed, not a new button, public listing or verified media result.

For a real request, ask for the desired happyhorse text/image/reference video and editing and explicitly authorize the current cost. The workflow uses `happyhorse_generate_video` and `happyhorse_get_task`. Keep the same returned task ID until success or failure. A preview, a tool-call card or a pending state is not a final result. When complete, use the media URLs actually returned. Never rerun a full generation just to check progress.

## Troubleshooting

| Symptom | Action |
|---|---|
| Plugin installs but no tools | Start a new session, confirm uv is on PATH, confirm the API key reaches that process, and check MCP stderr. |
| 401/403 | Copy the full raw service key, check service access, expiration and Allowed APIs. |
| Insufficient credits / rate limit | Check account balance/current price; preserve the error and retry only as allowed. |
| Package download fails | Check access to PyPI and its file host. A mirror is an explicit administrator/user choice; the plugin does not change global package indexes. |
| Pending task | Query `happyhorse_get_task` with the same ID. Do not resubmit generation. |
| Duplicate tools | Remove the duplicate manual MCP entry for this service; keep unrelated integrations. |

## Scope and verification

The source of truth is `AceDataCloud/MCPs/happyhorse/`; this repository is a distribution mirror. It reuses `mcp-happyhorse==2026.10.12.0` and does not fork the API implementation. This plugin exposes only the corresponding service MCP server. No automatic model fallback, analytics, hooks or permission expansion is added. Installing does not generate media. goose's inference model may incur separate charges.

Validated on 2026-10-18 with goose 1.55.0: the five plugins were installed by the real `goose plugin install` command from isolated local Git review snapshots, coexisted, and automatically exposed 64 service tools (42 Suno, 7 Seedance, 7 HappyHorse, 4 GPT Image, 4 Nano Banana). Four static reference calls completed with all business API traffic directed at a local rejecting endpoint. Nano Banana was verified by schema discovery only. A local deterministic model fixture was used; there was no real model inference or paid media generation. Public mirror installation remains pending source merge and sync. Registry publication, official discovery, default-provider inclusion, terminal media and billing are separate unverified stages.
