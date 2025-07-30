# 🚀 云主机API快速开始指南

欢迎使用GPU云主机环境！本指南将帮助您在几分钟内启动完整的用户管理API。

## 🌐 云主机信息

- **实例ID**: `gpu-4090-96g-instance-318`
- **域名**: `gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud`
- **JupyterLab**: [https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest)

## ⚡ 极速启动（30秒上手）

### 方式一：使用云主机启动脚本

```bash
# 进入项目目录
cd "文章汇总/云主机转为服务部署"

# 一键启动（包含演示数据）
python cloud_start.py --demo

# 或者基础启动
python cloud_start.py
```

### 方式二：在JupyterLab中开发

1. 打开 [JupyterLab环境](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest)
2. 运行 `notebooks/cloud_development.ipynb`
3. 按顺序执行所有单元格

### 方式三：传统启动

```bash
# 安装依赖
pip install -r deployment/requirements.txt

# 启动API服务
cd src
python app.py
```

## 🎯 访问您的API

启动成功后，您可以访问：

| 功能 | 地址 | 描述 |
|------|------|------|
| 🏠 **API首页** | [https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud) | 美观的首页和快速开始 |
| 📖 **API文档** | [https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/docs](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/docs) | Swagger交互式文档 |
| 📚 **ReDoc** | [https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/redoc](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/redoc) | 详细API文档 |
| 📊 **统计** | [https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/stats](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/stats) | 实时性能统计 |
| 🔍 **健康检查** | [https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/health](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/health) | 系统健康状态 |

## 🧪 快速测试

### 使用cURL测试

```bash
# 获取用户列表
curl 'https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users'

# 创建新用户
curl -X POST 'https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users' \
  -H 'Content-Type: application/json' \
  -d '{"name":"云主机用户","email":"cloud@example.com","age":28}'

# 搜索用户
curl 'https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/search/云'

# 获取API统计
curl 'https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/stats'
```

### 使用Python测试

```python
import requests

base_url = "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud"

# 健康检查
response = requests.get(f"{base_url}/health")
print(response.json())

# 获取用户列表
response = requests.get(f"{base_url}/users")
print(response.json())

# 创建用户
new_user = {
    "name": "Python测试用户",
    "email": "python@test.com",
    "age": 30
}
response = requests.post(f"{base_url}/users", json=new_user)
print(response.json())
```

### 使用JavaScript测试

```javascript
const baseUrl = "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud";

// 获取用户列表
fetch(`${baseUrl}/users`)
  .then(response => response.json())
  .then(data => console.log(data));

// 创建用户
fetch(`${baseUrl}/users`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'JS测试用户',
    email: 'js@test.com',
    age: 25
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📋 API功能一览

### 用户管理
- ✅ `GET /users` - 获取用户列表（支持分页）
- ✅ `POST /users` - 创建新用户
- ✅ `GET /users/{id}` - 获取用户详情
- ✅ `PUT /users/{id}` - 更新用户信息
- ✅ `DELETE /users/{id}` - 删除用户

### 搜索功能
- ✅ `GET /users/search/{keyword}` - 搜索用户（姓名、邮箱）
- ✅ `GET /users/age-range/{min}/{max}` - 按年龄范围查询

### 系统功能
- ✅ `GET /health` - 健康检查
- ✅ `GET /stats` - API性能统计
- ✅ `GET /` - 美观的首页

## 🔧 开发工具

### 云主机启动脚本

```bash
# 显示云主机信息
python cloud_start.py --info

# 启动API服务（基础）
python cloud_start.py

# 启动API服务（含演示数据）
python cloud_start.py --demo

# 运行API测试
python cloud_start.py --test

# 指定端口启动
python cloud_start.py --port 9000

# 设置环境
python cloud_start.py --setup
```

### 传统运行脚本

```bash
# 显示项目状态
python run.py --status

# 启动开发服务器
python run.py

# 运行测试
python run.py --test

# 运行负载测试
python run.py --load-test --users 20 --duration 60

# 部署到AWS
python run.py --deploy aws --stage prod
```

## 🚀 部署到生产环境

### AWS Lambda部署

```bash
# 使用部署脚本
./deploy.sh aws prod

# 或使用运行脚本
python run.py --deploy aws --stage prod
```

### 阿里云函数计算

```bash
./deploy.sh aliyun prod
```

### 腾讯云函数

```bash
./deploy.sh tencent prod
```

### Docker部署

```bash
# 构建镜像
./deploy.sh docker

# 或
python run.py --deploy docker
```

## 📊 监控和维护

### 性能监控

```bash
# 启动监控（1小时）
python monitoring/performance_monitor.py \
  --url https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud \
  --duration 1 \
  --email-user your-email@gmail.com

# 单次健康检查
python monitoring/performance_monitor.py \
  --url https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud \
  --single
```

### 负载测试

```bash
# 负载测试
python tests/load_test.py \
  --url https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud \
  --users 50 \
  --duration 120
```

## 🎨 自定义配置

### 环境变量

复制 `config/environment.example` 为 `.env` 并修改：

```bash
cp config/environment.example .env
```

主要配置项：

```bash
# 云主机配置
CLOUD_HOST=gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud
API_PORT=8888
ENVIRONMENT=cloud-production

# 监控配置
MONITOR_INTERVAL=60
ALERT_EMAIL=your-email@gmail.com

# 数据存储
USER_DATA_FILE=/tmp/users.json
```

## 🐛 故障排查

### 常见问题

1. **端口被占用**
   ```bash
   # 使用其他端口
   python cloud_start.py --port 9000
   ```

2. **依赖缺失**
   ```bash
   # 重新安装依赖
   python cloud_start.py --setup
   ```

3. **API无法访问**
   - 检查云主机防火墙设置
   - 确认端口8888已开放
   - 查看服务器日志

4. **JupyterLab无法使用**
   - 确认JupyterLab服务正在运行
   - 检查项目文件路径

### 查看日志

```bash
# 查看API服务日志
tail -f /var/log/user-api/app.log

# 查看云主机系统日志
journalctl -f -u your-service-name
```

## 📚 文档和资源

- 📖 [完整项目文档](README.md)
- 📝 [详细开发指南](test0730.md)
- 💻 [JupyterLab开发环境](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest)
- 🌐 [API在线文档](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/docs)

## 🆘 获取帮助

如果遇到问题：

1. 📖 查看 [API文档](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/docs)
2. 🔍 检查 [健康状态](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/health)
3. 📊 查看 [性能统计](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/stats)
4. 💻 使用 [JupyterLab调试](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest)

## 🎉 开始您的API之旅！

现在您已经拥有了一个完整的、生产就绪的用户管理API！

- 🌐 访问 [API首页](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud) 开始体验
- 📖 查看 [Swagger文档](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/docs) 进行API测试
- 💻 在 [JupyterLab](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest) 中继续开发
- 🚀 部署到您喜欢的Serverless平台

**祝您开发愉快！** 🎊 