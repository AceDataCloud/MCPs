"""Offline contracts for service-specific Glama guides and their package payload."""

import ast
import json
import re
import tomllib
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ("suno", "seedance", "happyhorse", "openai", "nanobanana")


def registered_tools(alias):
    if alias == "openai":
        tree = ast.parse((ROOT / alias / "gpt_image_tools.py").read_text())
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr != "add_tool":
                    continue
                explicit = next((value.value for value in node.keywords if value.arg == "name"), None)
                if isinstance(explicit, ast.Constant):
                    names.add(explicit.value)
                elif node.args and isinstance(node.args[0], ast.Name):
                    names.add(node.args[0].id)
        return names
    names = set()
    for path in (ROOT / alias / "tools").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
                "mcp.tool" in ast.unparse(decorator) for decorator in node.decorator_list
            ):
                names.add(node.name)
    return names


class GlamaGuideTest(unittest.TestCase):
    def test_guides_use_only_registered_service_tools(self):
        for alias in SERVICES:
            with self.subTest(service=alias):
                text = (ROOT / alias / "readme/GLAMA.md").read_text()
                prefix = "gpt_image" if alias == "openai" else alias
                names = set(re.findall(r"`(" + prefix + r"_[a-z_]+)`", text))
                self.assertTrue(names)
                self.assertLessEqual(names, registered_tools(alias))

    def test_gpt_image_is_the_exact_five_tool_package_profile(self):
        guide = (ROOT / "openai/readme/GLAMA.md").read_text()
        expected = {
            "gpt_image_generate", "gpt_image_edit", "gpt_image_get_task",
            "gpt_image_list_tasks", "gpt_image_list_models",
        }
        self.assertEqual(registered_tools("openai"), expected)
        for name in expected:
            self.assertIn(f"`{name}`", guide)
        config = json.loads(re.search(r"```json\n(.*?)```", guide, re.S)[1])
        installed = config["mcpServers"]["gpt-image-by-ace"]
        self.assertEqual(installed["command"], "uvx")
        self.assertEqual(installed["args"], ["mcp-openai-pro", "--profile", "gpt-image"])
        self.assertEqual(set(installed["env"]), {"ACEDATACLOUD_API_TOKEN"})
        self.assertNotIn("url", installed)
        self.assertIn("no separate hosted GPT Image URL", guide)
        self.assertIn("not a dedicated GPT Image install", guide)
        self.assertNotIn("`openai_generate_image`", guide)
        self.assertNotIn("`openai_list_image_models`", guide)

    def test_dedicated_glama_ctas_keep_all_four_attribution_fields(self):
        for alias in SERVICES:
            with self.subTest(service=alias):
                guide = (ROOT / alias / "readme/GLAMA.md").read_text()
                urls = re.findall(r"https://platform\.acedata\.cloud[^\s)]+", guide)
                self.assertTrue(urls)
                for url in urls:
                    query = parse_qs(urlsplit(url).query)
                    self.assertEqual(set(query), {"utm_source", "utm_medium", "utm_campaign", "utm_content"})
                    self.assertEqual(query["utm_source"], ["glama"])
                    self.assertEqual(query["utm_medium"], ["referral"])
                    self.assertEqual(query["utm_campaign"], ["evergreen"])
                    self.assertRegex(query["utm_content"][0], r"^[a-z0-9][a-z0-9_.-]{0,95}$")

    def test_package_guides_and_real_images_are_in_the_source_payload(self):
        for alias in SERVICES:
            with self.subTest(service=alias):
                folder = ROOT / alias
                project = tomllib.loads((folder / "pyproject.toml").read_text())
                include = project["tool"]["hatch"]["build"]["targets"]["sdist"]["include"]
                self.assertIn("readme/", include)
                guide = (folder / "readme/GLAMA.md").read_text()
                for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", guide):
                    if target.startswith(("https://", "http://", "#")):
                        continue
                    self.assertTrue((folder / "readme" / target.split("#", 1)[0]).exists(), target)
                provenance = json.loads((folder / "readme/glama-image-sources.json").read_text())
                image = folder / "readme/images/glama-suno-20261017.jpg"
                self.assertEqual(image.read_bytes()[:2], b"\xff\xd8")
                self.assertEqual(provenance["images"][0]["kind"], "real_page")
                self.assertIn("中文操作指南", guide)
                self.assertIn("not Glama authorization", guide)


if __name__ == "__main__":
    unittest.main()
