from supabase import create_client, Client
from app.core.config import settings


def get_supabase_client() -> Client:
    """创建Supabase客户端实例"""
    return create_client(settings.supabase_url, settings.supabase_key)


supabase_client = get_supabase_client()
