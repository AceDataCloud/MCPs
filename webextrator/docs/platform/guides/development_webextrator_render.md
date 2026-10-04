# WebExtrator 网页渲染 API 集成指南

`POST https://api.acedata.cloud/webextrator/render`

WebExtrator 网页渲染 API 是一个基于无头 Chromium 的网页渲染服务。给一个 URL，
返回完全渲染后的 HTML（包括 JS 注入的内容）、纯文本、页面标题和最终 URL。

Render 是 WebExtrator 最底层的接口。如果你需要**结构化的**抽取结果（文章正文、
商品价格、食谱配料 …），请使用
[`/webextrator/extract`](development_webextrator_extract) —— 它在同样的渲染基础
上跑了一整套类型化抽取流水线。

## 申请流程

要使用 WebExtrator 服务页，首先到 [Ace Data Cloud 控制台](https://platform.acedata.cloud/console/applications) 获取您的 API Token，留作备用。

![](https://cdn.acedata.cloud/dvc3cg.jpg)

如果你尚未登录或注册，会自动跳转到登录页面邀请你注册和登录，完成后会自动返回当前页面。

**一个 API Token 即可调用平台所有服务，无需为每个服务单独申请。** 首次申请会赠送免费额度，可免费体验；额度不足时可在 [控制台](https://platform.acedata.cloud/console/coin) 充值通用余额。

> 📘 完整文档：[WebExtrator 服务页 →](https://platform.acedata.cloud/service/webextrator)

## 鉴权

所有 WebExtrator 接口使用标准的 Bearer Token 鉴权：

```
Authorization: Bearer YOUR_API_KEY
Content-Type:  application/json
```

## 请求参数

| 字段 | 类型 | 必填 | 默认 | 说明 |
|------|------|:----:|------|------|
| `url` | string | ✅ | — | 要渲染的页面 URL，必须是 `http(s)://`。 |
| `user_agent` | string | ❌ | 内置 UA 池轮换 | 自定义 User-Agent。 |
| `timeout` | number | ❌ | `30` | 单次导航超时（**秒**）。 |
| `wait_until` | enum | ❌ | `networkidle` | 加载完成事件：`load` / `domcontentloaded` / `networkidle` / `commit`。 |
| `delay` | number | ❌ | `0` | `wait_until` 触发后的**额外等待秒数**（用于 SPA 二次渲染）。 |
| `wait_for_selector` | string | ❌ | — | 等待该 CSS 选择器出现，比 `networkidle` 更稳。 |
| `block_resources` | string[] | ❌ | `["image","font","media"]` | 屏蔽的资源类型，可选：`image` / `font` / `media` / `stylesheet` / `xhr` / `fetch`。 |
| `headers` | object | ❌ | — | 额外的 HTTP 请求头（例如 `{"Accept-Language": "en-US"}`）。 |
| `cookies` | array | ❌ | — | 导航前注入的 Cookie，结构见下。 |
| `callback_url` | string | ❌ | — | 异步模式下的回调地址，平台在任务完成时 `POST` 完整结果到此地址。 |
| `bypass_cache` | boolean | ❌ | `false` | 跳过 Redis 缓存读取（但仍会把本次结果写回缓存）。 |
| `cache_ttl_seconds` | number | ❌ | `3600` | 自定义本次写入的缓存 TTL，传 `0` 表示不缓存本次响应。 |
| `async` | boolean | ❌ | `false` | 设为 `true` 立即返回 `task_id`，结果通过 `callback_url` 或 Tasks API 取回。 |

> 平台契约统一使用 **snake_case**。内部渲染服务支持 camelCase，但对外调用一律
> 使用 snake_case。

### Cookie 结构

```json
{
  "name":      "string",
  "value":     "string",
  "domain":    "string",
  "path":      "/",
  "expires":   1735689600,
  "httpOnly":  false,
  "secure":    true,
  "sameSite":  "Lax"
}
```

## 同步响应

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": 1777717800.123,
  "finished_at": 1777717801.234,
  "elapsed": 1.111,
  "data": {
    "kind": "render",
    "url": "https://example.com",
    "finalUrl": "https://example.com/",
    "title": "Example Domain",
    "status": 200,
    "html": "<!DOCTYPE html><html>...</html>",
    "text": "Example Domain\nThis domain is for use in illustrative examples...",
    "userAgent": "Mozilla/5.0 ...",
    "elapsedMs": 1108
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `data.kind` | string | 固定 `"render"`。 |
| `data.url` | string | 你提交的 URL。 |
| `data.finalUrl` | string | 跟随重定向后的最终 URL。 |
| `data.title` | string | 渲染后的 `document.title`。 |
| `data.status` | number \| null | 主导航的 HTTP 状态码。 |
| `data.html` | string | 完整的渲染后 HTML。 |
| `data.text` | string | `document.body.innerText` 快照（如需更干净的正文请用 Extract）。 |
| `data.userAgent` | string | 实际使用的 UA。 |
| `data.elapsedMs` | number | 仅浏览器渲染耗时。 |
| `data.cached` | boolean? | 命中缓存时为 `true`。 |
| `data.cacheStoredAt` | number? | 缓存条目首次写入的 Unix 毫秒时间戳。 |

## 异步响应

`async=true`（或提供 `callback_url`）时立即返回（HTTP 200）：

```json
{
  "success": true,
  "task_id": "550e8400-...",
  "trace_id": "6ba7b810-...",
  "started_at": 1777717800.123
}
```

结果将通过 `POST` 推送到 `callback_url`（如果配置了），或者通过
[`/webextrator/tasks`](development_webextrator_tasks) 主动查询。

### 回调结构

平台 `POST` 与同步模式**完全相同**的 envelope 到 `callback_url`，
`Content-Type: application/json`。返回任意 `2xx` 即视为已确认；`5xx` 会被
指数退避重试约 5 分钟。

## 错误响应

| HTTP | `error.code` | 含义 |
|------|--------------|------|
| 400 | `bad_request` | 请求体未通过 Zod 校验（缺 `url`、类型不对 …）。 |
| 401 | `unauthorized` | 缺失或无效的 `Authorization: Bearer …`。 |
| 402 | (x402) | 平台余额不足，返回 x402 支付要求 envelope。 |
| 408 | `timeout` | 导航超过 `timeout`。 |
| 429 | `queue_busy` | 同步队列拥挤，请重试或改用 `async=true`。 |
| 500 | `internal_error` | 服务器端未处理异常（浏览器崩溃等），Worker 自动重试一次。 |

错误结构：

```json
{
  "success": false,
  "task_id": "...",
  "trace_id": "...",
  "started_at": 1777717800.123,
  "finished_at": 1777717800.135,
  "elapsed": 0.012,
  "error": { "code": "bad_request", "message": "url: Invalid url" }
}
```

## 示例

### cURL

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "wait_until": "networkidle",
    "block_resources": ["image", "media", "font"]
  }'
```

### Python (requests)

```python
import os, requests

API_KEY = os.environ["ACEDATA_API_KEY"]

resp = requests.post(
    "https://api.acedata.cloud/webextrator/render",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "url": "https://example.com",
        "wait_until": "networkidle",
        "block_resources": ["image", "media", "font"],
    },
    timeout=60,
)
resp.raise_for_status()
data = resp.json()["data"]
print(data["title"], data["status"], len(data["html"]))
```

### Node.js (fetch)

```js
const apiKey = process.env.ACEDATA_API_KEY;

const res = await fetch('https://api.acedata.cloud/webextrator/render', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://example.com',
    wait_until: 'networkidle',
    block_resources: ['image', 'media', 'font'],
  }),
});
const { data } = await res.json();
console.log(data.title, data.status, data.html.length);
```

### 异步 + 回调

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "async": true,
    "callback_url": "https://your-app.example.com/hooks/webextrator"
  }'
```

立即返回 `{ "success": true, "task_id": "...", "trace_id": "...", "started_at": 1777717800.123 }`；
任务完成时平台会 POST 完整结果到你的 `callback_url`。

### 强制绕过缓存

```bash
curl -X POST https://api.acedata.cloud/webextrator/render \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "bypass_cache": true
  }'
```

## 提示与坑

- **`wait_until` 选对很重要。** `networkidle` 最稳但最慢；`domcontentloaded`
  快但可能漏掉异步注入的内容；`load` 适合传统静态页。
- **缓存 Key 忽略 `async`。** 同一 URL 的同步与异步请求命中同一缓存条目，
  随意切换不会失效。
- **缓存 Key 忽略 `bypass_cache` 与 `cache_ttl_seconds`。** 这两个是操作开关，
  不影响响应内容。
- **`cookies` 与 `headers` 会分桶缓存。** 自定义这两个会让首次相同组合命中失败。
- **重 SPA 经常超过默认 30 秒。** 建议 `timeout: 60`、`wait_until:
  "domcontentloaded"`、`delay: 4`，再配合 `wait_for_selector` 等待真正关心
  的元素。
- **`block_resources` 是降低延迟的最快路径。** 默认已屏蔽图片 / 字体 / 媒体；
  如果你抽取不依赖 CSS 布局，加上 `stylesheet` 还能更快。
