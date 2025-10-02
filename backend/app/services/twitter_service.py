# app/services/twitter_service.py
import tweepy
from typing import List, Dict, Optional
from app.core.config import settings
import asyncio


class TwitterService:
    def __init__(self):
        # OAuth 2.0 PKCE认证需要在初始化时设置
        self.oauth2_user_handler = tweepy.OAuth2UserHandler(
            client_id=settings.x_client_id,
            redirect_uri=settings.x_redirect_uri,
            scope=["tweet.read", "users.read", "bookmark.read", "bookmark.write"],
            client_secret=settings.x_client_secret,  # 如果是Confidential Client则需要
        )

        # 如果已经有access_token，直接使用
        self.client = None
        if (
            hasattr(settings, "x_oauth2_access_token")
            and settings.x_oauth2_access_token
        ):
            self.client = tweepy.Client(
                bearer_token=settings.x_oauth2_access_token, wait_on_rate_limit=True
            )

    def get_authorization_url(self) -> tuple[str, str, str]:
        """
        获取OAuth 2.0授权URL
        返回: (授权URL, state, code_verifier)
        """
        auth_url = self.oauth2_user_handler.get_authorization_url()
        return (
            auth_url,
            self.oauth2_user_handler.state,
            self.oauth2_user_handler.code_verifier,
        )

    def fetch_token(self, authorization_response_url: str) -> str:
        """
        使用授权回调URL获取访问令牌
        参数: authorization_response_url - 用户授权后的完整回调URL
        返回: access_token
        """
        access_token = self.oauth2_user_handler.fetch_token(authorization_response_url)

        # 使用获取的token初始化client
        self.client = tweepy.Client(bearer_token=access_token, wait_on_rate_limit=True)

        return access_token

    async def fetch_bookmarks_batch(
        self, max_results: int = 100, pagination_token: Optional[str] = None
    ) -> Dict:
        """获取一批书签(最多100条)"""
        if not self.client:
            raise Exception("Client not initialized. Please authenticate first.")

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
        if not self.client:
            raise Exception("Client not initialized. Please authenticate first.")

        try:
            self.client.remove_bookmark(tweet_id)
            await asyncio.sleep(20)  # 每20秒删除一个
            return True
        except Exception as e:
            print(f"Error deleting bookmark {tweet_id}: {e}")
            return False


# 创建单例实例
twitter_service = TwitterService()
