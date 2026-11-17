#!/usr/bin/env python3
"""Reconcile every configured standalone repository from this fixed checkout."""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_mappings(root: Path) -> dict:
    mappings = yaml.safe_load((root / "sync.yaml").read_text())["mappings"]
    if not isinstance(mappings, dict) or not mappings:
        raise ValueError("sync.yaml must contain mappings")
    for directory, config in mappings.items():
        if not isinstance(directory, str) or not re.fullmatch(
            r"[A-Za-z0-9_-]+", directory
        ):
            raise ValueError("Invalid source directory")
        source = (root / directory).resolve()
        if source.parent != root.resolve() or not source.is_dir():
            raise ValueError(f"Missing or external source directory: {directory}")
        if not isinstance(config, dict) or not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", config.get("repo", "")
        ):
            raise ValueError(f"Invalid repository for {directory}")
        excludes = config.get("exclude", [])
        if not isinstance(excludes, list) or not all(
            isinstance(item, str) for item in excludes
        ):
            raise ValueError(f"Invalid exclusions for {directory}")
    return mappings


def mirror_contents(source: Path, target: Path, excludes: list[str]) -> None:
    # Compare content: checkout timestamps can otherwise hide equal-sized edits.
    subprocess.run(
        [
            "rsync",
            "-a",
            "--checksum",
            "--delete",
            "--exclude=.git",
            *(f"--exclude={item}" for item in excludes),
            f"{source}/",
            f"{target}/",
        ],
        check=True,
    )


def main() -> None:
    mappings = load_mappings(ROOT)
    source_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    for directory, config in mappings.items():
        with tempfile.TemporaryDirectory(prefix="standalone-sync-") as temporary:
            target = Path(temporary) / "target"
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--quiet",
                    "--depth=1",
                    "--branch=main",
                    f"https://github.com/{config['repo']}.git",
                    str(target),
                ],
                check=True,
            )
            mirror_contents(ROOT / directory, target, config.get("exclude", []))
            subprocess.run(["git", "add", "-A"], cwd=target, check=True)
            diff = subprocess.run(
                ["git", "diff", "--cached", "--quiet"], cwd=target, check=False
            )
            if diff.returncode == 0:
                print(f"Unchanged: {directory}", flush=True)
                continue
            if diff.returncode != 1:
                raise RuntimeError(f"Cannot inspect staged changes: {directory}")
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Ace Data Cloud Dev",
                    "-c",
                    "user.email=dev@acedata.cloud",
                    "commit",
                    "--quiet",
                    "-m",
                    f"sync: {directory} from {source_sha}",
                ],
                cwd=target,
                check=True,
            )
            subprocess.run(
                ["git", "push", "origin", "HEAD:main"], cwd=target, check=True
            )
            print(f"Synced: {directory} from {source_sha}", flush=True)


if __name__ == "__main__":
    main()
