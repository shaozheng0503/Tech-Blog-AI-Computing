import pytest
import sys
import os
import json
from typing import Dict, Any

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from fastapi.testclient import TestClient
from app import app
from models.schemas import CreateUserRequest, UpdateUserRequest

# 创建测试客户端
client = TestClient(app)

@pytest.fixture
def sample_user():
    """示例用户数据"""
    return {
        "name": "测试用户",
        "email": "test@example.com",
        "age": 25
    }

@pytest.fixture
def update_user_data():
    """更新用户数据"""
    return {
        "name": "更新的用户",
        "age": 30
    }

class TestHealthCheck:
    """健康检查测试"""
    
    def test_health_check(self):
        """测试健康检查端点"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

    def test_stats_endpoint(self):
        """测试统计端点"""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "total_requests" in data["data"]

class TestUserCRUD:
    """用户CRUD操作测试"""
    
    def test_get_users(self):
        """测试获取用户列表"""
        response = client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "users" in data["data"]
        assert "total" in data["data"]
        assert len(data["data"]["users"]) >= 0

    def test_get_users_with_pagination(self):
        """测试分页获取用户"""
        response = client.get("/users?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert len(data["data"]["users"]) <= 2
        assert data["data"]["limit"] == 2
        assert data["data"]["offset"] == 0

    def test_get_user_by_id_existing(self):
        """测试获取存在的用户"""
        response = client.get("/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["id"] == 1
        assert "name" in data["data"]
        assert "email" in data["data"]
        assert "age" in data["data"]

    def test_get_user_by_id_nonexistent(self):
        """测试获取不存在的用户"""
        response = client.get("/users/999")
        assert response.status_code == 404

    def test_get_user_invalid_id(self):
        """测试无效的用户ID"""
        response = client.get("/users/0")
        assert response.status_code == 400
        
        response = client.get("/users/-1")
        assert response.status_code == 400

    def test_create_user(self, sample_user):
        """测试创建用户"""
        response = client.post("/users", json=sample_user)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["name"] == sample_user["name"]
        assert data["data"]["email"] == sample_user["email"]
        assert data["data"]["age"] == sample_user["age"]
        assert "id" in data["data"]

    def test_create_user_invalid_age(self):
        """测试创建用户 - 无效年龄"""
        invalid_user = {
            "name": "无效用户",
            "email": "invalid@example.com",
            "age": -1
        }
        response = client.post("/users", json=invalid_user)
        assert response.status_code == 400

        invalid_user["age"] = 200
        response = client.post("/users", json=invalid_user)
        assert response.status_code == 400

    def test_create_user_invalid_email(self):
        """测试创建用户 - 无效邮箱"""
        invalid_user = {
            "name": "无效邮箱用户",
            "email": "invalid-email",
            "age": 25
        }
        response = client.post("/users", json=invalid_user)
        assert response.status_code == 400

    def test_create_user_duplicate_email(self, sample_user):
        """测试创建用户 - 重复邮箱"""
        # 先创建一个用户
        client.post("/users", json=sample_user)
        
        # 尝试创建相同邮箱的用户
        response = client.post("/users", json=sample_user)
        assert response.status_code == 400

    def test_update_user(self, sample_user, update_user_data):
        """测试更新用户"""
        # 先创建用户
        create_response = client.post("/users", json=sample_user)
        user_id = create_response.json()["data"]["id"]
        
        # 更新用户
        response = client.put(f"/users/{user_id}", json=update_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["name"] == update_user_data["name"]
        assert data["data"]["age"] == update_user_data["age"]

    def test_update_nonexistent_user(self, update_user_data):
        """测试更新不存在的用户"""
        response = client.put("/users/999", json=update_user_data)
        assert response.status_code == 404

    def test_delete_user(self, sample_user):
        """测试删除用户"""
        # 先创建用户
        create_response = client.post("/users", json=sample_user)
        user_id = create_response.json()["data"]["id"]
        
        # 删除用户
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["deleted_user_id"] == user_id
        
        # 验证用户已被删除
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_user(self):
        """测试删除不存在的用户"""
        response = client.delete("/users/999")
        assert response.status_code == 404

class TestUserSearch:
    """用户搜索测试"""
    
    def test_search_users(self):
        """测试搜索用户"""
        # 搜索现有用户
        response = client.get("/users/search/张")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "results" in data["data"]
        assert "count" in data["data"]
        assert "keyword" in data["data"]

    def test_search_users_short_keyword(self):
        """测试搜索关键词过短"""
        response = client.get("/users/search/a")
        assert response.status_code == 400

    def test_search_users_no_results(self):
        """测试搜索无结果"""
        response = client.get("/users/search/不存在的用户")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["count"] == 0

class TestAgeRange:
    """年龄范围查询测试"""
    
    def test_get_users_by_age_range(self):
        """测试按年龄范围获取用户"""
        response = client.get("/users/age-range/20/30")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "users" in data["data"]
        assert "count" in data["data"]
        assert "age_range" in data["data"]
        assert data["data"]["age_range"]["min"] == 20
        assert data["data"]["age_range"]["max"] == 30

    def test_age_range_invalid(self):
        """测试无效年龄范围"""
        # 最小年龄大于最大年龄
        response = client.get("/users/age-range/30/20")
        assert response.status_code == 400
        
        # 负数年龄
        response = client.get("/users/age-range/-1/30")
        assert response.status_code == 400
        
        # 超大年龄
        response = client.get("/users/age-range/20/200")
        assert response.status_code == 400

class TestErrorHandling:
    """错误处理测试"""
    
    def test_invalid_json_format(self):
        """测试无效JSON格式"""
        response = client.post(
            "/users",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_missing_required_fields(self):
        """测试缺少必需字段"""
        incomplete_user = {"name": "不完整用户"}
        response = client.post("/users", json=incomplete_user)
        assert response.status_code == 422

    def test_cors_headers(self):
        """测试CORS头部"""
        response = client.get("/")
        # 检查是否允许跨域
        assert response.status_code == 200

class TestPerformance:
    """性能测试"""
    
    def test_response_time_header(self):
        """测试响应时间头部"""
        response = client.get("/")
        assert response.status_code == 200
        assert "X-Process-Time" in response.headers
        
        process_time = float(response.headers["X-Process-Time"])
        assert process_time > 0
        assert process_time < 1.0  # 响应时间应该小于1秒

if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"]) 