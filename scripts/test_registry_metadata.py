import json
import unittest
from urllib.parse import parse_qs, urlsplit

from scripts.mcp_catalog import load_catalog
from scripts.registry_metadata import outputs


class RegistryMetadataTest(unittest.TestCase):
    def test_existing_entries_match_single_catalog_and_current_link_contract(self):
        catalog = load_catalog()
        for path, expected in outputs():
            with self.subTest(path=str(path)):
                actual = json.loads(path.read_text())
                self.assertEqual(actual, expected)
                self.assertNotEqual(path.parent.name, "sora")
                if path.name != "server.json":
                    profile = next(
                        item
                        for item in catalog[path.parent.name]["registry_profiles"]
                        if item["manifest"] == path.name
                    )
                    self.assertEqual(actual["title"], profile["title"])
                    self.assertNotIn("remotes", actual)
                    self.assertEqual(
                        actual["packages"][0]["packageArguments"],
                        profile["package_arguments"],
                    )
                    self.assertNotEqual(
                        actual["name"],
                        json.loads(path.with_name("server.json").read_text())["name"],
                    )
                    continue
                query = parse_qs(urlsplit(actual["websiteUrl"]).query)
                self.assertEqual(
                    set(query),
                    {"utm_source", "utm_medium", "utm_campaign", "utm_content"},
                )
                self.assertEqual(query["utm_source"], ["mcp_registry"])
                self.assertEqual(query["utm_medium"], ["referral"])
                if metadata := catalog[path.parent.name].get("registry"):
                    self.assertEqual(actual["title"], metadata["title"])
                    self.assertTrue(actual["title"].endswith(" by Ace Data Cloud"))
                    self.assertLessEqual(len(actual["description"]), 100)
                    self.assertTrue(actual["icons"][0]["src"].startswith("https://"))
