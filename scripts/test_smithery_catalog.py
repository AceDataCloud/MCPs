"""Keep native directory entries honest, installable, and backed by one source."""

import ast
import json
import re
import unittest
from urllib.parse import parse_qs, urlsplit

from scripts.smithery_catalog import (
    ROOT,
    config_schema,
    load_catalog,
    metadata,
    outputs,
    tagged_url,
)


class SmitheryCatalogTest(unittest.TestCase):
    def test_five_brands_keep_independent_directory_identity(self):
        services = load_catalog()["services"]
        self.assertEqual(len(services), 5)
        self.assertEqual(len({s["qualified_name"] for s in services}), 5)
        self.assertEqual(
            {s["service"] for s in services},
            {"Suno", "Seedance", "HappyHorse", "GPT Image", "Nano Banana"},
        )
        for service in services:
            self.assertEqual(
                metadata(service)["displayName"],
                service["service"] + " by Ace Data Cloud",
            )

    def test_every_entry_reuses_the_owned_package_and_endpoint(self):
        for service in load_catalog()["services"]:
            with self.subTest(alias=service["alias"]):
                server = json.loads((ROOT / service["alias"] / "server.json").read_text())
                self.assertIn(
                    service["package"],
                    [p["identifier"] for p in server["packages"]],
                )
                self.assertIn(service["endpoint"], [r["url"] for r in server["remotes"]])

    def test_current_producer_accepts_all_four_utm_values(self):
        rules = json.loads((ROOT / "contracts/marketing-attribution.json").read_text())["contract"]
        for service in load_catalog()["services"]:
            for placement in ["api_key", "pricing", "listing"]:
                url = tagged_url("/console/applications", service["alias"], placement)
                tags = parse_qs(urlsplit(url).query)
                self.assertEqual(set(tags), set(rules["utm_keys"]))
                source = tags["utm_source"][0]
                self.assertEqual(rules["sources"][source], tags["utm_medium"][0])
                self.assertIn("smithery", tags["utm_content"][0])
                self.assertTrue(
                    all(re.fullmatch(rules["tag_pattern"], v[0]) for v in tags.values())
                )

    def test_config_keeps_secret_header_boundary_and_documented_limits(self):
        for service in load_catalog()["services"]:
            schema = config_schema(service)
            self.assertLessEqual(len(json.dumps(schema).encode()), 1024)
            self.assertEqual(schema["required"], ["apiKey"])
            prop = schema["properties"]["apiKey"]
            self.assertEqual(prop["x-from"], {"header": "x-api-key"})
            self.assertEqual(prop["x-to"], {"header": "Authorization", "prefix": "Bearer "})

    def test_readonly_and_query_names_match_actual_tool_signatures(self):
        for service in load_catalog()["services"]:
            functions = {}
            for path in (ROOT / service["alias"] / "tools").glob("*.py"):
                tree = ast.parse(path.read_text())
                functions.update(
                    {
                        node.name: node
                        for node in tree.body
                        if isinstance(node, ast.AsyncFunctionDef)
                    }
                )
            with self.subTest(alias=service["alias"]):
                task = functions[service["task_tool"]]
                self.assertIn(service["task_field"], [a.arg for a in task.args.args])
                if service["read_tool"]:
                    self.assertIn(service["read_tool"], functions)
                self.assertIn(service["generation_tool"], functions)

    def test_generated_materials_preserve_candidate_and_credential_boundaries(self):
        for path, expected in outputs():
            self.assertEqual(path.read_text(), expected, str(path))
        for service in load_catalog()["services"]:
            for filename in ["README.md", "README_zh-CN.md"]:
                text = (ROOT / service["alias"] / "smithery" / filename).read_text()
                self.assertIn("General application", text)
                self.assertIn("platform-", text)
                self.assertIn("YOUR_EXISTING_TASK_ID", text)
                self.assertIn("get-api-key-en.png", text)
                self.assertIn("create-api-key-en.png", text)
                self.assertIn("AUTH_TIMEOUT", text)
                if service["status"] == "candidate":
                    self.assertTrue("candidate" in text or "候选" in text)

    def test_real_suno_screenshot_has_recorded_provenance(self):
        import hashlib

        folder = ROOT / "suno/smithery/assets"
        provenance = json.loads((folder / "source.json").read_text())
        image = folder / provenance["image"]
        self.assertTrue(image.read_bytes().startswith(b"\xff\xd8"))
        self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), provenance["sha256"])


if __name__ == "__main__":
    unittest.main()
