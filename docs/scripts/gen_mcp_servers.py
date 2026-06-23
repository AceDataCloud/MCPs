#!/usr/bin/env python3
"""Regenerate core/data/mcp_servers.json from the sibling MCPs/*/server.json files.

Run from the MCPs monorepo root:  python docs/scripts/gen_mcp_servers.py
Keeps `acedatacloud_list_mcp_servers` accurate without hand-maintaining a list.
"""

import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "docs", "core", "data", "mcp_servers.json")


def main() -> None:
    servers = []
    for sj in sorted(glob.glob(os.path.join(ROOT, "*", "server.json"))):
        d = os.path.basename(os.path.dirname(sj))
        if d == "docs":
            continue
        try:
            with open(sj, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:  # noqa: BLE001
            continue
        remote = next((r["url"] for r in data.get("remotes", []) or [] if r.get("url")), None)
        pkg = next(
            (p["identifier"] for p in data.get("packages", []) or [] if p.get("identifier")), None
        )
        servers.append(
            {
                "name": (data.get("name", "").split("/")[-1] or d),
                "description": data.get("description", ""),
                "remote_url": remote,
                "pypi_package": pkg,
                "website": data.get("websiteUrl"),
            }
        )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    payload = {"_generated_from": "MCPs/*/server.json", "count": len(servers), "servers": servers}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {len(servers)} servers to {OUT}")


if __name__ == "__main__":
    main()
