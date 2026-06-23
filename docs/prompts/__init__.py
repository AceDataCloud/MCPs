"""Prompts module for the AceDataCloud Docs MCP server."""

from core.server import mcp


@mcp.prompt()
def acedatacloud_docs_guide() -> str:
    """How to use the AceDataCloud Docs MCP to answer questions about AceData Cloud."""
    return (
        "You can answer questions about AceData Cloud (api.acedata.cloud) using these tools:\n"
        "- acedatacloud_search_docs(query): find docs by keyword — start here.\n"
        "- acedatacloud_list_docs / acedatacloud_fetch_doc(ref): browse and read full pages.\n"
        "- acedatacloud_list_services / acedatacloud_list_apis / acedatacloud_get_spec(api_path): API catalog + OpenAPI.\n"
        "- acedatacloud_list_models / acedatacloud_get_model / acedatacloud_get_pricing: model catalog + USD pricing.\n"
        "- acedatacloud_get_code_example(api_path): a runnable curl/python/js snippet.\n"
        "- acedatacloud_list_mcp_servers: AceData's other MCP servers.\n\n"
        "Prefer fetching the real spec/pricing over guessing. All data is live from the platform."
    )
