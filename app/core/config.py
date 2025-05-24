import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/ai_call')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings() 