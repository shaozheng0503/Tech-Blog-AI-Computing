import http.client
import json
import time

# --- 配置信息 ---
API_TOKEN = "d1e7f0a8-49df-4760-8cb2-09b7aeb48dbf-20250709180338"
TASK_ID = 3000  # 从您截图的 URL 中识别
TARGET_POINTS = 8   # 测试目标：扩展到 8 个节点

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

print("--- 准备发送请求 ---")
print(f"URL: https://openapi.suanli.cn/api/deployment/task/change_points")
print(f"请求方法: POST")
print(f"Headers: {headers}")
print(f"Payload: {payload}")
print("--------------------")

try:
    conn.request("POST", "/api/deployment/task/change_points", payload, headers)
    res = conn.getresponse()
    
    print(f"\n--- 收到响应 ---")
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
