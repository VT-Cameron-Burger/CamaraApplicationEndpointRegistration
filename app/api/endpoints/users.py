"""
User management endpoints
"""

from typing import Dict, List

from fastapi import APIRouter, HTTPException

from app.models.user import User, UserCreate, UserResponse

router = APIRouter()

# In-memory storage for demo purposes
# In a real application, you would use a database
users_db: List[User] = []


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    """
    Create a new user
    """
    # Check if user already exists
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        id=len(users_db) + 1, name=user.name, email=user.email, is_active=True
    )
    users_db.append(new_user)

    return UserResponse.model_validate(new_user)


@router.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100) -> List[UserResponse]:
    """
    Get all users
    """
    return [UserResponse.model_validate(user) for user in users_db[skip : skip + limit]]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    """
    Get a specific user by ID
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserCreate) -> UserResponse:
    """
    Update a user
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields
    user.name = user_update.name
    user.email = user_update.email

    return UserResponse.model_validate(user)


@router.delete("/users/{user_id}")
async def delete_user(user_id: int) -> Dict[str, str]:
    """
    Delete a user
    """
    user_index = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = users_db.pop(user_index)
    return {"message": f"User {deleted_user.name} deleted successfully"}
