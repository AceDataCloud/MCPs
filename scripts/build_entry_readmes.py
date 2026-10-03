"""Refresh the three pilot README entry sections; --check fails on drift."""
import argparse
from pathlib import Path
from entry_readmes import ENTRIES, render
ROOT = Path(__file__).resolve().parents[1]
START = "<!-- BEGIN GENERATED FIRST USE: scripts/build_entry_readmes.py -->"
END = "<!-- END GENERATED FIRST USE -->"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
stale = []
for alias in ENTRIES:
    path = ROOT / alias / "README.md"
    text = path.read_text()
    start, end = text.index(START), text.index(END) + len(END)
    updated = text[:start] + render(alias).rstrip() + text[end:]
    if updated != text:
        stale.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.write_text(updated)
if args.check and stale:
    raise SystemExit("Stale entry README sections: " + ", ".join(stale))
