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
from core.server import mcp
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
async def test_usage_guide_is_contract_generated():
    assert await acedatacloud_get_usage_guide() == render_usage_guide()
    guide = render_usage_guide()
    guide_lines = guide.splitlines()
    for tool in registered_contract_tools() - {INFO_TOOL}:
        assert sum(line.startswith(f"- {tool} —") for line in guide_lines) == 1


def test_readme_generated_reference_is_current():
    current = (ROOT / "README.md").read_text()
    assert replace_readme_reference(current) == current
