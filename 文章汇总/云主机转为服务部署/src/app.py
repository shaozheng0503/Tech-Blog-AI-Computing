from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import time
from datetime import datetime
import os
import sys

# 添加路径以便导入模块
sys.path.append(os.path.dirname(__file__))

from models.schemas import (
    APIResponse, CreateUserRequest, UpdateUserRequest, 
    HealthCheck, UserModel
)
from services.api_service import UserService
from utils.helpers import (
    timer, validate_age, validate_email, sanitize_string,
    format_response, log_request, log_response, performance_monitor
)

# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的初始化
    print("🚀 用户管理API启动中...")
    print(f"📅 启动时间: {datetime.now()}")
    print(f"🌍 环境: {os.getenv('ENVIRONMENT', 'cloud-development')}")
    print(f"🖥️ 主机: {os.getenv('HOST', '0.0.0.0')}")
    print(f"🔌 端口: {os.getenv('PORT', '8888')}")
    yield
    # 关闭时的清理
    print("⏹️ 用户管理API关闭")

# 创建FastAPI应用
app = FastAPI(
    title="🚀 云主机用户管理API",
    description="""
    ## 📋 项目简介
    
    这是一个完整的用户管理系统，展示了从JupyterLab开发到Serverless部署的完整流程。
    
    ## 🎯 功能特色
    
    - **完整的CRUD操作**: 创建、读取、更新、删除用户
    - **高级搜索功能**: 支持按姓名、邮箱搜索用户
    - **年龄范围查询**: 按年龄区间筛选用户
    - **数据验证**: 严格的输入验证和错误处理
    - **性能监控**: 实时API性能统计
    - **云主机优化**: 专为云主机环境优化配置
    
    ## 🔗 相关链接
    
    - **API文档**: [Swagger UI](/docs)
    - **ReDoc文档**: [ReDoc](/redoc)
    - **性能统计**: [GET /stats](/stats)
    - **健康检查**: [GET /](/
    - **云主机JupyterLab**: [JupyterLab环境](https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest)
    
    ## 📞 联系方式
    
    - 开发者: 云主机开发团队
    - 环境: GPU云主机 + JupyterLab
    - 部署: Serverless Ready
    """,
    version="1.0.0-cloud",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    servers=[
        {
            "url": "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud",
            "description": "云主机生产环境"
        },
        {
            "url": "http://localhost:8888",
            "description": "本地开发环境"
        }
    ]
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建服务实例
user_service = UserService()

# 依赖注入
def get_user_service() -> UserService:
    return user_service

# 中间件：请求性能监控
@app.middleware("http")
async def performance_middleware(request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        performance_monitor.record_request(process_time, False)
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Cloud-Instance"] = "gpu-4090-96g-instance-318"
        return response
    except Exception as e:
        process_time = time.time() - start_time
        performance_monitor.record_request(process_time, True)
        raise e

# 自定义首页
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def custom_homepage():
    """自定义API首页"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 云主机用户管理API</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .header h1 { font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 40px; }
            .card { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.2); }
            .card h3 { margin-top: 0; color: #FFD700; }
            .api-list { list-style: none; padding: 0; }
            .api-list li { padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
            .api-list li:last-child { border-bottom: none; }
            .method { padding: 3px 8px; border-radius: 5px; font-weight: bold; margin-right: 10px; }
            .get { background: #28a745; }
            .post { background: #007bff; }
            .put { background: #ffc107; color: black; }
            .delete { background: #dc3545; }
            .btn { display: inline-block; padding: 10px 20px; background: #FFD700; color: #333; text-decoration: none; border-radius: 5px; margin: 5px; font-weight: bold; }
            .btn:hover { background: #FFA500; }
            .stats { display: flex; justify-content: space-around; text-align: center; margin: 20px 0; }
            .stat-item { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; }
            .footer { text-align: center; margin-top: 40px; opacity: 0.8; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 云主机用户管理API</h1>
                <p>基于 JupyterLab 开发，支持 Serverless 部署的现代化用户管理系统</p>
                <div class="stats">
                    <div class="stat-item">
                        <h3>⚡ 高性能</h3>
                        <p>毫秒级响应</p>
                    </div>
                    <div class="stat-item">
                        <h3>☁️ 云原生</h3>
                        <p>多云部署</p>
                    </div>
                    <div class="stat-item">
                        <h3>🔒 安全可靠</h3>
                        <p>数据验证</p>
                    </div>
                </div>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>📖 API 文档</h3>
                    <p>完整的API接口文档和在线测试工具</p>
                    <a href="/docs" class="btn">Swagger UI</a>
                    <a href="/redoc" class="btn">ReDoc 文档</a>
                </div>
                
                <div class="card">
                    <h3>🔧 核心功能</h3>
                    <ul class="api-list">
                        <li><span class="method get">GET</span>/users - 获取用户列表</li>
                        <li><span class="method post">POST</span>/users - 创建新用户</li>
                        <li><span class="method get">GET</span>/users/{id} - 获取用户详情</li>
                        <li><span class="method put">PUT</span>/users/{id} - 更新用户</li>
                        <li><span class="method delete">DELETE</span>/users/{id} - 删除用户</li>
                        <li><span class="method get">GET</span>/users/search/{keyword} - 搜索用户</li>
                    </ul>
                </div>
                
                <div class="card">
                    <h3>📊 系统状态</h3>
                    <p>实时监控API性能和系统健康状态</p>
                    <a href="/health" class="btn">健康检查</a>
                    <a href="/stats" class="btn">性能统计</a>
                </div>
                
                <div class="card">
                    <h3>🛠️ 开发环境</h3>
                    <p>云主机 JupyterLab 开发环境</p>
                    <a href="https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest" class="btn">JupyterLab</a>
                </div>
            </div>
            
            <div class="card">
                <h3>🚀 快速开始</h3>
                <h4>1. 获取所有用户</h4>
                <code style="background: rgba(0,0,0,0.3); padding: 10px; display: block; border-radius: 5px;">
                    curl -X GET "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users"
                </code>
                
                <h4>2. 创建新用户</h4>
                <code style="background: rgba(0,0,0,0.3); padding: 10px; display: block; border-radius: 5px;">
                    curl -X POST "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users" \\<br>
                    &nbsp;&nbsp;-H "Content-Type: application/json" \\<br>
                    &nbsp;&nbsp;-d '{"name":"张三","email":"zhangsan@example.com","age":25}'
                </code>
                
                <h4>3. 搜索用户</h4>
                <code style="background: rgba(0,0,0,0.3); padding: 10px; display: block; border-radius: 5px;">
                    curl -X GET "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/search/张"
                </code>
            </div>
            
            <div class="footer">
                <p>💡 基于 FastAPI + JupyterLab + Serverless 架构 | 🌟 现代化 Python Web 开发实践</p>
                <p>🔗 云主机地址: <strong>gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud</strong></p>
            </div>
        </div>
        
        <script>
            // 添加一些交互效果
            document.querySelectorAll('.card').forEach(card => {
                card.addEventListener('mouseenter', () => {
                    card.style.transform = 'translateY(-5px)';
                    card.style.transition = 'transform 0.3s ease';
                });
                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'translateY(0)';
                });
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 健康检查端点
@app.get("/health", response_model=HealthCheck, tags=["系统监控"])
@timer
async def health_check():
    """
    健康检查端点
    
    返回系统健康状态和基本信息：
    - 系统状态
    - 当前时间
    - API版本
    - 云主机信息
    """
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0-cloud"
    )

# 获取API统计信息
@app.get("/stats", response_model=APIResponse, tags=["系统监控"])
async def get_stats():
    """
    获取API统计信息
    
    包含以下统计数据：
    - 总请求数
    - 成功请求数
    - 错误请求数
    - 平均响应时间
    - 错误率
    - 用户数量
    """
    stats = performance_monitor.get_stats()
    stats["user_count"] = len(user_service.get_all_users())
    stats["cloud_instance"] = "gpu-4090-96g-instance-318"
    stats["jupyter_lab_url"] = "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/lab/tree/data/changetest"
    
    return APIResponse(
        success=True,
        message="获取统计信息成功",
        data=stats
    )

# 获取所有用户
@app.get("/users", response_model=APIResponse, tags=["用户管理"], 
         summary="获取用户列表", description="获取所有用户信息，支持分页查询")
@timer
async def get_users(
    limit: int = Query(100, ge=1, le=1000, description="返回用户数量限制", example=10),
    offset: int = Query(0, ge=0, description="跳过的用户数量", example=0),
    service: UserService = Depends(get_user_service)
):
    """
    获取用户列表
    
    支持分页查询，返回用户数据和分页信息。
    
    **示例请求:**
    ```
    GET /users?limit=10&offset=0
    ```
    
    **示例响应:**
    ```json
    {
        "success": true,
        "message": "获取用户列表成功，共3个用户",
        "data": {
            "users": [...],
            "total": 3,
            "limit": 10,
            "offset": 0
        }
    }
    ```
    """
    try:
        all_users = service.get_all_users()
        total = len(all_users)
        users = all_users[offset:offset + limit]
        
        result = {
            "users": users,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total,
            "cloud_api_url": "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users"
        }
        
        return APIResponse(
            success=True,
            message=f"获取用户列表成功，共{total}个用户",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户列表失败: {str(e)}")

# 根据ID获取用户
@app.get("/users/{user_id}", response_model=APIResponse, tags=["用户管理"],
         summary="获取用户详情", description="根据用户ID获取特定用户的详细信息")
@timer
async def get_user(
    user_id: int = Query(..., description="用户ID", example=1), 
    service: UserService = Depends(get_user_service)
):
    """
    获取用户详情
    
    根据用户ID返回特定用户的详细信息。
    
    **示例请求:**
    ```
    GET /users/1
    ```
    
    **示例响应:**
    ```json
    {
        "success": true,
        "message": "获取用户成功",
        "data": {
            "id": 1,
            "name": "张三",
            "email": "zhangsan@example.com",
            "age": 25
        }
    }
    ```
    """
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="用户ID必须是正整数")
    
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return APIResponse(
        success=True,
        message="获取用户成功",
        data=user
    )

# 创建新用户
@app.post("/users", response_model=APIResponse, tags=["用户管理"],
          summary="创建新用户", description="创建一个新的用户账户")
@timer
async def create_user(
    user: CreateUserRequest, 
    service: UserService = Depends(get_user_service)
):
    """
    创建新用户
    
    创建一个新的用户账户，需要提供姓名、邮箱和年龄。
    
    **请求体示例:**
    ```json
    {
        "name": "李四",
        "email": "lisi@example.com",
        "age": 30
    }
    ```
    
    **cURL 示例:**
    ```bash
    curl -X POST "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users" \\
      -H "Content-Type: application/json" \\
      -d '{"name":"李四","email":"lisi@example.com","age":30}'
    ```
    
    **验证规则:**
    - 姓名: 必填，不能为空
    - 邮箱: 必填，格式必须正确，不能重复
    - 年龄: 必填，1-150之间的整数
    """
    try:
        # 数据验证
        if not validate_age(user.age):
            raise HTTPException(status_code=400, detail="年龄必须在1-150之间")
        
        if not validate_email(user.email):
            raise HTTPException(status_code=400, detail="邮箱格式不正确")
        
        # 清理输入数据
        user.name = sanitize_string(user.name)
        user.email = sanitize_string(user.email)
        
        new_user = service.create_user(user)
        new_user["api_url"] = f"https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/{new_user['id']}"
        
        return APIResponse(
            success=True,
            message="创建用户成功",
            data=new_user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")

# 更新用户信息
@app.put("/users/{user_id}", response_model=APIResponse, tags=["用户管理"],
         summary="更新用户信息", description="更新指定用户的信息")
@timer
async def update_user(
    user_id: int, 
    user: UpdateUserRequest, 
    service: UserService = Depends(get_user_service)
):
    """
    更新用户信息
    
    更新指定用户的部分或全部信息。
    
    **请求体示例:**
    ```json
    {
        "name": "张三更新",
        "age": 26
    }
    ```
    
    **cURL 示例:**
    ```bash
    curl -X PUT "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/1" \\
      -H "Content-Type: application/json" \\
      -d '{"name":"张三更新","age":26}'
    ```
    """
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="用户ID必须是正整数")
    
    try:
        # 数据验证
        if user.age is not None and not validate_age(user.age):
            raise HTTPException(status_code=400, detail="年龄必须在1-150之间")
        
        if user.email is not None and not validate_email(user.email):
            raise HTTPException(status_code=400, detail="邮箱格式不正确")
        
        # 清理输入数据
        if user.name:
            user.name = sanitize_string(user.name)
        if user.email:
            user.email = sanitize_string(user.email)
        
        updated_user = service.update_user(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return APIResponse(
            success=True,
            message="更新用户成功",
            data=updated_user
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新用户失败: {str(e)}")

# 删除用户
@app.delete("/users/{user_id}", response_model=APIResponse, tags=["用户管理"],
            summary="删除用户", description="删除指定的用户账户")
@timer
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    """
    删除用户
    
    永久删除指定的用户账户，此操作不可恢复。
    
    **cURL 示例:**
    ```bash
    curl -X DELETE "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/1"
    ```
    """
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="用户ID必须是正整数")
    
    try:
        success = service.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return APIResponse(
            success=True,
            message="删除用户成功",
            data={"deleted_user_id": user_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除用户失败: {str(e)}")

# 搜索用户
@app.get("/users/search/{keyword}", response_model=APIResponse, tags=["用户管理"],
         summary="搜索用户", description="根据关键词搜索用户（支持姓名和邮箱搜索）")
@timer
async def search_users(
    keyword: str = Query(..., description="搜索关键词", example="张"), 
    service: UserService = Depends(get_user_service)
):
    """
    搜索用户
    
    根据关键词在用户姓名和邮箱中进行模糊搜索。
    
    **示例请求:**
    ```
    GET /users/search/张
    ```
    
    **cURL 示例:**
    ```bash
    curl -X GET "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/search/张"
    ```
    
    **支持搜索范围:**
    - 用户姓名（模糊匹配）
    - 邮箱地址（模糊匹配）
    - 关键词至少2个字符
    """
    if len(keyword.strip()) < 2:
        raise HTTPException(status_code=400, detail="搜索关键词至少2个字符")
    
    try:
        keyword = sanitize_string(keyword)
        users = service.search_users(keyword)
        
        return APIResponse(
            success=True,
            message=f"搜索完成，找到{len(users)}个匹配用户",
            data={
                "keyword": keyword,
                "results": users,
                "count": len(users),
                "search_url": f"https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/search/{keyword}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# 按年龄范围获取用户
@app.get("/users/age-range/{min_age}/{max_age}", response_model=APIResponse, tags=["用户管理"],
         summary="按年龄范围查询", description="获取指定年龄范围内的所有用户")
@timer
async def get_users_by_age_range(
    min_age: int = Query(..., description="最小年龄", example=20), 
    max_age: int = Query(..., description="最大年龄", example=30), 
    service: UserService = Depends(get_user_service)
):
    """
    按年龄范围查询用户
    
    获取年龄在指定范围内的所有用户。
    
    **示例请求:**
    ```
    GET /users/age-range/20/30
    ```
    
    **cURL 示例:**
    ```bash
    curl -X GET "https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud/users/age-range/20/30"
    ```
    """
    if min_age < 0 or max_age > 150 or min_age > max_age:
        raise HTTPException(status_code=400, detail="年龄范围无效")
    
    try:
        users = service.get_users_by_age_range(min_age, max_age)
        
        return APIResponse(
            success=True,
            message=f"获取年龄在{min_age}-{max_age}岁的用户成功",
            data={
                "age_range": {"min": min_age, "max": max_age},
                "users": users,
                "count": len(users)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_response(
            success=False,
            message=exc.detail,
            error=f"HTTP {exc.status_code}"
        )
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=format_response(
            success=False,
            message="服务器内部错误",
            error=str(exc)
        )
    )

# 主程序入口
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8888))  # 云主机默认端口
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🌟 启动云主机服务器: http://{host}:{port}")
    print(f"📖 API文档: http://{host}:{port}/docs")
    print(f"🔗 云主机地址: https://gpu-4090-96g-instance-318-7byjgbwl-8888.550c.cloud")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    ) 