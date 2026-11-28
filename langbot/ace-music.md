<img src="https://cdn.acedata.cloud/acemusic-icon-52deddfc87b9.png" alt="ACE Music" width="64" height="64" />

## ACE Music by Ace Data Cloud

Create music from a prompt or your own lyrics, cover or mash up audio, and retrieve the finished tracks.

1. Open [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen). Sign in and open **General Application**. Select **Initialize General Application** if it is missing. Click the copy button marked **1** beside **API KEY**. Verify that the application can access the service.

   ![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)
2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/ace-music). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `acemusic_list_models` to see the available music models. Retrieve a previous result with `acemusic_get_task` and its original task ID.

Media generation uses Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/AceMusicMCP) · [Support](https://github.com/AceDataCloud/AceMusicMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
