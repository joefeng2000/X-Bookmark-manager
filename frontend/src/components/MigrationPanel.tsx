// frontend/src/components/MigrationPanel.tsx
"use client";

import { useState, useEffect, useRef } from "react";
import apiClient from "@/lib/api";
import { getErrorMessage } from "@/lib/errorHandler";

interface Progress {
  total_fetched: number;
  total_deleted: number;
  current_batch: number;
  status: string;
}

export default function MigrationPanel() {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [rateLimitSeconds, setRateLimitSeconds] = useState<number | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const countdownIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (isPolling) {
      fetchProgress();
      pollingIntervalRef.current = setInterval(fetchProgress, 2000);
    } else {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
    }

    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
      if (countdownIntervalRef.current) {
        clearInterval(countdownIntervalRef.current);
      }
    };
  }, [isPolling]);

  // 倒计时逻辑
  useEffect(() => {
    if (rateLimitSeconds !== null && rateLimitSeconds > 0) {
      countdownIntervalRef.current = setInterval(() => {
        setRateLimitSeconds((prev) => {
          if (prev === null || prev <= 1) {
            if (countdownIntervalRef.current) {
              clearInterval(countdownIntervalRef.current);
              countdownIntervalRef.current = null;
            }
            return null;
          }
          return prev - 1;
        });
      }, 1000);

      return () => {
        if (countdownIntervalRef.current) {
          clearInterval(countdownIntervalRef.current);
        }
      };
    }
  }, [rateLimitSeconds]);

  // frontend/src/components/MigrationPanel.tsx
  const fetchProgress = async () => {
    try {
      const response = await apiClient.get("/api/bookmarks/sync/status");
      setProgress(response.data);

      // 检查状态中是否包含速率限制信息
      const status = response.data.status;
      if (typeof status === "string") {
        // 新格式：rate_limited:900
        if (status.startsWith("rate_limited:")) {
          const seconds = parseInt(status.split(":")[1]);
          setRateLimitSeconds(seconds);
        }
        // 旧格式：Sleeping for X seconds（兼容）
        else if (status.includes("Sleeping for")) {
          const match = status.match(/Sleeping for (\d+) seconds/);
          if (match) {
            setRateLimitSeconds(parseInt(match[1]));
          }
        } else {
          setRateLimitSeconds(null);
        }
      }

      // 如果任务完成、失败或遇到速率限制，停止轮询
      if (
        status === "completed" ||
        status === "idle" ||
        (typeof status === "string" &&
          (status.startsWith("error:") || status.startsWith("rate_limited:")))
      ) {
        setIsPolling(false);
      }
    } catch (err) {
      console.error("Failed to fetch progress:", getErrorMessage(err));
      setIsPolling(false);
    }
  };

  const startMigration = async () => {
    const token = localStorage.getItem("twitter_access_token");
    if (!token) {
      alert("请先授权Twitter账号！");
      return;
    }

    try {
      await apiClient.post("/api/bookmarks/sync/start");
      setIsPolling(true);
      setRateLimitSeconds(null);
    } catch (err) {
      const errorMsg = getErrorMessage(err);
      console.error("Failed to start migration:", err);
      alert("启动迁移失败: " + errorMsg);
    }
  };

  const pauseMigration = async () => {
    try {
      await apiClient.post("/api/bookmarks/sync/pause");
      setIsPolling(false);
    } catch (err) {
      console.error("Failed to pause migration:", getErrorMessage(err));
    }
  };

  const getStatusColor = (status: string) => {
    if (status === "completed") return "text-green-600";
    if (status.startsWith("error:")) return "text-red-600";
    if (status === "idle") return "text-gray-600";
    if (status.includes("Sleeping")) return "text-orange-600";
    return "text-blue-600";
  };

  const getStatusDisplay = (status: string) => {
    // 速率限制 - 新格式
    if (status.startsWith("rate_limited:")) {
      const seconds = parseInt(status.split(":")[1]);
      const minutes = Math.floor(seconds / 60);
      return `遇到速率限制，请等待约 ${minutes} 分钟后重试`;
    }

    // 翻译其他常见状态
    if (status === "idle") return "空闲";
    if (status === "completed") return "完成";
    if (status === "paused") return "已暂停";
    if (status.startsWith("Fetching batch")) {
      const match = status.match(/Fetching batch (\d+)/);
      if (match) return `正在获取第 ${match[1]} 批书签`;
    }
    if (status.startsWith("Saving batch")) {
      const match = status.match(/Saving batch (\d+)/);
      if (match) return `正在保存第 ${match[1]} 批书签`;
    }
    if (status.startsWith("Deleting batch")) {
      const match = status.match(/Deleting batch (\d+)/);
      if (match) return `正在删除第 ${match[1]} 批书签`;
    }
    if (status.startsWith("error:")) {
      return `错误: ${status.substring(7)}`;
    }

    return status;
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">书签迁移</h2>

      {progress && (
        <div className="mb-4 space-y-3">
          <div className="flex items-start gap-2">
            <span className="text-gray-600 min-w-[60px]">状态:</span>
            <span
              className={`font-semibold ${getStatusColor(progress.status)}`}
            >
              {getStatusDisplay(progress.status)}
            </span>
          </div>

          {/* 速率限制倒计时显示 */}
          {rateLimitSeconds !== null && rateLimitSeconds > 0 && (
            <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <svg
                  className="w-5 h-5 text-orange-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span className="text-orange-800 font-semibold">
                  X API 速率限制
                </span>
              </div>
              <p className="text-orange-700 text-sm mb-2">
                已达到X API的速率限制，程序会自动等待后继续执行
              </p>
              <div className="flex items-center gap-3">
                <div className="flex-1 bg-orange-200 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-orange-600 h-full transition-all duration-1000"
                    style={{
                      width: `${100 - (rateLimitSeconds / 900) * 100}%`,
                    }}
                  />
                </div>
                <span className="text-orange-800 font-mono font-bold text-lg min-w-[60px]">
                  {formatTime(rateLimitSeconds)}
                </span>
              </div>
              <p className="text-orange-600 text-xs mt-2">
                提示：X API限制为 180次请求/15分钟，程序会自动恢复
              </p>
            </div>
          )}

          <div className="grid grid-cols-3 gap-4 pt-2">
            <div className="bg-blue-50 p-3 rounded">
              <p className="text-blue-600 text-sm mb-1">当前批次</p>
              <p className="text-2xl font-bold text-blue-700">
                {progress.current_batch}
              </p>
            </div>
            <div className="bg-green-50 p-3 rounded">
              <p className="text-green-600 text-sm mb-1">已获取</p>
              <p className="text-2xl font-bold text-green-700">
                {progress.total_fetched} 条
              </p>
            </div>
            <div className="bg-purple-50 p-3 rounded">
              <p className="text-purple-600 text-sm mb-1">已删除</p>
              <p className="text-2xl font-bold text-purple-700">
                {progress.total_deleted} 条
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="flex gap-3">
        <button
          onClick={startMigration}
          disabled={isPolling}
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {isPolling ? (
            <>
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              迁移中...
            </>
          ) : (
            "开始迁移"
          )}
        </button>
        <button
          onClick={pauseMigration}
          disabled={!isPolling}
          className="bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          暂停
        </button>
      </div>

      {/* 使用说明 */}
      <div className="mt-4 p-3 bg-gray-50 rounded text-sm text-gray-600">
        <p className="font-semibold mb-1">📌 使用说明：</p>
        <ul className="list-disc list-inside space-y-1">
          <li>迁移过程会自动处理速率限制，无需手动干预</li>
          <li>每批次最多获取800条书签</li>
          <li>删除操作会遵守API限制（每20秒删除1条）</li>
          <li>可以随时点击(暂停)停止迁移</li>
        </ul>
      </div>
    </div>
  );
}
