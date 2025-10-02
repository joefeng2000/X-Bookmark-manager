# app/services/twitter_service.py
import tweepy
import requests
import secrets
import hashlib
import base64
from typing import List, Dict, Optional, Tuple
from app.core.config import settings
import asyncio


class TwitterService:
    def __init__(self):
        self.client = None
        self.current_access_token = None

    def _generate_code_verifier(self) -> str:
        """生成code_verifier (43-128个字符)"""
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode(
            "utf-8"
        )
        code_verifier = code_verifier.rstrip("=")
        print(
            f"[TwitterService] Generated code_verifier: {code_verifier[:20]}... (length: {len(code_verifier)})"
        )
        return code_verifier

    def _generate_code_challenge(self, verifier: str) -> str:
        """从code_verifier生成code_challenge"""
        digest = hashlib.sha256(verifier.encode("utf-8")).digest()
        challenge = base64.urlsafe_b64encode(digest).decode("utf-8")
        challenge = challenge.rstrip("=")
        print(
            f"[TwitterService] Generated code_challenge: {challenge[:20]}... (length: {len(challenge)})"
        )
        return challenge

    def get_authorization_url(self) -> Tuple[str, str, str]:
        """
        获取OAuth 2.0授权URL（不使用tweepy）
        返回: (授权URL, state, code_verifier)
        """
        print("[TwitterService] Starting get_authorization_url")

        # 生成code_verifier和state
        code_verifier = self._generate_code_verifier()
        code_challenge = self._generate_code_challenge(code_verifier)
        state = secrets.token_urlsafe(32)

        # 手动构建授权URL
        scopes = [
            "tweet.read",
            "users.read",
            "bookmark.read",
            "bookmark.write",
            "offline.access",
        ]
        scope_string = " ".join(scopes)

        params = {
            "response_type": "code",
            "client_id": settings.x_client_id,
            "redirect_uri": settings.x_redirect_uri,
            "scope": scope_string,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        auth_url = "https://twitter.com/i/oauth2/authorize?" + "&".join(
            [f"{k}={requests.utils.quote(str(v))}" for k, v in params.items()]
        )

        print(f"[TwitterService] Authorization URL generated")
        print(f"[TwitterService] State: {state[:20]}...")
        print(f"[TwitterService] Code verifier: {code_verifier[:20]}...")
        print(f"[TwitterService] Code challenge: {code_challenge[:20]}...")

        return auth_url, state, code_verifier

    def fetch_token(self, code: str, code_verifier: str, state: str) -> Dict:
        """
        使用authorization code获取访问令牌（不使用tweepy）
        """
        print(f"[TwitterService] Starting fetch_token")
        print(f"[TwitterService] Code: {code[:20]}...")
        print(
            f"[TwitterService] Code verifier: {code_verifier[:20]}... (length: {len(code_verifier)})"
        )
        print(f"[TwitterService] State: {state[:20]}...")

        # 直接调用Twitter的token端点
        token_url = "https://api.twitter.com/2/oauth2/token"

        # 准备请求数据
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": settings.x_client_id,
            "redirect_uri": settings.x_redirect_uri,
            "code_verifier": code_verifier,
        }

        # 准备请求头
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # 如果是Confidential Client，使用Basic Authentication
        if hasattr(settings, "x_client_secret") and settings.x_client_secret:
            print(f"[TwitterService] Using Basic Authentication (Confidential Client)")
            # 创建Basic Auth Token: Base64(client_id:client_secret)
            credentials = f"{settings.x_client_id}:{settings.x_client_secret}"
            basic_auth_token = base64.b64encode(credentials.encode("utf-8")).decode(
                "utf-8"
            )
            headers["Authorization"] = f"Basic {basic_auth_token}"
            print(
                f"[TwitterService] Basic Auth Token created (first 20 chars): {basic_auth_token[:20]}..."
            )
        else:
            print(f"[TwitterService] No client_secret found, using Public Client mode")

        print(f"[TwitterService] Calling token endpoint...")
        print(f"[TwitterService] Token URL: {token_url}")
        print(f"[TwitterService] Data keys: {list(data.keys())}")
        print(f"[TwitterService] Headers: {list(headers.keys())}")

        try:
            response = requests.post(token_url, data=data, headers=headers)

            print(f"[TwitterService] Response status: {response.status_code}")

            if response.status_code != 200:
                print(f"[TwitterService] Error response: {response.text}")
                response.raise_for_status()

            token_dict = response.json()
            print(f"[TwitterService] Token received successfully")
            print(f"[TwitterService] Token keys: {list(token_dict.keys())}")

            # 初始化client
            self.current_access_token = token_dict["access_token"]
            self.client = tweepy.Client(
                bearer_token=token_dict["access_token"], wait_on_rate_limit=True
            )

            return token_dict
        except Exception as e:
            print(
                f"[TwitterService] Error fetching token: {type(e).__name__}: {str(e)}"
            )
            raise

    def set_access_token(self, access_token: str):
        """直接设置访问令牌"""
        print(f"[TwitterService] Setting access token: {access_token[:20]}...")
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
            await asyncio.sleep(20)
            return True
        except Exception as e:
            print(f"Error deleting bookmark {tweet_id}: {e}")
            return False


# 创建单例实例
twitter_service = TwitterService()
