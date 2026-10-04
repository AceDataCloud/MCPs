# WebExtrator 智能抽取 API 集成指南

`POST https://api.acedata.cloud/webextrator/extract`

WebExtrator 智能抽取 API 把一个 URL 转换成**类型化的结构化结果** —— 文章、商品、
食谱、视频、讨论、招聘等，同时附带清洗后的 Markdown 与纯文本。当你想要"干净的结
构化数据"而不是原始 HTML 时，这是该用的接口。

底层是一条三层流水线：

1. **schema.org JSON-LD 映射器** —— 确定性、零 LLM 成本。覆盖 Wikipedia /
   BestBuy / AllRecipes / YouTube / 大部分新闻 / 大部分商品页。
2. **类型化 LLM 抽取** —— 仅在 schema.org 未命中时触发。按页面类型选 Schema，
   Zod 严格校验。
3. **Readability + Markdown 兜底** —— 始终运行，补齐前两层没填的顶层字段。

URL 重复请求会被 Redis 结果缓存接住，<1 ms 返回。

## 申请流程

要使用 WebExtrator 服务页，首先到 [Ace Data Cloud 控制台](https://platform.acedata.cloud/console/applications) 获取您的 API Token，留作备用。

![](https://cdn.acedata.cloud/dvc3cg.jpg)

如果你尚未登录或注册，会自动跳转到登录页面邀请你注册和登录，完成后会自动返回当前页面。

**一个 API Token 即可调用平台所有服务，无需为每个服务单独申请。** 首次申请会赠送免费额度，可免费体验；额度不足时可在 [控制台](https://platform.acedata.cloud/console/coin) 充值通用余额。

> 📘 完整文档：[WebExtrator 服务页 →](https://platform.acedata.cloud/service/webextrator)

## 鉴权

```
Authorization: Bearer YOUR_API_KEY
Content-Type:  application/json
```

## 请求参数

Extract 接受**所有**[Render API](development_webextrator_render) 的参数
（`url`、`user_agent`、`timeout`、`wait_until`、`delay`、`wait_for_selector`、
`block_resources`、`headers`、`cookies`、`callback_url`、`bypass_cache`、
`cache_ttl_seconds`、`async`），外加两个 Extract 专属字段：

| 字段 | 类型 | 必填 | 默认 | 说明 |
|------|------|:----:|------|------|
| `expected_type` | enum | ❌ | 自动判断 | 页面类型提示：`product` / `article` / `general`。跳过 URL / 文本启发式，直接走对应分支。 |
| `enable_llm` | boolean | ❌ | `false` | 当 schema.org 未命中时允许调用 LLM 抽取。在 Amazon / HN / Greenhouse 这类无 JSON-LD 的页面上，需要打开才能拿到类型化结果。 |

> 当页面自带 schema.org JSON-LD 时，`enable_llm` 无效 —— 确定性映射器直接出结果，
> 永远不会浪费 LLM 调用。你**白嫖**到类型化结果。

## 同步响应

```json
{
  "success": true,
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "trace_id": "550e8400-e29b-41d4-a716-446655440001",
  "started_at": 1777717800.123,
  "finished_at": 1777717802.535,
  "elapsed": 2.412,
  "data": {
    "kind": "extract",
    "url": "https://en.wikipedia.org/wiki/Diffbot",
    "finalUrl": "https://en.wikipedia.org/wiki/Diffbot",
    "contentType": "article",
    "title": "Diffbot",
    "description": "American machine learning and knowledge management company",
    "byline": "Contributors to Wikimedia projects",
    "language": "en",
    "siteName": "Wikipedia",
    "publishedAt": "2007-08-08T05:47:27Z",
    "images": ["https://en.wikipedia.org/static/images/icons/enwiki-25.svg"],
    "links": ["https://en.wikipedia.org/wiki/Machine_learning"],
    "markdown": "# Diffbot\n\nDiffbot is a developer of machine learning ...",
    "text": "Diffbot is a developer of machine learning algorithms ...",
    "structured": {
      "schemaOrg": { "primary": { /* 类型化实体 */ }, "breadcrumbs": [], "all": [] },
      "openGraph": { "title": "...", "description": "...", "image": "...", "type": "..." },
      "jsonLd": [ /* 原始 JSON-LD */ ]
    },
    "rawSignals": {
      "hasJsonLd": true,
      "title": "Diffbot - Wikipedia",
      "metaDescription": null,
      "pageStatus": 200,
      "textLength": 11473
    },
    "elapsedMs": 2412
  }
}
```

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `kind` | string | 固定 `"extract"`。 |
| `url` | string | 你提交的 URL。 |
| `finalUrl` | string | 重定向后的最终 URL。 |
| `contentType` | enum | `product` / `article` / `general`，由 `expected_type` → schema.org primary → 启发式 依次确定。 |
| `title` | string | Readability `<title>` 或渲染后的 `document.title`。 |
| `description` | string? | 优先级：`<meta name="description">` → `og:description` → schema.org / LLM 抽取 → 正文首段截断。 |
| `byline` | string? | 作者 / 频道 / 公司。来源 `<meta name="author">` → schema.org / LLM。 |
| `language` | string? | `<html lang>`。 |
| `siteName` | string? | `og:site_name`。 |
| `publishedAt` | string? | ISO 8601。优先级：`article:published_time` → `<time datetime>` → schema.org / LLM。 |
| `images` | string[] | 最多 50 个 `<img src>`，已解析为绝对 URL、去重、丢弃 `data:` URI。 |
| `links` | string[] | 最多 100 个外链，已过滤片段 / `javascript:` / `mailto:` / `tel:`。 |
| `markdown` | string | Turndown 转出的 Markdown。 |
| `text` | string | Mozilla Readability 抽取的 `textContent`。 |
| `structured` | object | 完整结构化结果，见下。 |
| `rawSignals` | object | 调试用的诊断信息。 |
| `cached` | boolean? | 命中缓存时为 `true`。 |
| `cacheStoredAt` | number? | 缓存条目首次写入的 Unix 毫秒时间戳。 |

### `data.structured` 子字段

| 子字段 | 何时出现 | 说明 |
|--------|---------|------|
| `schemaOrg` | 始终 | `{ primary, breadcrumbs, all }`。`primary` 是最高优先级的类型化实体；找不到时为 `null`。 |
| `openGraph` | 始终 | `{ title, description, image, type }`，源自 `<meta property="og:*">`。 |
| `jsonLd` | 始终 | 所有 `<script type="application/ld+json">` 块的原始 JSON 数组。 |
| `llm` | LLM 跑了且成功时 | `{ kind, data, model, promptCharCount }`，Zod 校验过的类型化结果。 |
| `llmError` | LLM 跑了但失败时 | `{ kind, error, model }`，请求不会因此挂掉，启发式结果依然返回。 |
| `amazon` | URL 是 `amazon.*` 时 | 老的 amazon 专用抓取器结果（将逐步废弃）。 |

## schema.org 映射器覆盖范围

按优先级排序（命中即作为 `structured.schemaOrg.primary`）：

| schema.org 类型 | 映射 kind | 输出字段 |
|----------------|----------|----------|
| `Product` | product | `name, sku, gtin, model, color, brand, url, images, offer.{price,currency,availability,condition,seller}, rating.{value,count}, reviews[], properties[]` |
| `Recipe` | recipe | `name, description, image, datePublished, author, cookTime, prepTime, totalTime, recipeYield, ingredients[], instructions[], nutrition, rating, keywords, recipeCategory, recipeCuisine` |
| `VideoObject` | video | `name, description, thumbnailUrl, uploadDate, duration, embedUrl, contentUrl, channel, interactionCount` |
| `JobPosting` | job | `title, description, datePosted, validThrough, hiringOrganization, jobLocation, baseSalary, employmentType` |
| `Event`（含 `*Event`） | event | `name, description, startDate, endDate, location.{name,address}, organizer, offer.{url,price,currency}` |
| `Article` / `NewsArticle` / `BlogPosting` / `ScholarlyArticle` / `TechArticle` / `Report` / `*NewsArticle` | article | `subtype, headline, description, datePublished, dateModified, author, publisher, image[], url, sameAs[]` |
| `FAQPage` | faq | `questions[{question, answer}]` |
| `BreadcrumbList` | （挂在 sibling） | 始终输出到 `structured.schemaOrg.breadcrumbs[]`，不会作为 primary。 |

映射器处理：

- `@graph` 容器（递归展开）；
- `@type` 数组（如 `["Recipe", "NewsArticle"]` —— 两个都识别，按优先级取胜）；
- `http://schema.org/` 前缀变体；
- 嵌套 `Offer` 与 `AggregateOffer`（后者读 `lowPrice`）；
- 相对图像 URL（按 `finalUrl` 解析为绝对）。

## LLM 类型化 Schema

当 `enable_llm: true` **且** schema.org 没有 primary 时，抽取器按 URL 启发式
（或 `expected_type` 提示）选下面之一的 Zod Schema 校验模型输出：

| Kind | URL 启发式 | 必填字段 | 可选字段 |
|------|-----------|---------|---------|
| `article` | 文本 ≥400 字且其它未命中 | `headline` | `description, byline, publishedAt, language, topics[], sections[{heading,summary}]` |
| `product` | `amazon.* / ebay.* / aliexpress.* / temu.* / walmart.* / bestbuy.*` | `name` | `description, brand, sku, price, currency, availability, rating.{value,count}, bullets[], specifications[{name,value}]` |
| `discussion` | `news.ycombinator.com / reddit.com / lobste.rs` | `title` | `author, postedAt, points, commentCount, body, url` |
| `recipe` | `allrecipes / foodnetwork / seriouseats / epicurious / bonappetit / simplyrecipes` | `name` | `description, author, cookTime, prepTime, totalTime, recipeYield, ingredients[], instructions[], nutrition, rating, keywords[]` |
| `video` | `youtube.com/watch / youtu.be / vimeo.com/<id> / tiktok.com/@/video` | `name` | `description, channel, uploadDate, duration, viewCount, likeCount, thumbnailUrl, transcript` |
| `job` | `greenhouse.io / lever.co / jobs.* / careers.* / workable.com / bamboohr` | `title` | `description, company, location, remote, employmentType, datePosted, validThrough, salaryMin, salaryMax, salaryCurrency, salaryPeriod, responsibilities[], qualifications[]` |

LLM 成功时还会向顶层字段做"last-resort"回填：

- `article` → `description` / `byline` / `publishedAt` / `language`
- `product` → `description`
- `discussion` → `description`（= body 前 280 字）/ `byline`（= author）/ `publishedAt`（= postedAt）
- `recipe` → `description` / `byline`（= author）
- `video` → `description` / `byline`（= channel）/ `publishedAt`（= uploadDate）
- `job` → `description` / `byline`（= company）/ `publishedAt`（= datePosted）

回填只在确定性数据源**没填**对应字段时触发 —— LLM 始终是最后一道兜底。

## 缓存

相同请求会被哈希到同一个 Redis Key：
`webextrator:cache:extract:<sha256(canonical-json)>`。缓存 Key **忽略** `async`、
`bypass_cache`、`cache_ttl_seconds`（这是操作开关，不影响响应）。`cookies` /
`headers` **会**分桶缓存。

| 字段 | 效果 |
|------|------|
| `bypass_cache: true` | 跳过读取；本次结果仍会写回缓存，下次相同请求能命中。 |
| `cache_ttl_seconds: 0` | 本次响应**不缓存**。 |
| `cache_ttl_seconds: N` | 自定义本条目的 TTL（默认 3600 秒）。 |

命中缓存的响应会带上 `data.cached: true` 与 `data.cacheStoredAt: <unix-ms>`。

## 异步模式与回调

设置 `async: true` 进入异步模式（提供 `callback_url` 也会自动进入）。平台立即返回（HTTP 200）：

```json
{
  "success": true,
  "task_id": "550e8400-...",
  "trace_id": "6ba7b810-...",
  "started_at": 1777717800.123
}
```

任务完成时把完整 envelope `POST` 到你的 `callback_url`（如果配置了）。也可以事
后通过 [`/webextrator/tasks`](development_webextrator_tasks) 主动查询。

## 示例

### 1. Wikipedia 文章（schema.org 命中，不需要 LLM）

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Diffbot",
    "expected_type": "article"
  }'
```

`data.structured.schemaOrg.primary` 关键字段：

```json
{
  "kind": "article",
  "subtype": "Article",
  "headline": "American machine learning and knowledge management company",
  "datePublished": "2007-08-08T05:47:27Z",
  "dateModified": "2025-07-10T20:42:45Z",
  "author": { "name": "Contributors to Wikimedia projects", "type": "Organization" },
  "publisher": { "name": "Wikimedia Foundation, Inc." }
}
```

### 2. BestBuy 商品页（schema.org 命中）

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.bestbuy.com/product/apple-airpods-pro-2nd-generation-white/JJ8ZH6TPSW",
    "expected_type": "product"
  }'
```

schema.org 抽出：

```json
{
  "kind": "product",
  "name": "Apple - Refurbished Excellent - AirPods Pro (2nd generation) - White",
  "sku": "10845412",
  "model": "MQD83AM/A",
  "color": "White",
  "brand": "Apple",
  "offer": { "price": 159.99, "currency": "USD", "availability": "https://schema.org/InStock", "seller": "Best Buy" },
  "rating": { "value": 4.4, "count": 8 }
}
```

### 3. AllRecipes 食谱页（含营养与步骤）

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.allrecipes.com/recipe/16354/easy-meatloaf/"
  }'
```

schema.org 抽出：

```json
{
  "kind": "recipe",
  "name": "Easy Meatloaf",
  "cookTime": "PT60M",
  "totalTime": "PT75M",
  "recipeYield": "8 / 1 (9x5-inch) meatloaf",
  "ingredients": ["1 1/2 pounds ground beef", "..."],
  "instructions": [{ "text": "Preheat oven to 350°F ..." }, "..."],
  "rating": { "value": 4.7, "count": 9348 }
}
```

### 4. HN 讨论页（无 JSON-LD —— 需要启用 LLM）

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com/item?id=37000000",
    "enable_llm": true
  }'
```

`data.structured.llm.data`：

```json
{
  "kind": "discussion",
  "title": "Show HN: A new way to extract web pages",
  "author": "alice",
  "points": 173,
  "commentCount": 42,
  "body": "Hi HN, we built a self-hosted alternative to Diffbot's Analyze API ..."
}
```

顶层字段也被回填：`byline = "alice"`、`publishedAt = "..."`。

### 5. Amazon 商品页（Amazon 无 JSON-LD —— 需要启用 LLM）

```bash
curl -X POST https://api.acedata.cloud/webextrator/extract \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.amazon.com/dp/B0BSHF7WHW",
    "expected_type": "product",
    "enable_llm": true
  }'
```

`data.structured.llm.data`（类型化 `product`）：

```json
{
  "kind": "product",
  "name": "Apple 2023 MacBook Pro M2 Pro 14-inch",
  "brand": "Apple",
  "price": 1799,
  "currency": "USD",
  "bullets": ["Apple M2 Pro chip with 10-core CPU", "..."],
  "specifications": [{ "name": "Display size", "value": "14.2 inches" }, "..."]
}
```

### Python (requests)

```python
import os, requests

API_KEY = os.environ["ACEDATA_API_KEY"]

resp = requests.post(
    "https://api.acedata.cloud/webextrator/extract",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "url": "https://en.wikipedia.org/wiki/Diffbot",
        "expected_type": "article",
    },
    timeout=120,
)
resp.raise_for_status()
data = resp.json()["data"]

primary = (data.get("structured") or {}).get("schemaOrg", {}).get("primary")
print("contentType:", data["contentType"])
print("title:      ", data["title"])
print("byline:     ", data.get("byline"))
print("publishedAt:", data.get("publishedAt"))
if primary and primary["kind"] == "article":
    print("headline:    ", primary["headline"])
    print("dateModified:", primary.get("dateModified"))
```

### Node.js (fetch)

```js
const apiKey = process.env.ACEDATA_API_KEY;

const res = await fetch('https://api.acedata.cloud/webextrator/extract', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.allrecipes.com/recipe/16354/easy-meatloaf/',
  }),
});
const { data } = await res.json();
const recipe = data?.structured?.schemaOrg?.primary;
console.log(recipe.name, recipe.cookTime, recipe.ingredients.length, '种配料');
```

## 提示与坑

- **能传 `expected_type` 就传。** 免费提示，跳过启发式判断，对 URL 模式不在
  内置列表里的页面尤其有用。
- **`enable_llm: true` 在 schema.org 命中的页面上是免费的。** LLM 只在 schema.org
  没有 primary 时才被调用，所以默认开着也很安全。
- **调试时先看 `rawSignals.hasJsonLd`。** 如果是 `true` 但 `structured.schemaOrg.primary`
  为 `null`，说明页面用了我们映射器还没覆盖的 `@type` —— 提个 issue，我们加。
- **`structured.llmError` 是信息性的。** 请求依然成功，启发式结果依然返回。看
  `llmError.error` 来定位原因（超时、JSON 解析失败、Zod 校验失败）。
- **非文章页的 `links[]` 不会做相关性排序。** 仅按"上限 100 条 + 过滤无效协议"
  尽力清洗。
- **缓存命中也计费。** 缓存是为延迟和保护浏览器池，不是为省钱。
