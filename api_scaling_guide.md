# 1. 通过 API 实现弹性节点扩缩容

平台提供了强大的 Open API，允许您通过编程方式动态地对任务节点进行扩容或缩容。这对于实现自动化运维、根据业务负载高峰低谷自动调整资源、节约成本具有重要意义。


## 1.1 任务节点数量修改接口

此接口是实现弹性伸缩的核心，允许您实时修改指定任务的运行节点数量。

**接口地址**：
`POST /api/deployment/task/change_points`

**说明**：根据您在平台生成 API 密钥的模式 (简易模式或签名模式)，此接口的调用方式略有不同。

### 1.1.1 请求参数

**Header 参数**

| 参数名 | 类型 | 是否必需 | 描述 |
| --- | --- | --- | --- |
| `token` | string | 是 | 您在平台生成的 API 密钥 |
| `timestamp` | string | 是 | 请求时间戳 (毫秒)，例如 `1747379023000` |
| `version` | string | 是 | API 版本号，例如 `1.0.0` |
| `sign_str` | string | 否 | 签名字符串。如果 `token` 为简易模式，则无需填写此字段 |

**Body 参数** (`application/json`)

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| `task_id` | integer | 必需，您要修改的目标任务的 ID |
| `points` | integer | 必需，修改后任务的目标节点数量 |

### 1.1.2 请求体示例

```json
{
    "task_id": 388,
    "points": 1
}
```

### 1.1.3 调用示例代码 (Python)

以下是使用 Python 的 `http.client` 库调用此接口的示例：

```python
import http.client
import json

conn = http.client.HTTPSConnection("openapi.suanli.cn")

payload = json.dumps({
   "task_id": 388,
   "points": 1 # 将任务 ID 为 388 的节点数量修改为 1
})

headers = {
   'token': 'YOUR_API_TOKEN', # 替换为您的 Token
   'timestamp': '1747379023000', # 替换为当前的时间戳
   'version': '1.0.0',
   'sign_str': '', # 如果是签名模式，需要计算并填写
   'Content-Type': 'application/json'
}

conn.request("POST", "/api/deployment/task/change_points", payload, headers)
res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

### 1.1.4 返回响应

如果请求成功，您将收到如下格式的 JSON 响应：

`200 OK`

```json
{
    "code": "0000",
    "message": "success"
}
```

### 1.1.5 完整调用示例与成功响应

下面是一个将任务 ID 为 `3000` 的节点数量从 1 个调整为 2 个的真实调用示例。

**示例代码 (Python)**

```python
import http.client
import json
import time

# --- 配置信息 ---
API_TOKEN = "d1e7f0a8-49df-4760-8cb2-09b7aeb48dbf-20250709180338" # 示例 Token
TASK_ID = 3000  # 示例任务 ID
TARGET_POINTS = 2   # 目标节点数

# 动态生成当前的毫秒级时间戳
current_timestamp = int(time.time() * 1000)

# --- API 调用 ---
conn = http.client.HTTPSConnection("openapi.suanli.cn")

payload = json.dumps({
   "task_id": TASK_ID,
   "points": TARGET_POINTS
})

headers = {
   'token': API_TOKEN,
   'timestamp': str(current_timestamp),
   'version': '1.0.0',
   'sign_str': '', 
   'Content-Type': 'application/json'
}

try:
    conn.request("POST", "/api/deployment/task/change_points", payload, headers)
    res = conn.getresponse()
    
    print(f"状态码: {res.status} {res.reason}")
    data = res.read()
    print("响应内容:")
    try:
        response_json = json.loads(data.decode('utf-8'))
        print(json.dumps(response_json, indent=4, ensure_ascii=False))
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(data.decode('utf-8', errors='ignore'))

finally:
    conn.close()
```

**成功响应日志**

执行以上脚本后，得到的成功响应如下：

```shell
--- 准备发送请求 ---
URL: https://openapi.suanli.cn/api/deployment/task/change_points
请求方法: POST
Headers: {'token': 'd1e7f0a8-49df-4760-8cb2-09b7aeb48dbf-20250709180338', 'timestamp': '1752055431338', 'version': '1.0.0', 'sign_str': '', 'Content-Type': 'application/json'}
Payload: {"task_id": 3000, "points": 2}
--------------------

--- 收到响应 ---
状态码: 200 OK
响应内容:
{
    "code": "0000",
    "message": "success",
    "data": null
}
```

**效果验证**

调用成功后，回到控制台任务详情页，可以看到节点数量已成功变为 2 个，一个新的节点正在启动或已在运行中。

**【请在此处附上控制台节点列表截图】**

![在这里插入截图](此处替换为您的截图路径)

## 1.2 实践建议

您可以将此 API 集成到您的监控和自动化脚本中。例如，通过监控应用负载 (如队列长度、API 响应时间)，当负载超过预设阈值时，自动调用此接口增加节点 (`points` 调大)；当负载恢复正常时，再调用接口减少节点 (`points` 调小)，从而实现真正意义上的无人值守和成本优化。 