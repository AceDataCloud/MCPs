import unittest
from urllib.parse import parse_qs, urlsplit

from scripts.entry_readmes import ENTRIES, entry_url, render
from scripts.mcp_catalog import documentation_target, load_catalog


class EntryReadmeTests(unittest.TestCase):
    def test_ctas_open_existing_pages_without_an_analytics_redirect(self):
        for alias, entry in ENTRIES.items():
            canonical, _ = documentation_target(load_catalog()[alias])
            for content in ("quick_start", "api_token", "usage"):
                url = urlsplit(entry_url(alias, content))
                expected = "https://platform.acedata.cloud/console/applications" if content == "api_token" else canonical
                self.assertEqual(url.scheme + "://" + url.netloc + url.path, expected)
                self.assertNotIn("/api/", url.path)
                self.assertEqual(parse_qs(url.query), {
                    "utm_source": [entry[0].lower()], "utm_medium": ["readme"],
                    "utm_campaign": ["opensource_activation"], "utm_content": [content],
                })

    def test_example_anchor_is_local_and_markdown_is_not_backslash_escaped(self):
        for alias in ENTRIES:
            content = render(alias)
            self.assertIn("[Example prompt](#verify-your-first-result)", content)
            self.assertIn("### Verify your first result", content)
            self.assertNotIn("]\\(", content)
            self.assertNotIn("https\\://", content)
            self.assertNotIn("marketing-attribution/entry/", content)
