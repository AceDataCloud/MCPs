<img src="https://cdn.acedata.cloud/859plc.jpg" alt="Nano Banana" width="64" height="64" />

## Nano Banana by Ace Data Cloud

Generate an image from a prompt, or edit a reference image with text instructions.

1. Open [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen). Sign in and open **General Application**. Select **Initialize General Application** if it is missing. Click the copy button marked **1** beside **API KEY**. Verify that the application can access the service.

   ![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)
2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/nano-banana). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `nanobanana_list_models` to review available models. Retrieve a previous image with `nanobanana_get_task` and its original task ID.

Media generation uses Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/NanoBananaMCP) · [Support](https://github.com/AceDataCloud/NanoBananaMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
