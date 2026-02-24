import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Basic Learning"
    admin_email: str = "admin@example.com"
    debug_mode: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
