#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "scripts" / "vscode_extension_inventory.json"
SCHEMA_PATH = ROOT / "scripts" / "vscode_extension_inventory.schema.json"
CONFIG_PATH = ROOT / "scripts" / "vscode_extensions.yaml"
CATALOG_PATH = ROOT / "scripts" / "mcp_catalog.json"

EXPECTED_ALIASES = {
    "acedatacloud",
    "aichat",
    "face",
    "fish",
    "flux",
    "grok",
    "hailuo",
    "kling",
    "luma",
    "midjourney",
    "minimax",
    "nanobanana",
    "openai",
    "producer",
    "seedance",
    "seedream",
    "serp",
    "shorturl",
    "sora",
    "suno",
    "veo",
    "wan",
}
EXPECTED_CONFIGURED = EXPECTED_ALIASES - {"aichat", "minimax", "openai"}
EXPECTED_PROVIDER = EXPECTED_ALIASES - {"aichat", "face", "fish", "openai"}
EXPECTED_DECLARATIVE = {"aichat", "face", "fish", "openai"}
EXPECTED_MANUAL = {"aichat", "face", "fish", "minimax", "openai"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def architecture(package: dict[str, Any], vscode_dir: Path) -> str:
    contributes = package.get("contributes", {})
    has_provider = "mcpServerDefinitionProviders" in contributes
    has_declarative = "mcpServers" in contributes
    if has_provider == has_declarative:
        return "invalid"
    if has_provider:
        if package.get("main") != "./extension.js":
            return "invalid"
        return "provider" if (vscode_dir / "extension.js").is_file() else "invalid"
    if "main" in package or (vscode_dir / "extension.js").exists():
        return "invalid"
    return "declarative"


class VsCodeExtensionInventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = load_json(INVENTORY_PATH)
        cls.schema = load_json(SCHEMA_PATH)
        cls.records = cls.inventory["checked_in_packages"]
        cls.by_alias = {record["alias"]: record for record in cls.records}

    def test_inventory_validates_against_draft_2020_12_schema(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.inventory)

    def test_exact_checked_in_package_inventory(self) -> None:
        discovered = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.glob("*/vscode/package.json")
        }
        governed = {record["package_json"] for record in self.records}

        self.assertEqual(len(self.records), 22)
        self.assertEqual(set(self.by_alias), EXPECTED_ALIASES)
        self.assertEqual(len(self.by_alias), len(self.records))
        self.assertEqual(governed, discovered)

        extension_ids: set[str] = set()
        for record in self.records:
            package = load_json(ROOT / record["package_json"])
            self.assertEqual(
                record["package_json"], f"{record['alias']}/vscode/package.json"
            )
            self.assertEqual(
                record["extension_id"], f"{package['publisher']}.{package['name']}"
            )
            extension_ids.add(record["extension_id"])
        self.assertEqual(len(extension_ids), 22)

    def test_yaml_configuration_is_exact(self) -> None:
        config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
        configured = set(config["services"])
        governed_configured = {
            record["alias"] for record in self.records if record["yaml_configured"]
        }
        governed_unconfigured = {
            record["alias"] for record in self.records if not record["yaml_configured"]
        }

        self.assertEqual(configured, EXPECTED_CONFIGURED)
        self.assertEqual(governed_configured, EXPECTED_CONFIGURED)
        self.assertEqual(len(configured), 19)
        self.assertEqual(governed_unconfigured, {"aichat", "minimax", "openai"})

    def test_runtime_architecture_is_exact(self) -> None:
        observed: dict[str, str] = {}
        for record in self.records:
            package_path = ROOT / record["package_json"]
            observed[record["alias"]] = architecture(
                load_json(package_path), package_path.parent
            )
            self.assertEqual(observed[record["alias"]], record["runtime_architecture"])

        self.assertEqual(
            {alias for alias, value in observed.items() if value == "provider"},
            EXPECTED_PROVIDER,
        )
        self.assertEqual(
            {alias for alias, value in observed.items() if value == "declarative"},
            EXPECTED_DECLARATIVE,
        )
        self.assertEqual(len(EXPECTED_PROVIDER), 18)
        self.assertEqual(len(EXPECTED_DECLARATIVE), 4)

    def test_catalog_lifecycle_and_publish_policy_are_exact(self) -> None:
        catalog = load_json(CATALOG_PATH)["services"]
        for alias, record in self.by_alias.items():
            self.assertIn(alias, catalog)
            self.assertEqual(record["lifecycle"], catalog[alias]["status"])

        retired = {
            alias
            for alias, record in self.by_alias.items()
            if record["lifecycle"] == "retired"
        }
        nonpublishable = {
            alias
            for alias, record in self.by_alias.items()
            if record["publish_policy"] == "nonpublishable"
        }
        publishable = {
            alias
            for alias, record in self.by_alias.items()
            if record["publish_policy"] == "publishable"
        }

        self.assertEqual(retired, {"sora"})
        self.assertEqual(nonpublishable, {"sora"})
        self.assertEqual(publishable, EXPECTED_ALIASES - {"sora"})

    def test_manual_and_account_management_exceptions_are_exact(self) -> None:
        manual = {
            alias
            for alias, record in self.by_alias.items()
            if record["artifact_maintenance"] == "manual"
        }
        account_management = {
            alias
            for alias, record in self.by_alias.items()
            if record["product_class"] == "account-management"
        }

        self.assertEqual(manual, EXPECTED_MANUAL)
        self.assertEqual(account_management, {"acedatacloud"})
        for alias in {"face", "fish"}:
            self.assertTrue(self.by_alias[alias]["yaml_configured"])
            self.assertEqual(
                self.by_alias[alias]["runtime_architecture"], "declarative"
            )
            self.assertEqual(self.by_alias[alias]["artifact_maintenance"], "manual")

    def test_external_legacy_aggregate_is_separate_and_owner_gated(self) -> None:
        external = self.inventory["external_legacy_aggregate"]
        self.assertEqual(external["extension_id"], "acedatacloud.acedatacloud-mcp")
        self.assertFalse(external["checked_in"])
        self.assertEqual(external["lifecycle"], "retirement-pending")
        self.assertEqual(external["product_class"], "legacy-aggregate")
        self.assertEqual(external["publish_policy"], "owner-handoff")
        self.assertNotIn(
            external["extension_id"],
            {record["extension_id"] for record in self.records},
        )


if __name__ == "__main__":
    unittest.main()
