from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="X-Bookmark-Manager")
    debug: bool = Field(default=True)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    supabase_url: str = Field(default="")
    supabase_key: str = Field(default="")

    x_api_key: str = Field(default="")
    x_api_secret: str = Field(default="")
    x_access_token: str = Field(default="")
    x_access_secret: str = Field(default="")
    x_bearer_token: str = Field(default="")

    # OAuth 2.0 配置（用于书签API）
    x_client_id: str
    x_client_secret: str = ""  # 如果是Public Client可以为空
    x_redirect_uri: str = "http://localhost:8000/api/auth/callback"
    x_oauth2_access_token: str = ""  # 授权后保存的token

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
