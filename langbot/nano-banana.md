<img src="https://cdn.acedata.cloud/859plc.jpg" alt="Nano Banana" width="64" height="64" />

## Nano Banana

Generate an image from a prompt, or edit a reference image with text instructions.

1. Sign in to [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. Copy the key from the right of the **API KEY** field and check that the application has access to Nano Banana.

   ![API key in the General Application card](https://cdn.acedata.cloud/dvc3cg.jpg)

2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/nano-banana). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `nanobanana_list_models` to review available models. Retrieve a previous image with `nanobanana_get_task` and its original task ID.

Media generation uses Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/NanoBananaMCP) · [Support](https://github.com/AceDataCloud/NanoBananaMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
