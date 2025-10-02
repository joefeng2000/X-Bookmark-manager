# app/api/bookmarks.py
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from app.services.migration_service import migration_service
from app.core.database import supabase_client
from typing import Optional, List

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])


@router.post("/sync/start")
async def start_sync(background_tasks: BackgroundTasks):
    """启动书签同步迁移任务"""
    background_tasks.add_task(migration_service.start_migration)
    return {"message": "Migration started", "status": "processing"}


@router.post("/sync/pause")
async def pause_sync():
    """暂停正在进行的迁移"""
    migration_service.pause_migration()
    return {"message": "Migration paused"}


@router.get("/sync/status")
async def get_sync_status():
    """获取迁移进度"""
    return migration_service.get_progress()


@router.get("/")
async def get_bookmarks(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    folder_id: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
):
    """获取本地书签列表,支持筛选和搜索"""
    try:
        query = supabase_client.table("bookmarks").select("*")

        if folder_id:
            query = query.eq("local_folder_id", folder_id)

        if tag:
            query = query.contains("local_tags", [tag])

        if search:
            query = query.or_(f"text.ilike.%{search}%,author_name.ilike.%{search}%")

        response = (
            query.order("bookmarked_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )

        return {"bookmarks": response.data, "count": len(response.data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{tweet_id}")
async def delete_local_bookmark(tweet_id: str):
    """从本地删除书签"""
    try:
        response = (
            supabase_client.table("bookmarks")
            .delete()
            .eq("tweet_id", tweet_id)
            .execute()
        )
        return {"message": "Bookmark deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{tweet_id}")
async def update_bookmark(
    tweet_id: str,
    folder_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    notes: Optional[str] = None,
):
    """更新书签的本地信息(标签、文件夹、备注)"""
    try:
        update_data = {}
        if folder_id is not None:
            update_data["local_folder_id"] = folder_id
        if tags is not None:
            update_data["local_tags"] = tags
        if notes is not None:
            update_data["local_notes"] = notes

        response = (
            supabase_client.table("bookmarks")
            .update(update_data)
            .eq("tweet_id", tweet_id)
            .execute()
        )

        return {"message": "Bookmark updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
