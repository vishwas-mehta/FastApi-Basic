from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic model for User
class User(BaseModel):
    id: int
    name: str
    description: str

# In-memory database
users_db: List[User] = []

@app.get('/')
def root():
    return {"message": "Welcome to FastAPI Basic Learning"}

@app.get('/users')
def get_users():
    return {"users": users_db}

@app.get('/users/search')
def search_users(name: Optional[str] = None, skip: int = 0, limit: int = 10):
    results = users_db
    if name:
        results = [u for u in users_db if name.lower() in u.name.lower()]
    return {"users": results[skip:skip + limit]}

@app.post('/users')
def create_user(user: User):
    users_db.append(user)
    return {"message": "User created successfully", "user": user}

@app.get('/users/{user_id}')
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return {"user": user}
    return {"error": "User not found"}

@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            deleted_user = users_db.pop(i)
            return {"message": "User deleted", "user": deleted_user}
    return {"error": "User not found"}
