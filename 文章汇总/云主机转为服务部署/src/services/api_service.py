from typing import List, Dict, Optional
from models.schemas import UserModel, CreateUserRequest, UpdateUserRequest
import json
import os

class UserService:
    def __init__(self):
        # 初始化示例数据
        self.users_db = [
            {"id": 1, "name": "张三", "email": "zhangsan@example.com", "age": 25},
            {"id": 2, "name": "李四", "email": "lisi@example.com", "age": 30},
            {"id": 3, "name": "王五", "email": "wangwu@example.com", "age": 28}
        ]
        self._load_data()
    
    def _load_data(self):
        """从环境变量或文件加载数据（生产环境可连接数据库）"""
        data_file = os.getenv('USER_DATA_FILE', '/tmp/users.json')
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    self.users_db = json.load(f)
            except Exception as e:
                print(f"加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据到文件（生产环境可保存到数据库）"""
        data_file = os.getenv('USER_DATA_FILE', '/tmp/users.json')
        try:
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(self.users_db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def get_all_users(self) -> List[Dict]:
        """获取所有用户"""
        return self.users_db
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """根据ID获取用户"""
        return next((u for u in self.users_db if u["id"] == user_id), None)
    
    def create_user(self, user_data: CreateUserRequest) -> Dict:
        """创建新用户"""
        # 检查邮箱是否已存在
        if any(u["email"] == user_data.email for u in self.users_db):
            raise ValueError("邮箱已存在")
        
        # 生成新ID
        new_id = max([u["id"] for u in self.users_db]) + 1 if self.users_db else 1
        
        new_user = {
            "id": new_id,
            "name": user_data.name,
            "email": user_data.email,
            "age": user_data.age
        }
        
        self.users_db.append(new_user)
        self._save_data()
        return new_user
    
    def update_user(self, user_id: int, user_data: UpdateUserRequest) -> Optional[Dict]:
        """更新用户信息"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # 更新字段
        update_data = user_data.dict(exclude_unset=True)
        
        # 检查邮箱唯一性
        if "email" in update_data:
            if any(u["email"] == update_data["email"] and u["id"] != user_id for u in self.users_db):
                raise ValueError("邮箱已存在")
        
        user.update(update_data)
        self._save_data()
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.users_db = [u for u in self.users_db if u["id"] != user_id]
        self._save_data()
        return True
    
    def search_users(self, keyword: str) -> List[Dict]:
        """搜索用户"""
        keyword = keyword.lower()
        return [
            u for u in self.users_db 
            if keyword in u["name"].lower() or keyword in u["email"].lower()
        ]
    
    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[Dict]:
        """按年龄范围获取用户"""
        return [
            u for u in self.users_db 
            if min_age <= u["age"] <= max_age
        ] 