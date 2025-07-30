import logging
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def timer(func: Callable) -> Callable:
    """装饰器：记录函数执行时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper

def validate_age(age: int) -> bool:
    """验证年龄是否合理"""
    return 0 < age <= 150

def validate_email(email: str) -> bool:
    """简单的邮箱验证"""
    return "@" in email and "." in email.split("@")[1]

def sanitize_string(text: str) -> str:
    """清理字符串，移除特殊字符"""
    if not text:
        return ""
    return text.strip().replace("<", "&lt;").replace(">", "&gt;")

def format_response(success: bool, message: str, data: Any = None, error: str = None) -> dict:
    """格式化API响应"""
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    
    if error:
        response["error"] = error
    
    return response

def log_request(request_data: dict):
    """记录请求日志"""
    logger.info(f"收到请求: {json.dumps(request_data, ensure_ascii=False)}")

def log_response(response_data: dict):
    """记录响应日志"""
    logger.info(f"返回响应: {json.dumps(response_data, ensure_ascii=False)}")

class PerformanceMonitor:
    """性能监控类"""
    
    def __init__(self):
        self.requests_count = 0
        self.total_time = 0
        self.errors_count = 0
    
    def record_request(self, execution_time: float, is_error: bool = False):
        """记录请求"""
        self.requests_count += 1
        self.total_time += execution_time
        if is_error:
            self.errors_count += 1
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        avg_time = self.total_time / self.requests_count if self.requests_count > 0 else 0
        error_rate = self.errors_count / self.requests_count if self.requests_count > 0 else 0
        
        return {
            "total_requests": self.requests_count,
            "total_errors": self.errors_count,
            "average_response_time": round(avg_time, 4),
            "error_rate": round(error_rate * 100, 2)
        }

# 全局性能监控实例
performance_monitor = PerformanceMonitor() 