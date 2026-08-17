#!/usr/bin/env python3
"""Require README server inventory to match sync.yaml mappings."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    mappings = set(re.findall(r"^  ([a-z0-9_-]+):\s*$", (ROOT / "sync.yaml").read_text(), re.MULTILINE))
    listed = set(re.findall(r"^\| `([^/`]+)/`", (ROOT / "README.md").read_text(), re.MULTILINE))
    missing = sorted(mappings - listed)
    extra = sorted(listed - mappings)
    if missing or extra:
        if missing:
            print(f"README missing mapped servers: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"README lists unmapped servers: {', '.join(extra)}", file=sys.stderr)
        return 1
    print(f"README inventory matches {len(mappings)} mapped servers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
