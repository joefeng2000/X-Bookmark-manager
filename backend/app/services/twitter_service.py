# app/services/twitter_service.py
import tweepy
from typing import List, Dict, Optional, Tuple
from app.core.config import settings
import asyncio
import secrets
import hashlib
import base64


class TwitterService:
    def __init__(self):
        self.client = None
        self.current_access_token = None

    def _generate_code_verifier(self) -> str:
        """生成code_verifier"""
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode(
            "utf-8"
        )
        return code_verifier.replace("=", "")

    def _generate_code_challenge(self, verifier: str) -> str:
        """从code_verifier生成code_challenge"""
        digest = hashlib.sha256(verifier.encode("utf-8")).digest()
        challenge = base64.urlsafe_b64encode(digest).decode("utf-8")
        return challenge.replace("=", "")

    def get_authorization_url(self) -> Tuple[str, str, str]:
        """
        获取OAuth 2.0授权URL
        返回: (授权URL, state, code_verifier)
        """
        # 生成code_verifier和state
        code_verifier = self._generate_code_verifier()
        state = secrets.token_urlsafe(32)

        # 创建OAuth2UserHandler
        oauth2_handler = tweepy.OAuth2UserHandler(
            client_id=settings.x_client_id,
            redirect_uri=settings.x_redirect_uri,
            scope=[
                "tweet.read",
                "users.read",
                "bookmark.read",
                "bookmark.write",
                "offline.access",
            ],
            client_secret=(
                settings.x_client_secret
                if hasattr(settings, "x_client_secret") and settings.x_client_secret
                else None
            ),
        )

        # 手动设置内部属性（这是workaround）
        oauth2_handler._client.code_verifier = code_verifier
        oauth2_handler.state = state

        # 获取授权URL
        auth_url = oauth2_handler.get_authorization_url()

        return auth_url, state, code_verifier

    def fetch_token(
        self, authorization_response_url: str, code_verifier: str, state: str
    ) -> Dict:
        """
        使用授权回调URL获取访问令牌
        参数:
            authorization_response_url - 用户授权后的完整回调URL
            code_verifier - 之前生成的code_verifier
            state - 之前生成的state
        返回: token字典，包含access_token和refresh_token
        """
        # 创建新的OAuth2UserHandler
        oauth2_handler = tweepy.OAuth2UserHandler(
            client_id=settings.x_client_id,
            redirect_uri=settings.x_redirect_uri,
            scope=[
                "tweet.read",
                "users.read",
                "bookmark.read",
                "bookmark.write",
                "offline.access",
            ],
            client_secret=(
                settings.x_client_secret
                if hasattr(settings, "x_client_secret") and settings.x_client_secret
                else None
            ),
        )

        # 恢复code_verifier和state
        oauth2_handler._client.code_verifier = code_verifier
        oauth2_handler.state = state

        # 获取访问令牌
        token_dict = oauth2_handler.fetch_token(authorization_response_url)

        # 初始化client
        self.current_access_token = token_dict["access_token"]
        self.client = tweepy.Client(
            bearer_token=token_dict["access_token"], wait_on_rate_limit=True
        )

        return token_dict

    def set_access_token(self, access_token: str):
        """直接设置访问令牌"""
        self.current_access_token = access_token
        self.client = tweepy.Client(bearer_token=access_token, wait_on_rate_limit=True)

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
