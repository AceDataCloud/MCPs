"""Exercise actual initialize metadata in isolated self-contained packages."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.mcp_catalog import load_catalog
from scripts.runtime_metadata import runtime_icons

ROOT = Path(__file__).resolve().parents[1]
PROBE = """
import asyncio,json
from mcp.shared.memory import create_connected_server_and_client_session
from core.server import mcp
import tools
async def main():
    async with create_connected_server_and_client_session(mcp) as client:
        result=await client.initialize()
        tools=await client.list_tools()
        print(json.dumps({'server':result.serverInfo.model_dump(mode='json'), 'tools':[t.model_dump(mode='json') for t in tools.tools]}))
asyncio.run(main())
"""


@pytest.mark.parametrize(
    "alias,count",
    [("seedance", 7), ("nanobanana", 4), ("happyhorse", 7), ("openai", 15)],
)
def test_initialize_returns_catalog_icon_and_existing_tools(alias, count):
    env = os.environ.copy()
    for key in [
        "MCP_SERVER_URL",
        "MCP_SERVER_NAME",
        "MCP_OAUTH_REDIS_URL",
        "MCP_OAUTH_REDIS_PASSWORD",
    ]:
        env.pop(key, None)
    env.update(PYTHON_DOTENV_DISABLED="1", ACEDATACLOUD_API_TOKEN="metadata-test-dummy")
    result = subprocess.run(
        [sys.executable, "-c", PROBE],
        cwd=ROOT / alias,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=True,
    )
    data = json.loads(result.stdout)
    assert data["server"]["name"] == alias
    icon = runtime_icons(load_catalog())[alias]
    assert [{key: value[key] for key in icon} for value in data["server"]["icons"]] == [icon]
    assert len(data["tools"]) == count
    assert all(tool["inputSchema"]["type"] == "object" for tool in data["tools"])
