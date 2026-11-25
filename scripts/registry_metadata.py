"""Project Registry discovery fields from the canonical catalog and link contract."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlencode

from scripts.marketing_readmes import contract
from scripts.mcp_catalog import documentation_target, load_catalog

ROOT = Path(__file__).resolve().parents[1]


def listing_url(alias, entry, repository_url=None):
    destination, _ = documentation_target(entry)
    if guide := entry.get("registry", {}).get("guide"):
        if not repository_url or Path(guide).name != guide or not guide.endswith(".md"):
            raise ValueError(
                f"{alias}: Registry guide must name an existing repository Markdown file"
            )
        if not (ROOT / alias / guide).is_file():
            raise ValueError(f"{alias}: Registry guide does not exist: {guide}")
        destination = repository_url + "/blob/main/" + guide
    rules = contract()
    return (
        destination
        + "?"
        + urlencode(
            {
                "utm_source": "mcp_registry",
                "utm_medium": rules["sources"]["mcp_registry"],
                "utm_campaign": rules["link_defaults"]["campaign"],
            }
        )
    )


def outputs():
    for alias, entry in load_catalog().items():
        path = ROOT / alias / "server.json"
        if entry["status"] != "active" or not path.exists():
            continue
        server = json.loads(path.read_text())
        server["websiteUrl"] = listing_url(alias, entry, server["repository"]["url"])
        if metadata := entry.get("registry"):
            server["title"] = metadata["title"]
            server["description"] = metadata["description"]
            server["icons"] = [metadata["icon"]]
        yield path, server
        for profile in entry.get("registry_profiles", []):
            scoped = json.loads(json.dumps(server))
            scoped.update(
                name=profile["name"],
                title=profile["title"],
                description=profile["description"],
                websiteUrl=server["repository"]["url"] + "/blob/main/" + profile["guide"],
                icons=[profile["icon"]],
            )
            scoped.pop("remotes", None)
            scoped["packages"][0]["packageArguments"] = profile["package_arguments"]
            yield path.with_name(profile["manifest"]), scoped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, expected in outputs():
        if json.loads(path.read_text()) != expected:
            stale.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.write_text(json.dumps(expected, indent=2) + "\n")
    if args.check and stale:
        raise SystemExit("Stale Registry metadata: " + ", ".join(stale))
    print(f"Registry metadata: {len(stale)} {'stale' if args.check else 'updated'}")


if __name__ == "__main__":
    main()
