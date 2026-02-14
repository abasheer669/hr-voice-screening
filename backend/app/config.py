# backend/app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_service_key: str
    anthropic_api_key: str
    supabase_url: str
    supabase_bucket: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # <- ignore extra env vars
settings = Settings() 