import tweepy
from typing import List, Dict, Optional
from app.core.config import settings


class TwitterService:
    def __init__(self):
        # OAuth 1.0a认证
        self.auth = tweepy.OAuthHandler(settings.x_api_key, settings.x_api_secret)
        self.auth.set_access_token(settings.x_access_token, settings.x_access_secret)

        # OAuth 2.0 Bearer Token认证
        self.client = tweepy.Client(
            bearer_token=settings.x_bearer_token,
            consumer_key=settings.x_api_key,
            consumer_secret=settings.x_api_secret,
            access_token=settings.x_access_token,
            access_token_secret=settings.x_access_secret,
            wait_on_rate_limit=True,
        )

    async def get_bookmarks(
        self,
        user_id: str,
        max_results: int = 100,
        pagination_token: Optional[str] = None,
    ) -> Dict:
        """获取用户书签"""
        try:
            response = self.client.get_bookmarks(
                max_results=max_results,
                pagination_token=pagination_token,
                expansions=["author_id", "attachments.media_keys"],
                tweet_fields=["created_at", "text", "author_id", "entities"],
                user_fields=["name", "username", "profile_image_url"],
                media_fields=["url", "preview_image_url"],
            )
            return response
        except Exception as e:
            print(f"Error fetching bookmarks: {e}")
            return None

    async def delete_bookmark(self, tweet_id: str) -> bool:
        """删除书签"""
        try:
            self.client.remove_bookmark(tweet_id)
            return True
        except Exception as e:
            print(f"Error deleting bookmark {tweet_id}: {e}")
            return False


# 创建单例实例
twitter_service = TwitterService()
