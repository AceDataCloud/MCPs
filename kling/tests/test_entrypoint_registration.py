"""The production entrypoint must expose tools without importing test modules."""

import json
import os
import subprocess
import sys
from pathlib import Path


def test_clean_entrypoint_registers_kling_capabilities():
    env = {**os.environ, "MCP_SERVER_URL": "", "LOG_LEVEL": "ERROR"}
    script = """
import asyncio, json
import tools
from core.server import mcp
async def main():
    print(json.dumps([tool.name for tool in await mcp.list_tools()]))
asyncio.run(main())
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    names = set(json.loads(result.stdout))
    expected = {
        "kling_generate_turbo_video",
        "kling_generate_storyboard",
        "kling_goods_studio",
        "kling_video_commerce",
        "kling_generate_with_assets",
    }
    assert expected <= names

    assert not {"kling_apparel_video", "kling_virtual_try_on", "kling_manage_elements", "kling_manage_voices"} & names
