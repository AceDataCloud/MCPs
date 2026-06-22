"""Prompts module for the AceData Docs MCP server."""

from core.server import mcp


@mcp.prompt()
def acedata_docs_guide() -> str:
    """How to use the AceData Docs MCP to answer questions about AceData Cloud."""
    return (
        "You can answer questions about AceData Cloud (api.acedata.cloud) using these tools:\n"
        "- acedata_search_docs(query): find docs by keyword — start here.\n"
        "- acedata_list_docs / acedata_fetch_doc(ref): browse and read full pages.\n"
        "- acedata_list_services / acedata_list_apis / acedata_get_spec(api_path): API catalog + OpenAPI.\n"
        "- acedata_list_models / acedata_get_model / acedata_get_pricing: model catalog + USD pricing.\n"
        "- acedata_get_code_example(api_path): a runnable curl/python/js snippet.\n"
        "- acedata_list_mcp_servers: AceData's other MCP servers.\n\n"
        "Prefer fetching the real spec/pricing over guessing. All data is live from the platform."
    )
