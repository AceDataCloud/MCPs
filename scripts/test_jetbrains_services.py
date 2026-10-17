"""Native service entries must be discoverable, isolated and tied to real MCP tools."""

import ast
import json
from pathlib import Path
import subprocess
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SERVICES = json.loads((ROOT / "scripts/jetbrains_services.json").read_text())[
    "services"
]


class JetBrainsServiceTest(unittest.TestCase):
    def test_generated_service_artifacts_are_current(self):
        subprocess.run(
            ["python3", "scripts/build_jetbrains_services.py", "--check"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )

    def test_top_five_keep_service_first_names_and_independent_ids(self):
        self.assertEqual(
            {s["alias"] for s in SERVICES},
            {"suno", "seedance", "nanobanana", "happyhorse", "gpt-image"},
        )
        identities = set()
        for service in SERVICES:
            root = ET.parse(
                ROOT / service["directory"] / "src/main/resources/META-INF/plugin.xml"
            ).getroot()
            self.assertEqual(root.findtext("name"), service["title"])
            self.assertTrue(service["title"].startswith(service["brand"]))
            self.assertIn("by Ace Data Cloud", service["title"])
            self.assertLessEqual(len(service["title"]), 30)
            self.assertEqual(root.findtext("id"), service["package"])
            self.assertNotIn(root.findtext("id"), identities)
            identities.add(root.findtext("id"))
            self.assertIn("not an official", root.findtext("description"))

    def test_native_buttons_call_existing_service_tools_and_task_argument(self):
        for service in SERVICES:
            source = ROOT / service["directory"].split("/")[0]
            functions = {}
            for path in (source / "tools").glob("*.py"):
                for node in ast.walk(ast.parse(path.read_text())):
                    if isinstance(node, ast.AsyncFunctionDef):
                        functions[node.name] = node
            for key in ["model_tool", "generate_tool", "task_tool"]:
                name = service[key].removeprefix("@schema:")
                self.assertIn(name, functions, (service["alias"], key))
            task = functions[service["task_tool"]]
            self.assertIn(service["task_arg"], [a.arg for a in task.args.args])
            generate = functions[service["generate_tool"]]
            self.assertIn("prompt", [a.arg for a in generate.args.args])
            self.assertIn("model", [a.arg for a in generate.args.args])

    def test_native_keys_do_not_persist_and_generation_has_an_explicit_gate(self):
        for service in SERVICES:
            directory = (
                ROOT
                / service["directory"]
                / "src/main/kotlin"
                / service["package"].replace(".", "/")
            )
            panel = (directory / "AceServicePanel.kt").read_text()
            self.assertIn("JPasswordField", panel)
            self.assertIn('apiKey.text = ""', panel)
            self.assertNotIn("PersistentStateComponent", panel)
            self.assertIn("billable = true", panel)
            self.assertIn("Submit once", panel)
            self.assertIn("model.text.isNotBlank()", panel)
            self.assertIn("No retry sent", panel)
            self.assertIn('"Existing task ID"', panel)
            configurable = (directory / (service["configurable"] + ".kt")).read_text()
            self.assertIn("AceServicePanel()", configurable)
            self.assertIn("nativePanel?.dispose()", configurable)

    def test_package_guides_have_real_sourced_images_key_flow_and_channel_tags(self):
        for service in SERVICES:
            directory = ROOT / service["directory"]
            guide = (directory / "README.md").read_text()
            for text in [
                "General application",
                "Allowed APIs",
                "current pricing",
                "Existing task ID",
                "中文上手",
                "not a screenshot of Ace connected",
                "utm_source=jetbrains_marketplace",
            ]:
                self.assertIn(text, guide, (service["alias"], text))
            for image in ["marketplace-official.png", "mcp-http-official.png"]:
                self.assertTrue(
                    (directory / "_assets" / image)
                    .read_bytes()
                    .startswith(b"\x89PNG\r\n\x1a\n")
                )
            if not service["listing"]:
                self.assertIn("not publicly approved yet", guide)
            self.assertNotIn("Free trial credit", guide)

    def test_missing_top_five_entries_have_release_jobs_with_approval_readback(self):
        for alias, directory, job in [
            ("happyhorse", "jetbrains", "publish-jetbrains"),
            ("openai", "jetbrains-gpt-image", "publish-gpt-image-jetbrains"),
        ]:
            workflow = (ROOT / alias / ".github/workflows/publish.yml").read_text()
            self.assertIn(job + ":", workflow)
            self.assertIn("working-directory: " + directory, workflow)
            self.assertIn(
                "Verify uploaded version and report approval status", workflow
            )
            self.assertIn("isBlocked", workflow)


if __name__ == "__main__":
    unittest.main()
