# app/services/twitter_service.py
import tweepy
from typing import List, Dict, Optional
from app.core.config import settings
import asyncio


class TwitterService:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=settings.x_bearer_token,
            consumer_key=settings.x_api_key,
            consumer_secret=settings.x_api_secret,
            access_token=settings.x_access_token,
            access_token_secret=settings.x_access_secret,
            wait_on_rate_limit=True,
        )

    async def fetch_bookmarks_batch(
        self, max_results: int = 100, pagination_token: Optional[str] = None
    ) -> Dict:
        """获取一批书签(最多100条)"""
        try:
            response = self.client.get_bookmarks(
                max_results=max_results,
                pagination_token=pagination_token,
                expansions=["author_id", "attachments.media_keys"],
                tweet_fields=["created_at", "text", "author_id", "entities"],
                user_fields=["name", "username", "profile_image_url"],
                media_fields=["url", "preview_image_url"],
            )
            return {
                "data": response.data,
                "includes": response.includes,
                "meta": response.meta,
            }
        except Exception as e:
            print(f"Error fetching bookmarks: {e}")
            return None

    async def delete_bookmark(self, tweet_id: str) -> bool:
        """删除单个书签,遵守速率限制"""
        try:
            self.client.remove_bookmark(tweet_id)
            await asyncio.sleep(20)  # 每20秒删除一个
            return True
        except Exception as e:
            print(f"Error deleting bookmark {tweet_id}: {e}")
            return False


# 创建单例实例
twitter_service = TwitterService()
