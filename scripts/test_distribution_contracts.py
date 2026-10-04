"""Prevent publishing packages that fail registry ownership or install another project."""

import json
import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]


class DistributionContractsTest(unittest.TestCase):
    def test_registry_packages_have_matching_identity_and_ownership_marker(self):
        catalog = json.loads((ROOT / "scripts/mcp_catalog.json").read_text())[
            "services"
        ]
        for alias, entry in catalog.items():
            server_path = ROOT / alias / "server.json"
            if entry["status"] != "active" or not server_path.exists():
                continue
            with self.subTest(alias=alias):
                server = json.loads(server_path.read_text())
                project = tomllib.loads((ROOT / alias / "pyproject.toml").read_text())[
                    "project"
                ]
                for package in server.get("packages", []):
                    if package["registryType"] == "pypi":
                        self.assertEqual(package["identifier"], project["name"])
                        readme = (ROOT / alias / project["readme"]).read_text()
                        self.assertIn(f"mcp-name: {server['name']}", readme)

    def test_openai_distribution_and_entry_point_are_unambiguous(self):
        project = tomllib.loads((ROOT / "openai/pyproject.toml").read_text())["project"]
        self.assertEqual(project["name"], "mcp-openai-pro")
        self.assertEqual(project["scripts"], {"mcp-openai-pro": "main:main"})
        dockerfile = (ROOT / "openai/Dockerfile").read_text()
        self.assertIn('CMD ["mcp-openai-pro",', dockerfile)
