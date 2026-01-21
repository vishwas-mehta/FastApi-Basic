"""
FastAPI Basic Learning Application

A simple REST API demonstrating FastAPI fundamentals including
CRUD operations, data validation, and proper error handling.
"""

from fastapi import FastAPI, HTTPException, status
from typing import List, Optional
from models import User, UserUpdate

app = FastAPI(
    title="FastAPI Basic Learning",
    description="A simple REST API for learning FastAPI fundamentals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# In-memory database with sample data
users_db: List[User] = [
    User(id=1, name="John Doe", description="Software developer"),
    User(id=2, name="Jane Smith", description="Data scientist"),
    User(id=3, name="Bob Johnson", description="DevOps engineer")
]

@app.get('/')
def root():
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to FastAPI Basic Learning"}

@app.get('/health')
def health_check():
    """Health check endpoint returning API status."""
    return {"status": "healthy", "users_count": len(users_db)}

@app.get('/users')
def get_users():
    """Retrieve all users from the database."""
    return {"users": users_db}

@app.get('/users/search')
def search_users(name: Optional[str] = None, skip: int = 0, limit: int = 10):
    results = users_db
    if name:
        results = [u for u in users_db if name.lower() in u.name.lower()]
    return {"users": results[skip:skip + limit]}

@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    """Create a new user in the database."""
    # Check if user with same ID already exists
    for existing_user in users_db:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
    users_db.append(user)
    return {"message": "User created successfully", "user": user}

@app.get('/users/{user_id}')
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return {"user": user}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete('/users/{user_id}', status_code=status.HTTP_200_OK)
def delete_user(user_id: int):
    """Delete a user by their ID."""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            deleted_user = users_db.pop(i)
            return {"message": "User deleted", "user": deleted_user}
    raise HTTPException(status_code=404, detail="User not found")

@app.put('/users/{user_id}')
def update_user(user_id: int, updated_user: User):
    """Update a user completely by their ID."""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db[i] = updated_user
            return {"message": "User updated", "user": updated_user}
    raise HTTPException(status_code=404, detail="User not found")

@app.patch('/users/{user_id}')
def partial_update_user(user_id: int, user_update: UserUpdate):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            if user_update.name is not None:
                users_db[i] = User(id=user.id, name=user_update.name, description=user.description)
            if user_update.description is not None:
                users_db[i] = User(id=users_db[i].id, name=users_db[i].name, description=user_update.description)
            return {"message": "User partially updated", "user": users_db[i]}
    raise HTTPException(status_code=404, detail="User not found")

