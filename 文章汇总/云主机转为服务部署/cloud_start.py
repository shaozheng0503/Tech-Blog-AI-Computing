#!/usr/bin/env python3
"""
云主机快速启动脚本
专为GPU云主机环境优化的API启动工具

使用方式：
  python cloud_start.py                # 启动API服务
  python cloud_start.py --port 8888   # 指定端口启动
  python cloud_start.py --demo        # 启动演示模式
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

# 云主机配置
CLOUD_HOST = "gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud"
DEFAULT_PORT = 8888

def setup_environment():
    """设置云主机环境"""
    print("🔧 正在设置云主机环境...")
    
    # 添加项目路径
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root / "src"))
    
    # 设置环境变量
    os.environ.update({
        "ENVIRONMENT": "cloud-production",
        "HOST": "0.0.0.0",
        "PORT": str(DEFAULT_PORT),
        "CLOUD_INSTANCE": "gpu-4090-96g-instance-318",
        "JUPYTER_LAB_URL": f"https://{CLOUD_HOST}/lab/tree/data/changetest"
    })
    
    print("✅ 云主机环境设置完成")

def install_dependencies():
    """安装必要依赖"""
    print("📦 检查并安装依赖...")
    
    requirements_file = Path(__file__).parent / "deployment" / "requirements.txt"
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 依赖安装完成")
        else:
            print(f"⚠️ 依赖安装警告: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")

def create_demo_data():
    """创建演示数据"""
    print("📋 创建演示数据...")
    
    try:
        sys.path.append("src")
        from services.api_service import UserService
        from models.schemas import CreateUserRequest
        
        service = UserService()
        
        # 添加更多演示用户
        demo_users = [
            {"name": "云主机用户1", "email": "cloud1@gpu-instance.com", "age": 28},
            {"name": "云主机用户2", "email": "cloud2@gpu-instance.com", "age": 32},
            {"name": "JupyterLab开发者", "email": "dev@jupyter.com", "age": 29},
            {"name": "Serverless工程师", "email": "serverless@cloud.com", "age": 35},
            {"name": "API测试员", "email": "tester@api.com", "age": 26}
        ]
        
        for user_data in demo_users:
            try:
                user_request = CreateUserRequest(**user_data)
                service.create_user(user_request)
                print(f"  ➕ 添加用户: {user_data['name']}")
            except ValueError:
                # 用户已存在，跳过
                pass
        
        print(f"✅ 演示数据创建完成，当前用户总数: {len(service.get_all_users())}")
        
    except Exception as e:
        print(f"⚠️ 演示数据创建失败: {e}")

def start_api_server(port=DEFAULT_PORT, demo_mode=False):
    """启动API服务器"""
    print(f"🚀 启动云主机API服务器...")
    print(f"🌐 云主机地址: https://{CLOUD_HOST}")
    print(f"🔌 端口: {port}")
    
    if demo_mode:
        create_demo_data()
    
    try:
        # 导入FastAPI应用
        from src.app import app
        import uvicorn
        
        print(f"\n📍 API服务地址:")
        print(f"   🏠 首页: https://{CLOUD_HOST}")
        print(f"   📖 API文档: https://{CLOUD_HOST}/docs")
        print(f"   📚 ReDoc: https://{CLOUD_HOST}/redoc")
        print(f"   📊 统计: https://{CLOUD_HOST}/stats")
        print(f"   🔍 健康检查: https://{CLOUD_HOST}/health")
        
        print(f"\n🛠️ JupyterLab环境:")
        print(f"   📓 JupyterLab: https://{CLOUD_HOST}/lab/tree/data/changetest")
        
        print(f"\n🧪 API测试示例:")
        print(f"   curl -X GET 'https://{CLOUD_HOST}/users'")
        print(f"   curl -X GET 'https://{CLOUD_HOST}/users/search/云'")
        
        print(f"\n⏹️ 按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        # 启动服务器
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装所有依赖: pip install -r deployment/requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ API服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

def run_api_tests():
    """运行API测试"""
    print("🧪 运行API功能测试...")
    
    import requests
    import time
    
    base_url = f"https://{CLOUD_HOST}"
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)
    
    tests = [
        ("健康检查", "GET", "/health"),
        ("获取统计", "GET", "/stats"),
        ("获取用户列表", "GET", "/users"),
        ("搜索用户", "GET", "/users/search/云"),
        ("获取用户详情", "GET", "/users/1"),
    ]
    
    for test_name, method, endpoint in tests:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"  ✅ {test_name}: 成功")
            else:
                print(f"  ❌ {test_name}: 失败 ({response.status_code})")
                
        except Exception as e:
            print(f"  ❌ {test_name}: 异常 ({str(e)})")
    
    print("✅ API测试完成")

def show_cloud_info():
    """显示云主机信息"""
    print("☁️ 云主机信息")
    print("=" * 50)
    print(f"🖥️ 实例ID: gpu-4090-96g-instance-318")
    print(f"🌐 域名: {CLOUD_HOST}")
    print(f"🔌 默认端口: {DEFAULT_PORT}")
    print(f"📓 JupyterLab: https://{CLOUD_HOST}/lab/tree/data/changetest")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 工作目录: {os.getcwd()}")
    print("=" * 50)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="云主机API快速启动工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python cloud_start.py                 # 启动API服务
  python cloud_start.py --port 9000    # 指定端口启动
  python cloud_start.py --demo         # 启动演示模式
  python cloud_start.py --test         # 运行测试
  python cloud_start.py --info         # 显示云主机信息
        """
    )
    
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="服务器端口")
    parser.add_argument("--demo", action="store_true", help="演示模式（添加示例数据）")
    parser.add_argument("--test", action="store_true", help="运行API测试")
    parser.add_argument("--info", action="store_true", help="显示云主机信息")
    parser.add_argument("--setup", action="store_true", help="仅设置环境")
    
    args = parser.parse_args()
    
    try:
        # 显示启动信息
        print("🚀 云主机用户管理API启动工具")
        print("=" * 50)
        
        if args.info:
            show_cloud_info()
            return
        
        # 设置环境
        setup_environment()
        
        if args.setup:
            install_dependencies()
            print("✅ 环境设置完成")
            return
        
        if args.test:
            run_api_tests()
            return
        
        # 安装依赖
        install_dependencies()
        
        # 启动API服务器
        start_api_server(port=args.port, demo_mode=args.demo)
        
    except KeyboardInterrupt:
        print("\n👋 操作已取消")
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 