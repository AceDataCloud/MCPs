#!/usr/bin/env python3
"""Distribute the shared OAuth source into self-contained MCP packages."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("shared/oauth.py")
HEADER = "# Generated from shared/oauth.py by scripts/sync_oauth.py; do not edit.\n\n"
STATE_SOURCE = Path("shared/oauth_state.py")
STATE_HEADER = (
    "# Generated from shared/oauth_state.py by scripts/sync_oauth.py; do not edit.\n\n"
)
DEPLOY_SOURCE = Path("shared/deploy_oauth_state.sh")

SHARED_SERVERS = (
    "aichat",
    "face",
    "fish",
    "flux",
    "glm",
    "grok",
    "hailuo",
    "hcaptcha",
    "image2text",
    "kling",
    "luma",
    "maestro",
    "minimax",
    "nanobanana",
    "openai",
    "producer",
    "qwen-image",
    "recaptcha",
    "seedance",
    "seedream",
    "serp",
    "shorturl",
    "sora",
    "suno",
    "turnstile",
    "veo",
    "wan",
    "webextrator",
)

# These implementations have different behavior and must not be overwritten.
LOCAL_SERVERS = {
    "acedatacloud": "PlatformToken instead of an API Credential",
    "digitalhuman": "redirect validation and revoked-token tracking",
    "happyhorse": "redirect validation and revoked-token tracking",
    "midjourney": "distinct callback/token-exchange implementation",
}
STATE_SERVERS = (*SHARED_SERVERS, "digitalhuman", "happyhorse", "midjourney")
DEPLOY_SERVERS = tuple(
    server
    for server in STATE_SERVERS
    if server
    not in {"digitalhuman", "hcaptcha", "image2text", "recaptcha", "sora", "turnstile"}
)


def sync(root: Path = ROOT, *, check: bool = False) -> list[Path]:
    """Return stale package paths; update them unless this is a check-only run."""
    expected = set(SHARED_SERVERS) | LOCAL_SERVERS.keys()
    discovered = {path.parent.parent.name for path in root.glob("*/core/oauth.py")}
    if discovered != expected:
        raise ValueError(
            "OAuth inventory changed; classify new servers before syncing. "
            f"Unclassified: {sorted(discovered - expected)}; "
            f"missing: {sorted(expected - discovered)}"
        )

    rendered = HEADER.encode() + (root / SOURCE).read_bytes()
    rendered_state = STATE_HEADER.encode() + (root / STATE_SOURCE).read_bytes()
    rendered_deploy = (root / DEPLOY_SOURCE).read_bytes()
    stale = []
    for server in SHARED_SERVERS:
        relative = Path(server) / "core/oauth.py"
        target = root / relative
        if target.read_bytes() != rendered:
            stale.append(relative)
            if not check:
                target.write_bytes(rendered)
    for server in STATE_SERVERS:
        relative = Path(server) / "core/oauth_state.py"
        target = root / relative
        if not target.exists() or target.read_bytes() != rendered_state:
            stale.append(relative)
            if not check:
                target.write_bytes(rendered_state)
    for server in DEPLOY_SERVERS:
        relative = Path(server) / "deploy/oauth-state.sh"
        target = root / relative
        if not target.exists() or target.read_bytes() != rendered_deploy:
            stale.append(relative)
            if not check:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(rendered_deploy)
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail on stale copies without writing"
    )
    args = parser.parse_args()
    try:
        stale = sync(check=args.check)
    except ValueError as error:
        parser.exit(1, f"{error}\n")
    if args.check and stale:
        print("Shared OAuth copies are stale; run python3 scripts/sync_oauth.py:")
        for path in stale:
            print(f"  {path}")
        return 1
    print(
        f"Shared OAuth: {len(SHARED_SERVERS)} providers, {len(STATE_SERVERS)} stores, and {len(DEPLOY_SERVERS)} deploy helpers checked; {len(stale)} copies updated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
