# app/api/auth.py
from fastapi import APIRouter, HTTPException, Query
from app.services.twitter_service import twitter_service
from app.core.config import settings
from app.core.database import supabase_client
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.get("/twitter/login")
async def twitter_login():
    """启动Twitter OAuth 2.0认证流程"""
    try:
        auth_url, state, code_verifier = twitter_service.get_authorization_url()

        # 将state和code_verifier存储到数据库
        expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

        result = (
            supabase_client.table("oauth_sessions")
            .insert(
                {
                    "state": state,
                    "code_verifier": code_verifier,
                    "expires_at": expires_at,
                }
            )
            .execute()
        )

        print(
            f"[Auth] Stored PKCE session - state: {state[:20]}..., verifier: {code_verifier[:20]}..."
        )

        return {
            "authorization_url": auth_url,
            "message": "请在浏览器中打开此URL进行授权",
        }
    except Exception as e:
        print(f"[Auth] Error in twitter_login: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callback")
async def auth_callback(code: str = Query(...), state: str = Query(...)):
    """OAuth 2.0回调处理"""
    try:
        print(
            f"[Auth] Callback received - state: {state[:20]}..., code: {code[:20]}..."
        )

        # 从数据库中获取PKCE参数
        result = (
            supabase_client.table("oauth_sessions")
            .select("*")
            .eq("state", state)
            .execute()
        )

        if not result.data or len(result.data) == 0:
            print(f"[Auth] No session found for state: {state[:20]}...")
            raise HTTPException(
                status_code=400, detail="Invalid state parameter or session expired"
            )

        session = result.data[0]
        code_verifier = session["code_verifier"]

        print(
            f"[Auth] Retrieved code_verifier from DB: {code_verifier[:20]}... (length: {len(code_verifier)})"
        )

        # 检查会话是否过期
        expires_at = datetime.fromisoformat(
            session["expires_at"].replace("Z", "+00:00")
        )
        if datetime.now(expires_at.tzinfo) > expires_at:
            print(f"[Auth] Session expired")
            raise HTTPException(status_code=400, detail="Session expired")

        print(f"[Auth] Fetching token...")

        # 获取访问令牌（使用新的实现）
        token_dict = twitter_service.fetch_token(
            code=code, code_verifier=code_verifier, state=state
        )

        print(f"[Auth] Token fetched successfully")

        # 清理已使用的PKCE会话
        supabase_client.table("oauth_sessions").delete().eq("state", state).execute()

        print(f"[Auth] Session cleaned up")

        return {
            "message": "Authentication successful",
            "access_token": token_dict.get("access_token"),
            "refresh_token": token_dict.get("refresh_token"),
            "expires_in": token_dict.get("expires_in"),
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Auth] Error in callback: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@router.post("/set-token")
async def set_token(access_token: str = Query(...)):
    """手动设置访问令牌"""
    try:
        print(f"[Auth] Setting token: {access_token[:20]}...")
        twitter_service.set_access_token(access_token)
        return {"message": "Token set successfully"}
    except Exception as e:
        print(f"[Auth] Error setting token: {e}")
        raise HTTPException(status_code=500, detail=str(e))
