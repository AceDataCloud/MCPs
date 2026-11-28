<img src="https://cdn.acedata.cloud/8nxyy9.jpg" alt="Veo" width="64" height="64" />

## Veo by Ace Data Cloud

Generate video from text or reference frames, then retrieve the finished clips.

1. Sign in to [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Copy the key from the right of the **API KEY** field and check that the application has access to Veo.

   ![API key in the General Application card](https://cdn.acedata.cloud/dvc3cg.jpg)

2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/veo). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `veo_list_models` to inspect available models. Use `veo_get_task` with the original task ID to look up an existing clip.

Media generation uses Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/VeoMCP) · [Support](https://github.com/AceDataCloud/VeoMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
