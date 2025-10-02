from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.services.twitter_service import twitter_service
from app.core.database import supabase_client
from typing import Optional

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])


@router.get("/")
async def get_all_bookmarks(limit: int = 100, offset: int = 0):
    """获取本地存储的所有书签"""
    try:
        response = (
            supabase_client.table("bookmarks")
            .select("*")
            .order("bookmarked_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return {"bookmarks": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/start")
async def start_sync(background_tasks: BackgroundTasks):
    """启动书签同步任务"""
    # 这里会在后台任务中执行同步逻辑
    return {"message": "Sync started", "status": "processing"}


@router.get("/sync/status")
async def get_sync_status():
    """查询同步任务状态"""
    return {"status": "idle", "progress": 0}
