<img src="https://cdn.acedata.cloud/9q90dl.png" alt="Seedance" width="64" height="64" />

## Seedance by Ace Data Cloud

Generate video from text or animate a reference image.

1. Open [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen). Sign in and open **General Application**. Select **Initialize General Application** if it is missing. Click the copy button marked **1** beside **API KEY**. Verify that the application can access the service.

   ![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)
2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/seedance). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `seedance_list_resolutions` to see the supported sizes. Retrieve an existing video with `seedance_get_task` and its original task ID.

Media generation uses Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/SeedanceMCP) · [Support](https://github.com/AceDataCloud/SeedanceMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
