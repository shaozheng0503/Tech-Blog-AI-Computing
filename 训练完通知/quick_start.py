#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器学习训练通知系统 - 快速开始脚本
Quick Start Script for ML Training Notification System

这是一个简化版本，让您能够快速开始使用训练通知功能。
"""

import os
import time
import json
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SimpleMLNotifier:
    """简化的机器学习训练通知器"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置"""
        config_file = "simple_config.json"
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置"""
        config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "your_email@gmail.com",
                "password": "your_app_password",
                "to_email": "recipient@example.com"
            },
            "wechat": {
                "enabled": False,
                "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=your_token"
            },
            "phone": {
                "enabled": False,
                "api_key": "your_api_key",
                "api_secret": "your_api_secret",
                "phone_number": "13800138000"
            }
        }
        
        # 保存默认配置
        with open("simple_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ 已创建默认配置文件: simple_config.json")
        print("📝 请编辑配置文件，填入您的通知设置")
        return config
    
    def send_email_notification(self, model_name, training_info):
        """发送邮件通知"""
        if not self.config["email"]["enabled"]:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["username"]
            msg['To'] = self.config["email"]["to_email"]
            msg['Subject'] = f"🎉 机器学习训练完成 - {model_name}"
            
            # 邮件正文
            body = f"""
            <html>
            <body>
                <h2>🎉 机器学习训练完成通知</h2>
                <p><strong>模型名称:</strong> {model_name}</p>
                <p><strong>完成时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>训练时长:</strong> {training_info.get('duration', '未知')}</p>
                <p><strong>最终准确率:</strong> {training_info.get('accuracy', '未知')}</p>
                <p><strong>最终损失:</strong> {training_info.get('loss', '未知')}</p>
                <br>
                <p>训练已完成，请检查结果！</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 发送邮件
            with smtplib.SMTP(self.config["email"]["smtp_server"], self.config["email"]["smtp_port"]) as server:
                server.starttls()
                server.login(self.config["email"]["username"], self.config["email"]["password"])
                server.send_message(msg)
            
            print("✅ 邮件通知发送成功")
            return True
            
        except Exception as e:
            print(f"❌ 邮件通知发送失败: {str(e)}")
            return False
    
    def send_wechat_notification(self, model_name, training_info):
        """发送微信通知"""
        if not self.config["wechat"]["enabled"]:
            return False
        
        try:
            message = {
                "msgtype": "text",
                "text": {
                    "content": f"🎉 机器学习训练完成通知\n\n模型: {model_name}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n准确率: {training_info.get('accuracy', '未知')}\n损失: {training_info.get('loss', '未知')}"
                }
            }
            
            response = requests.post(self.config["wechat"]["webhook_url"], json=message)
            if response.status_code == 200:
                print("✅ 微信通知发送成功")
                return True
            else:
                print(f"❌ 微信通知发送失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 微信通知发送失败: {str(e)}")
            return False
    
    def send_phone_notification(self, model_name, training_info):
        """发送短信通知"""
        if not self.config["phone"]["enabled"]:
            return False
        
        try:
            # 这里使用简化的短信发送方式
            # 实际使用时需要配置具体的短信服务商
            print("📱 短信通知功能需要配置具体的短信服务商")
            print(f"   模型: {model_name}")
            print(f"   准确率: {training_info.get('accuracy', '未知')}")
            return False
            
        except Exception as e:
            print(f"❌ 短信通知发送失败: {str(e)}")
            return False
    
    def notify_training_completion(self, model_name, training_info=None):
        """发送训练完成通知"""
        if training_info is None:
            training_info = {}
        
        print(f"🚀 发送训练完成通知: {model_name}")
        
        # 发送各种通知
        self.send_email_notification(model_name, training_info)
        self.send_wechat_notification(model_name, training_info)
        self.send_phone_notification(model_name, training_info)
        
        print("✅ 通知发送完成")
    
    def monitor_training(self, model_name, training_duration=3600):
        """监控训练过程（简化版）"""
        print(f"🔍 开始监控训练: {model_name}")
        print(f"⏰ 预计训练时长: {training_duration} 秒")
        
        # 模拟训练过程
        for i in range(training_duration // 10):  # 每10秒检查一次
            time.sleep(10)
            print(f"⏳ 训练进行中... ({i+1}/{training_duration//10})")
        
        # 训练完成，发送通知
        training_info = {
            'duration': f"{training_duration//3600}小时{(training_duration%3600)//60}分钟",
            'accuracy': '95.2%',
            'loss': '0.048'
        }
        
        self.notify_training_completion(model_name, training_info)

def setup_configuration():
    """交互式配置设置"""
    print("🔧 配置训练通知系统")
    print("=" * 50)
    
    config = {}
    
    # 邮件配置
    print("\n📧 邮件通知配置")
    email_enabled = input("是否启用邮件通知? (y/n): ").lower() == 'y'
    if email_enabled:
        config["email"] = {
            "enabled": True,
            "smtp_server": input("SMTP服务器 (默认: smtp.gmail.com): ") or "smtp.gmail.com",
            "smtp_port": int(input("SMTP端口 (默认: 587): ") or "587"),
            "username": input("邮箱地址: "),
            "password": input("应用专用密码: "),
            "to_email": input("接收通知的邮箱: ")
        }
    else:
        config["email"] = {"enabled": False}
    
    # 微信配置
    print("\n💬 微信通知配置")
    wechat_enabled = input("是否启用微信通知? (y/n): ").lower() == 'y'
    if wechat_enabled:
        config["wechat"] = {
            "enabled": True,
            "webhook_url": input("钉钉机器人Webhook地址: ")
        }
    else:
        config["wechat"] = {"enabled": False}
    
    # 短信配置
    print("\n📱 短信通知配置")
    phone_enabled = input("是否启用短信通知? (y/n): ").lower() == 'y'
    if phone_enabled:
        config["phone"] = {
            "enabled": True,
            "api_key": input("API密钥: "),
            "api_secret": input("API密钥: "),
            "phone_number": input("手机号码: ")
        }
    else:
        config["phone"] = {"enabled": False}
    
    # 保存配置
    with open("simple_config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("\n✅ 配置已保存到 simple_config.json")
    return config

def main():
    """主函数"""
    print("🎯 机器学习训练通知系统 - 快速开始")
    print("=" * 50)
    
    # 检查配置文件
    if not os.path.exists("simple_config.json"):
        print("📝 首次使用，需要配置通知设置")
        setup_configuration()
    
    # 创建通知器
    notifier = SimpleMLNotifier()
    
    # 选择操作
    print("\n请选择操作:")
    print("1. 重新配置通知设置")
    print("2. 发送测试通知")
    print("3. 监控训练过程")
    print("4. 直接发送训练完成通知")
    
    choice = input("\n请输入选择 (1-4): ")
    
    if choice == "1":
        setup_configuration()
        print("✅ 配置完成")
        
    elif choice == "2":
        print("\n🧪 发送测试通知")
        notifier.notify_training_completion("测试模型", {
            'duration': '30分钟',
            'accuracy': '98.5%',
            'loss': '0.015'
        })
        
    elif choice == "3":
        print("\n🔍 监控训练过程")
        model_name = input("请输入模型名称: ")
        duration = int(input("请输入预计训练时长(秒): ") or "3600")
        notifier.monitor_training(model_name, duration)
        
    elif choice == "4":
        print("\n📤 直接发送训练完成通知")
        model_name = input("请输入模型名称: ")
        duration = input("请输入训练时长: ")
        accuracy = input("请输入最终准确率: ")
        loss = input("请输入最终损失: ")
        
        training_info = {
            'duration': duration,
            'accuracy': accuracy,
            'loss': loss
        }
        
        notifier.notify_training_completion(model_name, training_info)
        
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 