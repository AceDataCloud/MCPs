"""Copy the release verifier into servers that already publish to Smithery."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "shared/smithery_release.py"


def targets():
    catalog = json.loads((ROOT / "scripts/mcp_catalog.json").read_text())["services"]
    for alias, entry in catalog.items():
        workflow = ROOT / alias / ".github/workflows/publish.yml"
        if entry["status"] == "active" and workflow.exists():
            if "publish-smithery:" in workflow.read_text():
                yield ROOT / alias / ".github/scripts/verify_smithery_release.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = SOURCE.read_text()
    stale = []
    for target in targets():
        if target.exists() and target.read_text() == content:
            continue
        if args.check:
            stale.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    if stale:
        parser.exit(1, "Stale Smithery release verifiers: " + ", ".join(stale) + "\n")


if __name__ == "__main__":
    main()
