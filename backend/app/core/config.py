from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="X-Bookmark-Manager")
    debug: bool = Field(default=True)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # OAuth 2.0 配置
    x_client_id: str
    x_client_secret: str = ""
    x_redirect_uri: str = "http://localhost:8000/api/auth/callback"

    # Supabase配置
    supabase_url: str
    supabase_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
