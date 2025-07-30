# 云主机JupyterLab开发转Serverless部署

> 本教程展示如何在GPU云主机的JupyterLab环境中开发API，然后一键部署到Serverless平台

## Overview

通过本教程，您将学会：
- 在云主机JupyterLab中快速开发API
- 本地测试和调试API功能
- 一键部署到多个Serverless平台
- 监控和维护已部署的服务

**预计完成时间**: 15分钟

---

## 准备工作

### 环境要求
- GPU云主机实例（已配置JupyterLab）
- Python 3.9+
- 网络连接

### 快速检查
在JupyterLab终端中运行：
```bash
python --version
pip --version
```

![环境检查截图占位](./images/environment-check.png)

---

## Step 1: 进入开发环境

### 1.1 访问JupyterLab
打开您的云主机JupyterLab环境：

```
https://your-cloud-instance.com/lab
```

![JupyterLab界面截图占位](./images/jupyterlab-interface.png)

### 1.2 创建项目目录
在JupyterLab中新建终端，创建项目：

```bash
mkdir serverless-api-demo
cd serverless-api-demo
```

![创建项目目录截图占位](./images/create-project.png)

---

## Step 2: 快速开发API

### 2.1 创建FastAPI应用
新建文件 `app.py`：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="云主机API示例", version="1.0.0")

class User(BaseModel):
    name: str
    email: str
    age: int

# 模拟数据库
users_db = []

@app.get("/")
def read_root():
    return {"message": "云主机API运行中", "users_count": len(users_db)}

@app.get("/users")
def get_users():
    return {"users": users_db, "total": len(users_db)}

@app.post("/users")
def create_user(user: User):
    user_dict = user.dict()
    user_dict["id"] = len(users_db) + 1
    users_db.append(user_dict)
    return {"message": "用户创建成功", "user": user_dict}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "云主机API"}
```

![编写API代码截图占位](./images/write-api-code.png)

### 2.2 安装依赖
创建 `requirements.txt`：

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
mangum==0.17.0
pydantic==2.5.0
```

安装依赖：
```bash
pip install -r requirements.txt
```

![安装依赖截图占位](./images/install-dependencies.png)

---

## Step 3: 本地测试

### 3.1 启动开发服务器
在JupyterLab终端中：

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

![启动服务器截图占位](./images/start-server.png)

### 3.2 测试API功能
在新的JupyterLab笔记本中测试：

```python
import requests

# 测试健康检查
response = requests.get("http://localhost:8000/health")
print("健康检查:", response.json())

# 创建用户
new_user = {
    "name": "测试用户",
    "email": "test@example.com", 
    "age": 25
}
response = requests.post("http://localhost:8000/users", json=new_user)
print("创建用户:", response.json())

# 获取用户列表
response = requests.get("http://localhost:8000/users")
print("用户列表:", response.json())
```

![API测试结果截图占位](./images/api-test-results.png)

### 3.3 查看API文档
访问自动生成的API文档：
```
http://localhost:8000/docs
```

![API文档截图占位](./images/api-docs.png)

---

## Step 4: 准备Serverless部署

### 4.1 创建Serverless处理器
新建 `handler.py`：

```python
from mangum import Mangum
from app import app

# Serverless处理器
lambda_handler = Mangum(app)

# 阿里云函数处理器
def aliyun_handler(event, context):
    return lambda_handler(event, context)

# 腾讯云函数处理器  
def tencent_handler(event, context):
    return lambda_handler(event, context)
```

![创建处理器截图占位](./images/create-handler.png)

### 4.2 配置部署文件
创建 `serverless.yml`：

```yaml
service: cloud-api-demo

provider:
  name: aws
  runtime: python3.9
  region: us-east-1

functions:
  api:
    handler: handler.lambda_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
      - http:
          path: /
          method: ANY

plugins:
  - serverless-python-requirements
```

![配置部署文件截图占位](./images/serverless-config.png)

---

## Step 5: 一键部署

### 5.1 部署到AWS Lambda

安装Serverless Framework：
```bash
npm install -g serverless
npm install serverless-python-requirements
```

部署：
```bash
serverless deploy
```

![AWS部署截图占位](./images/aws-deploy.png)

### 5.2 部署到阿里云函数计算

安装阿里云工具：
```bash
npm install -g @alicloud/fun
```

创建 `template.yml`：
```yaml
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'

Resources:
  cloud-api:
    Type: 'Aliyun::Serverless::Service'
    Properties:
      Description: 云主机API示例
    
    api:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Handler: handler.aliyun_handler
        Runtime: python3.9
        CodeUri: ./
      Events:
        httpTrigger:
          Type: HTTP
          Properties:
            AuthType: ANONYMOUS
            Methods: ['GET', 'POST', 'PUT', 'DELETE']
```

部署：
```bash
fun deploy
```

![阿里云部署截图占位](./images/aliyun-deploy.png)

### 5.3 部署到腾讯云函数

使用腾讯云Serverless Framework：
```bash
npm install -g serverless
serverless create --template tencent-python3 --path tencent-api
```

部署：
```bash
cd tencent-api
serverless deploy
```

![腾讯云部署截图占位](./images/tencent-deploy.png)

---

## Step 6: 验证部署

### 6.1 获取部署URL
部署完成后，各平台会返回API网关地址：

**AWS Lambda:**
```
https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/
```

**阿里云函数计算:**
```
https://xxxxxx.fc.aliyun.com/api/
```

**腾讯云函数:**
```
https://xxxxxx.apigw.tencentcs.com/release/
```

![部署URL截图占位](./images/deployment-urls.png)

### 6.2 测试部署的API
使用生产环境URL测试：

```python
import requests

# 替换为您的实际部署URL
api_url = "https://your-deployed-api.amazonaws.com/dev"

# 测试健康检查
response = requests.get(f"{api_url}/health")
print("生产环境健康检查:", response.json())

# 测试创建用户
new_user = {
    "name": "生产用户",
    "email": "prod@example.com",
    "age": 30
}
response = requests.post(f"{api_url}/users", json=new_user)
print("生产环境创建用户:", response.json())
```

![生产环境测试截图占位](./images/production-test.png)

---

## Step 7: 监控和维护

### 7.1 查看服务状态
**AWS CloudWatch:**
- 访问AWS控制台查看Lambda函数指标
- 监控调用次数、错误率、响应时间

![AWS监控截图占位](./images/aws-monitoring.png)

**阿里云函数计算控制台:**
- 查看函数执行情况和日志
- 监控资源使用情况

![阿里云监控截图占位](./images/aliyun-monitoring.png)

### 7.2 设置告警
配置关键指标告警：
- API响应时间超过5秒
- 错误率超过5%
- 调用量异常增长

![告警配置截图占位](./images/alert-setup.png)

### 7.3 更新部署
当需要更新API时，只需：

1. 在JupyterLab中修改代码
2. 重新运行部署命令
3. 验证更新是否生效

```bash
# 更新AWS Lambda
serverless deploy

# 更新阿里云函数
fun deploy

# 更新腾讯云函数
serverless deploy
```

![更新部署截图占位](./images/update-deployment.png)

---

## 最佳实践

### 性能优化
- 使用函数预留并发减少冷启动
- 优化依赖包大小
- 合理设置函数内存和超时时间

### 成本控制
- 监控函数调用次数和执行时长
- 使用按量计费，避免资源浪费
- 设置合理的函数超时时间

### 安全考虑
- 配置API网关访问控制
- 使用环境变量存储敏感信息
- 定期更新依赖包版本

![最佳实践总结截图占位](./images/best-practices.png)

---

## 总结

通过本教程，您已经学会了：

✅ 在云主机JupyterLab中快速开发API  
✅ 本地测试和调试功能  
✅ 一键部署到多个Serverless平台  
✅ 监控和维护生产服务  

### 下一步
- 探索更多API功能开发
- 集成数据库和缓存
- 实现更复杂的业务逻辑
- 配置CI/CD自动化部署

![教程完成截图占位](./images/tutorial-complete.png)

---

## 相关资源

- [共绩算力云主机文档](https://www.gongjiyun.com/docs/)
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Serverless Framework文档](https://www.serverless.com/framework/docs/)
- [AWS Lambda文档](https://docs.aws.amazon.com/lambda/)
- [阿里云函数计算文档](https://help.aliyun.com/product/50980.html)

**需要帮助？**  
如有问题，请访问我们的技术支持页面或联系技术团队。 