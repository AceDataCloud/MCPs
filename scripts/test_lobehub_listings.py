"""Validate the five LobeHub owner declarations against existing source servers."""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SERVICES = {
    "suno": ("acedatacloud-mcpsuno", "Suno"),
    "seedance": ("acedatacloud-seedancemcp", "Seedance"),
    "happyhorse": ("acedatacloud-happyhorsemcp", "HappyHorse"),
    "openai": ("acedatacloud-openaimcp", "GPT Image"),
    "nanobanana": ("acedatacloud-nanobananamcp", "Nano Banana"),
}


class LobeHubListingsTest(unittest.TestCase):
    def test_existing_identifiers_real_tools_and_separate_authenticated_setup(self):
        for service, (identifier, brand) in SERVICES.items():
            with self.subTest(service=service):
                directory = ROOT / service / "lobehub"
                manifest = json.loads((directory / "lhm.plugin.json").read_text())
                self.assertEqual(manifest["identifier"], identifier)
                self.assertEqual(manifest["name"], f"{brand} by Ace Data Cloud")
                self.assertEqual(manifest["cloudEndpoint"], f"https://{service}.mcp.acedata.cloud/mcp")
                source_names = set()
                for path in (ROOT / service / "tools").glob("*.py"):
                    source_names.update(re.findall(r"async def (\w+)\(", path.read_text()))
                self.assertTrue(manifest["tools"])
                for tool in manifest["tools"]:
                    self.assertIn(tool["name"], source_names)
                    self.assertEqual(tool["inputSchema"]["type"], "object")
                for kind in ("http", "stdio"):
                    install = json.loads((directory / f"install-{kind}.json").read_text())
                    self.assertEqual(len(install["mcpServers"]), 1)
                    config = next(iter(install["mcpServers"].values()))
                    if kind == "http":
                        self.assertEqual(set(config), {"type", "url"})
                    else:
                        self.assertEqual(config["env"]["ACEDATACLOUD_API_TOKEN"], "YOUR_API_TOKEN")
                        if service == "openai":
                            self.assertEqual(config["command"], "uvx")
                            self.assertEqual(config["args"][-1], "mcp-openai-pro")

    def test_token_onboarding_and_current_contract_links_in_both_languages(self):
        for service in SERVICES:
            for name in ("README.md", "README_zh-CN.md"):
                with self.subTest(service=service, language=name):
                    text = (ROOT / service / "lobehub" / name).read_text()
                    self.assertIn("General application", text)
                    self.assertIn("Manage Keys", text)
                    self.assertIn("get-api-key-en.png", text)
                    self.assertIn("create-api-key-en.png", text)
                    self.assertIn("Bearer", text)
                    urls = re.findall(r"https://platform\.acedata\.cloud/[^\s)]+", text)
                    self.assertTrue(urls)
                    for url in urls:
                        query = parse_qs(urlsplit(url).query)
                        self.assertEqual(query["utm_source"], ["opensource"])
                        self.assertEqual(query["utm_medium"], ["referral"])
                        self.assertEqual(query["utm_campaign"], ["evergreen"])
                        self.assertIn("lobehub", query["utm_content"][0])
                        self.assertLessEqual(len(query["utm_content"][0]), 96)
