# VS Code Extension Outcome Bundle

## Status and scope

This document defines the evidence to collect after an authorized extension release or retirement action. It is a handoff template, not evidence that any package was submitted, published, unpublished, installed from Marketplace, or retired.

The repository source of truth is `scripts/vscode_extension_inventory.json`. Its `publish_policy` field is a gate, not proof of Marketplace state:

- `publishable` permits an owner to consider a checked-in active package for release; it does not authorize or record a release.
- `nonpublishable` blocks release. The checked-in Sora package is retired and nonpublishable.
- `owner-handoff` requires the account owner to decide and perform any external action. The unchecked-in `acedatacloud.acedatacloud-mcp` legacy aggregate remains retirement-pending.

Do not use a Marketplace search result or listing page alone as proof. External actions require an owner-provided receipt or export tied to the extension ID, version, account, and timestamp. Never include API keys, publisher credentials, session cookies, authorization headers, or unredacted user data.

## Common packet manifest

Each client packet must contain:

1. **Identity:** extension ID, checked-in alias, version, product class, runtime architecture, lifecycle, and publish policy copied from the inventory and package manifest.
2. **Build provenance:** repository URL, commit SHA, clean-tree result, build command, artifact filename, SHA-256 digest, and build log.
3. **Authorized external action:** owner identity or ticket, approval reference, UTC timestamp, intended action, and the provider-generated receipt/export. Record `not performed` when no action occurred.
4. **Install provenance:** installation source, client name/version, operating system, extension ID/version displayed by the client, and artifact digest when installed from a local package.
5. **Runtime result:** MCP server discovery, authentication boundary, one non-mutating representative tool call, redacted result, and extension-host/MCP logs covering the same UTC interval.
6. **Acquisition result:** the rendered platform and credential URLs, expected `utm_source=vscode`, `utm_medium=extension`, alias-specific campaign, and an authorized analytics export if attribution is being evaluated.
7. **Disposition:** pass, fail, blocked, or not run; observed limitations; follow-up owner; and evidence file index.

Screenshots must include the client chrome, extension identity, and clock where practical. Pair screenshots with machine-readable text or logs; screenshots alone are insufficient. Redact tokens at capture time rather than editing raw secrets into the packet and masking them later.

## Claude-in-VS-Code packet

Use this packet for the Claude client operating in VS Code:

- Record the Claude extension/client version and VS Code version independently.
- Capture the extension installation identity and enabled state.
- Open a fresh Claude conversation and capture MCP server/tool discovery for the selected representative.
- Exercise only a safe, non-mutating tool. Capture the prompt, tool name, redacted arguments, result, and correlated extension-host/MCP log interval.
- Record whether the credential prompt or existing secret storage supplied authentication without exposing the credential.
- Save the common packet manifest and evidence index as `claude-vscode/<extension-id>/<utc-run-id>/`.

A successful local or pre-release packet proves only the recorded client/artifact interaction. It does not prove Marketplace submission, publication, discoverability, install counts, or account ownership.

## Cursor packet

Use this packet for Cursor:

- Record the Cursor version, VS Code compatibility version if displayed, and operating system.
- Capture the extension installation identity, version, enabled state, and installation source.
- Start a fresh agent chat and capture MCP server/tool discovery for the selected representative.
- Exercise the same safe, non-mutating scenario used in the Claude packet where the tool surface permits it. Capture the prompt, tool name, redacted arguments, result, and correlated logs.
- Record any architecture-specific behavior, especially declarative input prompting versus provider runtime secret storage.
- Save the common packet manifest and evidence index as `cursor/<extension-id>/<utc-run-id>/`.

A Cursor packet and a Claude packet are separate outcomes. Success in one client must not be copied or inferred for the other.

## Representative governance classes

The owner should collect both client packets for at least one entry in every in-scope class. The named representatives are stable audit fixtures; substitution requires an inventory and test update.

| Class | Representative | Required outcome |
| --- | --- | --- |
| Configured, generator-maintained provider | `acedatacloud.mcp-suno` | Provider registration, secret-backed auth, and one safe read-only tool |
| Configured, manually maintained declarative | `acedatacloud.mcp-face-transform` | Declarative server/input registration without runtime migration |
| Active, unconfigured provider | `acedatacloud.mcp-minimax` | Existing provider runtime works without adding it to YAML or regenerating artifacts |
| Active, unconfigured declarative | `acedatacloud.mcp-aichat` | Existing declarative package works without adding it to YAML |
| Account management | `acedatacloud.mcp-acedatacloud` | Platform-token credential route and one non-mutating account read |
| Retired, nonpublishable checked-in package | `acedatacloud.mcp-sora` | Release remains blocked; no runtime or publication exercise is required |
| External legacy aggregate | `acedatacloud.acedatacloud-mcp` | Owner decision and external retirement receipt remain pending; no repository artifact is asserted |

`acedatacloud.mcp-fish` must retain the same configured/manual/declarative controls as the Face representative. `acedatacloud.mcp-openai` must retain the same active/unconfigured/declarative controls as the AiChat representative. These sibling assertions are enforced offline even when they are not selected for every client run.

## Owner handoff checklist

Before any external action, the owner must:

- confirm the target extension ID and publisher account;
- verify the inventory lifecycle and publish policy at the candidate commit;
- approve the exact version and artifact digest;
- decide whether the external legacy aggregate should be retired;
- perform account and Marketplace actions outside repository automation; and
- return receipts for attachment to the outcome packet.

Repository maintainers may validate the returned packet against this contract. They must not translate a proposed action, a public listing, or a locally built package into a claim that submission or retirement occurred.
