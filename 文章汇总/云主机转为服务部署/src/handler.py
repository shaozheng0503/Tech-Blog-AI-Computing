import json
import os
import sys
from typing import Dict, Any

# 添加路径以便导入模块
sys.path.append(os.path.dirname(__file__))

try:
    from mangum import Mangum
    from app import app
    
    # 创建Mangum处理器，用于AWS Lambda
    lambda_handler = Mangum(app, lifespan="off")
    
except ImportError as e:
    print(f"导入错误: {e}")
    # 如果mangum未安装，创建一个简单的处理器
    def lambda_handler(event, context):
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Mangum未安装，请运行: pip install mangum"
            })
        }

def serverless_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    通用Serverless处理器
    支持AWS Lambda、阿里云函数计算、腾讯云函数
    """
    print(f"收到事件: {json.dumps(event, ensure_ascii=False)}")
    
    try:
        # 调用Lambda处理器
        response = lambda_handler(event, context)
        print(f"响应: {json.dumps(response, ensure_ascii=False)}")
        return response
    except Exception as e:
        print(f"处理请求时出错: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({
                "success": False,
                "message": "服务器内部错误",
                "error": str(e)
            }, ensure_ascii=False)
        }

def aliyun_handler(environ: Dict[str, Any], start_response: callable):
    """
    阿里云函数计算处理器
    使用WSGI接口
    """
    try:
        from mangum import Mangum
        handler = Mangum(app, lifespan="off")
        return handler(environ, start_response)
    except ImportError:
        # 简单的WSGI响应
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        
        error_response = json.dumps({
            "success": False,
            "message": "Mangum未安装",
            "error": "请运行: pip install mangum"
        }, ensure_ascii=False)
        
        return [error_response.encode('utf-8')]
    except Exception as e:
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        
        error_response = json.dumps({
            "success": False,
            "message": "服务器内部错误",
            "error": str(e)
        }, ensure_ascii=False)
        
        return [error_response.encode('utf-8')]

def tencent_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    腾讯云函数处理器
    兼容API Gateway事件格式
    """
    print(f"腾讯云函数收到事件: {json.dumps(event, ensure_ascii=False)}")
    
    try:
        # 腾讯云函数的事件格式可能略有不同，需要做格式转换
        if "requestContext" in event:
            # API Gateway格式
            return lambda_handler(event, context)
        else:
            # 直接调用格式，需要包装成API Gateway格式
            wrapped_event = {
                "httpMethod": "POST",
                "path": "/",
                "headers": event.get("headers", {}),
                "queryStringParameters": event.get("queryStringParameters"),
                "body": json.dumps(event.get("body", {})),
                "isBase64Encoded": False,
                "requestContext": {
                    "requestId": context.request_id if hasattr(context, 'request_id') else "unknown",
                }
            }
            return lambda_handler(wrapped_event, context)
    except Exception as e:
        print(f"腾讯云函数处理错误: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": False,
                "message": "服务器内部错误",
                "error": str(e)
            }, ensure_ascii=False)
        }

def huawei_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    华为云函数工作流处理器
    """
    print(f"华为云函数收到事件: {json.dumps(event, ensure_ascii=False)}")
    
    try:
        # 华为云的事件格式转换
        if "headers" in event and "httpMethod" in event:
            # API Gateway格式
            return lambda_handler(event, context)
        else:
            # 其他格式转换
            wrapped_event = {
                "httpMethod": event.get("method", "POST"),
                "path": event.get("path", "/"),
                "headers": event.get("headers", {}),
                "queryStringParameters": event.get("queryStringParameters"),
                "body": event.get("body"),
                "isBase64Encoded": event.get("isBase64Encoded", False)
            }
            return lambda_handler(wrapped_event, context)
    except Exception as e:
        print(f"华为云函数处理错误: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": False,
                "message": "服务器内部错误", 
                "error": str(e)
            }, ensure_ascii=False)
        }

def test_handler_locally():
    """
    本地测试处理器函数
    """
    # 模拟AWS Lambda事件
    test_events = [
        {
            "httpMethod": "GET",
            "path": "/",
            "headers": {"Content-Type": "application/json"},
            "queryStringParameters": None,
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {"requestId": "test-request-1"}
        },
        {
            "httpMethod": "GET",
            "path": "/users",
            "headers": {"Content-Type": "application/json"},
            "queryStringParameters": None,
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {"requestId": "test-request-2"}
        },
        {
            "httpMethod": "POST",
            "path": "/users",
            "headers": {"Content-Type": "application/json"},
            "queryStringParameters": None,
            "body": json.dumps({
                "name": "测试用户",
                "email": "test@example.com",
                "age": 25
            }),
            "isBase64Encoded": False,
            "requestContext": {"requestId": "test-request-3"}
        }
    ]
    
    class MockContext:
        def __init__(self, request_id):
            self.request_id = request_id
            self.function_name = "test-function"
            self.memory_limit_in_mb = 256
            self.remaining_time_in_millis = 30000
    
    print("=== 开始本地测试 ===")
    
    for i, event in enumerate(test_events):
        print(f"\n--- 测试 {i+1} ---")
        context = MockContext(f"test-{i+1}")
        
        try:
            response = serverless_handler(event, context)
            print(f"状态码: {response.get('statusCode')}")
            
            if response.get('body'):
                body = json.loads(response['body'])
                print(f"响应: {json.dumps(body, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"测试失败: {str(e)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    # 本地测试
    test_handler_locally() 