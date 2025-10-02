# app/api/auth.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from app.services.twitter_service import twitter_service
from app.core.config import settings
from typing import Dict

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# 临时存储PKCE参数（生产环境应使用Redis或数据库）
pkce_storage: Dict[str, Dict[str, str]] = {}


@router.get("/twitter/login")
async def twitter_login():
    """
    启动Twitter OAuth 2.0认证流程
    """
    try:
        auth_url, state, code_verifier = twitter_service.get_authorization_url()

        # 将state和code_verifier存储起来
        pkce_storage[state] = {"code_verifier": code_verifier, "state": state}

        return {
            "authorization_url": auth_url,
            "message": "请在浏览器中打开此URL进行授权",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callback")
async def auth_callback(code: str = Query(...), state: str = Query(...)):
    """
    OAuth 2.0回调处理
    """
    try:
        # 从存储中获取PKCE参数
        if state not in pkce_storage:
            raise HTTPException(status_code=400, detail="Invalid state parameter")

        pkce_params = pkce_storage[state]
        code_verifier = pkce_params["code_verifier"]

        # 构建完整的回调URL
        callback_url = f"{settings.x_redirect_uri}?code={code}&state={state}"

        # 获取访问令牌
        token_dict = twitter_service.fetch_token(
            authorization_response_url=callback_url,
            code_verifier=code_verifier,
            state=state,
        )

        # 清理已使用的PKCE参数
        del pkce_storage[state]

        # 在生产环境中，应该将token安全地存储到数据库
        # 这里简化处理，返回给前端
        return {
            "message": "Authentication successful",
            "access_token": token_dict.get("access_token"),
            "refresh_token": token_dict.get("refresh_token"),
            "expires_in": token_dict.get("expires_in"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/set-token")
async def set_token(access_token: str):
    """
    手动设置访问令牌（用于前端存储token后重新初始化）
    """
    try:
        twitter_service.set_access_token(access_token)
        return {"message": "Token set successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
