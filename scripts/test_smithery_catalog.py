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
                service["service"],
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

    def test_current_producer_accepts_the_projected_utm_values(self):
        rules = json.loads((ROOT / "contracts/marketing-attribution.json").read_text())["contract"]
        tags = parse_qs(urlsplit(tagged_url("/console/applications")).query)
        self.assertEqual(set(tags), set(rules["utm_keys"]))
        source = tags["utm_source"][0]
        self.assertEqual(rules["sources"][source], tags["utm_medium"][0])
        self.assertTrue(all(re.fullmatch(rules["tag_pattern"], v[0]) for v in tags.values()))

    def test_config_keeps_secret_header_boundary_and_documented_limits(self):
        schema = config_schema()
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

    def test_generated_guides_use_the_canonical_direct_endpoint(self):
        for service in load_catalog()["services"]:
            folder = ROOT / service["alias"] / "smithery"
            for filename in ("README.md", "README_zh-CN.md"):
                with self.subTest(alias=service["alias"], filename=filename):
                    text = (folder / filename).read_text()
                    self.assertIn(service["endpoint"], text)
                    self.assertIn("https://smithery.ai/future", text)
                    self.assertNotIn("smithery.ai/servers/", text)
                    self.assertIn(service["task_tool"], text)

    def test_real_suno_screenshot_has_recorded_provenance(self):
        import hashlib

        folder = ROOT / "suno/smithery/assets"
        provenance = json.loads((folder / "source.json").read_text())
        image = folder / provenance["image"]
        self.assertTrue(image.read_bytes().startswith(b"\xff\xd8"))
        self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), provenance["sha256"])


if __name__ == "__main__":
    unittest.main()
