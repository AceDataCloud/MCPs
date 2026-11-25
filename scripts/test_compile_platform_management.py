import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compile_platform_management.py"
SURFACE = ROOT / "acedatacloud/contracts/management_surface.json"
MODEL_PATH = "admin/upstreams/{domain}/models"


class ScopedManagementCompilationTests(unittest.TestCase):
    def compile(self, directory, *paths):
        export = directory / "export.json"
        export.write_text(json.dumps([{
            "path": "admin/upstreams/<str:domain>/models/",
            "method": "GET",
            "class": "UpstreamModelListView",
            "scope": "provider-routing:read",
            "permissions": ["IsAuthenticated", "HasPermission"],
            "queries": {"q": {"type": "string"}, "status": {"type": "string"}, "provider": {"type": "string"}},
        }]))
        output = directory / "surface.json"
        result = subprocess.run([
            sys.executable, str(SCRIPT), "--input", str(export), "--backend", str(ROOT),
            "--source-sha", "HEAD", "--output", str(output), "--paths", *paths,
        ], capture_output=True, text=True)
        return result, output

    def test_scoped_refresh_preserves_unrelated_contracts_and_records_provenance(self):
        previous = json.loads(SURFACE.read_text())
        with tempfile.TemporaryDirectory() as temporary:
            result, output = self.compile(Path(temporary), MODEL_PATH)
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = json.loads(output.read_text())
        self.assertEqual(updated["source_sha"], previous["source_sha"])
        for section in ("operations", "tools"):
            self.assertEqual(len(updated[section]), len(previous[section]))
            self.assertEqual(
                [row for row in updated[section] if row["path"].strip("/") != MODEL_PATH],
                [row for row in previous[section] if row["path"].strip("/") != MODEL_PATH],
            )
        canonical = next(row for row in updated["tools"] if row["path"].strip("/") == MODEL_PATH)
        self.assertEqual(canonical["name"], "acedatacloud_list_configuration_models")
        self.assertEqual(canonical["required_permissions"], ["provider-routing:read"])
        self.assertTrue({"q", "status", "provider"} <= canonical["query_schema"]["properties"].keys())
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        self.assertEqual(updated["source_overrides"][MODEL_PATH], sha)

    def test_unknown_route_does_not_write_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            result, output = self.compile(Path(temporary), "missing/route")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unknown routes", result.stderr)
            self.assertFalse(output.exists())

    def test_scoped_refresh_removes_retired_routes_without_touching_other_contracts(self):
        previous = json.loads(SURFACE.read_text())
        retired_path = "admin/upstreams/{domain}/providers"
        self.assertTrue(any(row["path"].strip("/") == retired_path for row in previous["tools"]))
        with tempfile.TemporaryDirectory() as temporary:
            result, output = self.compile(Path(temporary), MODEL_PATH, retired_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = json.loads(output.read_text())
        for section in ("operations", "tools"):
            self.assertFalse(any(row["path"].strip("/") == retired_path for row in updated[section]))
            self.assertEqual(
                [row for row in updated[section] if row["path"].strip("/") != MODEL_PATH],
                [row for row in previous[section] if row["path"].strip("/") not in {MODEL_PATH, retired_path}],
            )
        self.assertNotIn(retired_path, updated["source_overrides"])
        self.assertIn(MODEL_PATH, updated["source_overrides"])


if __name__ == "__main__":
    unittest.main()
