"""Prevent publishing packages that fail registry ownership or install another project."""

import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]


class DistributionContractsTest(unittest.TestCase):
    def test_jetbrains_settings_copy_the_token_without_a_literal_dollar_prefix(self):
        catalog = json.loads((ROOT / "scripts/mcp_catalog.json").read_text())[
            "services"
        ]
        for alias, entry in catalog.items():
            if entry["status"] != "active":
                continue
            for path in (ROOT / alias / "jetbrains/src/main/kotlin").glob(
                "**/*Settings.kt"
            ):
                with self.subTest(alias=alias):
                    text = path.read_text()
                    self.assertNotIn("$$token", text)
                    self.assertIn('"Bearer $token"', text)

    def test_jetbrains_descriptors_and_settings_have_distinct_namespaces(self):
        catalog = json.loads((ROOT / "scripts/mcp_catalog.json").read_text())[
            "services"
        ]
        seen = {}
        for alias, entry in catalog.items():
            descriptor = (
                ROOT / alias / "jetbrains/src/main/resources/META-INF/plugin.xml"
            )
            if entry["status"] != "active" or not descriptor.exists():
                continue
            root = ET.parse(descriptor).getroot()
            identities = [("plugin", root.findtext("id"))]
            for element in root.iter():
                if element.tag in {
                    "action",
                    "group",
                    "applicationConfigurable",
                    "notificationGroup",
                }:
                    if element.get("id"):
                        identities.append((element.tag, element.get("id")))
            for path in (ROOT / alias / "jetbrains/src/main/kotlin").glob(
                "**/*Settings.kt"
            ):
                text = path.read_text()
                identities.extend(
                    ("state", name)
                    for name in re.findall(r'@State\(name = "([^"]+)"', text)
                )
                identities.extend(
                    ("storage", name)
                    for name in re.findall(r'Storage\("([^"]+)"\)', text)
                )
            for identity in identities:
                with self.subTest(alias=alias, identity=identity):
                    self.assertNotIn(identity, seen)
                    seen[identity] = alias

    def test_jetbrains_plugins_do_not_overwrite_each_others_installation(self):
        catalog = json.loads((ROOT / "scripts/mcp_catalog.json").read_text())[
            "services"
        ]
        install_directories = {}
        for alias, entry in catalog.items():
            settings = ROOT / alias / "jetbrains/settings.gradle.kts"
            if entry["status"] != "active" or not settings.exists():
                continue
            with self.subTest(alias=alias):
                match = re.search(
                    r'rootProject.name\s*=\s*"([^"]+)"', settings.read_text()
                )
                self.assertIsNotNone(match)
                directory = match[1]
                self.assertNotIn(directory, install_directories)
                self.assertEqual(directory, f"mcp-{alias}")
                install_directories[directory] = alias

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
