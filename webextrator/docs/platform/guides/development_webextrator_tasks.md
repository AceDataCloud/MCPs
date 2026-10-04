# WebExtrator 任务查询 API 集成指南

`POST https://api.acedata.cloud/webextrator/tasks`

WebExtrator 任务查询 API 用于查询历史的 `render` / `extract` 任务结果。常见
用法：

- 异步任务完成后**回查**完整 envelope（除了 `callback_url` 推送或主动轮询）。
- **审计**自己提交过什么 —— 任务记录同时存了原始 `request` 与最终 `response`。
- **批量回填** —— 一次按 `id` 或 `trace_id` 拉多条。

任务记录在 Redis 中保留 **7 天**。

任务查询接口**免费**（不计入 Credits 用量）。

## 鉴权

```
Authorization: Bearer YOUR_API_KEY
Content-Type:  application/json
```

只能查到自己 AceDataCloud 账户下的任务。

## 请求参数

请求体是按 `action` 区分的判别式联合，共两种动作：

### `action: "retrieve"` —— 单条查询

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `action` | const | ✅ | 固定 `"retrieve"`。 |
| `id` | string | 二选一 | 任务 ID（出现在每次 render/extract envelope 的 `task_id` 字段）。 |
| `trace_id` | string | 二选一 | 调用链 ID（envelope 的 `trace_id` 字段）。 |

`id` 与 `trace_id` 二选一传入。

### `action: "retrieve_batch"` —— 批量查询

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `action` | const | ✅ | 固定 `"retrieve_batch"`。 |
| `ids` | string[] | 二选一 | 任务 ID 列表。 |
| `trace_ids` | string[] | 二选一 | 调用链 ID 列表。 |
| `offset` | number | ❌ | 分页偏移（默认 0）。 |
| `limit` | number | ❌ | 单页大小，1–100（默认 50）。 |

`ids` 与 `trace_ids` 二选一传入。

## 单条响应

```json
{
  "task": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "trace_id": "550e8400-e29b-41d4-a716-446655440001",
    "type": "extract",
    "created_at": 1777717800.05,
    "started_at": 1777717800.123,
    "finished_at": 1777717802.535,
    "elapsed": 2.412,
    "request": {
      "url": "https://en.wikipedia.org/wiki/Diffbot",
      "expected_type": "article"
    },
    "response": {
      "success": true,
      "data": { /* 完整 extract envelope */ }
    }
  }
}
```

查不到时返回 `{ "task": null }`（HTTP 200，不是 404）。

`task` 对象的计时字段说明如下。

- `created_at`，任务创建时间，Unix 时间戳（秒，浮点）。
- `started_at`，任务开始执行时间，Unix 时间戳（秒，浮点）。任务尚未开始时为 `null`。
- `finished_at`，任务完成时间，Unix 时间戳（秒，浮点）。任务未完成时为 `null`。
- `elapsed`，任务执行耗时，单位为秒（浮点，保留 3 位小数）。任务未完成时为 `null`。

## 批量响应

```json
{
  "tasks": [
    { /* 同单条 .task 结构 */ },
    { /* ... */ }
  ],
  "offset": 0,
  "limit":  50
}
```

不存在的 ID 不会报错，只是从 `tasks` 中缺失。

## 示例

### 按 task_id 查询单条

```bash
curl -X POST https://api.acedata.cloud/webextrator/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "retrieve",
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### 按 trace_id 查询单条

```bash
curl -X POST https://api.acedata.cloud/webextrator/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "retrieve",
    "trace_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

### 批量查询

```bash
curl -X POST https://api.acedata.cloud/webextrator/tasks \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "retrieve_batch",
    "ids": [
      "550e8400-e29b-41d4-a716-446655440000",
      "550e8400-e29b-41d4-a716-446655440002"
    ],
    "limit": 50
  }'
```

### Python (requests) —— 轮询直到完成

```python
import os, time, requests

API_KEY = os.environ["ACEDATA_API_KEY"]
BASE = "https://api.acedata.cloud"

# 1) 提交异步抽取
queue = requests.post(
    f"{BASE}/webextrator/extract",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={"url": "https://example.com", "mode": "async"},
).json()

job_id = queue["jobId"]

# 2) 用 Tasks API 轮询直到任务完成
while True:
    r = requests.post(
        f"{BASE}/webextrator/tasks",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"action": "retrieve", "id": job_id},
    ).json()
    task = r.get("task")
    if task and task.get("finished_at"):
        print("耗时", task["elapsed"], "秒")
        print(task["response"]["data"]["title"])
        break
    time.sleep(2)
```

### Node.js (fetch) —— 收到回调后再拉完整 envelope

```js
// 在你的 callback_url 处理函数里：
app.post('/hooks/webextrator', async (req, res) => {
  res.status(200).end();              // 先快速 ack

  const taskId = req.body?.task_id;
  if (!taskId) return;

  const fetchRes = await fetch('https://api.acedata.cloud/webextrator/tasks', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.ACEDATA_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ action: 'retrieve', id: taskId }),
  });
  const { task } = await fetchRes.json();
  console.log('完整 envelope:', task.response.data);
});
```

## 错误响应

| HTTP | `error.code` | 含义 |
|------|--------------|------|
| 400 | `bad_request` | 校验失败（缺 `action`、同时传 `id` 与 `trace_id` 等）。 |
| 401 | `unauthorized` | 缺失或无效的 `Authorization: Bearer …`。 |

```json
{ "error": { "code": "bad_request", "message": "..." } }
```

## 提示与坑

- **能自定义 `trace_id` 就自定义。** 在原始 render/extract 请求上传
  `?trace_id=…`（QueryString），把它跟你自己的业务 ID（工作流 run id 等）对齐，
  之后就能用业务 ID 查任务。没传时服务器自动生成 UUID。
- **保留期 7 天。** 更早的任务返回 `task: null` —— 需要长期归档请自行落库。
- **任务查询免费。** 想查多少次就查多少次，原始 render/extract 调用时费用已经付过。
- **优先用异步 + 回调，而不是轮询。** 业务允许的话，在原请求里传
  `callback_url`，让平台把 envelope 推送给你，比每 2 秒轮一次更高效。
