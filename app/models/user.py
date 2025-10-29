"""
User model definitions
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user model"""

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """User creation model"""

    pass


class User(UserBase):
    """User model with ID"""

    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """User response model"""

    id: int
    is_active: bool

    class Config:
        from_attributes = True
