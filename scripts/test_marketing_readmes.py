import json
import re
import tomllib
import unittest
from urllib.parse import parse_qs, urlsplit

from scripts.marketing_readmes import ROOT, contract, outputs, render, tagged_url
from scripts.mcp_catalog import load_catalog


class MarketingReadmeTest(unittest.TestCase):
    def test_all_active_packages_and_marketplaces_are_generated(self):
        paths = set()
        for path, expected in outputs():
            self.assertEqual(path.read_text(), expected, str(path))
            paths.add(path.relative_to(ROOT).as_posix())
        for alias, item in load_catalog().items():
            if item["status"] != "active":
                self.assertNotIn(f"{alias}/README.pypi.md", paths)
                continue
            self.assertIn(f"{alias}/README.pypi.md", paths)
            project = (ROOT / alias / "pyproject.toml").read_text()
            self.assertIn('readme = "README.pypi.md"', project)
            self.assertIn(
                "README.pypi.md",
                tomllib.loads(project)["tool"]["hatch"]["build"]["targets"]["sdist"][
                    "include"
                ],
            )
            for source, file in [
                ("github", "README.md"),
                ("pypi", "README.pypi.md"),
                ("vscode_marketplace", "vscode/README.md"),
                ("jetbrains_marketplace", "jetbrains/README.md"),
            ]:
                path = ROOT / alias / file
                if not path.exists():
                    continue
                text = path.read_text()
                tagged = re.findall(
                    r"\]\((https://platform\.acedata\.cloud[^)]+)\)", text
                )
                self.assertTrue(tagged, str(path))
                for url in tagged:
                    query = parse_qs(urlsplit(url).query)
                    self.assertEqual(query["utm_source"], [source], url)
                    self.assertEqual(query["utm_medium"], ["referral"], url)
                    self.assertEqual(query["utm_campaign"], ["evergreen"], url)
                    self.assertLessEqual(len(query["utm_content"][0]), 96)

    def test_code_protocols_and_retired_packages_are_untouched(self):
        sample = '```json\n{"base_url": "https://platform.acedata.cloud"}\n```\n`[config](https://platform.acedata.cloud)`\n[mcp](https://suno.mcp.acedata.cloud/mcp)\n[API](https://platform.acedata.cloud/api/v1/users/)\n'
        self.assertEqual(render(sample, "suno", "github"), sample)
        self.assertEqual(
            render("[setup](https://platform.acedata.cloud)", "sora", "github"),
            "[setup](https://platform.acedata.cloud)",
        )

    def test_existing_parameters_and_fragments_survive_without_duplicate_tags(self):
        url = "https://platform.acedata.cloud/console/applications?tab=key&utm_source=old#new"
        result = tagged_url(url, "suno", "pypi", contract(), load_catalog())
        self.assertEqual(
            parse_qs(urlsplit(result).query),
            {
                "tab": ["key"],
                "utm_source": ["pypi"],
                "utm_medium": ["referral"],
                "utm_campaign": ["evergreen"],
                "utm_content": ["suno_mcp_package_api_key"],
            },
        )
        self.assertEqual(urlsplit(result).fragment, "new")
        self.assertEqual(
            tagged_url(result, "suno", "pypi", contract(), load_catalog()), result
        )

    def test_seedance_setup_anchor_and_protocol_stay_valid(self):
        text = (ROOT / "seedance/README.md").read_text()
        self.assertIn("(#verify-your-first-result)", text)
        self.assertIn("### Verify your first result", text)
        self.assertIn("https://seedance.mcp.acedata.cloud/mcp", text)
        self.assertNotIn("https://seedance.mcp.acedata.cloud/mcp?", text)

    def test_remote_client_setup_examples_use_safe_client_settings(self):
        for alias, item in load_catalog().items():
            if item["status"] != "active":
                continue
            text = (ROOT / alias / "README.md").read_text()
            for title, root_key, transport in [
                ("Claude Code", "mcpServers", "http"),
                ("Cline", "mcpServers", "streamableHttp"),
                ("VS Code (Copilot)", "servers", "http"),
            ]:
                marker = f"#### {title}\n"
                if alias == "suno":
                    # Suno documents OAuth URL-only setup and API-token setup
                    # in separate sections. Validate those paths below.
                    continue
                if marker not in text:
                    continue
                section = text.split(marker, 1)[1].split("\n#### ", 1)[0]
                snippets = re.findall(r"```json\n(.*?)\n```", section, re.DOTALL)
                with self.subTest(alias=alias, client=title):
                    self.assertEqual(len(snippets), 1)
                    server = json.loads(snippets[0])[root_key][alias]
                    self.assertEqual(server["type"], transport)
                    self.assertEqual(
                        server["url"], f"https://{alias}.mcp.acedata.cloud/mcp"
                    )
                    if title == "Claude Code":
                        self.assertEqual(
                            server["headers"]["Authorization"],
                            "Bearer ${ACEDATACLOUD_API_TOKEN}",
                        )
                        self.assertIn("--scope user", section)
                        self.assertIn(
                            "--header 'Authorization: Bearer ${ACEDATACLOUD_API_TOKEN}'",
                            section,
                        )
                        self.assertIn("$env:ACEDATACLOUD_API_TOKEN", section)
                        self.assertIn("Run `/mcp`", section)
                    elif title == "Cline":
                        self.assertIn("~/.cline/mcp.json", section)
                        self.assertNotIn(".cline/mcp_settings.json", section)
                        self.assertEqual(server["autoApprove"], [])
                        self.assertIs(server["disabled"], False)
                        self.assertIn("do not commit or share", section)
                    else:
                        self.assertIn("MCP: Open User Configuration", section)
                        self.assertIn("MCP: List Servers", section)
                        self.assertNotIn(".vscode/mcp.json", section)
                        self.assertIn("out of version control", section)


    def test_suno_auth_routes_and_client_configs(self):
        text = (ROOT / "suno/README.md").read_text()
        self.assertIn("DCR is client registration", text)
        self.assertIn("Claude Desktop's `claude_desktop_config.json` is for **local**", text)
        self.assertIn("codex mcp login suno", text)
        self.assertIn("~/.cursor/mcp.json", text)
        self.assertIn("MCP: Open User Configuration", text)
        self.assertIn("~/.cline/data/settings/cline_mcp_settings.json", text)
        self.assertIn("`suno_list_models` and `suno_list_actions` return static reference data", text)

        snippets = [json.loads(block) for block in re.findall(r"```json\n(.*?)\n```", text, re.DOTALL)]
        self.assertEqual(len(snippets), 6)
        url = "https://suno.mcp.acedata.cloud/mcp"
        cursor_oauth = snippets[0]["mcpServers"]["suno"]
        vscode_oauth = snippets[1]["servers"]["suno"]
        claude_key = snippets[2]["mcpServers"]["suno"]
        cursor_key = snippets[3]["mcpServers"]["suno"]
        vscode_key = snippets[4]["servers"]["suno"]
        local = snippets[5]["mcpServers"]["suno"]
        self.assertEqual(cursor_oauth, {"url": url})
        self.assertEqual(vscode_oauth, {"type": "http", "url": url})
        self.assertEqual(claude_key["headers"]["Authorization"], "Bearer ${ACEDATACLOUD_API_TOKEN}")
        self.assertEqual(cursor_key["headers"]["Authorization"], "Bearer ${env:ACEDATACLOUD_API_TOKEN}")
        self.assertEqual(vscode_key["headers"]["Authorization"], "Bearer ${input:acedata-suno-token}")
        self.assertEqual(local["command"], "uvx")
        self.assertEqual(local["args"], ["mcp-suno"])

    def test_generation_is_idempotent(self):
        for alias, item in load_catalog().items():
            if item["status"] == "active":
                text = (ROOT / alias / "README.md").read_text()
                self.assertEqual(
                    render(render(text, alias, "github"), alias, "github"), text
                )
