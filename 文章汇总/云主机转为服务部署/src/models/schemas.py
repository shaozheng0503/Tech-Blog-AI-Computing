from pydantic import BaseModel, EmailStr
from typing import Any, Optional

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
    error: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: str
    version: str 