"""Site-admin and white-label self-service tools."""

from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json


def _body(**values: Any) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


async def _get(path: str, params: dict | None = None) -> str:
    try:
        return dumps(await client.get(path, params))
    except PlatformError as error:
        return error_json(error.code, error.message)


async def _mutate(method: str, path: str, body: dict, confirm: bool) -> str:
    if not confirm:
        return confirmation_required(f"{method} {path}", body)
    try:
        if method == "POST":
            result = await client.post(path, body)
        elif method == "PATCH":
            result = await client.patch(path, body)
        else:
            result = await client.delete(path)
        return dumps(result if result is not None else {"status": "deleted"})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_initialize_site(
    origin: Annotated[str, Field(description="Site origin URL.")],
    confirm: Annotated[bool, Field(description="Must be true to initialize.")] = False,
) -> str:
    """Resolve or initialize a site for an origin."""
    return await _mutate("POST", "/sites/initialize/", {"origin": origin}, confirm)


@mcp.tool()
async def acedatacloud_list_sites(
    limit: Annotated[int, Field(ge=1, le=100)] = 50, offset: Annotated[int, Field(ge=0)] = 0
) -> str:
    """List caller-visible sites."""
    return await _get("/sites/", {"limit": limit, "offset": offset})


@mcp.tool()
async def acedatacloud_get_site(site_id: Annotated[str, Field(description="Site UUID.")]) -> str:
    """Get one site."""
    return await _get(f"/sites/{site_id}")


@mcp.tool()
async def acedatacloud_update_site(
    site_id: Annotated[str, Field(description="Site UUID.")],
    title: Annotated[str | None, Field(description="Site title.")] = None,
    description: Annotated[str | None, Field(description="Site description.")] = None,
    branding: Annotated[dict[str, Any] | None, Field(description="Branding configuration.")] = None,
    features: Annotated[dict[str, Any] | None, Field(description="Feature configuration.")] = None,
    auth: Annotated[
        dict[str, Any] | None,
        Field(description="Authentication configuration; secrets are redacted."),
    ] = None,
    distribution: Annotated[
        dict[str, Any] | None, Field(description="Distribution configuration.")
    ] = None,
    nav: Annotated[
        dict[str, Any] | None, Field(description="Public navigation configuration.")
    ] = None,
    console_nav: Annotated[
        dict[str, Any] | None, Field(description="Console navigation configuration.")
    ] = None,
    tags: Annotated[list[str] | None, Field(description="Site tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Site metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to update.")] = False,
) -> str:
    """Patch safe site-admin configuration fields."""
    return await _mutate(
        "PATCH",
        f"/sites/{site_id}",
        _body(
            title=title,
            description=description,
            branding=branding,
            features=features,
            auth=auth,
            distribution=distribution,
            nav=nav,
            console_nav=console_nav,
            tags=tags,
            metadata=metadata,
        ),
        confirm,
    )


@mcp.tool()
async def acedatacloud_set_site_menu_translation(
    site_id: Annotated[str, Field(description="Site UUID.")],
    scope: Annotated[Literal["nav", "console_nav"], Field(description="Menu scope.")],
    custom_item_id: Annotated[str, Field(description="Custom menu item ID.")],
    enabled: Annotated[bool, Field(description="Enable auto-translation.")],
    content: Annotated[str | None, Field(description="Source text when enabling.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to update translation.")] = False,
) -> str:
    """Enable or disable translation for one custom menu item."""
    return await _mutate(
        "POST",
        f"/sites/{site_id}/menu-translations",
        _body(scope=scope, custom_item_id=custom_item_id, enabled=enabled, content=content),
        confirm,
    )


@mcp.tool()
async def acedatacloud_list_site_domains(
    site: Annotated[str | None, Field(description="Optional site UUID.")] = None,
    status: Annotated[str | None, Field(description="Optional status.")] = None,
    kind: Annotated[Literal["Page", "Api"] | None, Field(description="Page or API domain.")] = None,
) -> str:
    """List custom domains administered by the caller."""
    return await _get("/site-domains/", {"site": site, "status": status, "kind": kind})


@mcp.tool()
async def acedatacloud_get_site_domain(
    domain_id: Annotated[str, Field(description="Domain UUID.")],
) -> str:
    """Get one custom domain and DNS instructions."""
    return await _get(f"/site-domains/{domain_id}/")


@mcp.tool()
async def acedatacloud_create_site_domain(
    site: Annotated[str, Field(description="Site UUID.")],
    hostname: Annotated[str, Field(description="Custom hostname.")],
    kind: Annotated[Literal["Page", "Api"], Field(description="Domain kind.")] = "Page",
    tags: Annotated[list[str] | None, Field(description="Tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to bind domain.")] = False,
) -> str:
    """Bind a custom domain to a site."""
    return await _mutate(
        "POST",
        "/site-domains/",
        _body(site=site, hostname=hostname, kind=kind, tags=tags, metadata=metadata),
        confirm,
    )


@mcp.tool()
async def acedatacloud_update_site_domain(
    domain_id: Annotated[str, Field(description="Domain UUID.")],
    tags: Annotated[list[str] | None, Field(description="Replacement tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Replacement metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to update.")] = False,
) -> str:
    """Patch mutable custom-domain metadata; hostname and kind are immutable."""
    return await _mutate(
        "PATCH", f"/site-domains/{domain_id}/", _body(tags=tags, metadata=metadata), confirm
    )


@mcp.tool()
async def acedatacloud_delete_site_domain(
    domain_id: Annotated[str, Field(description="Domain UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to unbind.")] = False,
) -> str:
    """Unbind a custom domain."""
    return await _mutate("DELETE", f"/site-domains/{domain_id}/", {"id": domain_id}, confirm)


@mcp.tool()
async def acedatacloud_verify_site_domain(
    domain_id: Annotated[str, Field(description="Domain UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to run HTTPS probe.")] = False,
) -> str:
    """Run the end-to-end DNS/TLS/site health probe."""
    return await _mutate("POST", f"/site-domains/{domain_id}/verify/", {}, confirm)


@mcp.tool()
async def acedatacloud_check_site_domain(
    hostname: Annotated[str, Field(description="Hostname.")],
    kind: Annotated[Literal["Page", "Api"], Field(description="Domain kind.")] = "Page",
) -> str:
    """Check whether a hostname is allowed for on-demand TLS."""
    return await _get("/site-domains/check", {"hostname": hostname, "kind": kind})


@mcp.tool()
async def acedatacloud_check_frame_ancestor(
    origin: Annotated[str, Field(description="Embedding origin or referer.")],
) -> str:
    """Check whether an origin may frame the login page."""
    return await _get("/site-domains/frame-ancestors", {"origin": origin})


# Banner CRUD
@mcp.tool()
async def acedatacloud_list_site_banners(
    site: Annotated[str | None, Field(description="Optional site UUID.")] = None,
    public: Annotated[bool, Field(description="Use the public active-banner view.")] = False,
) -> str:
    return await _get("/site-banners/public/" if public else "/site-banners/", {"site": site})


@mcp.tool()
async def acedatacloud_get_site_banner(
    banner_id: Annotated[str, Field(description="Banner UUID.")],
) -> str:
    return await _get(f"/site-banners/{banner_id}/")


@mcp.tool()
async def acedatacloud_create_site_banner(
    site: Annotated[str, Field(description="Site UUID.")],
    image_url: Annotated[str | None, Field(description="Image URL.")] = None,
    link_url: Annotated[str | None, Field(description="Link URL.")] = None,
    title: Annotated[str | None, Field(description="Display title.")] = None,
    subtitle: Annotated[str | None, Field(description="Display subtitle.")] = None,
    visible: Annotated[bool, Field(description="Visibility.")] = True,
    sort_order: Annotated[int, Field(description="Sort order.")] = 0,
    start_at: Annotated[str | None, Field(description="ISO-8601 visibility start.")] = None,
    end_at: Annotated[str | None, Field(description="ISO-8601 visibility end.")] = None,
    tags: Annotated[list[str] | None, Field(description="Tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "POST",
        "/site-banners/",
        _body(
            site=site,
            image_url=image_url,
            link_url=link_url,
            title=title,
            subtitle=subtitle,
            visible=visible,
            sort_order=sort_order,
            start_at=start_at,
            end_at=end_at,
            tags=tags,
            metadata=metadata,
        ),
        confirm,
    )


@mcp.tool()
async def acedatacloud_update_site_banner(
    banner_id: Annotated[str, Field(description="Banner UUID.")],
    image_url: Annotated[str | None, Field(description="Image URL.")] = None,
    link_url: Annotated[str | None, Field(description="Link URL.")] = None,
    title: Annotated[str | None, Field(description="Display title.")] = None,
    subtitle: Annotated[str | None, Field(description="Display subtitle.")] = None,
    visible: Annotated[bool | None, Field(description="Visibility.")] = None,
    sort_order: Annotated[int | None, Field(description="Sort order.")] = None,
    start_at: Annotated[str | None, Field(description="ISO-8601 visibility start.")] = None,
    end_at: Annotated[str | None, Field(description="ISO-8601 visibility end.")] = None,
    tags: Annotated[list[str] | None, Field(description="Tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "PATCH",
        f"/site-banners/{banner_id}/",
        _body(
            image_url=image_url,
            link_url=link_url,
            title=title,
            subtitle=subtitle,
            visible=visible,
            sort_order=sort_order,
            start_at=start_at,
            end_at=end_at,
            tags=tags,
            metadata=metadata,
        ),
        confirm,
    )


@mcp.tool()
async def acedatacloud_delete_site_banner(
    banner_id: Annotated[str, Field(description="Banner UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to delete.")] = False,
) -> str:
    return await _mutate("DELETE", f"/site-banners/{banner_id}/", {"id": banner_id}, confirm)


# Typed override CRUD helpers exposed as distinct tools.
async def _list_override(base: str, site: str | None) -> str:
    return await _get(base, {"site": site})


@mcp.tool()
async def acedatacloud_list_site_capability_overrides(
    site: Annotated[str | None, Field(description="Optional site UUID.")] = None,
) -> str:
    return await _list_override("/site-capability-overrides/", site)


@mcp.tool()
async def acedatacloud_get_site_capability_override(
    override_id: Annotated[str, Field(description="Override UUID.")],
) -> str:
    return await _get(f"/site-capability-overrides/{override_id}/")


@mcp.tool()
async def acedatacloud_create_site_capability_override(
    site: Annotated[str, Field(description="Site UUID.")],
    capability: Annotated[str, Field(description="Capability key.")],
    display_name: Annotated[str | None, Field(description="Display name.")] = None,
    icon_url: Annotated[str | None, Field(description="Icon URL.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "POST",
        "/site-capability-overrides/",
        _body(site=site, capability=capability, display_name=display_name, icon_url=icon_url),
        confirm,
    )


@mcp.tool()
async def acedatacloud_update_site_capability_override(
    override_id: Annotated[str, Field(description="Override UUID.")],
    display_name: Annotated[str | None, Field(description="Display name.")] = None,
    icon_url: Annotated[str | None, Field(description="Icon URL.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "PATCH",
        f"/site-capability-overrides/{override_id}/",
        _body(display_name=display_name, icon_url=icon_url),
        confirm,
    )


@mcp.tool()
async def acedatacloud_delete_site_capability_override(
    override_id: Annotated[str, Field(description="Override UUID.")], confirm: bool = False
) -> str:
    return await _mutate(
        "DELETE", f"/site-capability-overrides/{override_id}/", {"id": override_id}, confirm
    )


@mcp.tool()
async def acedatacloud_list_site_service_overrides(
    site: Annotated[str | None, Field(description="Optional site UUID.")] = None,
) -> str:
    return await _list_override("/site-service-overrides/", site)


@mcp.tool()
async def acedatacloud_get_site_service_override(
    override_id: Annotated[str, Field(description="Override UUID.")],
) -> str:
    return await _get(f"/site-service-overrides/{override_id}/")


@mcp.tool()
async def acedatacloud_create_site_service_override(
    site: Annotated[str, Field(description="Site UUID.")],
    service: Annotated[str, Field(description="Service UUID.")],
    visible: Annotated[bool, Field(description="Visibility.")] = True,
    markup_ratio: Annotated[
        float | None, Field(description="Pricing markup ratio.", ge=0, le=5)
    ] = None,
    display_title: Annotated[str | None, Field(description="Display title.")] = None,
    display_summary: Annotated[str | None, Field(description="Display summary.")] = None,
    sort_order: Annotated[int, Field(description="Sort order.")] = 0,
    tags: Annotated[list[str] | None, Field(description="Tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "POST",
        "/site-service-overrides/",
        _body(
            site=site,
            service=service,
            visible=visible,
            markup_ratio=markup_ratio,
            display_title=display_title,
            display_summary=display_summary,
            sort_order=sort_order,
            tags=tags,
            metadata=metadata,
        ),
        confirm,
    )


@mcp.tool()
async def acedatacloud_update_site_service_override(
    override_id: Annotated[str, Field(description="Override UUID.")],
    visible: Annotated[bool | None, Field(description="Visibility.")] = None,
    markup_ratio: Annotated[
        float | None, Field(description="Pricing markup ratio.", ge=0, le=5)
    ] = None,
    display_title: Annotated[str | None, Field(description="Display title.")] = None,
    display_summary: Annotated[str | None, Field(description="Display summary.")] = None,
    sort_order: Annotated[int | None, Field(description="Sort order.")] = None,
    tags: Annotated[list[str] | None, Field(description="Tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "PATCH",
        f"/site-service-overrides/{override_id}/",
        _body(
            visible=visible,
            markup_ratio=markup_ratio,
            display_title=display_title,
            display_summary=display_summary,
            sort_order=sort_order,
            tags=tags,
            metadata=metadata,
        ),
        confirm,
    )


@mcp.tool()
async def acedatacloud_delete_site_service_override(
    override_id: Annotated[str, Field(description="Override UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to delete.")] = False,
) -> str:
    return await _mutate(
        "DELETE", f"/site-service-overrides/{override_id}/", {"id": override_id}, confirm
    )


@mcp.tool()
async def acedatacloud_list_site_document_overrides(
    site: Annotated[str | None, Field(description="Optional site UUID.")] = None,
) -> str:
    return await _list_override("/site-document-overrides/", site)


@mcp.tool()
async def acedatacloud_get_site_document_override(
    override_id: Annotated[str, Field(description="Override UUID.")],
) -> str:
    return await _get(f"/site-document-overrides/{override_id}/")


@mcp.tool()
async def acedatacloud_create_site_document_override(
    site: Annotated[str, Field(description="Site UUID.")],
    document: Annotated[str, Field(description="Document UUID.")],
    visible: Annotated[bool, Field(description="Visibility.")] = True,
    cascade: Annotated[bool, Field(description="Cascade visibility to descendants.")] = False,
    display_title: Annotated[str | None, Field(description="Display title.")] = None,
    display_summary: Annotated[str | None, Field(description="Display summary.")] = None,
    content_mode: Annotated[str, Field(description="Content mode.")] = "default",
    content_markdown: Annotated[str | None, Field(description="Override Markdown content.")] = None,
    sort_order: Annotated[int, Field(description="Sort order.")] = 0,
    tags: Annotated[list[str] | None, Field(description="Tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "POST",
        "/site-document-overrides/",
        _body(
            site=site,
            document=document,
            visible=visible,
            cascade=cascade,
            display_title=display_title,
            display_summary=display_summary,
            content_mode=content_mode,
            content_markdown=content_markdown,
            sort_order=sort_order,
            tags=tags,
            metadata=metadata,
        ),
        confirm,
    )


@mcp.tool()
async def acedatacloud_update_site_document_override(
    override_id: Annotated[str, Field(description="Override UUID.")],
    visible: Annotated[bool | None, Field(description="Visibility.")] = None,
    cascade: Annotated[bool | None, Field(description="Cascade visibility.")] = None,
    display_title: Annotated[str | None, Field(description="Display title.")] = None,
    display_summary: Annotated[str | None, Field(description="Display summary.")] = None,
    content_mode: Annotated[str | None, Field(description="Content mode.")] = None,
    content_markdown: Annotated[str | None, Field(description="Override Markdown content.")] = None,
    sort_order: Annotated[int | None, Field(description="Sort order.")] = None,
    tags: Annotated[list[str] | None, Field(description="Tags.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to execute.")] = False,
) -> str:
    return await _mutate(
        "PATCH",
        f"/site-document-overrides/{override_id}/",
        _body(
            visible=visible,
            cascade=cascade,
            display_title=display_title,
            display_summary=display_summary,
            content_mode=content_mode,
            content_markdown=content_markdown,
            sort_order=sort_order,
            tags=tags,
            metadata=metadata,
        ),
        confirm,
    )


@mcp.tool()
async def acedatacloud_delete_site_document_override(
    override_id: Annotated[str, Field(description="Override UUID.")], confirm: bool = False
) -> str:
    return await _mutate(
        "DELETE", f"/site-document-overrides/{override_id}/", {"id": override_id}, confirm
    )
