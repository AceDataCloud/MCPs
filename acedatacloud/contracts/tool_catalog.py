"""Curated discovery policy, independent of the complete API coverage ledger."""

import re
from dataclasses import dataclass
from typing import Literal

from contracts.management_surface import SURFACE_TOOLS
from contracts.platform_operations import OPERATIONS, Operation

INFO_TOOL = "acedatacloud_get_usage_guide"
ToolProfile = Literal["curated", "full"]
Audience = Literal["public", "account", "workspace", "admin"]

CATEGORIES = {
    "Account & API keys": {"Account", "Credentials", "Platform Tokens"},
    "Catalog & documentation": {
        "Catalog",
        "Documentation",
        "Models",
        "Services",
        "Apis",
        "Datasets",
        "Documents",
        "Integrations",
        "Search",
        "App Version",
        "Config",
    },
    "Applications & deployments": {"Applications"},
    "Usage & billing": {
        "Usage",
        "Orders",
        "Invoices",
        "Billing Profiles",
        "Auto Recharge",
        "Auto Recharge Configs",
        "Recharge Cards",
        "Order Discounts",
    },
    "Sites & branding": {
        "Sites",
        "Site Domains",
        "Site Banners",
        "Site Home Sections",
        "Logo Assets",
        "Site Capability Overrides",
        "Site Service Overrides",
        "Site Document Overrides",
    },
    "Community & wallet": {
        "Distribution",
        "Distribution Histories",
        "Distribution Statuses",
        "Distribution Redemptions",
        "Distribution Levels",
        "Coin",
        "Coin Infos",
        "Coin Wallet",
        "Coin Policies",
        "Surveys",
        "Translation",
        "Translations",
        "Preferences",
        "Content Reports",
        "Reports",
    },
    "Content & announcements": {"Blog", "Blogs", "Announcements", "Admin", "Showcases"},
    "Email marketing & analytics": {"Email Marketing", "Marketing Attribution", "Attribution"},
    "Access control & automation": {
        "Access Requests",
        "Access Grants",
        "Access Policies",
        "Api Request Access",
        "Feature Flags",
        "Webhooks",
        "Webhook Subscriptions",
    },
    "Payment authorization": {"X402"},
    "Administration & risk": {"Administration", "Distribution Risk", "Payment Risk Holds"},
    "Files & utilities": {"Files", "Utils"},
}

ADMIN_PERMISSIONS = {
    "access-control",
    "ace-snapshot",
    "distribution-risk",
    "email-marketing",
    "feature-flags",
    "marketing-attribution",
    "provider-routing",
    "revenue",
    "content-reports",
    "surveys",
}

CROSS_ACCOUNT_TOOLS = {
    "acedatacloud_list_applications_detail": "applications:read:any",
    "acedatacloud_list_credentials_detail": "credentials:write:any",
    "acedatacloud_list_orders_detail": "orders:read:any",
    "acedatacloud_list_usage_apis": "usage:read:any",
    "acedatacloud_list_usage_proxies": "usage:read:any",
    "acedatacloud_list_distribution_statuses": "distribution:read:any",
}

PREFERRED_READS = {
    "acedatacloud_get_services_lookup_value": "acedatacloud_get_service",
    "acedatacloud_get_documents_lookup_value": "acedatacloud_get_doc",
    "acedatacloud_get_models_slug": "acedatacloud_get_model",
    "acedatacloud_get_models_introduction": "acedatacloud_get_model",
}

CLIENT_HELPERS = {
    "acedatacloud_get_config",
    "acedatacloud_get_app_version",
    "acedatacloud_create_utils_share_images",
    "acedatacloud_create_logo_assets_analyze",
    "acedatacloud_create_logo_assets_process",
    "acedatacloud_check_site_domain",
    "acedatacloud_check_frame_ancestor",
    "acedatacloud_create_attribution_resolve",
    "acedatacloud_get_attribution_landing_inviter_id",
    "acedatacloud_create_announcements_read_all",
    "acedatacloud_create_announcements_read",
    "acedatacloud_get_announcements_unread_count",
    "acedatacloud_get_distribution_risk",
    "acedatacloud_get_distribution_risk_format",
    "acedatacloud_get_x402_solana_latest_blockhash",
    "acedatacloud_verify_apple_order",
}


@dataclass(frozen=True)
class CatalogEntry:
    """An audited tool's discovery category, audience and suppression rationale."""

    category: str
    audience: Audience
    required_permissions: tuple[str, ...]
    advertised: bool = True
    reason: str = "business operation"
    replacement: str | None = None


def _route(path: str) -> str:
    return re.sub(r"\{[^{}]+\}", "{}", path.rstrip("/"))


def _audience(operation: Operation, permissions: tuple[str, ...]) -> Audience:
    if operation.authentication == "public":
        return "public"
    if any(
        permission.endswith(":any") or permission.split(":")[0] in ADMIN_PERMISSIONS
        for permission in permissions
    ):
        return "admin"
    if any(
        permission.startswith(("sites:", "blog:", "announcements:", "webhooks:"))
        for permission in permissions
    ):
        return "workspace"
    return "account"


def build_catalog() -> dict[str, CatalogEntry]:
    """Prefer task-oriented native tools without discarding legacy implementations."""
    generated = {spec["name"] for spec in SURFACE_TOOLS}
    operations = {operation.tool: operation for operation in OPERATIONS if operation.tool}
    helper_routes = {
        (operation.method, _route(operation.path))
        for operation in OPERATIONS
        if operation.tool in CLIENT_HELPERS
    }
    native_routes: dict[tuple[str, str], str] = {}
    for operation in OPERATIONS:
        if operation.tool and operation.tool not in generated:
            native_routes.setdefault((operation.method, _route(operation.path)), operation.tool)
    patch_routes = {
        _route(operation.path): operation.tool
        for operation in OPERATIONS
        if operation.tool and operation.method == "PATCH"
    }
    patch_routes.update(
        {path: name for (method, path), name in native_routes.items() if method == "PATCH"}
    )
    catalog = {}
    for name, operation in operations.items():
        category = next(
            title for title, domains in CATEGORIES.items() if operation.domain in domains
        )
        permissions = operation.required_permissions
        if name in CROSS_ACCOUNT_TOOLS:
            permissions = (*permissions, CROSS_ACCOUNT_TOOLS[name])
        advertised = True
        reason = "business operation"
        replacement = None
        if name in CLIENT_HELPERS or (operation.method, _route(operation.path)) in helper_routes:
            advertised, reason = False, "client rendering, telemetry or protocol helper"
        elif name in PREFERRED_READS:
            advertised, reason = False, "prefer the task-oriented catalog reader"
            replacement = PREFERRED_READS[name]
        elif name in generated and name not in CROSS_ACCOUNT_TOOLS:
            replacement = native_routes.get((operation.method, _route(operation.path)))
            if replacement:
                advertised, reason = False, "duplicate native route"
            elif operation.method == "PUT" and _route(operation.path) in patch_routes:
                advertised, reason = False, "alternate full-replacement update"
                replacement = patch_routes[_route(operation.path)]
        catalog[name] = CatalogEntry(
            category,
            _audience(operation, permissions),
            permissions,
            advertised,
            reason,
            replacement,
        )
    return catalog


TOOL_CATALOG = build_catalog()


def advertised_tools(profile: ToolProfile = "curated") -> set[str]:
    """Return discoverable names; the full profile still requires account permissions."""
    return {
        name for name, entry in TOOL_CATALOG.items() if profile == "full" or entry.advertised
    } | {INFO_TOOL}
