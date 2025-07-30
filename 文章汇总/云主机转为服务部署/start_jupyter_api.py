#!/usr/bin/env python3
"""
JupyterLab API启动脚本
专为在JupyterLab环境中使用而优化

在JupyterLab Cell中运行:
exec(open('start_jupyter_api.py').read())

或者在终端中运行:
python start_jupyter_api.py
"""

import os
import sys
import time
import threading
import asyncio
from pathlib import Path
from datetime import datetime

# 云主机配置
CLOUD_HOST = "gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud"
API_PORT = 8888
JUPYTER_LAB_URL = f"https://{CLOUD_HOST}/lab/tree/data/changetest"

def setup_jupyter_environment():
    """设置JupyterLab环境"""
    print("🔧 设置JupyterLab环境...")
    
    # 获取当前目录并设置项目根目录
    current_dir = Path().resolve()
    if 'notebooks' in str(current_dir):
        project_root = current_dir.parent
    else:
        project_root = current_dir
    
    # 添加src到Python路径
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    print(f"✅ 项目根目录: {project_root}")
    print(f"✅ 源码路径已添加: {src_path}")
    
    return project_root

def install_required_packages():
    """安装必要的包"""
    print("📦 检查并安装必要的包...")
    
    required_packages = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "mangum"
    ]
    
    import subprocess
    
    for package in required_packages:
        try:
            __import__(package.split('[')[0])  # 去掉额外选项检查
            print(f"  ✅ {package} - 已安装")
        except ImportError:
            print(f"  📦 安装 {package}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
                print(f"  ✅ {package} - 安装完成")
            except subprocess.CalledProcessError:
                print(f"  ⚠️ {package} - 安装失败")

def create_demo_users():
    """创建演示用户数据"""
    print("👥 创建演示用户数据...")
    
    try:
        from models.schemas import CreateUserRequest
        from services.api_service import UserService
        
        service = UserService()
        
        demo_users = [
            {"name": "云主机管理员", "email": "admin@gpu-cloud.com", "age": 35},
            {"name": "JupyterLab开发者", "email": "jupyter@dev.com", "age": 28},
            {"name": "Serverless架构师", "email": "serverless@arch.com", "age": 32},
            {"name": "API测试工程师", "email": "api@test.com", "age": 29},
            {"name": "数据科学家", "email": "datascience@ai.com", "age": 31}
        ]
        
        added_count = 0
        for user_data in demo_users:
            try:
                user_request = CreateUserRequest(**user_data)
                new_user = service.create_user(user_request)
                print(f"  ➕ {user_data['name']} (ID: {new_user['id']})")
                added_count += 1
            except ValueError:
                # 用户已存在
                print(f"  ⚠️ {user_data['name']} - 已存在")
        
        total_users = len(service.get_all_users())
        print(f"✅ 演示数据创建完成 (新增: {added_count}, 总计: {total_users})")
        
        return service
        
    except ImportError as e:
        print(f"❌ 无法导入用户服务: {e}")
        return None

def start_api_server_background():
    """在后台启动API服务器"""
    print("🚀 启动API服务器...")
    
    try:
        from app import app
        import uvicorn
        
        def run_server():
            """运行服务器的函数"""
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=API_PORT,
                log_level="info",
                access_log=False  # 减少日志输出
            )
        
        # 在后台线程中启动服务器
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # 等待服务器启动
        print("⏳ 等待服务器启动...")
        time.sleep(3)
        
        # 测试连接
        import requests
        try:
            response = requests.get(f"http://localhost:{API_PORT}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API服务器启动成功!")
                return True
            else:
                print(f"⚠️ 服务器响应异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠️ 连接测试失败: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ 无法导入FastAPI应用: {e}")
        return False
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")
        return False

def display_api_info():
    """显示API信息和使用指南"""
    
    from IPython.display import display, HTML
    
    info_html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 25px; border-radius: 15px; margin: 15px 0; 
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
        
        <div style="text-align: center; margin-bottom: 25px;">
            <h1 style="margin: 0; font-size: 2.5em;">🚀 云主机API已启动！</h1>
            <p style="margin: 10px 0; font-size: 1.2em; opacity: 0.9;">
                GPU云主机实例: <strong>gpu-4090-96g-instance-318</strong>
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 25px 0;">
            
            <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin-top: 0; color: #FFD700;">🌐 访问链接</h3>
                <div style="margin: 10px 0;">
                    <a href="https://{CLOUD_HOST}" 
                       style="color: #FFD700; text-decoration: none; display: block; margin: 8px 0;">
                        🏠 API首页
                    </a>
                    <a href="https://{CLOUD_HOST}/docs" 
                       style="color: #FFD700; text-decoration: none; display: block; margin: 8px 0;">
                        📖 Swagger文档
                    </a>
                    <a href="https://{CLOUD_HOST}/stats" 
                       style="color: #FFD700; text-decoration: none; display: block; margin: 8px 0;">
                        📊 API统计
                    </a>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 10px;">
                <h3 style="margin-top: 0; color: #FFD700;">🧪 快速测试</h3>
                <div style="font-family: 'Courier New', monospace; font-size: 0.9em;">
                    <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; margin: 5px 0;">
                        GET /users
                    </div>
                    <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; margin: 5px 0;">
                        POST /users
                    </div>
                    <div style="background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; margin: 5px 0;">
                        GET /users/search/云
                    </div>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="margin-top: 0; color: #FFD700;">💻 开发环境</h3>
                <div style="margin: 10px 0;">
                    <a href="{JUPYTER_LAB_URL}" 
                       style="color: #FFD700; text-decoration: none; display: block; margin: 8px 0;">
                        📓 JupyterLab
                    </a>
                    <div style="color: #E0E0E0; margin: 8px 0;">
                        🐍 Python {sys.version_info.major}.{sys.version_info.minor}
                    </div>
                    <div style="color: #E0E0E0; margin: 8px 0;">
                        ⚡ FastAPI + Uvicorn
                    </div>
                </div>
            </div>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #FFD700;">🔥 在JupyterLab中测试API</h3>
            <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; overflow-x: auto; margin: 10px 0;">
<code style="color: #E0E0E0;">
import requests

# 获取用户列表
response = requests.get('https://{CLOUD_HOST}/users')
print(response.json())

# 创建新用户
new_user = {{
    "name": "JupyterLab用户",
    "email": "jupyter@example.com", 
    "age": 28
}}
response = requests.post('https://{CLOUD_HOST}/users', json=new_user)
print(response.json())

# 搜索用户
response = requests.get('https://{CLOUD_HOST}/users/search/云')
print(response.json())
</code></pre>
        </div>
        
        <div style="text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
            <p style="margin: 0; font-size: 1.1em;">
                🎉 <strong>API已就绪！</strong> 开始您的开发之旅吧！
            </p>
        </div>
    </div>
    """
    
    try:
        # 尝试在Jupyter环境中显示HTML
        display(HTML(info_html))
    except:
        # 如果不在Jupyter环境中，显示文本版本
        print_text_info()

def print_text_info():
    """打印文本版本的信息"""
    print("\n" + "="*80)
    print("🎉 云主机API启动成功！")
    print("="*80)
    
    print(f"\n🌐 云主机信息:")
    print(f"   实例: gpu-4090-96g-instance-318")
    print(f"   域名: {CLOUD_HOST}")
    print(f"   端口: {API_PORT}")
    
    print(f"\n📍 访问地址:")
    print(f"   🏠 API首页: https://{CLOUD_HOST}")
    print(f"   📖 API文档: https://{CLOUD_HOST}/docs")
    print(f"   📚 ReDoc: https://{CLOUD_HOST}/redoc")
    print(f"   📊 API统计: https://{CLOUD_HOST}/stats")
    print(f"   🔍 健康检查: https://{CLOUD_HOST}/health")
    
    print(f"\n💻 开发环境:")
    print(f"   📓 JupyterLab: {JUPYTER_LAB_URL}")
    print(f"   🐍 Python: {sys.version}")
    
    print(f"\n🧪 测试命令:")
    print(f"   curl 'https://{CLOUD_HOST}/users'")
    print(f"   curl 'https://{CLOUD_HOST}/users/search/云'")
    print(f"   curl 'https://{CLOUD_HOST}/stats'")
    
    print(f"\n🎯 Python测试代码:")
    print(f"""
import requests

# 获取用户列表
response = requests.get('https://{CLOUD_HOST}/users')
print(response.json())

# 创建新用户
new_user = {{
    "name": "JupyterLab用户",
    "email": "jupyter@example.com", 
    "age": 28
}}
response = requests.post('https://{CLOUD_HOST}/users', json=new_user)
print(response.json())

# 搜索用户
response = requests.get('https://{CLOUD_HOST}/users/search/云')
print(response.json())
""")

def test_api_quickly():
    """快速测试API功能"""
    print("\n🧪 快速API测试...")
    
    try:
        import requests
        
        base_url = f"https://{CLOUD_HOST}"
        
        # 健康检查
        print("🔍 健康检查...")
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("  ✅ 健康检查通过")
            else:
                print(f"  ⚠️ 健康检查异常: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 健康检查失败: {e}")
        
        # 获取用户列表
        print("📋 获取用户列表...")
        try:
            response = requests.get(f"{base_url}/users?limit=3", timeout=5)
            if response.status_code == 200:
                data = response.json()
                user_count = data['data']['total']
                print(f"  ✅ 成功获取用户列表 (总计: {user_count}个用户)")
            else:
                print(f"  ⚠️ 获取用户列表异常: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 获取用户列表失败: {e}")
        
        # 获取API统计
        print("📊 获取API统计...")
        try:
            response = requests.get(f"{base_url}/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ 成功获取API统计")
            else:
                print(f"  ⚠️ 获取API统计异常: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 获取API统计失败: {e}")
            
        print("✅ 快速测试完成")
        
    except ImportError:
        print("❌ 无法导入requests库，请先安装: pip install requests")

def main():
    """主函数"""
    print("🚀 JupyterLab API启动脚本")
    print(f"📅 {datetime.now()}")
    print(f"🖥️ 云主机: {CLOUD_HOST}")
    print("="*60)
    
    # 1. 设置环境
    project_root = setup_jupyter_environment()
    
    # 2. 安装包
    install_required_packages()
    
    # 3. 创建演示数据
    user_service = create_demo_users()
    
    # 4. 启动API服务器
    server_started = start_api_server_background()
    
    if server_started:
        # 5. 显示信息
        display_api_info()
        
        # 6. 快速测试
        test_api_quickly()
    else:
        print("❌ API服务器启动失败")
        return False
    
    print("\n🎊 JupyterLab API环境配置完成！")
    print("💡 您可以现在开始在JupyterLab中开发和测试API了！")
    
    return True

# 如果直接运行此脚本
if __name__ == "__main__":
    success = main()
    if success:
        print("\n📝 提示: 如果要在JupyterLab Cell中运行此脚本，请使用:")
        print("   exec(open('start_jupyter_api.py').read())")
    sys.exit(0 if success else 1)

# 如果在Jupyter中执行，也运行主函数
try:
    # 检查是否在Jupyter环境中
    get_ipython()
    print("🔍 检测到Jupyter环境，自动执行启动流程...")
    main()
except NameError:
    # 不在Jupyter环境中，只有直接运行时才执行
    pass 