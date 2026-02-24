"""
FastAPI Basic Learning Application

A simple REST API demonstrating FastAPI fundamentals including
CRUD operations, data validation, and proper error handling.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import User, UserUpdate

# API Version constant
API_VERSION = "1.0.0"

app = FastAPI(
    title="FastAPI Basic Learning",
    description="A simple REST API for learning FastAPI fundamentals",
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database with sample data
users_db: List[User] = [
    User(id=1, name="John Doe", email="john.doe@example.com", description="Software developer"),
    User(id=2, name="Jane Smith", email="jane.smith@example.com", description="Data scientist"),
    User(id=3, name="Bob Johnson", email="bob.johnson@example.com", description="DevOps engineer")
]

@app.get('/')
def root():
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to FastAPI Basic Learning"}

@app.get('/health')
def health_check():
    """Health check endpoint returning API status."""
    return {"status": "healthy", "users_count": len(users_db)}

@app.get('/api/info')
def api_info():
    """Return API metadata and configuration."""
    return {
        "name": "FastAPI Basic Learning",
        "description": "A simple REST API for learning FastAPI fundamentals",
        "version": API_VERSION,
        "author": "Vishwas",
        "endpoints": ["/health", "/stats", "/users", "/api/info"]
    }

@app.get('/stats')
def get_stats():
    """Return API statistics including user count and active users."""
    active_count = sum(1 for u in users_db if u.is_active)
    return {"total_users": len(users_db), "active_users": active_count, "api_version": API_VERSION}

@app.get('/users/active')
def get_active_users():
    """Retrieve only active users from the database."""
    active = [u for u in users_db if u.is_active]
    return {"users": active, "count": len(active)}

@app.get('/users/count')
def get_user_count():
    """Return the total number of users and breakdown by role."""
    role_counts = {}
    for u in users_db:
        role_counts[u.role] = role_counts.get(u.role, 0) + 1
    return {"total": len(users_db), "by_role": role_counts}

@app.get('/users')
def get_users(sort_by_name: bool = False):
    """Retrieve all users from the database, optionally sorted by name."""
    if sort_by_name:
        return {"users": sorted(users_db, key=lambda u: u.name.lower())}
    return {"users": users_db}

@app.get('/users/search')
def search_users(name: Optional[str] = None, skip: int = 0, limit: int = 10):
    """
    Search users by name with pagination support.
    
    Args:
        name: Optional name filter (case-insensitive partial match)
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 10)
    """
    results = users_db
    if name:
        results = [u for u in users_db if name.lower() in u.name.lower()]
    return {"users": results[skip:skip + limit], "total": len(results)}

@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    """Create a new user in the database."""
    # Check if user with same ID already exists
    for existing_user in users_db:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
        if user.email and existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    users_db.append(user)
    return {"message": "User created successfully", "user": user}

@app.get('/users/{user_id}')
def get_user(user_id: int):
    """Retrieve a specific user by their ID."""
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
    
# patch api
@app.patch('/users/{user_id}')
def partial_update_user(user_id: int, user_update: UserUpdate):
    """Partially update a user by their ID."""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            if user_update.name is not None:
                users_db[i] = User(id=user.id, name=user_update.name, description=user.description)
            if user_update.description is not None:
                users_db[i] = User(id=users_db[i].id, name=users_db[i].name, description=user_update.description)
            return {"message": "User partially updated", "user": users_db[i]}
    raise HTTPException(status_code=404, detail="User not found")

@app.patch('/users/{user_id}/deactivate')
def deactivate_user(user_id: int):
    """Deactivate a user by their ID."""
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db[i].is_active = False
            return {"message": "User deactivated", "user": users_db[i]}
    raise HTTPException(status_code=404, detail="User not found")

