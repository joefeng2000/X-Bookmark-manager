# app/services/migration_service.py
from app.services.twitter_service import twitter_service
from app.services.database_service import DatabaseService
from typing import Dict, Optional, List
import asyncio


class MigrationService:
    def __init__(self):
        self.twitter_service = twitter_service
        self.db_service = DatabaseService()
        self.is_running = False
        self.progress = {
            "total_fetched": 0,
            "total_deleted": 0,
            "current_batch": 0,
            "status": "idle",
        }

    async def start_migration(self) -> Dict:
        """启动完整迁移流程"""
        if self.is_running:
            return {"error": "Migration already in progress"}

        self.is_running = True
        self.progress["status"] = "running"

        try:
            batch_number = 1
            while self.is_running:
                # 步骤1: 获取最多800个书签
                self.progress["current_batch"] = batch_number
                self.progress["status"] = f"Fetching batch {batch_number}"

                bookmarks = []
                pagination_token = None

                for page in range(8):  # 8页 x 100 = 800
                    result = await self.twitter_service.fetch_bookmarks_batch(
                        max_results=100, pagination_token=pagination_token
                    )

                    if not result or not result.get("data"):
                        break

                    bookmarks.extend(self._parse_bookmarks(result))
                    pagination_token = result.get("meta", {}).get("next_token")

                    if not pagination_token:
                        break

                if not bookmarks:
                    # 没有更多书签,迁移完成
                    self.progress["status"] = "completed"
                    break

                # 步骤2: 保存到本地数据库
                self.progress["status"] = f"Saving batch {batch_number}"
                await self.db_service.save_bookmarks(bookmarks)
                self.progress["total_fetched"] += len(bookmarks)

                # 步骤3: 逐个删除
                self.progress["status"] = f"Deleting batch {batch_number}"
                for bookmark in bookmarks:
                    if not self.is_running:
                        break

                    success = await self.twitter_service.delete_bookmark(bookmark["id"])
                    if success:
                        await self.db_service.mark_as_deleted(bookmark["id"])
                        self.progress["total_deleted"] += 1

                batch_number += 1

        except Exception as e:
            self.progress["status"] = f"error: {str(e)}"
        finally:
            self.is_running = False

        return self.progress

    def _parse_bookmarks(self, api_response: Dict) -> List[Dict]:
        """解析API响应为标准格式"""
        bookmarks = []
        tweets = api_response.get("data", [])
        includes = api_response.get("includes", {})
        users = {user["id"]: user for user in includes.get("users", [])}
        media = {m["media_key"]: m for m in includes.get("media", [])}

        for tweet in tweets:
            author = users.get(tweet.get("author_id", ""), {})
            bookmarks.append(
                {
                    "id": tweet["id"],
                    "text": tweet.get("text", ""),
                    "author_id": tweet.get("author_id", ""),
                    "author_name": author.get("name", ""),
                    "author_handle": author.get("username", ""),
                    "author_avatar_url": author.get("profile_image_url", ""),
                    "created_at": tweet.get("created_at"),
                    "media_urls": self._extract_media_urls(tweet, media),
                }
            )

        return bookmarks

    def _extract_media_urls(self, tweet: Dict, media_dict: Dict) -> List[str]:
        """提取媒体URL"""
        media_keys = tweet.get("attachments", {}).get("media_keys", [])
        return [media_dict.get(key, {}).get("url", "") for key in media_keys]

    def get_progress(self) -> Dict:
        """获取迁移进度"""
        return self.progress

    def pause_migration(self):
        """暂停迁移"""
        self.is_running = False
        self.progress["status"] = "paused"


migration_service = MigrationService()
