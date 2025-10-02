from fastapi import FastAPI
from app.api import bookmarks, auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api import bookmarks

app = FastAPI(
    title="X Bookmark Manager API",
    description="API for managing X.com bookmarks",
    version="1.0.0",
)

app.include_router(bookmarks.router)
app.include_router(auth.router)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "X Bookmark Manager API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# 注册路由
app.include_router(bookmarks.router)

# 后续会挂载前端静态文件
# if os.path.exists("../frontend/out"):
#     app.mount("/", StaticFiles(directory="../frontend/out", html=True), name="static")
