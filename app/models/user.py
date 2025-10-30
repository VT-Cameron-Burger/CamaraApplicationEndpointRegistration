"""
User model definitions
"""

from pydantic import BaseModel, ConfigDict, EmailStr


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

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    """User response model"""

    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
