# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # OAuth 2.0 配置（用于书签API）
    x_client_id: str
    x_client_secret: str = ""
    x_redirect_uri: str = "http://localhost:8000/api/auth/callback"

    # Supabase配置
    supabase_url: str
    supabase_key: str

    # 配置允许额外字段（不会报错）
    model_config = ConfigDict(
        env_file=".env", extra="ignore"  # 忽略未定义的字段，而不是报错
    )


settings = Settings()
