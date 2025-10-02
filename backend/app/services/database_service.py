# app/services/database_service.py
from app.core.database import supabase_client
from typing import List, Dict, Optional
from datetime import datetime


class DatabaseService:

    async def save_bookmarks(self, bookmarks: List[Dict]) -> bool:
        """批量保存书签到本地数据库"""
        try:
            formatted_data = []
            for bookmark in bookmarks:
                formatted_data.append(
                    {
                        "tweet_id": bookmark["id"],
                        "text": bookmark.get("text", ""),
                        "author_id": bookmark.get("author_id", ""),
                        "author_name": bookmark.get("author_name", ""),
                        "author_handle": bookmark.get("author_handle", ""),
                        "author_avatar_url": bookmark.get("author_avatar_url", ""),
                        "created_at": bookmark.get("created_at"),
                        "bookmarked_at": datetime.now().isoformat(),
                        "original_url": f"https://twitter.com/i/status/{bookmark['id']}",
                        "media_urls": bookmark.get("media_urls", []),
                        "sync_status": "synced",
                    }
                )

            response = (
                supabase_client.table("bookmarks").upsert(formatted_data).execute()
            )
            return True
        except Exception as e:
            print(f"Error saving bookmarks: {e}")
            return False

    async def get_synced_bookmarks(self, limit: int = 800) -> List[Dict]:
        """获取已同步但未删除的书签"""
        try:
            response = (
                supabase_client.table("bookmarks")
                .select("*")
                .eq("sync_status", "synced")
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error getting synced bookmarks: {e}")
            return []

    async def mark_as_deleted(self, tweet_id: str) -> bool:
        """标记书签已从X平台删除"""
        try:
            response = (
                supabase_client.table("bookmarks")
                .update({"sync_status": "deleted_from_x"})
                .eq("tweet_id", tweet_id)
                .execute()
            )
            return True
        except Exception as e:
            print(f"Error marking bookmark as deleted: {e}")
            return False
