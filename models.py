from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    """User model with basic fields"""
    id: int
    name: str
    description: str


class UserUpdate(BaseModel):
    """Model for partial user updates"""
    name: Optional[str] = None
    description: Optional[str] = None
