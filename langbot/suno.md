<img src="https://cdn.acedata.cloud/l3ffw7.jpg" alt="Suno" width="64" height="64" />

## Suno by Ace Data Cloud

Create and extend songs, write lyrics, separate stems, and look up the resulting audio.

1. Open [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen). Sign in and open **General Application**. Select **Initialize General Application** if it is missing. Click the copy button marked **1** beside **API KEY**. Verify that the application can access the service.

   ![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)
2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/suno). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `suno_list_models` to inspect the available models. Use `suno_get_task` with an existing task ID to retrieve the track.

Media generation uses Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/SunoMCP) · [Support](https://github.com/AceDataCloud/SunoMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
