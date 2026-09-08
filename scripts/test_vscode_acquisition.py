#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

from build_vscode_extensions import (
    attributed_url,
    load_services,
    render_extension_js,
    render_readme,
)


ROOT = Path(__file__).resolve().parents[1]


def service_path(alias: str) -> Path:
    return ROOT / alias / "vscode"


class VsCodeAcquisitionTest(unittest.TestCase):
    def test_builds_path_before_query_parameters(self) -> None:
        self.assertEqual(
            attributed_url(
                "https://platform.acedata.cloud", "console/applications", "vscode-suno"
            ),
            "https://platform.acedata.cloud/console/applications?utm_source=vscode&utm_medium=extension&utm_campaign=vscode-suno",
        )

    def test_every_extension_has_an_alias_campaign(self) -> None:
        services = load_services()
        self.assertTrue(services)
        for service in services:
            campaign = f"utm_campaign=vscode-{service.alias}"
            self.assertIn(campaign, service.platform_url)
            self.assertIn(campaign, service.credential_url)

    def test_management_extension_uses_platform_token_page(self) -> None:
        service = next(item for item in load_services() if item.alias == "acedatacloud")
        self.assertIn("/console/platform-tokens?", service.credential_url)
        self.assertEqual(service.credential_hint, "Platform Tokens -> Create")

    def test_committed_extension_surfaces_match_each_campaign(self) -> None:
        for service in load_services():
            readme = (service_path(service.alias) / "README.md").read_text()
            self.assertIn(service.credential_url, readme)
            self.assertIn(service.platform_url, readme)
            extension = service_path(service.alias) / "extension.js"
            if extension.exists():
                self.assertIn(
                    f'const CREDENTIAL_URL = "{service.credential_url}";',
                    extension.read_text(),
                )
            else:
                package = (service_path(service.alias) / "package.json").read_text()
                self.assertIn(service.credential_url, package)

    def test_generated_suno_surfaces_use_valid_attributed_urls(self) -> None:
        service = next(item for item in load_services() if item.alias == "suno")
        javascript = render_extension_js(service)
        readme = render_readme(service, [])
        self.assertIn(f'const CREDENTIAL_URL = "{service.credential_url}";', javascript)
        self.assertIn(f"[Ace Data Cloud]({service.credential_url})", readme)
        self.assertIn(f"**Ace Data Cloud platform:** {service.platform_url}", readme)
        self.assertNotIn("?utm_source=vscode/console/applications", javascript + readme)


if __name__ == "__main__":
    unittest.main()
