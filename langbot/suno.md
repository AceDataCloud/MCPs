<img src="https://cdn.acedata.cloud/l3ffw7.jpg" alt="Suno" width="64" height="64" />

## Suno

Create and extend songs, write lyrics, separate stems, and look up the resulting audio.

1. Sign in to [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. Copy the key from the right of the **API KEY** field and check that the application has access to Suno.

   ![API key in the General Application card](https://cdn.acedata.cloud/dvc3cg.jpg)

2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/suno). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `suno_list_models` to inspect the available models. Use `suno_get_task` with an existing task ID to retrieve the track.

Media generation uses Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/SunoMCP) · [Support](https://github.com/AceDataCloud/SunoMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
