from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """User model with basic fields and validation"""
    id: int = Field(..., gt=0, description="User ID must be positive")
    name: str = Field(..., min_length=1, max_length=100, description="User name")
    email: Optional[str] = Field(None, description="User email address")
    description: str = Field(..., min_length=1, max_length=500, description="User description")
    is_active: bool = Field(default=True, description="User active status")
    role: str = Field(default="user", description="User role (user, admin, moderator)")
    created_at: datetime = Field(default_factory=datetime.now, description="Account creation timestamp")


class UserUpdate(BaseModel):
    """Model for partial user updates"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, description="User email address")
    description: Optional[str] = Field(None, min_length=1, max_length=500)


class UserResponse(BaseModel):
    """Model for user responses hiding sensitive information"""
    id: int
    name: str
    description: str
    role: str
