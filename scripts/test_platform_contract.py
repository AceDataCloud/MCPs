import ast
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "platform_contract.py"
SPEC = importlib.util.spec_from_file_location("platform_contract", SCRIPT)
assert SPEC and SPEC.loader
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class PlatformContractTests(unittest.TestCase):
    def test_published_chat_models_have_an_appropriate_mcp_tool(self) -> None:
        root = Path(__file__).resolve().parents[1]
        expected = set(json.loads((root / "scripts/fixtures/published_chat_models.json").read_text())["model_ids"])
        choices = set()
        for relative, names in (
            ("aichat/core/types.py", {"AiChatModel", "AiChatV2Model"}),
            ("aichat/core/messages_models.py", {"MessagesModel"}),
            ("openai/core/types.py", {"ChatModel", "ResponsesModel"}),
        ):
            for node in ast.parse((root / relative).read_text()).body:
                if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in names:
                    choices.update(ast.literal_eval(node.value.slice))
        self.assertFalse(expected - choices, f"Published models missing from MCP tools: {sorted(expected - choices)}")

    def test_alias_and_group_targets_are_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle = root / "bundle"
            (bundle / "services").mkdir(parents=True)
            (bundle / "manifest.json").write_text(json.dumps({"services": ["nano-banana", "openai", "unknown"]}))
            (bundle / "services/nano-banana.json").write_text(json.dumps({"targets": {"mcp": "nanobanana", "cli": "nanobanana"}, "openapi": "openapi/nano-banana.json"}))
            (bundle / "services/openai.json").write_text(json.dumps({"targets": {"mcp": "aichat", "cli": "aichat"}, "openapi": "openapi/openai.json"}))
            (bundle / "services/unknown.json").write_text(json.dumps({"targets": {}, "openapi": "openapi/unknown.json"}))
            mapping = root / "sync.yaml"
            mapping.write_text("mappings:\n  nanobanana:\n    repo: example/nano\n  aichat:\n    repo: example/chat\n")
            targets = contract.resolve_targets(bundle, mapping, "mcp", ["all"])
            self.assertEqual([item["directory"] for item in targets], ["aichat", "nanobanana"])
            self.assertEqual(targets[0]["services"], ["openai"])

    def test_unknown_requested_service_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle = root / "bundle"
            bundle.mkdir()
            (bundle / "manifest.json").write_text(json.dumps({"services": ["suno"]}))
            mapping = root / "sync.yaml"
            mapping.write_text("mappings:\n  suno:\n    repo: example/suno\n")
            with self.assertRaisesRegex(ValueError, "unknown PlatformBackend services"):
                contract.resolve_targets(bundle, mapping, "mcp", ["missing"])
