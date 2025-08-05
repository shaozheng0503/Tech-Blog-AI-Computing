# 🎯 机器学习训练完成通知系统

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> 一个智能的机器学习训练监控和通知系统，支持邮件、微信、短信等多种通知方式

## 📖 项目简介

机器学习训练通知系统是一个Python程序，能够在机器学习模型训练完成后自动发送通知到您的邮箱、微信或手机，并生成详细的训练报告。无论您是在本地训练还是在云服务器上训练，都能及时获得训练完成的通知。

### 🌟 主要特性

- **🔔 多种通知方式**：支持邮件、微信（钉钉/企业微信）、短信通知
- **📊 智能监控**：实时监控训练进度和系统资源使用情况
- **📈 详细报告**：自动生成包含训练指标、系统资源、性能分析的Markdown报告
- **⚙️ 灵活配置**：支持YAML配置文件，易于定制
- **🚀 快速开始**：提供简化版本，5分钟即可上手
- **🔧 易于集成**：可以轻松集成到现有的训练代码中

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/your-username/ml-training-notifier.git
cd ml-training-notifier

# 安装依赖
pip install -r requirements.txt
```

### 2. 快速体验

```bash
# 运行快速开始脚本
python quick_start.py
```

按照提示配置通知设置，即可开始使用！

### 3. 完整功能使用

```bash
# 运行完整版本
python ml_training_notifier.py
```

## 📁 项目结构

```
ml-training-notifier/
├── ml_training_notifier.py      # 完整功能版本
├── quick_start.py              # 快速开始版本
├── requirements.txt            # 依赖包列表
├── README.md                   # 项目说明
├── 机器学习训练通知系统使用指南.md  # 详细使用指南
├── notifier_config.yaml        # 配置文件（自动生成）
├── simple_config.json          # 简化配置（自动生成）
├── reports/                    # 训练报告目录
└── logs/                       # 日志文件目录
```

## 🔧 配置说明

### 邮件通知配置

```yaml
email:
  smtp_server: smtp.gmail.com
  smtp_port: 587
  username: your_email@gmail.com
  password: your_app_password
  from_email: your_email@gmail.com
  to_emails: ['recipient@example.com']
```

### 微信通知配置

```yaml
wechat:
  webhook_url: https://oapi.dingtalk.com/robot/send?access_token=your_token
```

### 短信通知配置

```yaml
phone:
  provider: aliyun
  api_key: your_api_key
  api_secret: your_api_secret
  phone_numbers: ['13800138000']
  sign_name: ML训练
  template_code: SMS_123456789
```

## 💻 使用示例

### 基本使用

```python
from ml_training_notifier import TrainingMonitor

# 初始化监控器
monitor = TrainingMonitor()

# 开始监控训练
monitor.start_monitoring(
    model_name="ResNet50",
    training_func=your_training_function,
    epochs=100,
    dataset_size=50000,
    batch_size=32,
    learning_rate=0.001,
    optimizer="Adam"
)
```

### 集成到现有代码

```python
def your_training_function(epochs, **kwargs):
    # 您的训练代码
    for epoch in range(epochs):
        # 训练逻辑
        pass
    
    # 返回训练结果
    return {
        'final_loss': 0.1234,
        'final_accuracy': 0.95,
        'best_epoch': 85,
        'best_accuracy': 0.96,
        'epochs': epochs
    }
```

## 📧 通知方式详解

### 1. 邮件通知

支持多种邮箱服务：
- **Gmail**：需要开启两步验证和应用专用密码
- **QQ邮箱**：使用授权码而非登录密码
- **企业邮箱**：支持SMTP协议的企业邮箱

### 2. 微信通知

支持两种方式：
- **钉钉机器人**：通过Webhook发送消息
- **企业微信应用**：通过企业微信API发送消息

### 3. 短信通知

支持主流云服务商：
- **阿里云短信**：稳定可靠，价格实惠
- **腾讯云短信**：功能丰富，支持多种模板

## 📊 报告示例

系统会自动生成详细的训练报告，包含：

- **训练概览**：模型名称、训练状态、时间信息
- **训练指标**：准确率、损失值、最佳轮数等
- **系统资源**：GPU使用率、内存使用率
- **性能分析**：训练效率、模型表现评估

## 🔧 高级功能

### 自定义训练检测

```python
class CustomTrainingMonitor(TrainingMonitor):
    def _is_training_completed(self) -> bool:
        # 自定义训练完成检测逻辑
        model_path = f"models/{self.metrics.model_name}.pth"
        return os.path.exists(model_path)
```

### 批量训练监控

```python
def monitor_multiple_training():
    models = [
        {"name": "ResNet50", "epochs": 100},
        {"name": "VGG16", "epochs": 50},
        {"name": "InceptionV3", "epochs": 75}
    ]
    
    monitors = []
    for model in models:
        monitor = TrainingMonitor()
        monitor.start_monitoring(model_name=model["name"], epochs=model["epochs"])
        monitors.append(monitor)
```

## 🛠️ 故障排除

### 常见问题

1. **邮件发送失败**
   - 检查用户名和密码
   - 确认开启了应用专用密码
   - 检查SMTP服务器设置

2. **微信通知失败**
   - 检查Webhook URL是否正确
   - 确认机器人没有被禁用
   - 检查消息格式

3. **短信发送失败**
   - 检查API密钥权限
   - 确认短信模板已审核
   - 检查签名设置

### 日志查看

```bash
# 查看实时日志
tail -f ml_notifier.log

# 查看错误日志
grep "ERROR" ml_notifier.log
```

## 📚 文档

- [详细使用指南](机器学习训练通知系统使用指南.md)
- [API文档](docs/api.md)
- [配置说明](docs/configuration.md)
- [故障排除](docs/troubleshooting.md)

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 贡献方式

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范

- 遵循PEP 8代码规范
- 添加适当的注释和文档
- 编写单元测试

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目的支持：

- [PyYAML](https://github.com/yaml/pyyaml) - YAML解析器
- [Requests](https://github.com/psf/requests) - HTTP库
- [psutil](https://github.com/giampaolo/psutil) - 系统监控
- [GPUtil](https://github.com/anderskm/gputil) - GPU监控

## 📞 联系方式

- **项目主页**：[GitHub](https://github.com/your-username/ml-training-notifier)
- **问题反馈**：[Issues](https://github.com/your-username/ml-training-notifier/issues)
- **邮箱**：your-email@example.com

## 📈 更新日志

### v1.0.0 (2024-12-XX)

- ✨ 初始版本发布
- 🔔 支持邮件、微信、短信通知
- 📊 自动生成训练报告
- ⚙️ 支持YAML配置文件
- 🚀 提供快速开始版本

---

**⭐ 如果这个项目对您有帮助，请给它一个星标！**
