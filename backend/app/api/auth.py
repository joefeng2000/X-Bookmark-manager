# app/api/auth.py
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from app.services.twitter_service import twitter_service
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.get("/twitter/login")
async def twitter_login():
    """
    启动Twitter OAuth 2.0认证流程
    """
    try:
        auth_url, state, code_verifier = twitter_service.get_authorization_url()

        # 将state和code_verifier保存到数据库或session中
        # 这里简化处理，实际项目应该安全存储

        return {
            "authorization_url": auth_url,
            "state": state,
            "code_verifier": code_verifier,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/callback")
async def auth_callback(code: str = Query(...), state: str = Query(...)):
    """
    OAuth 2.0回调处理
    """
    try:
        # 构建完整的回调URL
        callback_url = f"{settings.x_redirect_uri}?code={code}&state={state}"

        # 获取访问令牌
        access_token = twitter_service.fetch_token(callback_url)

        # 将token保存到环境变量或数据库
        # 实际项目中应该加密存储

        return {"message": "Authentication successful", "access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
