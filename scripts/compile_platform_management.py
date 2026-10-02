import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=Path, required=True)
parser.add_argument("--backend", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1] / "acedatacloud"
sys.path.insert(0, str(root))
from contracts.platform_operations import OPERATIONS


def norm(path):
    path = re.sub(r"\(\?P<(\w+)>[^)]+\)", r"{\1}", path)
    path = re.sub(r"<(?:\w+:)?(\w+)>", r"{\1}", path)
    return re.sub(r"\{(?:pk|id)\}", "{id}", path.replace("^", "").replace("$", "").strip("/"))


covered = {
    (o.method, norm(o.path)): o
    for o in OPERATIONS
    if o.coverage in {"covered", "shared"} and not o.operation_id.startswith("surface.")
}
rows = json.loads(args.input.read_text())
seen = set()
specs = []
inventory = []
expected = set()
names = {o.tool for o in OPERATIONS if o.tool and not o.operation_id.startswith("surface.")}
exclude_prefixes = {
    "applications/{id}/appliance-request": "Generic appliance reverse proxy bypasses typed management boundaries; use workload-specific tools.",
    "browser-transfers/": "Device-transfer protocol requires browser capability grants, not a standalone account API.",
    "og/": "Rendered website image, not a platform management operation.",
    "site-assets/": "Website asset delivery, not a management operation.",
    "site-head/": "Website HTML bootstrap, not a management operation.",
    "status-page/snapshot": "Service-internal authentication; platform credentials cannot call this endpoint.",
    "credentials/agent/": "Agent bootstrap protocol uses its own identity and signing contract.",
    "email-marketing/events/tencent/": "Provider callback, not a caller-driven management tool.",
    "email-marketing/unsubscribe/": "Tokenized website unsubscribe flow; authenticated email preference tools cover this capability.",
    "invoices/provider/callback": "Provider callback, not a user operation.",
    "invoices/stripe/webhook": "Provider callback, not a user operation.",
    "invoices/{id}/public-upload": "Tokenized public upload flow; authenticated admin invoice upload tools cover this capability.",
    "x402/demo": "Interactive payment demonstration, not an account control operation.",
}


def clean_schema(schema, partial=False):
    if not schema:
        return {"type": "object", "properties": {}}
    schema = json.loads(json.dumps(schema))
    props = schema.get("properties", {})
    props = {k: v for k, v in props.items() if not v.get("readOnly")}
    for v in props.values():
        v.pop("readOnly", None)
        if v.get("type") == "array":
            v.setdefault("items", {})
    schema["properties"] = props
    schema["required"] = [] if partial else [n for n in schema.get("required", []) if n in props]
    schema["additionalProperties"] = False
    return schema


for row in rows:
    if not row.get("method") or "(?P<format>" in row["path"]:
        continue
    route = norm(row["path"])
    method = row["method"]
    key = method, route
    if key in seen:
        continue
    seen.add(key)
    variants = [row]
    if row.get("action_choices") and ("{action}" in route or "{action_name}" in route):
        variants = []
        for action in row["action_choices"]:
            clone = dict(row)
            clone["fixed_action"] = action
            variants.append(clone)
    for row in variants:
        actual = route
        if row.get("fixed_action"):
            actual = actual.replace("{action}", row["fixed_action"]).replace(
                "{action_name}", row["fixed_action"]
            )
        key = method, actual
        expected.add(key)
        rec = {
            "method": method,
            "path": "/" + actual + ("/" if row["path"].endswith(("/", "$")) else ""),
            "handler": row["class"],
        }
        reason = next((v for k, v in exclude_prefixes.items() if actual.startswith(k)), None)
        if "/webhook" in actual and actual.startswith(("orders/", "invoices/")):
            reason = "Provider callback, not a caller-driven management tool."
        if row.get("unsupported"):
            reason = "The backend deliberately rejects this HTTP method with 405."
        if reason:
            rec.update(coverage="excluded", rationale=reason)
            inventory.append(rec)
            continue
        auth = (
            "public"
            if not row["permissions"] or row["permissions"] == ["AllowAny"]
            else "authenticated"
        )
        scope = row.get("scope")
        if row.get("fixed_action") and actual.startswith("email-marketing/admin/campaigns/"):
            scope = (
                "email-marketing:write"
                if row["fixed_action"]
                in {
                    "preview-audience",
                    "create-carryover",
                    "prepare",
                    "prepare-carryover",
                    "revise",
                }
                else "email-marketing:send"
            )
        if actual.startswith("announcements/admin"):
            scope = "announcements:read" if method == "GET" else "announcements:write"
        if actual.startswith(("sites", "site-")) and auth != "public":
            scope = "sites:read" if method == "GET" else "sites:write"
        if actual.startswith("recharge-cards/") and not scope:
            scope = "applications:write" if method != "GET" else "applications:read"
        if actual.startswith("x402/") and not scope:
            scope = "coin:write" if method != "GET" else "coin:read"
        body = clean_schema(row.get("body"), method == "PATCH")
        queries = dict(row.get("queries") or {})
        if method == "GET":
            filters = row.get("filters") or []
            if isinstance(filters, dict):
                filters = list(filters)
            for f in filters:
                queries.setdefault(f, {"type": "string"})
            queries.update(
                limit={"type": "integer", "minimum": 1, "maximum": 100},
                offset={"type": "integer", "minimum": 0},
            )
            if row.get("ordering"):
                queries.setdefault("ordering", {"type": "string"})
        parameters = re.findall(r"\{(\w+)\}", actual)
        for p in parameters:
            queries.pop(p, None)
        static = re.sub(r"\{\w+\}", "", actual).replace("-", "_")
        static = re.sub("_+", "_", static.replace("/", "_")).strip("_")
        verb = {
            "GET": "get",
            "POST": "create",
            "PUT": "replace",
            "PATCH": "update",
            "DELETE": "delete",
        }[method]
        if method == "GET" and (row.get("action") == "list" or "List" in row["class"]):
            verb = "list"
        if method == "POST" and row.get("fixed_action"):
            verb = "run"
        if parameters and actual.endswith("}"):
            static += "_" + parameters[-1]
        static = (
            static.replace("email_marketing_admin_", "email_")
            .replace("auto_recharge_configs_admin_card_fingerprints_", "card_fingerprints_")
            .replace("admin_upstreams_", "configuration_")
            .replace("x402_payment_authorization_transaction_", "x402_transaction_")
            .replace("distribution_risk_histories_", "distribution_cases_")
            .replace("configuration_providers_capabilities_", "configuration_capabilities_")
        )
        name = "acedatacloud_" + verb + "_" + static
        if name in names:
            name += "_detail" if method == "GET" else "_record"
        if name in names:
            raise RuntimeError(name)
        names.add(name)
        domain = actual.split("/")[0].replace("-", " ").title()
        if actual.startswith("admin/"):
            domain = "Administration"
        required = [scope] if scope else []
        confirm = method != "GET" or scope == "webhooks:reveal"
        disclosure = ["/value"] if scope == "webhooks:reveal" else []
        if method == "POST" and actual in {"credentials", "platform-tokens"}:
            disclosure = ["/token"]
        if actual.endswith("/pay") and method == "POST":
            disclosure = ["/pay_url"]
        if actual.endswith("/setup/") or actual.endswith("/setup"):
            disclosure = ["/setup_token"]
        spec = {
            "operation_id": "surface." + name.removeprefix("acedatacloud_"),
            "name": name,
            "method": method,
            "path": rec["path"],
            "domain": domain,
            "authentication": auth,
            "required_permissions": required,
            "confirm": confirm,
            "path_parameters": parameters,
            "query_schema": {
                "type": "object",
                "properties": queries,
                "additionalProperties": False,
            },
            "body_schema": body,
            "description": verb.capitalize()
            + " "
            + static.replace("_", " ")
            + ". Backend account permissions and ownership checks apply.",
            "disclose": disclosure,
        }
        if (
            actual == "files"
            or actual.startswith("logo-assets/")
            or actual == "invoices/admin/{id}/file"
        ):
            spec["encoding"] = "multipart"
            spec["body_schema"] = {
                "type": "object",
                "properties": {
                    **body["properties"],
                    "filename": {"type": "string"},
                    "content_base64": {"type": "string"},
                    "content_type": {"type": "string"},
                },
                "required": ["filename", "content_base64"],
                "additionalProperties": False,
            }
        if actual == "recharge-cards/allocations" and method == "POST" and not body["properties"]:
            raise RuntimeError("Allocation body missing")
        specs.append(spec)
        rec.update(coverage="covered", tool=name)
        inventory.append(rec)

recorded = {(row["method"], norm(row["path"])) for row in inventory}
if recorded != expected:
    raise RuntimeError(f"Incomplete route ledger: {sorted(expected - recorded)}")

source = args.backend.resolve()
sha = subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=source, text=True).strip()
output = {
    "source_repository": "AceDataCloud/PlatformBackend",
    "source_sha": sha,
    "operations": inventory,
    "tools": specs,
}
(root / "contracts/management_surface.json").write_text(
    json.dumps(output, indent=2, ensure_ascii=False) + "\n"
)
print(
    "Surface operations:",
    len(inventory),
    "new tools:",
    len(specs),
    "excluded:",
    sum(r["coverage"] == "excluded" for r in inventory),
)
print(collections.Counter(s["domain"] for s in specs))
print(
    "Writes without body:",
    [
        (s["name"], s["path"])
        for s in specs
        if s["method"] in ("POST", "PUT", "PATCH") and not s["body_schema"]["properties"]
    ],
)
