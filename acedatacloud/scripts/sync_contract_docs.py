#!/usr/bin/env python3
"""Generate or check contract-backed public documentation."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from contracts.render import replace_readme_reference  # noqa: E402

README = ROOT / "README.md"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail when generated docs are stale.")
    args = parser.parse_args()

    current = README.read_text()
    expected = replace_readme_reference(current)
    if args.check:
        if current != expected:
            print("README.md tool reference is stale; run python scripts/sync_contract_docs.py")
            return 1
        print("Contract-backed documentation is current.")
        return 0

    README.write_text(expected)
    print("Updated README.md tool reference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
