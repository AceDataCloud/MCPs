"""Project catalog icons into existing FastMCP servers, without changing identity."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from urllib.parse import urlsplit

from scripts.mcp_catalog import load_catalog

ROOT = Path(__file__).resolve().parents[1]


def runtime_icons(catalog: dict) -> dict[str, dict[str, str]]:
    """Project only services with an explicit runtime_icon opt-in.

    Registry profiles are separate identities and never supply generic-server
    metadata implicitly. An explicit runtime icon does not create a listing.
    """
    icons = {}
    for alias, entry in catalog.items():
        if entry["status"] != "active":
            continue
        icon = entry.get("runtime_icon")
        if icon is None:
            continue
        if icon == "registry":
            icon = entry.get("registry", {}).get("icon")
        if not isinstance(icon, dict):
            raise ValueError(f"{alias}: runtime_icon requires an icon or existing registry icon")
        src = icon.get("src")
        if (
            not isinstance(src, str)
            or not src
            or any(not char.isprintable() or char.isspace() for char in src)
        ):
            raise ValueError(f"{alias}: runtime icon requires a nonempty printable HTTPS URL")
        url = urlsplit(src)
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError(f"{alias}: runtime icon requires a public HTTPS URL")
        if icon.get("mimeType") not in {
            "image/png",
            "image/jpeg",
            "image/svg+xml",
            "image/webp",
        }:
            raise ValueError(f"{alias}: unsupported runtime icon MIME type")
        if set(icon) != {"src", "mimeType"}:
            raise ValueError(f"{alias}: unsupported runtime icon fields")
        icons[alias] = icon
    return icons


def source_span(source: bytes, node: ast.AST) -> tuple[int, int]:
    """AST columns are UTF-8 byte offsets, including for non-ASCII source."""
    lines = source.splitlines(keepends=True)
    start = sum(map(len, lines[: node.lineno - 1])) + node.col_offset
    end = sum(map(len, lines[: node.end_lineno - 1])) + node.end_col_offset
    return start, end


def render_server(source: bytes, icon: dict[str, str]) -> bytes:
    tree = ast.parse(source)
    calls = [
        node.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "mcp" for target in node.targets)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "FastMCP"
    ]
    if len(calls) != 1:
        raise ValueError("expected exactly one existing mcp = FastMCP(...) initialization")
    expected = f"Icon(src={json.dumps(icon['src'])}, mimeType={json.dumps(icon['mimeType'])})"
    value = f"[{expected}]".encode()
    call = calls[0]
    keyword = next((item for item in call.keywords if item.arg == "icons"), None)
    if keyword:
        if ast.dump(keyword.value) != ast.dump(ast.parse(value, mode="eval").body):
            start, end = source_span(source, keyword.value)
            source = source[:start] + value + source[end:]
    else:
        kwargs = next((item for item in call.keywords if item.arg is None), None)
        if kwargs is None:
            raise ValueError("expected existing FastMCP **kwargs before inserting icon")
        start, _ = source_span(source, kwargs)
        source = source[:start] + b"icons=" + value + b", " + source[start:]
    if not any(
        isinstance(node, ast.ImportFrom)
        and node.module == "mcp.types"
        and any(item.name == "Icon" and item.asname is None for item in node.names)
        for node in tree.body
    ):
        imports = [
            node
            for node in tree.body
            if isinstance(node, ast.ImportFrom) and node.module == "mcp.server.fastmcp"
        ]
        if len(imports) != 1:
            raise ValueError("expected existing FastMCP import before inserting Icon import")
        _, end = source_span(source, imports[0])
        source = source[:end] + b"\nfrom mcp.types import Icon" + source[end:]
    ast.parse(source)
    return source


def sync(root: Path = ROOT, *, check: bool = False, catalog: dict | None = None) -> list[Path]:
    icons = runtime_icons(load_catalog() if catalog is None else catalog)
    # Validate every input before writing any service file.
    outputs = {}
    for alias, icon in icons.items():
        path = Path(alias) / "core/server.py"
        outputs[path] = render_server((root / path).read_bytes(), icon)
    stale = []
    for path, expected in outputs.items():
        if (root / path).read_bytes() != expected:
            stale.append(path)
            if not check:
                (root / path).write_bytes(expected)
    return stale


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = sync(check=args.check)
    if args.check and stale:
        raise SystemExit("Stale runtime icons: " + ", ".join(map(str, stale)))
    print(f"Runtime icons: {len(stale)} {'stale' if args.check else 'updated'}")


if __name__ == "__main__":
    main()
