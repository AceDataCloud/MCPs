<img src="https://cdn.acedata.cloud/7dljuv.png" alt="OpenAI API" width="64" height="64" />

## OpenAI API by Ace Data Cloud

Use the OpenAI chat, image, audio, and embedding tools provided through Ace Data Cloud.

1. Open [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen). Sign in and open **General Application**. Select **Initialize General Application** if it is missing. Click the copy button marked **1** beside **API KEY**. Verify that the application can access the service.

   ![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)
2. Install this server from [LangBot Space](https://space.langbot.app/market/acedatacloud/openai). Paste the key into the private token field without the `Bearer` prefix. LangBot supplies that prefix when it connects.
3. Enable the server for your agent. Run `openai_list_chat_models` to inspect chat options or `openai_list_image_models` to inspect image options. Use `openai_get_task` to check an existing asynchronous task.

Chat, image, audio, and embedding requests use Ace credits. [View service pricing](https://platform.acedata.cloud/models?utm_source=langbot&utm_medium=referral&utm_campaign=evergreen).

[Source and usage](https://github.com/AceDataCloud/OpenAIMCP) · [Support](https://github.com/AceDataCloud/OpenAIMCP/issues) · [Privacy](https://platform.acedata.cloud/privacy)
