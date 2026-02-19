# FastApi Basics

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A simple FastAPI learning project demonstrating basic API concepts.

## Features
- Complete CRUD operations (Create, Read, Update, Delete)
- Pydantic models for data validation
- Path and query parameters
- HTTPException for proper error handling
- Input validation with Field constraints
- API documentation with Swagger UI

## Getting Started

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```


## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/stats` | API statistics |
| GET | `/users` | Get all users |
| GET | `/users/search` | Search users with query params |
| GET | `/users/{user_id}` | Get user by ID |
| POST | `/users` | Create new user |
| PUT | `/users/{user_id}` | Update user completely |
| PATCH | `/users/{user_id}` | Partial user update |
| DELETE | `/users/{user_id}` | Delete user |
