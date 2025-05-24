import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'postgresql://default:pL9akltcEDT8@ep-solitary-wave-a4f1k0qk-pooler.us-east-1.aws.neon.tech/verceldb?sslmode=require')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 43200))
    SCHEMA: str = os.getenv('SCHEMA', 'ai-call')

settings = Settings() 