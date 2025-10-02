# app/main.py
import os

# ⚠️ 仅用于开发环境 - 允许OAuth2使用HTTP而不是HTTPS
# 生产环境部署时应该删除这行，使用真正的HTTPS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import bookmarks, auth

app = FastAPI(
    title="X Bookmark Manager API",
    description="Personal X.com bookmark management system",
    version="1.0.0",
)

# CORS配置 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(bookmarks.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {
        "message": "X Bookmark Manager API",
        "status": "running",
        "version": "1.0.0",
    }
