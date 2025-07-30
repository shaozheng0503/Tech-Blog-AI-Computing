#!/usr/bin/env python3
"""
Serverless应用性能监控脚本

功能:
- 监控API响应时间
- 检查服务可用性
- 生成性能报告
- 发送告警通知
"""

import boto3
import time
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import argparse
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class AlertConfig:
    """告警配置"""
    email_host: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: str = ""
    email_password: str = ""
    alert_recipients: List[str] = None
    
    def __post_init__(self):
        if self.alert_recipients is None:
            self.alert_recipients = []

@dataclass
class MonitorConfig:
    """监控配置"""
    api_url: str
    check_interval: int = 60  # 秒
    response_timeout: int = 30  # 秒
    max_response_time: float = 2.0  # 秒
    min_success_rate: float = 95.0  # 百分比
    
class CloudWatchMonitor:
    """AWS CloudWatch监控"""
    
    def __init__(self, function_name: str, region: str = 'us-west-2'):
        self.function_name = function_name
        self.region = region
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.logs_client = boto3.client('logs', region_name=region)
    
    def get_lambda_metrics(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """获取Lambda函数指标"""
        try:
            metrics = {}
            
            # 获取调用次数
            invocations = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Invocations',
                Dimensions=[
                    {'Name': 'FunctionName', 'Value': self.function_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Sum']
            )
            
            # 获取错误次数
            errors = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Errors',
                Dimensions=[
                    {'Name': 'FunctionName', 'Value': self.function_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Sum']
            )
            
            # 获取持续时间
            duration = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Duration',
                Dimensions=[
                    {'Name': 'FunctionName', 'Value': self.function_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum']
            )
            
            # 获取并发执行数
            concurrent = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='ConcurrentExecutions',
                Dimensions=[
                    {'Name': 'FunctionName', 'Value': self.function_name}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Maximum']
            )
            
            # 处理数据
            total_invocations = sum(point['Sum'] for point in invocations['Datapoints'])
            total_errors = sum(point['Sum'] for point in errors['Datapoints'])
            
            avg_duration = 0
            max_duration = 0
            if duration['Datapoints']:
                avg_duration = sum(point['Average'] for point in duration['Datapoints']) / len(duration['Datapoints'])
                max_duration = max(point['Maximum'] for point in duration['Datapoints'])
            
            max_concurrent = 0
            if concurrent['Datapoints']:
                max_concurrent = max(point['Maximum'] for point in concurrent['Datapoints'])
            
            metrics = {
                'invocations': total_invocations,
                'errors': total_errors,
                'error_rate': (total_errors / total_invocations * 100) if total_invocations > 0 else 0,
                'avg_duration': avg_duration,
                'max_duration': max_duration,
                'max_concurrent': max_concurrent,
                'period': f"{start_time} - {end_time}"
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"获取CloudWatch指标失败: {e}")
            return {}
    
    def get_recent_logs(self, hours: int = 1, error_only: bool = False) -> List[Dict]:
        """获取最近的日志"""
        try:
            log_group = f"/aws/lambda/{self.function_name}"
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            filter_pattern = "ERROR" if error_only else ""
            
            response = self.logs_client.filter_log_events(
                logGroupName=log_group,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000),
                filterPattern=filter_pattern,
                limit=100
            )
            
            logs = []
            for event in response.get('events', []):
                logs.append({
                    'timestamp': datetime.fromtimestamp(event['timestamp'] / 1000),
                    'message': event['message'],
                    'stream': event.get('logStreamName', '')
                })
            
            return logs
            
        except Exception as e:
            logger.error(f"获取日志失败: {e}")
            return []

class APIMonitor:
    """API监控器"""
    
    def __init__(self, config: MonitorConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ServerlessMonitor/1.0'
        })
    
    def check_health(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            start_time = time.time()
            response = self.session.get(
                self.config.api_url,
                timeout=self.config.response_timeout
            )
            response_time = time.time() - start_time
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': response_time,
                'timestamp': datetime.now(),
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'status_code': 0,
                'response_time': time.time() - start_time,
                'timestamp': datetime.now(),
                'error': str(e)
            }
    
    def check_endpoints(self) -> List[Dict[str, Any]]:
        """检查多个端点"""
        endpoints = [
            {'path': '/', 'method': 'GET', 'name': '健康检查'},
            {'path': '/users', 'method': 'GET', 'name': '用户列表'},
            {'path': '/stats', 'method': 'GET', 'name': '统计信息'},
            {'path': '/users/1', 'method': 'GET', 'name': '获取用户'},
        ]
        
        results = []
        for endpoint in endpoints:
            try:
                url = f"{self.config.api_url.rstrip('/')}{endpoint['path']}"
                start_time = time.time()
                
                if endpoint['method'] == 'GET':
                    response = self.session.get(url, timeout=self.config.response_timeout)
                elif endpoint['method'] == 'POST':
                    response = self.session.post(url, timeout=self.config.response_timeout)
                else:
                    continue
                
                response_time = time.time() - start_time
                
                results.append({
                    'endpoint': endpoint['name'],
                    'path': endpoint['path'],
                    'method': endpoint['method'],
                    'success': response.status_code < 400,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'timestamp': datetime.now(),
                    'error': None
                })
                
            except Exception as e:
                results.append({
                    'endpoint': endpoint['name'],
                    'path': endpoint['path'],
                    'method': endpoint['method'],
                    'success': False,
                    'status_code': 0,
                    'response_time': 0,
                    'timestamp': datetime.now(),
                    'error': str(e)
                })
        
        return results

class AlertManager:
    """告警管理器"""
    
    def __init__(self, config: AlertConfig):
        self.config = config
    
    def send_email_alert(self, subject: str, message: str) -> bool:
        """发送邮件告警"""
        if not self.config.alert_recipients:
            logger.warning("未配置告警收件人")
            return False
        
        try:
            msg = MimeMultipart()
            msg['From'] = self.config.email_user
            msg['To'] = ', '.join(self.config.alert_recipients)
            msg['Subject'] = f"[Serverless Alert] {subject}"
            
            msg.attach(MimeText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(self.config.email_host, self.config.email_port)
            server.starttls()
            server.login(self.config.email_user, self.config.email_password)
            
            text = msg.as_string()
            server.sendmail(self.config.email_user, self.config.alert_recipients, text)
            server.quit()
            
            logger.info("告警邮件发送成功")
            return True
            
        except Exception as e:
            logger.error(f"发送告警邮件失败: {e}")
            return False
    
    def check_and_alert(self, health_result: Dict, endpoint_results: List[Dict]) -> None:
        """检查指标并发送告警"""
        alerts = []
        
        # 检查主要健康状态
        if not health_result['success']:
            alerts.append(f"API健康检查失败: {health_result.get('error', 'Unknown error')}")
        
        # 检查响应时间
        if health_result['response_time'] > 2.0:  # 2秒阈值
            alerts.append(f"响应时间过长: {health_result['response_time']:.2f}秒")
        
        # 检查端点失败率
        failed_endpoints = [r for r in endpoint_results if not r['success']]
        if len(failed_endpoints) > 0:
            failure_rate = len(failed_endpoints) / len(endpoint_results) * 100
            if failure_rate > 20:  # 20%失败率阈值
                alerts.append(f"端点失败率过高: {failure_rate:.1f}% ({len(failed_endpoints)}/{len(endpoint_results)})")
        
        # 发送告警
        if alerts:
            subject = "Serverless API告警"
            message = "检测到以下问题:\n\n"
            message += "\n".join(f"- {alert}" for alert in alerts)
            message += f"\n\n检查时间: {datetime.now()}"
            message += f"\nAPI地址: {health_result.get('api_url', 'Unknown')}"
            
            self.send_email_alert(subject, message)

class PerformanceReporter:
    """性能报告生成器"""
    
    def __init__(self):
        self.health_history = []
        self.endpoint_history = []
    
    def add_health_record(self, record: Dict) -> None:
        """添加健康检查记录"""
        self.health_history.append(record)
        
        # 保留最近1000条记录
        if len(self.health_history) > 1000:
            self.health_history = self.health_history[-1000:]
    
    def add_endpoint_records(self, records: List[Dict]) -> None:
        """添加端点检查记录"""
        self.endpoint_history.extend(records)
        
        # 保留最近5000条记录
        if len(self.endpoint_history) > 5000:
            self.endpoint_history = self.endpoint_history[-5000:]
    
    def generate_report(self, hours: int = 24) -> Dict[str, Any]:
        """生成性能报告"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # 过滤时间范围内的记录
        recent_health = [r for r in self.health_history if r['timestamp'] > cutoff_time]
        recent_endpoints = [r for r in self.endpoint_history if r['timestamp'] > cutoff_time]
        
        if not recent_health:
            return {"error": "没有可用的监控数据"}
        
        # 计算统计信息
        total_checks = len(recent_health)
        successful_checks = len([r for r in recent_health if r['success']])
        success_rate = (successful_checks / total_checks) * 100 if total_checks > 0 else 0
        
        response_times = [r['response_time'] for r in recent_health if r['success']]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        
        # 按端点统计
        endpoint_stats = {}
        for record in recent_endpoints:
            endpoint = record['endpoint']
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {
                    'total': 0,
                    'successful': 0,
                    'response_times': []
                }
            
            endpoint_stats[endpoint]['total'] += 1
            if record['success']:
                endpoint_stats[endpoint]['successful'] += 1
                endpoint_stats[endpoint]['response_times'].append(record['response_time'])
        
        # 处理端点统计
        for endpoint, stats in endpoint_stats.items():
            stats['success_rate'] = (stats['successful'] / stats['total']) * 100
            if stats['response_times']:
                stats['avg_response_time'] = sum(stats['response_times']) / len(stats['response_times'])
            else:
                stats['avg_response_time'] = 0
            del stats['response_times']  # 移除原始数据
        
        report = {
            'period': f"过去{hours}小时",
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_checks': total_checks,
                'successful_checks': successful_checks,
                'success_rate': round(success_rate, 2),
                'avg_response_time': round(avg_response_time * 1000, 2),  # 转换为毫秒
                'max_response_time': round(max_response_time * 1000, 2),
                'min_response_time': round(min_response_time * 1000, 2)
            },
            'endpoint_stats': endpoint_stats,
            'health_status': 'Good' if success_rate >= 95 and avg_response_time < 1.0 else 'Warning' if success_rate >= 90 else 'Critical'
        }
        
        return report
    
    def save_report(self, report: Dict, filename: Optional[str] = None) -> str:
        """保存报告到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return filename

class ServerlessMonitor:
    """Serverless监控主类"""
    
    def __init__(self, 
                 monitor_config: MonitorConfig,
                 alert_config: AlertConfig,
                 cloudwatch_function_name: Optional[str] = None):
        self.monitor_config = monitor_config
        self.api_monitor = APIMonitor(monitor_config)
        self.alert_manager = AlertManager(alert_config)
        self.reporter = PerformanceReporter()
        
        self.cloudwatch_monitor = None
        if cloudwatch_function_name:
            self.cloudwatch_monitor = CloudWatchMonitor(cloudwatch_function_name)
    
    def run_single_check(self) -> Dict[str, Any]:
        """执行单次检查"""
        logger.info("执行监控检查...")
        
        # API健康检查
        health_result = self.api_monitor.check_health()
        self.reporter.add_health_record(health_result)
        
        # 端点检查
        endpoint_results = self.api_monitor.check_endpoints()
        self.reporter.add_endpoint_records(endpoint_results)
        
        # 检查告警
        self.alert_manager.check_and_alert(health_result, endpoint_results)
        
        return {
            'health': health_result,
            'endpoints': endpoint_results,
            'timestamp': datetime.now()
        }
    
    def run_continuous_monitoring(self, duration_hours: int = 24) -> None:
        """持续监控"""
        logger.info(f"开始持续监控，持续时间: {duration_hours}小时")
        
        end_time = datetime.now() + timedelta(hours=duration_hours)
        
        try:
            while datetime.now() < end_time:
                self.run_single_check()
                
                logger.info(f"等待{self.monitor_config.check_interval}秒后进行下次检查...")
                time.sleep(self.monitor_config.check_interval)
                
        except KeyboardInterrupt:
            logger.info("监控被用户中断")
        
        # 生成最终报告
        report = self.reporter.generate_report()
        filename = self.reporter.save_report(report)
        logger.info(f"监控完成，报告已保存: {filename}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Serverless应用性能监控")
    parser.add_argument("--url", required=True, help="API基础URL")
    parser.add_argument("--function-name", help="AWS Lambda函数名（可选）")
    parser.add_argument("--interval", type=int, default=60, help="检查间隔（秒）")
    parser.add_argument("--duration", type=int, default=1, help="监控持续时间（小时）")
    parser.add_argument("--single", action="store_true", help="执行单次检查")
    parser.add_argument("--report-only", action="store_true", help="仅生成报告")
    
    # 告警配置
    parser.add_argument("--email-host", default="smtp.gmail.com", help="邮件服务器")
    parser.add_argument("--email-user", help="邮件用户名")
    parser.add_argument("--email-password", help="邮件密码")
    parser.add_argument("--alert-recipients", nargs="+", help="告警收件人")
    
    args = parser.parse_args()
    
    # 配置
    monitor_config = MonitorConfig(
        api_url=args.url,
        check_interval=args.interval
    )
    
    alert_config = AlertConfig(
        email_host=args.email_host,
        email_user=args.email_user or "",
        email_password=args.email_password or "",
        alert_recipients=args.alert_recipients or []
    )
    
    # 创建监控器
    monitor = ServerlessMonitor(
        monitor_config=monitor_config,
        alert_config=alert_config,
        cloudwatch_function_name=args.function_name
    )
    
    if args.report_only:
        # 仅生成报告
        report = monitor.reporter.generate_report()
        filename = monitor.reporter.save_report(report)
        print(f"报告已生成: {filename}")
        
    elif args.single:
        # 单次检查
        result = monitor.run_single_check()
        print(f"检查结果: {json.dumps(result, default=str, ensure_ascii=False, indent=2)}")
        
    else:
        # 持续监控
        monitor.run_continuous_monitoring(args.duration)

if __name__ == "__main__":
    main() 