"""Native goose distribution contracts; no network or credentials required."""

import json
import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ("suno", "seedance", "happyhorse", "openai", "nanobanana")


class GoosePluginContracts(unittest.TestCase):
    def test_every_plugin_is_independent_and_uses_private_skill_paths(self):
        names = set()
        for service in SERVICES:
            with self.subTest(service=service):
                root = ROOT / service
                manifest = json.loads((root / ".goose-plugin/plugin.json").read_text())
                name = manifest["name"]
                self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertNotIn(name, names)
                names.add(name)
                self.assertEqual(
                    manifest["skills"], {"paths": ["./goose/skills"], "exclusive": True}
                )
                self.assertEqual(
                    manifest["mcpServers"],
                    {"paths": ["./.mcp.json"], "exclusive": True},
                )
                servers = json.loads((root / ".mcp.json").read_text())["mcpServers"]
                self.assertEqual(len(servers), 1)
                server = next(iter(servers.values()))
                self.assertNotIn(
                    "env", server
                )  # Inherit user environment; no literal token in Git.
                self.assertNotIn("ACEDATACLOUD_API_TOKEN", json.dumps(server))
                self.assertFalse((root / "goose/hooks").exists())
                self.assertEqual(
                    len(list((root / "goose/skills").glob("*/SKILL.md"))), 1
                )

    def test_acquisition_links_have_four_existing_attribution_fields(self):
        for service in SERVICES:
            text = (ROOT / service / "goose/README.md").read_text()
            urls = re.findall(r"https://platform\.acedata\.cloud/[^)\s]+", text)
            self.assertTrue(urls, service)
            for url in urls:
                query = parse_qs(urlparse(url).query)
                self.assertEqual(query["utm_source"], ["opensource"])
                self.assertEqual(query["utm_medium"], ["referral"])
                self.assertEqual(query["utm_campaign"], ["evergreen"])
                self.assertIn("goose", query["utm_content"][0])


if __name__ == "__main__":
    unittest.main()
