from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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
