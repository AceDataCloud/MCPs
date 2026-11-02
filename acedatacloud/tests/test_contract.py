"""Coverage-contract, generated-doc, and MCP protocol parity tests."""

import json
from pathlib import Path

import pytest

import tools  # noqa: F401
from contracts.platform_operations import OPERATIONS
from contracts.render import (
    INFO_TOOL,
    registered_contract_tools,
    render_usage_guide,
    replace_readme_reference,
)
from contracts.tool_catalog import advertised_tools
from core.server import mcp
from core.visibility import list_visible_tools
from tools.info_tools import acedatacloud_get_usage_guide

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "tests" / "snapshots" / "tools_list.json"


def test_operation_contract_is_well_formed():
    operation_ids = [operation.operation_id for operation in OPERATIONS]
    assert len(operation_ids) == len(set(operation_ids))

    for operation in OPERATIONS:
        if operation.coverage in {"covered", "shared"}:
            assert operation.tool
            assert operation.test_id not in {"", "pending"}
        else:
            assert operation.tool is None
            assert operation.rationale
        if operation.risk != "read" and operation.coverage in {"covered", "shared"}:
            assert operation.confirm


@pytest.mark.asyncio
async def test_registered_tools_match_contract():
    tools_list = await mcp.list_tools()
    registered = {tool.name for tool in tools_list}
    assert registered == registered_contract_tools()
    assert INFO_TOOL in registered


@pytest.mark.asyncio
async def test_tools_list_schema_snapshot():
    tools_list = await mcp.list_tools()
    actual = [
        {
            "name": tool.name,
            "inputSchema": tool.inputSchema,
        }
        for tool in sorted(tools_list, key=lambda item: item.name)
    ]
    expected = json.loads(SNAPSHOT.read_text())
    assert actual == expected


@pytest.mark.asyncio
async def test_usage_guide_is_contract_generated(monkeypatch):
    monkeypatch.setattr("core.visibility.client.api_token", "")
    assert await acedatacloud_get_usage_guide() == render_usage_guide()
    guide = render_usage_guide()
    guide_lines = guide.splitlines()
    for tool in advertised_tools() - {INFO_TOOL}:
        assert sum(line.startswith(f"- {tool} —") for line in guide_lines) == 1


@pytest.mark.asyncio
async def test_usage_retention_and_saved_balance_guidance_is_discoverable(monkeypatch):
    monkeypatch.setattr("core.visibility.client.api_token", "")
    visible = {tool.name: tool for tool in await list_visible_tools()}
    for name in (
        "acedatacloud_list_usage",
        "acedatacloud_get_usage",
        "acedatacloud_export_usage",
        "acedatacloud_usage_summary",
    ):
        description = visible[name].description
        assert "60 days" in description
        assert "30" in description
    assert "metadata.request" in visible["acedatacloud_get_usage"].description
    assert "metadata.response" in visible["acedatacloud_get_usage"].description
    for name in ("acedatacloud_get_application", "acedatacloud_get_balance"):
        description = " ".join(visible[name].description.split())
        assert "last-saved" in description
        assert "times out" in description
        assert "service status" in description
    guide = await acedatacloud_get_usage_guide()
    assert "60 days" in guide
    assert "30 days without changing charges, usage or aggregate totals" in guide
    assert "Save bodies at call time" in guide
    assert "A positive balance does not prove availability" in guide


def test_readme_generated_reference_is_current():
    current = (ROOT / "README.md").read_text()
    assert replace_readme_reference(current) == current
