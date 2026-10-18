# Ace Data Cloud model preset for goose

[简体中文](README_zh_Hans.md)

This is a shareable, independently installed preset for goose 1.55.0+, not an official built-in provider. The target remains **Ace Data Cloud in the default provider picker**. Upstream [provider policy](https://github.com/aaif-goose/goose/blob/bfcc6ee6f1ee18d0c4c852a65c49b25f87ee40dc/CONTRIBUTING.md#llm-provider-integrations) currently recommends custom JSON for third-party services and only occasionally accepts exceptions. External preset PRs need an issue marked Ready; the current contributor guide asks the human contributor to write that issue. No upstream PR or built-in release is claimed here.

## Key and installation

Register/sign in at [Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_goose_api_key), open General application, copy or create a separately named API Key. Check chat permissions, expiry/Allowed APIs, balance and [current model price](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_goose_pricing). Do not use a `platform-...` management token.

![Copy the API Key or Manage Keys — real Ace console reference](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Create a dedicated API Key — real Ace console reference](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

Images are redacted shared Ace console screenshots from the fixed SunoDify tutorial, referenced 2026-10-18; not goose runtime evidence.

Run `goose info` to locate the profile's config directory, then copy `acedatacloud.json` into its `custom_providers/` directory. Do not overwrite another preset. Start goose with `ACEDATACLOUD_API_TOKEN` in its process environment, or use goose's normal credential configuration for this provider. Choose **Ace Data Cloud** after installing the preset. Selecting it still requires this installation; it is not present in a clean default goose install.

Only the public text/tool Chat Completions model IDs `gpt-4.1-mini` and `gpt-4.1` are listed. This is a picker list, not fallback. No image/audio generation, Responses, reasoning, vision or model substitution is implied. The transport URL is complete: `https://api.acedata.cloud/openai/chat/completions`. Real hosted inference and unique billing are not tested by the free local fixture.

## Upstream acceptance material

The user-facing problem: goose users who have Ace service keys cannot select Ace Data Cloud in a fresh provider list without discovering custom endpoint settings. Proposed minimal native definition: use the same declarative contract as current built-ins, separate credential name, a small verified Chat Completions list, current setup/pricing link, no automatic fallback. Verification needed: default picker visibility, key entry, streaming tool call/result turns and matched usage record; mock/local checks can run before paid verification. The maintainer must accept this scope and move the human-authored issue to Ready before an external implementation PR. That requirement is tracked as a release gate, not evidence of acceptance.
