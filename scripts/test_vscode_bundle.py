import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_vscode_bundle import ROOT, bundle_services, outputs


class VscodeBundleTest(unittest.TestCase):
    def test_checked_in_outputs_match_the_source_catalog(self):
        for path, expected in outputs():
            self.assertEqual(path.read_text(), expected, str(path))
        services, _ = bundle_services()
        self.assertEqual(len({item["id"] for item in services}), len(services))
        self.assertNotIn("sora", {item["id"] for item in services})

    def make_source(
        self,
        root,
        *,
        status="active",
        url="https://suno.mcp.acedata.cloud/mcp",
        token="ACEDATACLOUD_API_TOKEN",
    ):
        (root / "scripts").mkdir()
        (root / "suno").mkdir()
        entry = {"status": status, "vscode_bundle": {"label": "Suno", "default": True}}
        (root / "scripts/mcp_catalog.json").write_text(
            json.dumps({"services": {"suno": entry}})
        )
        server = {
            "remotes": [{"type": "streamable-http", "url": url}],
            "packages": [{"environmentVariables": [{"name": token}]}],
        }
        (root / "suno/server.json").write_text(json.dumps(server))

    def test_retired_and_unverified_services_are_not_exposed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_source(root)
            path = root / "scripts/mcp_catalog.json"
            catalog = json.loads(path.read_text())
            catalog["services"]["retired"] = {
                "status": "retired",
                "vscode_bundle": {"label": "Retired"},
            }
            catalog["services"]["unverified"] = {"status": "active"}
            path.write_text(json.dumps(catalog))
            services, defaults = bundle_services(root)
            self.assertEqual([item["id"] for item in services], ["suno"])
            self.assertEqual(defaults, ["suno"])

    def test_unexpected_endpoint_cannot_receive_bundle_credentials(self):
        for url in [
            "https://example.com/mcp",
            "http://suno.mcp.acedata.cloud/mcp",
            "https://suno.mcp.acedata.cloud/mcp?token=x",
        ]:
            with self.subTest(url=url), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.make_source(root, url=url)
                with self.assertRaisesRegex(ValueError, "unexpected hosted endpoint"):
                    bundle_services(root)

    def test_account_token_cannot_be_routed_to_an_api_service(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_source(root, token="ACEDATACLOUD_PLATFORM_TOKEN")
            with self.assertRaisesRegex(ValueError, "credential contract"):
                bundle_services(root)

    def test_extension_identity_and_sync_destination(self):
        package = json.loads((ROOT / "vscode-bundle/package.json").read_text())
        self.assertEqual(package["name"], "mcp-toolbox")
        self.assertEqual(package["publisher"], "acedatacloud")
        self.assertEqual(package["displayName"], "Ace Data Cloud MCP")
        account = json.loads((ROOT / "acedatacloud/vscode/package.json").read_text())
        self.assertEqual(account["name"], "mcp-acedatacloud")
        self.assertEqual(account["displayName"], "Ace Data Cloud Account MCP")
        self.assertNotEqual(account["displayName"], package["displayName"])
        self.assertIn(
            "  vscode-bundle:\n    repo: AceDataCloud/VSCodeMCP\n",
            (ROOT / "sync.yaml").read_text(),
        )
