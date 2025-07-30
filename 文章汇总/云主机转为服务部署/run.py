#!/usr/bin/env python3
"""
快速运行脚本 - 一键启动用户管理API

使用方式：
  python run.py                    # 启动开发服务器
  python run.py --test            # 运行测试
  python run.py --monitor         # 启动监控
  python run.py --deploy aws      # 部署到AWS
  python run.py --help           # 显示帮助
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def run_dev_server(host="127.0.0.1", port=8000):
    """启动开发服务器"""
    print(f"🚀 启动开发服务器: http://{host}:{port}")
    print(f"📖 API文档: http://{host}:{port}/docs")
    
    try:
        from src.app import app
        import uvicorn
        uvicorn.run(app, host=host, port=port, reload=True)
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请先安装依赖: pip install -r deployment/requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")

def run_tests():
    """运行测试"""
    print("🧪 运行测试套件...")
    
    # 设置环境变量
    os.environ["PYTHONPATH"] = f"{project_root}/src:{os.environ.get('PYTHONPATH', '')}"
    
    try:
        # 运行pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "-v", "--tb=short"
        ], cwd=project_root)
        
        if result.returncode == 0:
            print("✅ 所有测试通过")
        else:
            print("❌ 测试失败")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ pytest未安装，请运行: pip install pytest")
        sys.exit(1)

def run_load_test(url="http://localhost:8000", users=10, duration=30):
    """运行负载测试"""
    print(f"⚡ 运行负载测试: {users}用户, {duration}秒")
    
    try:
        result = subprocess.run([
            sys.executable, "tests/load_test.py",
            "--url", url,
            "--users", str(users),
            "--duration", str(duration)
        ], cwd=project_root)
        
        if result.returncode != 0:
            print("❌ 负载测试失败")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ 负载测试脚本未找到")
        sys.exit(1)

def run_monitor(url="http://localhost:8000", duration=1):
    """启动监控"""
    print(f"📊 启动性能监控: {duration}小时")
    
    try:
        result = subprocess.run([
            sys.executable, "monitoring/performance_monitor.py",
            "--url", url,
            "--duration", str(duration),
            "--single" if duration == 0 else ""
        ], cwd=project_root)
        
        if result.returncode != 0:
            print("❌ 监控启动失败")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ 监控脚本未找到")
        sys.exit(1)

def deploy_to_platform(platform, stage="dev"):
    """部署到指定平台"""
    print(f"🚀 部署到 {platform} ({stage}环境)")
    
    deploy_script = project_root / "deploy.sh"
    if not deploy_script.exists():
        print("❌ 部署脚本未找到")
        sys.exit(1)
    
    try:
        # 使脚本可执行
        os.chmod(deploy_script, 0o755)
        
        result = subprocess.run([
            str(deploy_script), platform, stage
        ], cwd=project_root)
        
        if result.returncode == 0:
            print(f"✅ 部署到 {platform} 成功")
        else:
            print(f"❌ 部署到 {platform} 失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        sys.exit(1)

def setup_environment():
    """设置开发环境"""
    print("🔧 设置开发环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 9):
        print("❌ 需要Python 3.9或更高版本")
        sys.exit(1)
    
    # 检查依赖文件
    requirements_file = project_root / "deployment" / "requirements.txt"
    if not requirements_file.exists():
        print("❌ 依赖文件不存在: deployment/requirements.txt")
        sys.exit(1)
    
    # 安装依赖
    print("📦 安装Python依赖...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", str(requirements_file)
        ])
        
        if result.returncode == 0:
            print("✅ 依赖安装完成")
        else:
            print("❌ 依赖安装失败")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 安装依赖时出错: {e}")
        sys.exit(1)

def show_status():
    """显示项目状态"""
    print("📊 项目状态")
    print("=" * 50)
    
    # 检查文件
    files_to_check = [
        "src/app.py",
        "src/handler.py", 
        "deployment/requirements.txt",
        "deployment/serverless.yml",
        "tests/test_api.py",
        "deploy.sh"
    ]
    
    for file_path in files_to_check:
        full_path = project_root / file_path
        status = "✅" if full_path.exists() else "❌"
        print(f"{status} {file_path}")
    
    # 检查Python模块
    print("\n📚 Python模块检查:")
    modules_to_check = ["fastapi", "uvicorn", "pydantic", "requests", "pytest"]
    
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} (未安装)")
    
    print(f"\n📁 项目根目录: {project_root}")
    print(f"🐍 Python版本: {sys.version}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="用户管理API - 快速运行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python run.py                     # 启动开发服务器
  python run.py --test             # 运行测试
  python run.py --load-test        # 运行负载测试
  python run.py --monitor          # 启动监控
  python run.py --deploy aws prod  # 部署到AWS生产环境
  python run.py --setup            # 设置开发环境
  python run.py --status           # 显示项目状态
        """
    )
    
    parser.add_argument("--host", default="127.0.0.1", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    parser.add_argument("--test", action="store_true", help="运行测试套件")
    parser.add_argument("--load-test", action="store_true", help="运行负载测试")
    parser.add_argument("--monitor", action="store_true", help="启动性能监控")
    parser.add_argument("--deploy", choices=["aws", "aliyun", "tencent", "docker"], help="部署到指定平台")
    parser.add_argument("--stage", default="dev", choices=["dev", "test", "prod"], help="部署环境")
    parser.add_argument("--setup", action="store_true", help="设置开发环境")
    parser.add_argument("--status", action="store_true", help="显示项目状态")
    parser.add_argument("--url", default="http://localhost:8000", help="API URL (用于测试和监控)")
    parser.add_argument("--users", type=int, default=10, help="负载测试并发用户数")
    parser.add_argument("--duration", type=int, default=30, help="测试持续时间(秒)")
    
    args = parser.parse_args()
    
    try:
        if args.setup:
            setup_environment()
        elif args.status:
            show_status()
        elif args.test:
            run_tests()
        elif args.load_test:
            run_load_test(args.url, args.users, args.duration)
        elif args.monitor:
            run_monitor(args.url, args.duration // 3600 or 1)  # 转换为小时
        elif args.deploy:
            deploy_to_platform(args.deploy, args.stage)
        else:
            # 默认启动开发服务器
            run_dev_server(args.host, args.port)
            
    except KeyboardInterrupt:
        print("\n👋 操作已取消")
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 