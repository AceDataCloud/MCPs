# GPT Image by Ace Data Cloud for Smithery

[简体中文](README_zh-CN.md) · [API and current pricing](https://platform.acedata.cloud/documents/openai?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_smithery_pricing)

Generate and edit images with GPT Image, then retrieve the same image task through Ace Data Cloud. This is an independent Ace Data Cloud integration, not an official integration from the model vendor. This is a publication candidate; normal installation from the directory has not been verified. Check the listing's release status first.

## 1. Install from the official directory

Open [GPT Image by Ace Data Cloud](https://smithery.ai/servers/acedatacloud-mcp/gpt-image) and check the publisher namespace is `acedatacloud-mcp`. Search for `gpt image`; choose **Try now** or the client installation entry, then select your client. Controls may move between versions.

Reuse an existing connection for this service. The official CLI provides another directory installation entry; this command is not evidence that normal installation has passed:

```bash
npx -y smithery mcp add acedatacloud-mcp/gpt-image
```

## 2. Register, sign in, and get an application API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_smithery_api_key) and register or sign in. If **General application** does not exist, choose **Initialize General Application** first.
2. Copy its API Key, or open **Manage Keys → Create** for a separate `Smithery GPT Image` key. A service-specific application's key is limited to that service.
3. Check expiration, usage limits, Allowed APIs, service access, [current pricing and balance](https://platform.acedata.cloud/documents/openai?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_smithery_pricing). This flow uses `/openai/images/generations, /openai/images/edits, /openai/tasks`. Task lookup access does not grant generation access.
4. Copy only the raw token, without `Bearer `, quotes, or whitespace. A `platform-...` account-management token cannot replace this application key.

![Copy the application key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create an optional dedicated key and review restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These are real, redacted screenshots from Ace's SunoDify tutorial at a pinned source revision, referenced on 2026-10-18. They are not screenshots of successful Smithery authorization.

## 3. Where to paste the token in Smithery

Follow the connection's sign-in prompt. If the configuration form shows **apiKey / API Token**, paste the raw application token and save. The published schema maps `x-api-key` to the service's Bearer header. Do not manually overwrite Smithery's reserved Authorization field; it is also used for Smithery authentication.

If the connection opens a browser sign-in flow instead of a token field, finish that existing authorization flow. Do not configure both routes. Existing scan releases have timed out waiting for authorization, and the verification connection still needs sign-in; keep the error and do not resubmit generation to fix authentication.

![Smithery's official client selection screenshot](https://mintcdn.com/smithery/r4y1nsnAhcafdzOF/images/clients.png)

Unmodified official reference from [Smithery's client documentation](https://smithery.ai/docs/use/listing_your_client), referenced on 2026-10-18; original capture date/version unspecified. It illustrates client selection, not a successful connection to this service.

## 4. Start with a check that does not generate content

Ask the client: **List the GPT Image models available through this integration. Do not generate an image.**

Read-only tool: `openai_list_image_models`.

This directory entry reuses OpenAI MCP: it also exposes chat/audio tools. Choose GPT Image tools explicitly; it is not an image-only runtime.

## 5. Separate generation from task lookup

Only call `openai_generate_image` after reviewing the model, parameters, current price, and your budget. Save the returned `task_id`; accepted/pending is not completion. Query `openai_get_task` using that same value in `id` until the service reaches a successful terminal state and returns accessible media. Never rerun generation because a task is pending or failed.

```json
{"id": "YOUR_EXISTING_TASK_ID"}
```

This is a lookup-argument example, not an executed request. A client success indicator or an old media result does not prove a new generation completed. Never include keys, account details, or signed media URLs in screenshots.

## Troubleshooting

- **Search does not find it:** try the service terms above or open the exact listing. Candidate records, search indexing, and installability are separate; no ranking is promised.
- **401 / auth_required:** check the existing connection's sign-in, raw token, expiry, and permissions. Publisher scan authorization and consumer connection authorization are separate.
- **AUTH_TIMEOUT:** the publishing scan timed out waiting for authorization. It is not a generation failure; do not keep republishing to bypass it.
- **Still pending:** query the original task ID. Count completion only after a successful terminal result and accessible media.
- **Pricing and support:** use the account's current rate and allowance; no free allowance is promised. See [Ace service documentation](https://platform.acedata.cloud/documents/openai?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_smithery_pricing) for limits and support.
