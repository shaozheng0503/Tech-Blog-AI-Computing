#!/usr/bin/env python3
"""
JupyterLab快速开发脚本
这个脚本展示了如何在JupyterLab中快速开发和测试用户管理API

运行方式：
1. 在JupyterLab中以notebook形式运行
2. 在终端中直接运行: python notebooks/quick_start.py
"""

import sys
import os
import json
import time
import threading
from datetime import datetime

# 添加src路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

print("🚀 用户管理API - JupyterLab快速开发")
print("=" * 50)

# =============================================================================
# 第一步：导入必要的库
# =============================================================================
print("\n📚 第一步：导入库...")

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import Optional, List, Dict, Any
    import uvicorn
    print("✅ FastAPI相关库导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请运行: pip install fastapi uvicorn pydantic")
    sys.exit(1)

# =============================================================================
# 第二步：定义数据模型
# =============================================================================
print("\n📋 第二步：定义数据模型...")

class UserModel(BaseModel):
    id: int
    name: str
    email: str
    age: int

class CreateUserRequest(BaseModel):
    name: str
    email: str
    age: int

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any = None
    timestamp: str = None

print("✅ 数据模型定义完成")

# =============================================================================
# 第三步：创建用户服务
# =============================================================================
print("\n🔧 第三步：创建用户服务...")

class UserService:
    def __init__(self):
        self.users_db = [
            {"id": 1, "name": "张三", "email": "zhangsan@example.com", "age": 25},
            {"id": 2, "name": "李四", "email": "lisi@example.com", "age": 30},
            {"id": 3, "name": "王五", "email": "wangwu@example.com", "age": 28}
        ]
    
    def get_all_users(self) -> List[Dict]:
        return self.users_db
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        return next((u for u in self.users_db if u["id"] == user_id), None)
    
    def create_user(self, user_data: CreateUserRequest) -> Dict:
        # 检查邮箱重复
        if any(u["email"] == user_data.email for u in self.users_db):
            raise ValueError("邮箱已存在")
        
        new_id = max([u["id"] for u in self.users_db]) + 1 if self.users_db else 1
        new_user = {
            "id": new_id,
            "name": user_data.name,
            "email": user_data.email,
            "age": user_data.age
        }
        self.users_db.append(new_user)
        return new_user
    
    def update_user(self, user_id: int, user_data: UpdateUserRequest) -> Optional[Dict]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        user.update(update_data)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.users_db = [u for u in self.users_db if u["id"] != user_id]
        return True
    
    def search_users(self, keyword: str) -> List[Dict]:
        keyword = keyword.lower()
        return [
            u for u in self.users_db 
            if keyword in u["name"].lower() or keyword in u["email"].lower()
        ]

# 创建服务实例
user_service = UserService()
print(f"✅ 用户服务创建成功，初始用户数: {len(user_service.get_all_users())}")

# =============================================================================
# 第四步：创建FastAPI应用
# =============================================================================
print("\n🌟 第四步：创建FastAPI应用...")

app = FastAPI(
    title="用户管理API - JupyterLab开发版",
    description="在JupyterLab中开发的用户管理系统",
    version="1.0.0-dev"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ FastAPI应用创建成功")

# =============================================================================
# 第五步：定义API端点
# =============================================================================
print("\n🛠️ 第五步：定义API端点...")

@app.get("/")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "message": "用户管理API运行正常",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-dev",
        "environment": "jupyter-development"
    }

@app.get("/users")
async def get_users(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """获取用户列表"""
    try:
        all_users = user_service.get_all_users()
        total = len(all_users)
        users = all_users[offset:offset + limit]
        
        return APIResponse(
            success=True,
            message=f"获取用户列表成功，共{total}个用户",
            data={
                "users": users,
                "total": total,
                "limit": limit,
                "offset": offset
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """获取特定用户"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="用户ID必须是正整数")
    
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return APIResponse(
        success=True,
        message="获取用户成功",
        data=user,
        timestamp=datetime.now().isoformat()
    )

@app.post("/users")
async def create_user(user: CreateUserRequest):
    """创建新用户"""
    try:
        new_user = user_service.create_user(user)
        return APIResponse(
            success=True,
            message="创建用户成功",
            data=new_user,
            timestamp=datetime.now().isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UpdateUserRequest):
    """更新用户"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="用户ID必须是正整数")
    
    try:
        updated_user = user_service.update_user(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return APIResponse(
            success=True,
            message="更新用户成功",
            data=updated_user,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="用户ID必须是正整数")
    
    try:
        success = user_service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return APIResponse(
            success=True,
            message="删除用户成功",
            data={"deleted_user_id": user_id},
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/search/{keyword}")
async def search_users(keyword: str):
    """搜索用户"""
    if len(keyword.strip()) < 2:
        raise HTTPException(status_code=400, detail="搜索关键词至少2个字符")
    
    try:
        users = user_service.search_users(keyword)
        return APIResponse(
            success=True,
            message=f"搜索完成，找到{len(users)}个匹配用户",
            data={
                "keyword": keyword,
                "results": users,
                "count": len(users)
            },
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

print("✅ API端点定义完成")

# =============================================================================
# 第六步：启动开发服务器（可选）
# =============================================================================
def start_dev_server(host="127.0.0.1", port=8000):
    """启动开发服务器"""
    print(f"\n🌟 启动开发服务器...")
    print(f"📍 地址: http://{host}:{port}")
    print(f"📖 API文档: http://{host}:{port}/docs")
    print(f"📚 ReDoc文档: http://{host}:{port}/redoc")
    print("⏹️ 按 Ctrl+C 停止服务器")
    
    try:
        uvicorn.run(app, host=host, port=port, log_level="info")
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")

# =============================================================================
# 第七步：API测试函数
# =============================================================================
def test_api_functionality():
    """测试API功能"""
    print("\n🧪 第七步：API功能测试...")
    
    try:
        import requests
    except ImportError:
        print("❌ 需要安装requests库: pip install requests")
        return
    
    BASE_URL = "http://127.0.0.1:8000"
    
    def check_server():
        """检查服务器是否运行"""
        try:
            response = requests.get(f"{BASE_URL}/", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    if not check_server():
        print("⚠️ 服务器未运行，请先启动服务器进行测试")
        print("提示：运行 start_dev_server() 或在终端中运行 python src/app.py")
        return
    
    print("✅ 服务器运行中，开始测试...")
    
    # 测试健康检查
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"🔍 健康检查: {response.status_code} - {response.json()['message']}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
    
    # 测试获取用户列表
    try:
        response = requests.get(f"{BASE_URL}/users")
        data = response.json()
        print(f"📋 用户列表: 获取到{data['data']['total']}个用户")
    except Exception as e:
        print(f"❌ 获取用户列表失败: {e}")
    
    # 测试创建用户
    try:
        new_user = {
            "name": "JupyterLab测试用户",
            "email": f"jupyter_test_{int(time.time())}@example.com",
            "age": 25
        }
        response = requests.post(f"{BASE_URL}/users", json=new_user)
        if response.status_code == 200:
            created_user = response.json()['data']
            print(f"➕ 创建用户: 成功创建用户 {created_user['name']} (ID: {created_user['id']})")
            
            # 测试更新用户
            update_data = {"name": "更新后的用户名"}
            response = requests.put(f"{BASE_URL}/users/{created_user['id']}", json=update_data)
            if response.status_code == 200:
                print("✏️ 更新用户: 成功")
            
            # 测试删除用户
            response = requests.delete(f"{BASE_URL}/users/{created_user['id']}")
            if response.status_code == 200:
                print("🗑️ 删除用户: 成功")
        
    except Exception as e:
        print(f"❌ 用户操作测试失败: {e}")
    
    # 测试搜索
    try:
        response = requests.get(f"{BASE_URL}/users/search/张")
        data = response.json()
        print(f"🔍 搜索用户: 找到{data['data']['count']}个匹配结果")
    except Exception as e:
        print(f"❌ 搜索测试失败: {e}")
    
    print("✅ API功能测试完成")

# =============================================================================
# 第八步：性能基准测试
# =============================================================================
def run_performance_test(num_requests=20):
    """运行简单的性能测试"""
    print(f"\n⚡ 第八步：性能测试 ({num_requests}个请求)...")
    
    try:
        import requests
        import concurrent.futures
    except ImportError:
        print("❌ 需要安装requests库: pip install requests")
        return
    
    BASE_URL = "http://127.0.0.1:8000"
    
    def make_request():
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/users", timeout=5)
            response_time = time.time() - start_time
            return {
                "success": response.status_code == 200,
                "response_time": response_time,
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "response_time": 0,
                "error": str(e)
            }
    
    # 检查服务器
    try:
        requests.get(f"{BASE_URL}/", timeout=2)
    except:
        print("⚠️ 服务器未运行，无法进行性能测试")
        return
    
    # 并发测试
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    # 分析结果
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    if successful:
        avg_time = sum(r["response_time"] for r in successful) / len(successful)
        min_time = min(r["response_time"] for r in successful)
        max_time = max(r["response_time"] for r in successful)
        
        print(f"📊 测试结果:")
        print(f"   总请求: {len(results)}")
        print(f"   成功: {len(successful)}")
        print(f"   失败: {len(failed)}")
        print(f"   成功率: {len(successful)/len(results)*100:.1f}%")
        print(f"   平均响应时间: {avg_time*1000:.1f}ms")
        print(f"   最快响应: {min_time*1000:.1f}ms")
        print(f"   最慢响应: {max_time*1000:.1f}ms")
        
        if avg_time < 0.1:
            print("🚀 性能: 优秀")
        elif avg_time < 0.2:
            print("✅ 性能: 良好")
        else:
            print("⚠️ 性能: 需要优化")
    
    if failed:
        print(f"❌ 有 {len(failed)} 个请求失败")

# =============================================================================
# 交互式功能
# =============================================================================
def show_menu():
    """显示交互菜单"""
    print("\n" + "="*50)
    print("🎛️ JupyterLab开发菜单")
    print("="*50)
    print("1. 启动开发服务器")
    print("2. 运行API功能测试")
    print("3. 运行性能测试")
    print("4. 查看当前用户数据")
    print("5. 添加测试用户")
    print("6. 显示API信息")
    print("0. 退出")
    print("="*50)

def interactive_mode():
    """交互式模式"""
    while True:
        show_menu()
        try:
            choice = input("请选择操作 (0-6): ").strip()
            
            if choice == "0":
                print("👋 再见！")
                break
            elif choice == "1":
                start_dev_server()
            elif choice == "2":
                test_api_functionality()
            elif choice == "3":
                run_performance_test()
            elif choice == "4":
                users = user_service.get_all_users()
                print(f"\n📋 当前用户数据 ({len(users)}个用户):")
                for user in users:
                    print(f"  - {user['name']} ({user['email']}) - {user['age']}岁")
            elif choice == "5":
                print("\n➕ 添加测试用户...")
                name = input("姓名: ").strip()
                email = input("邮箱: ").strip()
                age = input("年龄: ").strip()
                
                if name and email and age.isdigit():
                    try:
                        user_data = CreateUserRequest(name=name, email=email, age=int(age))
                        new_user = user_service.create_user(user_data)
                        print(f"✅ 用户创建成功: {new_user}")
                    except Exception as e:
                        print(f"❌ 创建失败: {e}")
                else:
                    print("❌ 输入信息不完整或格式错误")
            elif choice == "6":
                print(f"\n📖 API信息:")
                print(f"   标题: {app.title}")
                print(f"   版本: {app.version}")
                print(f"   描述: {app.description}")
                print(f"   端点数量: {len(app.routes)}")
                print(f"   用户数量: {len(user_service.get_all_users())}")
            else:
                print("❌ 无效选择，请重试")
        
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 操作失败: {e}")

# =============================================================================
# 主函数
# =============================================================================
def main():
    """主函数"""
    print("\n🎉 JupyterLab开发环境准备完成！")
    print("\n📋 可用功能:")
    print("- start_dev_server(): 启动开发服务器")
    print("- test_api_functionality(): 测试API功能")
    print("- run_performance_test(): 性能测试")
    print("- interactive_mode(): 交互式模式")
    print("- user_service: 用户服务实例")
    print("- app: FastAPI应用实例")
    
    print(f"\n📊 当前状态:")
    print(f"- 用户数量: {len(user_service.get_all_users())}")
    print(f"- API端点: {len([route for route in app.routes if hasattr(route, 'methods')])}")
    
    # 如果作为脚本运行，启动交互模式
    if __name__ == "__main__":
        print("\n🎛️ 启动交互模式...")
        interactive_mode()

# 运行主函数
if __name__ == "__main__":
    main()
else:
    # 如果在Jupyter中导入，显示信息
    main() 