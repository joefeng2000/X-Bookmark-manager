from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="X Bookmark Manager API",
    description="API for managing X.com bookmarks",
    version="1.0.0",
)

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


# 后续会挂载前端静态文件
# if os.path.exists("../frontend/out"):
#     app.mount("/", StaticFiles(directory="../frontend/out", html=True), name="static")
