# goose 的 Ace Data Cloud 模型预设

[English](README.md)

这是适用于 goose 1.55.0+、需要**独立安装**的命名预设，不是官方默认内置，也不会随媒体插件安装自动注册。目标仍是让全新 goose 的模型服务商列表直接显示 **Ace Data Cloud**；本候选不能算该目标已完成。

## 1. 注册、登录并获取服务 API Token

1. 打开 [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_goose_api_key)，先注册或登录。
2. 打开 **General application**；没有通用应用时先选择 **Initialize General Application**。核对聊天服务访问权限、余额及[当前模型价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_goose_pricing)。不要把历史示例价格当当前报价。
3. 复制应用卡片的 API Key，或打开 **Manage Keys → Create**，创建可独立撤销的专用 Key，例如 `goose models`。根据实际需要设置过期、用量限制和 Allowed APIs；聊天模型需要访问 `/openai/chat/completions`。
4. 复制原始 Token 字符串，不加 `Bearer `、引号或空格。`platform-...` 管理 Token 不能替代服务 API Key。不要把 Key 写到聊天、Git、共享配置或截图里。

![真实脱敏 Ace 页面：复制 API Key 或打开 Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![真实 Ace 页面：创建可选的专用 Key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

图片复用 SunoDify 固定提交 `8d3d035` 的真实脱敏账户页面，2026-10-18 引用；原拍摄日期未标注。创建图的示例名仍是 `Dify tutorial`，不是已创建的 goose Key，也不是 goose 运行或计费证据。

## 2. 独立安装命名预设

运行 `goose info` 查看当前 profile 的配置目录。将本目录的 `acedatacloud.json` 复制到该配置目录下的 `custom_providers/`，不要覆盖其他已有预设。

在启动 goose 的进程环境设置 `ACEDATACLOUD_API_TOKEN`，或通过 goose 对该服务商的正常凭据设置保存 Key。使用环境变量时，可在 Bash 终端隐藏输入：

```bash
read -r -s -p 'Ace service API Token: ' ACEDATACLOUD_API_TOKEN
printf '\n'
export ACEDATACLOUD_API_TOKEN
goose session
```

安装后才可选择 **Ace Data Cloud**，再选 `gpt-4.1-mini` 或 `gpt-4.1`。已经打开的桌面进程不会自动继承后来终端设置的变量；需要让启动它的进程获得环境变量并重新打开。本预设没有新增 Key 弹窗，不要求用户在 prompt 中提交凭据。

公开传输地址固定为 `https://api.acedata.cloud/openai/chat/completions`。两个模型 ID 是可选列表，不是自动 fallback；不暗示图像、音频、Responses、视觉或推理参数也已兼容。

## 3. 首次使用与结果边界

本轮只验证了真实 goose 读取预设及本地模拟模型的工具循环，没有发真实线上推理请求。选择模型后发送聊天通常会使用账户余额；先核当前价和自己的费用限制。不要为了测试安装而默认发起收费调用。

确认具体聊天任务及费用后，才执行用户要求的一次请求并查看实际返回。普通文本聊天不涉及媒体异步 task；若另装媒体插件，其生成结果须保留原 task ID，并查询同一个 ID 到成功或失败，不能重复生成来检查进度。模型聊天账单和媒体任务账单分别核对，不用本地检查代替唯一 usage 记录。

## 4. 排错

| 情况 | 检查 |
|---|---|
| 列表没有 Ace Data Cloud | 确认当前 profile 的 `custom_providers/` 已有该 JSON，再启动新会话；不能假定全新 goose 已内置。 |
| 401 / 403 | 核完整原始服务 Key、聊天访问权限、过期、Allowed APIs；不要改用管理 Token。 |
| 余额不足或限流 | 查看当前余额、限制与价格，保留上游错误含义；不要自动更换模型或创建新 Key 绕过限制。 |
| 桌面有变量却取不到 Key | 核启动桌面进程的环境；终端后来 export 不会注入已有进程。 |
| 工具返回或费用不符合预期 | 保留实际请求/usage 证据核对；本地模拟通过不证明线上推理或计费已验收。 |

## 官方默认服务商的准入材料

用户问题：已有 Ace 服务 Key 的用户，在全新 goose 服务商列表里找不到 Ace Data Cloud，必须自己探索自定义地址。希望的最小原生实现是独立的声明式服务商、独立凭据名、小范围经过验证的 Chat Completions 模型、当前设置/价格入口，不添加自动 fallback。

待验收内容包括：全新默认选择器可见、真实 Key 设置、流式工具调用与结果回传、真实 usage 账单核对。本地模拟验证可先完成，但不能代替这些生产验收。

上游[模型服务商政策](https://github.com/aaif-goose/goose/blob/bfcc6ee6f1ee18d0c4c852a65c49b25f87ee40dc/CONTRIBUTING.md#llm-provider-integrations)通常建议第三方发布 custom JSON，内置只偶尔接受例外。[贡献说明要求人类自己写 issue](https://github.com/aaif-goose/goose/blob/bfcc6ee6f1ee18d0c4c852a65c49b25f87ee40dc/CONTRIBUTING.md#how-to-contribute)，且[issue 必须进入 Ready 后才可开外部实现 PR](https://github.com/aaif-goose/goose/blob/bfcc6ee6f1ee18d0c4c852a65c49b25f87ee40dc/CONTRIBUTING.md#from-issue-to-pull-request)。本材料用于支持该人工准入流程，不表示已获接受、已投稿或正式内置。
