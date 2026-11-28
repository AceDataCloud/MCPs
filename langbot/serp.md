<img src="https://cdn.acedata.cloud/27e11e555d.png" alt="Google Search" width="64" height="64" />

## Google Search

Search the web, images, news, videos, maps, and places with country and language controls.

1. Open [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen) and copy an application API key with access to Google Search.
2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/serp). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `serp_list_countries` and `serp_list_languages` to see the supported settings. Use them with `serp_google_search` when ready to run a billable web search.

Search requests use Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/SerpMCP) · [Support](https://github.com/AceDataCloud/SerpMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
