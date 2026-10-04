import re
import unittest
from urllib.parse import parse_qs, urlsplit

from scripts.seedance_readmes import ROOT, render


class SeedanceReadmeTest(unittest.TestCase):
    def test_channels_are_distinct_and_protocol_url_is_unchanged(self):
        for source, filename in [("github", "README.md"), ("pypi", "README.pypi.md")]:
            text = render(source)
            self.assertEqual(text, (ROOT / "seedance" / filename).read_text())
            tagged = [url for url in re.findall(r"\]\((https://[^)]+)\)", text) if "utm_source=" in url]
            self.assertEqual(len(tagged), 2)
            for url in tagged:
                parsed = urlsplit(url)
                query = parse_qs(parsed.query)
                self.assertEqual(query["utm_source"], [source])
                self.assertEqual(query["utm_medium"], ["referral"])
                self.assertEqual(query["utm_campaign"], ["evergreen"])
                self.assertIn(parsed.path, ["/documents/seedance-mcp", "/console/applications"])
                self.assertEqual(len(query), 4)
            self.assertIn("https://seedance.mcp.acedata.cloud/mcp", text)
            self.assertNotIn("https://seedance.mcp.acedata.cloud/mcp?", text)
            self.assertIn("(#verify-your-first-result)", text)
            self.assertIn("### Verify your first result", text)

    def test_package_uses_the_pypi_readme(self):
        project = (ROOT / "seedance/pyproject.toml").read_text()
        self.assertIn('readme = "README.pypi.md"', project)
        self.assertIn('    "README.pypi.md",', project)
