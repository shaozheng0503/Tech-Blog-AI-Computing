#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习训练完成通知系统
Machine Learning Training Completion Notifier

功能：
1. 监控训练进度
2. 训练完成后发送通知到邮箱/微信/电话
3. 生成训练报告
4. 支持多种通知方式

作者：AI Assistant
版本：1.0.0
"""

import os
import time
import json
import smtplib
import requests
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
import threading
from typing import Dict, List, Optional, Any
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass, asdict
import psutil
import GPUtil

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_notifier.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TrainingMetrics:
    """训练指标数据类"""
    model_name: str
    start_time: str
    end_time: str
    duration: float
    epochs: int
    final_loss: float
    final_accuracy: float
    best_epoch: int
    best_accuracy: float
    gpu_usage: float
    memory_usage: float
    dataset_size: int
    batch_size: int
    learning_rate: float
    optimizer: str
    status: str  # 'running', 'completed', 'failed'
    error_message: Optional[str] = None

@dataclass
class NotificationConfig:
    """通知配置数据类"""
    email_enabled: bool = True
    wechat_enabled: bool = True
    phone_enabled: bool = False
    email_config: Dict = None
    wechat_config: Dict = None
    phone_config: Dict = None

class EmailNotifier:
    """邮件通知类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.smtp_server = config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = config.get('smtp_port', 587)
        self.username = config.get('username')
        self.password = config.get('password')
        self.from_email = config.get('from_email')
        self.to_emails = config.get('to_emails', [])
        
    def send_notification(self, metrics: TrainingMetrics, report_path: str = None):
        """发送邮件通知"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = f"🎉 机器学习训练完成通知 - {metrics.model_name}"
            
            # 邮件正文
            body = self._create_email_body(metrics)
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 附件训练报告
            if report_path and os.path.exists(report_path):
                with open(report_path, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype='pdf')
                    attachment.add_header('Content-Disposition', 'attachment', 
                                        filename=os.path.basename(report_path))
                    msg.attach(attachment)
            
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
            logger.info(f"邮件通知发送成功: {', '.join(self.to_emails)}")
            return True
            
        except Exception as e:
            logger.error(f"邮件通知发送失败: {str(e)}")
            return False
    
    def _create_email_body(self, metrics: TrainingMetrics) -> str:
        """创建邮件正文"""
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ margin: 20px 0; }}
                .metric {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; }}
                .success {{ color: #4CAF50; font-weight: bold; }}
                .error {{ color: #f44336; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 机器学习训练完成通知</h1>
            </div>
            <div class="content">
                <h2>模型信息</h2>
                <div class="metric"><strong>模型名称:</strong> {metrics.model_name}</div>
                <div class="metric"><strong>训练状态:</strong> 
                    <span class="{'success' if metrics.status == 'completed' else 'error'}">
                        {metrics.status.upper()}
                    </span>
                </div>
                <div class="metric"><strong>开始时间:</strong> {metrics.start_time}</div>
                <div class="metric"><strong>结束时间:</strong> {metrics.end_time}</div>
                <div class="metric"><strong>训练时长:</strong> {metrics.duration:.2f} 小时</div>
                
                <h2>训练指标</h2>
                <div class="metric"><strong>训练轮数:</strong> {metrics.epochs}</div>
                <div class="metric"><strong>最终损失:</strong> {metrics.final_loss:.4f}</div>
                <div class="metric"><strong>最终准确率:</strong> {metrics.final_accuracy:.2%}</div>
                <div class="metric"><strong>最佳轮数:</strong> {metrics.best_epoch}</div>
                <div class="metric"><strong>最佳准确率:</strong> {metrics.best_accuracy:.2%}</div>
                
                <h2>资源使用</h2>
                <div class="metric"><strong>GPU使用率:</strong> {metrics.gpu_usage:.1%}</div>
                <div class="metric"><strong>内存使用率:</strong> {metrics.memory_usage:.1%}</div>
                
                <h2>训练配置</h2>
                <div class="metric"><strong>数据集大小:</strong> {metrics.dataset_size:,}</div>
                <div class="metric"><strong>批次大小:</strong> {metrics.batch_size}</div>
                <div class="metric"><strong>学习率:</strong> {metrics.learning_rate}</div>
                <div class="metric"><strong>优化器:</strong> {metrics.optimizer}</div>
                
                {f'<h2>错误信息</h2><div class="metric error">{metrics.error_message}</div>' if metrics.error_message else ''}
            </div>
        </body>
        </html>
        """

class WeChatNotifier:
    """微信通知类（企业微信/钉钉）"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.webhook_url = config.get('webhook_url')
        self.access_token = config.get('access_token')
        self.agent_id = config.get('agent_id')
        self.corp_id = config.get('corp_id')
        self.secret = config.get('secret')
        
    def send_notification(self, metrics: TrainingMetrics):
        """发送微信通知"""
        try:
            if self.webhook_url:  # 钉钉/企业微信机器人
                return self._send_webhook_notification(metrics)
            elif self.access_token:  # 企业微信应用
                return self._send_wechat_app_notification(metrics)
            else:
                logger.error("微信通知配置不完整")
                return False
                
        except Exception as e:
            logger.error(f"微信通知发送失败: {str(e)}")
            return False
    
    def _send_webhook_notification(self, metrics: TrainingMetrics) -> bool:
        """通过Webhook发送通知"""
        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": f"🎉 机器学习训练完成通知",
                "text": self._create_wechat_message(metrics)
            }
        }
        
        response = requests.post(self.webhook_url, json=message)
        if response.status_code == 200:
            logger.info("微信Webhook通知发送成功")
            return True
        else:
            logger.error(f"微信Webhook通知发送失败: {response.text}")
            return False
    
    def _send_wechat_app_notification(self, metrics: TrainingMetrics) -> bool:
        """通过企业微信应用发送通知"""
        # 获取access_token
        token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.secret}"
        token_response = requests.get(token_url)
        token_data = token_response.json()
        
        if token_data.get('errcode') != 0:
            logger.error(f"获取企业微信token失败: {token_data}")
            return False
        
        access_token = token_data['access_token']
        
        # 发送消息
        message_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        message_data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {
                "content": self._create_wechat_text_message(metrics)
            }
        }
        
        response = requests.post(message_url, json=message_data)
        if response.json().get('errcode') == 0:
            logger.info("企业微信应用通知发送成功")
            return True
        else:
            logger.error(f"企业微信应用通知发送失败: {response.json()}")
            return False
    
    def _create_wechat_message(self, metrics: TrainingMetrics) -> str:
        """创建微信Markdown消息"""
        status_emoji = "✅" if metrics.status == 'completed' else "❌"
        return f"""
## 🎉 机器学习训练完成通知

**模型名称:** {metrics.model_name}
**训练状态:** {status_emoji} {metrics.status.upper()}

### 📊 训练指标
- **训练时长:** {metrics.duration:.2f} 小时
- **训练轮数:** {metrics.epochs}
- **最终准确率:** {metrics.final_accuracy:.2%}
- **最佳准确率:** {metrics.best_accuracy:.2%}
- **最终损失:** {metrics.final_loss:.4f}

### 💻 资源使用
- **GPU使用率:** {metrics.gpu_usage:.1%}
- **内存使用率:** {metrics.memory_usage:.1%}

### ⚙️ 训练配置
- **数据集大小:** {metrics.dataset_size:,}
- **批次大小:** {metrics.batch_size}
- **学习率:** {metrics.learning_rate}
- **优化器:** {metrics.optimizer}

{f'### ❌ 错误信息\n{metrics.error_message}' if metrics.error_message else ''}
        """
    
    def _create_wechat_text_message(self, metrics: TrainingMetrics) -> str:
        """创建微信文本消息"""
        status_emoji = "✅" if metrics.status == 'completed' else "❌"
        return f"""
🎉 机器学习训练完成通知

模型: {metrics.model_name}
状态: {status_emoji} {metrics.status.upper()}
时长: {metrics.duration:.2f} 小时
准确率: {metrics.final_accuracy:.2%}
损失: {metrics.final_loss:.4f}
        """

class PhoneNotifier:
    """电话通知类（短信/语音）"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('api_key')
        self.api_secret = config.get('api_secret')
        self.phone_numbers = config.get('phone_numbers', [])
        self.provider = config.get('provider', 'aliyun')  # aliyun, tencent, huawei
        
    def send_notification(self, metrics: TrainingMetrics):
        """发送电话通知"""
        try:
            if self.provider == 'aliyun':
                return self._send_aliyun_sms(metrics)
            elif self.provider == 'tencent':
                return self._send_tencent_sms(metrics)
            else:
                logger.error(f"不支持的短信服务商: {self.provider}")
                return False
                
        except Exception as e:
            logger.error(f"电话通知发送失败: {str(e)}")
            return False
    
    def _send_aliyun_sms(self, metrics: TrainingMetrics) -> bool:
        """发送阿里云短信"""
        # 这里需要安装阿里云SDK: pip install aliyun-python-sdk-core aliyun-python-sdk-dysmsapi
        try:
            from aliyunsdkcore.client import AcsClient
            from aliyunsdkcore.request import CommonRequest
            
            client = AcsClient(self.api_key, self.api_secret, 'cn-hangzhou')
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain('dysmsapi.aliyuncs.com')
            request.set_method('POST')
            request.set_protocol_type('https')
            request.set_version('2017-05-25')
            request.set_action_name('SendSms')
            
            # 短信模板参数
            template_param = {
                "model_name": metrics.model_name,
                "status": metrics.status,
                "accuracy": f"{metrics.final_accuracy:.2%}",
                "duration": f"{metrics.duration:.2f}h"
            }
            
            request.add_query_param('PhoneNumbers', ','.join(self.phone_numbers))
            request.add_query_param('SignName', self.config.get('sign_name', 'ML训练'))
            request.add_query_param('TemplateCode', self.config.get('template_code'))
            request.add_query_param('TemplateParam', json.dumps(template_param))
            
            response = client.do_action_with_exception(request)
            response_data = json.loads(response)
            
            if response_data.get('Code') == 'OK':
                logger.info("阿里云短信发送成功")
                return True
            else:
                logger.error(f"阿里云短信发送失败: {response_data}")
                return False
                
        except ImportError:
            logger.error("请安装阿里云SDK: pip install aliyun-python-sdk-core aliyun-python-sdk-dysmsapi")
            return False
    
    def _send_tencent_sms(self, metrics: TrainingMetrics) -> bool:
        """发送腾讯云短信"""
        # 这里需要安装腾讯云SDK: pip install tencentcloud-sdk-python
        try:
            from tencentcloud.common import credential
            from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
            from tencentcloud.sms.v20210111 import sms_client, models
            
            cred = credential.Credential(self.api_key, self.api_secret)
            client = sms_client.SmsClient(cred, "ap-guangzhou")
            
            req = models.SendSmsRequest()
            req.PhoneNumberSet = [f"+86{phone}" for phone in self.phone_numbers]
            req.SmsSdkAppId = self.config.get('sdk_app_id')
            req.SignName = self.config.get('sign_name', 'ML训练')
            req.TemplateId = self.config.get('template_id')
            req.TemplateParamSet = [
                metrics.model_name,
                metrics.status,
                f"{metrics.final_accuracy:.2%}",
                f"{metrics.duration:.2f}h"
            ]
            
            resp = client.SendSms(req)
            if resp.SendStatusSet[0].Code == "Ok":
                logger.info("腾讯云短信发送成功")
                return True
            else:
                logger.error(f"腾讯云短信发送失败: {resp.SendStatusSet[0].Message}")
                return False
                
        except ImportError:
            logger.error("请安装腾讯云SDK: pip install tencentcloud-sdk-python")
            return False

class TrainingMonitor:
    """训练监控器"""
    
    def __init__(self, config_path: str = "notifier_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.notifiers = self._init_notifiers()
        self.metrics = None
        self.monitoring = False
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            logger.warning(f"配置文件 {self.config_path} 不存在，使用默认配置")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'notifications': {
                'email_enabled': True,
                'wechat_enabled': True,
                'phone_enabled': False,
                'email': {
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'username': 'your_email@gmail.com',
                    'password': 'your_app_password',
                    'from_email': 'your_email@gmail.com',
                    'to_emails': ['recipient@example.com']
                },
                'wechat': {
                    'webhook_url': 'https://oapi.dingtalk.com/robot/send?access_token=your_token',
                    'access_token': 'your_wechat_token',
                    'agent_id': 'your_agent_id',
                    'corp_id': 'your_corp_id',
                    'secret': 'your_secret'
                },
                'phone': {
                    'provider': 'aliyun',
                    'api_key': 'your_api_key',
                    'api_secret': 'your_api_secret',
                    'phone_numbers': ['13800138000'],
                    'sign_name': 'ML训练',
                    'template_code': 'SMS_123456789'
                }
            },
            'monitoring': {
                'check_interval': 60,  # 检查间隔（秒）
                'gpu_threshold': 0.1,  # GPU使用率阈值
                'memory_threshold': 0.1  # 内存使用率阈值
            },
            'reporting': {
                'save_path': './reports',
                'generate_plots': True,
                'include_system_info': True
            }
        }
    
    def _init_notifiers(self) -> Dict:
        """初始化通知器"""
        notifiers = {}
        config = self.config['notifications']
        
        if config.get('email_enabled', False):
            notifiers['email'] = EmailNotifier(config['email'])
        
        if config.get('wechat_enabled', False):
            notifiers['wechat'] = WeChatNotifier(config['wechat'])
        
        if config.get('phone_enabled', False):
            notifiers['phone'] = PhoneNotifier(config['phone'])
        
        return notifiers
    
    def start_monitoring(self, model_name: str, training_func=None, **kwargs):
        """开始监控训练"""
        self.monitoring = True
        self.metrics = TrainingMetrics(
            model_name=model_name,
            start_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            end_time='',
            duration=0.0,
            epochs=kwargs.get('epochs', 0),
            final_loss=0.0,
            final_accuracy=0.0,
            best_epoch=0,
            best_accuracy=0.0,
            gpu_usage=0.0,
            memory_usage=0.0,
            dataset_size=kwargs.get('dataset_size', 0),
            batch_size=kwargs.get('batch_size', 32),
            learning_rate=kwargs.get('learning_rate', 0.001),
            optimizer=kwargs.get('optimizer', 'Adam'),
            status='running'
        )
        
        # 启动监控线程
        monitor_thread = threading.Thread(target=self._monitor_training, args=(training_func, kwargs))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        logger.info(f"开始监控训练: {model_name}")
    
    def _monitor_training(self, training_func, kwargs):
        """监控训练过程"""
        start_time = time.time()
        check_interval = self.config['monitoring']['check_interval']
        
        try:
            # 如果提供了训练函数，执行训练
            if training_func:
                result = training_func(**kwargs)
                self._update_metrics_from_result(result)
            
            # 监控训练状态
            while self.monitoring:
                # 检查系统资源
                self._update_system_metrics()
                
                # 检查训练是否完成
                if self._is_training_completed():
                    break
                
                time.sleep(check_interval)
            
            # 训练完成，发送通知
            self._complete_training(start_time)
            
        except Exception as e:
            logger.error(f"训练监控出错: {str(e)}")
            self.metrics.status = 'failed'
            self.metrics.error_message = str(e)
            self._complete_training(start_time)
    
    def _update_system_metrics(self):
        """更新系统指标"""
        # 内存使用率
        memory = psutil.virtual_memory()
        self.metrics.memory_usage = memory.percent / 100.0
        
        # GPU使用率
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                self.metrics.gpu_usage = gpus[0].load
        except:
            self.metrics.gpu_usage = 0.0
    
    def _is_training_completed(self) -> bool:
        """检查训练是否完成"""
        # 这里可以根据实际情况检查训练状态
        # 例如检查特定的文件、进程等
        return False
    
    def _update_metrics_from_result(self, result: Dict):
        """从训练结果更新指标"""
        if result:
            self.metrics.final_loss = result.get('final_loss', 0.0)
            self.metrics.final_accuracy = result.get('final_accuracy', 0.0)
            self.metrics.best_epoch = result.get('best_epoch', 0)
            self.metrics.best_accuracy = result.get('best_accuracy', 0.0)
            self.metrics.epochs = result.get('epochs', 0)
    
    def _complete_training(self, start_time: float):
        """完成训练并发送通知"""
        self.monitoring = False
        self.metrics.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.metrics.duration = (time.time() - start_time) / 3600  # 转换为小时
        
        if self.metrics.status != 'failed':
            self.metrics.status = 'completed'
        
        # 生成报告
        report_path = self._generate_report()
        
        # 发送通知
        self._send_notifications(report_path)
        
        logger.info(f"训练监控完成: {self.metrics.model_name}")
    
    def _generate_report(self) -> str:
        """生成训练报告"""
        try:
            report_dir = self.config['reporting']['save_path']
            os.makedirs(report_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = os.path.join(report_dir, f"training_report_{timestamp}.md")
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(self._create_markdown_report())
            
            logger.info(f"训练报告已生成: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"生成报告失败: {str(e)}")
            return None
    
    def _create_markdown_report(self) -> str:
        """创建Markdown格式的报告"""
        return f"""
# 机器学习训练报告

## 📊 训练概览

- **模型名称**: {self.metrics.model_name}
- **训练状态**: {self.metrics.status.upper()}
- **开始时间**: {self.metrics.start_time}
- **结束时间**: {self.metrics.end_time}
- **训练时长**: {self.metrics.duration:.2f} 小时

## 🎯 训练指标

| 指标 | 值 |
|------|-----|
| 训练轮数 | {self.metrics.epochs} |
| 最终损失 | {self.metrics.final_loss:.4f} |
| 最终准确率 | {self.metrics.final_accuracy:.2%} |
| 最佳轮数 | {self.metrics.best_epoch} |
| 最佳准确率 | {self.metrics.best_accuracy:.2%} |

## 💻 系统资源

| 资源 | 使用率 |
|------|--------|
| GPU使用率 | {self.metrics.gpu_usage:.1%} |
| 内存使用率 | {self.metrics.memory_usage:.1%} |

## ⚙️ 训练配置

| 参数 | 值 |
|------|-----|
| 数据集大小 | {self.metrics.dataset_size:,} |
| 批次大小 | {self.metrics.batch_size} |
| 学习率 | {self.metrics.learning_rate} |
| 优化器 | {self.metrics.optimizer} |

{f'## ❌ 错误信息\n\n{self.metrics.error_message}' if self.metrics.error_message else ''}

## 📈 性能分析

### 训练效率
- 平均每轮训练时间: {self.metrics.duration / max(self.metrics.epochs, 1):.2f} 小时/轮
- 资源利用率: {(self.metrics.gpu_usage + self.metrics.memory_usage) / 2:.1%}

### 模型表现
- 准确率提升: {(self.metrics.final_accuracy - self.metrics.best_accuracy) * 100:.2f}%
- 训练稳定性: {'良好' if self.metrics.final_accuracy > 0.8 else '需要优化'}

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
        """
    
    def _send_notifications(self, report_path: str = None):
        """发送所有通知"""
        for name, notifier in self.notifiers.items():
            try:
                if name == 'email':
                    notifier.send_notification(self.metrics, report_path)
                else:
                    notifier.send_notification(self.metrics)
                logger.info(f"{name} 通知发送成功")
            except Exception as e:
                logger.error(f"{name} 通知发送失败: {str(e)}")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        logger.info("训练监控已停止")

def create_config_template():
    """创建配置文件模板"""
    config = {
        'notifications': {
            'email_enabled': True,
            'wechat_enabled': True,
            'phone_enabled': False,
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'username': 'your_email@gmail.com',
                'password': 'your_app_password',
                'from_email': 'your_email@gmail.com',
                'to_emails': ['recipient@example.com']
            },
            'wechat': {
                'webhook_url': 'https://oapi.dingtalk.com/robot/send?access_token=your_token',
                'access_token': 'your_wechat_token',
                'agent_id': 'your_agent_id',
                'corp_id': 'your_corp_id',
                'secret': 'your_secret'
            },
            'phone': {
                'provider': 'aliyun',
                'api_key': 'your_api_key',
                'api_secret': 'your_api_secret',
                'phone_numbers': ['13800138000'],
                'sign_name': 'ML训练',
                'template_code': 'SMS_123456789'
            }
        },
        'monitoring': {
            'check_interval': 60,
            'gpu_threshold': 0.1,
            'memory_threshold': 0.1
        },
        'reporting': {
            'save_path': './reports',
            'generate_plots': True,
            'include_system_info': True
        }
    }
    
    with open('notifier_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print("配置文件模板已创建: notifier_config.yaml")

# 使用示例
def example_training_function(epochs=10, **kwargs):
    """示例训练函数"""
    import time
    import random
    
    print("开始训练...")
    for epoch in range(epochs):
        time.sleep(1)  # 模拟训练时间
        loss = 1.0 - (epoch + 1) * 0.08 + random.uniform(-0.02, 0.02)
        accuracy = 0.1 + (epoch + 1) * 0.08 + random.uniform(-0.02, 0.02)
        print(f"Epoch {epoch+1}/{epochs}: Loss={loss:.4f}, Accuracy={accuracy:.4f}")
    
    return {
        'final_loss': loss,
        'final_accuracy': accuracy,
        'best_epoch': epochs,
        'best_accuracy': accuracy,
        'epochs': epochs
    }

if __name__ == "__main__":
    # 创建配置文件模板
    create_config_template()
    
    # 初始化监控器
    monitor = TrainingMonitor()
    
    # 开始监控训练
    monitor.start_monitoring(
        model_name="ResNet50",
        training_func=example_training_function,
        epochs=5,
        dataset_size=10000,
        batch_size=32,
        learning_rate=0.001,
        optimizer="Adam"
    )
    
    # 等待训练完成
    try:
        while monitor.monitoring:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n用户中断训练")
        monitor.stop_monitoring() 