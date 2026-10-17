"""The five independent service cards must remain installable from one source."""

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location(
    "vscode_codegen", ROOT / "scripts/build_vscode_extensions.py"
)
codegen = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = codegen
spec.loader.exec_module(codegen)


class BrandPackagesTest(unittest.TestCase):
    def test_five_packages_use_unique_stable_runtime_and_branded_identities(self):
        ids = set()
        for svc in codegen.load_services():
            if svc.alias not in codegen.BRAND_TOOLS:
                continue
            with self.subTest(service=svc.alias):
                directory = ROOT / svc.alias / "vscode"
                pkg = json.loads((directory / "package.json").read_text())
                self.assertNotIn(pkg["name"], ids)
                ids.add(pkg["name"])
                self.assertEqual(pkg["publisher"], "acedatacloud")
                self.assertIn("by Ace Data Cloud", pkg["displayName"])
                self.assertLessEqual(len(pkg["keywords"]), 30)
                self.assertEqual(pkg["engines"]["vscode"], "^1.101.0")
                self.assertNotIn("mcpServers", pkg["contributes"])
                self.assertTrue(codegen.extract_tools(ROOT / svc.alias / "README.md"))
                self.assertEqual(
                    pkg["contributes"]["mcpServerDefinitionProviders"][0]["id"],
                    svc.provider_id,
                )
                self.assertEqual(
                    (directory / "extension.js").read_text(),
                    codegen.render_extension_js(svc),
                )
                self.assertEqual(
                    (directory / "README.md").read_text(),
                    codegen.render_readme(
                        svc, codegen.extract_tools(ROOT / svc.alias / "README.md")
                    ),
                )
                self.assertEqual(
                    (directory / "README.zh-CN.md").read_text(),
                    codegen.render_chinese_readme(svc),
                )
                self.assertTrue((directory / "icon.png").is_file())
                self.assertTrue((directory / "LICENSE").is_file())
                if svc.alias == "openai":
                    text = (directory / "README.md").read_text()
                    self.assertIn("does not filter its schema", text)
                    self.assertIn("| `openai_get_task` |", text)
                    self.assertNotIn("**11 tools** available", text)
                for filename in ["README.md", "README.zh-CN.md"]:
                    text = (directory / filename).read_text()
                    self.assertIn("SecretStorage", text)
                    self.assertIn("TASK_ID", text)
                    self.assertIn("2026-10-09", text)
                    self.assertIn("/assets/tutorial/04-tools.png", text)
                    self.assertIn("utm_source=vscode_marketplace", text)
                tags = parse_qs(urlsplit(svc.credential_url).query)
                self.assertEqual(tags["utm_source"], ["vscode"])
        self.assertEqual(len(ids), 5)
        self.assertIn("mcp-gpt-image", ids)
        self.assertIn("mcp-happyhorse", ids)

    def test_workflow_has_no_duplicate_yaml_keys(self):
        import yaml

        class UniqueLoader(yaml.SafeLoader):
            pass

        def unique_mapping(loader, node, deep=False):
            result = {}
            for key, value in node.value:
                name = loader.construct_object(key, deep=deep)
                if name in result:
                    raise ValueError("Duplicate YAML key: " + str(name))
                result[name] = loader.construct_object(value, deep=deep)
            return result

        UniqueLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
        )
        for filename in [
            ".github/workflows/ci.yaml",
            "vscode-bundle/.github/workflows/publish-service-extensions.yml",
        ]:
            yaml.load((ROOT / filename).read_text(), Loader=UniqueLoader)

    def test_publisher_checks_out_main_and_reuses_existing_credential(self):
        workflow = (
            ROOT / "vscode-bundle/.github/workflows/publish-service-extensions.yml"
        ).read_text()
        self.assertIn("github.ref == 'refs/heads/main'", workflow)
        self.assertIn("repository: AceDataCloud/MCPs", workflow)
        self.assertIn("secrets.VSCE_PAT", workflow)
        self.assertNotIn("inputs.repository", workflow)
        self.assertNotIn("inputs.ref", workflow)


if __name__ == "__main__":
    unittest.main()
