"""Render public tool inventories from the operation coverage contract."""

from collections import Counter, defaultdict

from contracts.platform_operations import OPERATIONS, Operation
from contracts.tool_catalog import (
    CATEGORIES,
    INFO_TOOL,
    TOOL_CATALOG,
    ToolProfile,
    advertised_tools,
    tool_description,
)

README_START = "<!-- BEGIN GENERATED TOOL REFERENCE -->"
README_END = "<!-- END GENERATED TOOL REFERENCE -->"
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
        if operation.tool is not None and operation.tool in advertised_tools():
            groups[TOOL_CATALOG[operation.tool].category].append(operation)

    hidden = Counter(entry.reason for entry in TOOL_CATALOG.values() if not entry.advertised)
    lines = [
        README_START,
        "## Tool Reference",
        "",
        f"The default curated catalog advertises **{len(advertised_tools())} tools** before",
        "account-permission filtering, including `acedatacloud_get_usage_guide`.",
        f"The complete compatibility registry retains **{len(registered_contract_tools())} tools**.",
        "Discovery is grouped by business task, not by one tool per REST endpoint.",
        "",
        "| Not advertised by default | Count |",
        "|---------------------------|-------|",
    ]
    for reason, count in sorted(hidden.items()):
        lines.append(f"| {reason} | {count} |")
    lines.extend(
        (
            "",
            "### Categories",
            "",
            "| Category | Public | Account | Workspace | Admin |",
            "|----------|--------|---------|-----------|-------|",
        )
    )
    for title in CATEGORIES:
        counts = Counter(
            TOOL_CATALOG[operation.tool].audience
            for operation in groups[title]
            if operation.tool is not None
        )
        lines.append(
            f"| {title} | {counts['public']} | {counts['account']} | {counts['workspace']} | {counts['admin']} |"
        )
    lines.extend(
        (
            "",
            "Workspace tools cover delegated editing and site/webhook management.",
            "Admin tools require their exact permission grants, not just an admin label.",
            "",
        )
    )
    for title in CATEGORIES:
        items = sorted(groups[title], key=lambda item: item.tool or "")
        if not items:
            continue
        lines.extend(
            (
                f"### {title}",
                "",
                "| Tool | Description | Audience | Required permissions |",
                "|------|-------------|----------|----------------------|",
            )
        )
        for operation in items:
            assert operation.tool is not None
            entry = TOOL_CATALOG[operation.tool]
            scopes = ", ".join(entry.required_permissions) or operation.authentication
            description = tool_description(operation.tool, operation.description)
            lines.append(f"| `{operation.tool}` | {description} | {entry.audience} | {scopes} |")
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


def render_usage_guide(profile: ToolProfile = "curated", tool_names: set[str] | None = None) -> str:
    """Render the runtime usage guide from the same contract as the README."""
    groups: dict[str, list[Operation]] = defaultdict(list)
    included = advertised_tools(profile) if tool_names is None else tool_names
    for operation in documented_operations():
        if operation.tool is not None and operation.tool in included:
            groups[TOOL_CATALOG[operation.tool].category].append(operation)

    lines = [
        "# AceDataCloud Platform Management — Tool Guide",
        "",
        "These tools manage your AceDataCloud account through the platform management API.",
        "Use a platform token, not an api.acedata.cloud service token. Hosted OAuth clients",
        "receive the appropriate platform credential automatically.",
        "",
    ]
    for title in CATEGORIES:
        items = sorted(groups[title], key=lambda item: item.tool or "")
        if not items:
            continue
        lines.append(f"## {title}")
        for operation in items:
            assert operation.tool is not None
            suffix = " Requires confirm=true." if operation.confirm else ""
            entry = TOOL_CATALOG[operation.tool]
            suffix += " Audience: " + entry.audience + "."
            if entry.required_permissions:
                suffix += " Permissions: " + ", ".join(entry.required_permissions) + "."
            description = tool_description(operation.tool, operation.description)
            lines.append(f"- {operation.tool} — {description}{suffix}")
        lines.append("")
    lines.extend(
        (
            "## Safety",
            "- Mutations without confirm=true return a redacted dry-run and make zero HTTP calls.",
            "- Amounts are in Credits, not USD.",
            "- Newly created tokens are disclosed only once at their exact response path.",
            "- Backend account permissions and ownership checks apply to every authenticated operation.",
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
