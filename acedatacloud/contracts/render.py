"""Render public tool inventories from the operation coverage contract."""

from collections import defaultdict

from contracts.platform_operations import OPERATIONS, Operation

README_START = "<!-- BEGIN GENERATED TOOL REFERENCE -->"
README_END = "<!-- END GENERATED TOOL REFERENCE -->"
INFO_TOOL = "acedatacloud_get_usage_guide"
INFO_DESCRIPTION = "Explain authentication, safety, and the available management tools."


def documented_operations() -> tuple[Operation, ...]:
    """Return one representative operation per registered API-backed tool."""
    seen: set[str] = set()
    result: list[Operation] = []
    for operation in OPERATIONS:
        if operation.coverage not in {"covered", "shared"} or operation.tool is None:
            continue
        if operation.tool in seen:
            continue
        seen.add(operation.tool)
        result.append(operation)
    return tuple(result)


def registered_contract_tools() -> set[str]:
    """Return every tool expected to be registered, including the static guide."""
    return {operation.tool for operation in documented_operations() if operation.tool} | {INFO_TOOL}


def render_readme_reference() -> str:
    """Render the README's generated Tool Reference section."""
    groups: dict[str, list[Operation]] = defaultdict(list)
    for operation in documented_operations():
        groups[_group(operation)].append(operation)

    lines = [README_START, "## Tool Reference", ""]
    for title in ("Account reads", "Catalog & docs", "Writes", "Admin"):
        items = sorted(groups[title], key=lambda item: item.tool or "")
        if not items:
            continue
        lines.extend((f"### {title}", "", "| Tool | Description |", "|------|-------------|"))
        for operation in items:
            lines.append(f"| `{operation.tool}` | {operation.description} |")
        lines.append("")
    lines.extend(
        (
            "Calling a write/admin tool **without** `confirm=true` returns a redacted",
            "dry-run preview and performs no HTTP request.",
            "",
            README_END,
        )
    )
    return "\n".join(lines)


def render_usage_guide() -> str:
    """Render the runtime usage guide from the same contract as the README."""
    groups: dict[str, list[Operation]] = defaultdict(list)
    for operation in documented_operations():
        groups[_group(operation)].append(operation)

    lines = [
        "# AceDataCloud Platform Management — Tool Guide",
        "",
        "These tools manage your AceDataCloud account through the platform management API.",
        "Use a platform token, not an api.acedata.cloud service token. Hosted OAuth clients",
        "receive the appropriate platform credential automatically.",
        "",
    ]
    for title in ("Account reads", "Catalog & docs", "Writes", "Admin"):
        items = sorted(groups[title], key=lambda item: item.tool or "")
        if not items:
            continue
        lines.append(f"## {title}")
        for operation in items:
            suffix = " Requires confirm=true." if operation.confirm else ""
            lines.append(f"- {operation.tool} — {operation.description}{suffix}")
        lines.append("")
    lines.extend(
        (
            "## Safety",
            "- Mutations without confirm=true return a redacted dry-run and make zero HTTP calls.",
            "- Amounts are in Credits, not USD.",
            "- Newly created tokens are disclosed only once at their exact response path.",
            "- All account queries resolve and scope to the authenticated token subject.",
        )
    )
    return "\n".join(lines)


def replace_readme_reference(content: str) -> str:
    """Replace the marked README region, or migrate its legacy Tool Reference section."""
    generated = render_readme_reference()
    if README_START in content and README_END in content:
        before, remainder = content.split(README_START, 1)
        _, after = remainder.split(README_END, 1)
        return f"{before}{generated}{after}"

    start = content.index("## Tool Reference")
    end = content.index("## Quick Start", start)
    return f"{content[:start]}{generated}\n\n{content[end:]}"


def _group(operation: Operation) -> str:
    if operation.permission == "superuser":
        return "Admin"
    if operation.risk != "read":
        return "Writes"
    if operation.permission == "public" or operation.domain in {"Catalog", "Documentation"}:
        return "Catalog & docs"
    return "Account reads"
