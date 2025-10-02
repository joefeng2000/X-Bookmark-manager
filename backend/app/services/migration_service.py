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

    # app/services/migration_service.py
    async def start_migration(self) -> Dict:
        """启动完整迁移流程"""
        if self.is_running:
            return {"error": "Migration already in progress"}

        self.is_running = True
        self.progress["status"] = "running"
        self.progress["total_fetched"] = 0
        self.progress["total_deleted"] = 0
        self.progress["current_batch"] = 0

        try:
            batch_number = 1
            while self.is_running:
                self.progress["current_batch"] = batch_number
                self.progress["status"] = f"Fetching batch {batch_number}"

                print(f"[Migration] Starting batch {batch_number}")

                bookmarks = []
                pagination_token = None

                for page in range(8):
                    print(f"[Migration] Fetching page {page + 1}/8")

                    result = await self.twitter_service.fetch_bookmarks_batch(
                        max_results=100, pagination_token=pagination_token
                    )

                    # 检查是否遇到速率限制
                    if result and result.get("rate_limited"):
                        wait_seconds = result.get("wait_seconds", 900)
                        # 检查是否是月度配额用完
                        if "Monthly product cap" in str(result):
                            error_msg = f"月度API配额已用完"
                            print(f"[Migration] {error_msg}")
                            self.progress["status"] = f"error: {error_msg}"
                        else:
                            error_msg = f"Rate limit exceeded. Please wait {wait_seconds} seconds and try again."
                            print(f"[Migration] {error_msg}")
                            self.progress["status"] = f"rate_limited:{wait_seconds}"

                        self.is_running = False
                        return self.progress

                    if result is None:
                        error_msg = "Failed to fetch bookmarks from Twitter API"
                        print(f"[Migration] Error: {error_msg}")
                        self.progress["status"] = f"error: {error_msg}"
                        self.is_running = False
                        return self.progress

                    if not result.get("data"):
                        print(f"[Migration] No more bookmarks found")
                        break

                    parsed = self._parse_bookmarks(result)
                    bookmarks.extend(parsed)
                    print(
                        f"[Migration] Fetched {len(parsed)} bookmarks, total: {len(bookmarks)}"
                    )

                    pagination_token = result.get("meta", {}).get("next_token")

                    if not pagination_token:
                        print(f"[Migration] No more pages")
                        break

                if not bookmarks:
                    print(f"[Migration] No bookmarks found, migration complete")
                    self.progress["status"] = "completed"
                    break

                # 步骤2: 保存到本地数据库
                self.progress["status"] = f"Saving batch {batch_number}"
                print(f"[Migration] Saving {len(bookmarks)} bookmarks to database")

                await self.db_service.save_bookmarks(bookmarks)
                self.progress["total_fetched"] += len(bookmarks)

                print(
                    f"[Migration] Saved successfully, total fetched: {self.progress['total_fetched']}"
                )

                # 步骤3: 逐个删除
                self.progress["status"] = f"Deleting batch {batch_number}"
                print(f"[Migration] Starting deletion of {len(bookmarks)} bookmarks")

                for idx, bookmark in enumerate(bookmarks):
                    if not self.is_running:
                        print(f"[Migration] Migration paused by user")
                        break

                    print(
                        f"[Migration] Deleting bookmark {idx + 1}/{len(bookmarks)}: {bookmark['id']}"
                    )

                    success = await self.twitter_service.delete_bookmark(bookmark["id"])
                    if success:
                        await self.db_service.mark_as_deleted(bookmark["id"])
                        self.progress["total_deleted"] += 1
                        print(
                            f"[Migration] Deleted successfully, total: {self.progress['total_deleted']}"
                        )

                batch_number += 1
                print(f"[Migration] Batch {batch_number - 1} complete")

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"[Migration] Exception: {error_msg}")
            import traceback

            print(f"[Migration] Traceback: {traceback.format_exc()}")
            self.progress["status"] = f"error: {error_msg}"
        finally:
            self.is_running = False
            print(
                f"[Migration] Migration stopped, final status: {self.progress['status']}"
            )

        return self.progress

    def _parse_bookmarks(self, api_response: Dict) -> List[Dict]:
        """解析API响应为标准格式"""
        bookmarks = []
        tweets = api_response.get("data", [])

        # 安全获取includes数据
        includes = api_response.get("includes") or {}
        users = (
            {user["id"]: user for user in includes.get("users", [])} if includes else {}
        )
        media_list = includes.get("media", []) if includes else []
        media = {m.get("media_key"): m for m in media_list if m.get("media_key")}

        print(f"[Migration] Parsing {len(tweets)} tweets")
        print(f"[Migration] Available users: {len(users)}, media: {len(media)}")

        for idx, tweet in enumerate(tweets):
            try:
                tweet_id = tweet.get("id", "")
                author_id = tweet.get("author_id", "")

                # 安全获取作者信息
                author = users.get(author_id) if author_id else None

                bookmark_data = {
                    "id": tweet_id,
                    "text": tweet.get("text", ""),
                    "author_id": author_id,
                    "author_name": author.get("name", "") if author else "Unknown",
                    "author_handle": (
                        author.get("username", "") if author else "unknown"
                    ),
                    "author_avatar_url": (
                        author.get("profile_image_url", "") if author else ""
                    ),
                    "created_at": tweet.get("created_at", ""),
                    "media_urls": self._extract_media_urls(tweet, media),
                }

                bookmarks.append(bookmark_data)

            except Exception as e:
                print(
                    f"[Migration] Error parsing tweet {idx + 1}: {type(e).__name__}: {str(e)}"
                )
                print(f"[Migration] Tweet data: {tweet}")
                # 跳过有问题的tweet，继续处理其他的
                continue

        print(f"[Migration] Successfully parsed {len(bookmarks)} bookmarks")
        return bookmarks

    def _extract_media_urls(self, tweet: Dict, media_dict: Dict) -> List[str]:
        """提取媒体URL"""
        try:
            attachments = tweet.get("attachments")
            if not attachments:
                return []

            media_keys = attachments.get("media_keys", [])
            urls = []

            for key in media_keys:
                if key in media_dict:
                    media_item = media_dict[key]
                    url = media_item.get("url") or media_item.get(
                        "preview_image_url", ""
                    )
                    if url:
                        urls.append(url)

            return urls
        except Exception as e:
            print(
                f"[Migration] Error extracting media URLs: {type(e).__name__}: {str(e)}"
            )
            return []

    def get_progress(self) -> Dict:
        """获取迁移进度"""
        return self.progress

    def pause_migration(self):
        """暂停迁移"""
        print(f"[Migration] Pause requested")
        self.is_running = False
        self.progress["status"] = "paused"


migration_service = MigrationService()
