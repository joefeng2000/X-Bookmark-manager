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
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

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
    };
  }, [isPolling]);

  const fetchProgress = async () => {
    try {
      const response = await apiClient.get("/api/bookmarks/sync/status");
      setProgress(response.data);

      if (
        response.data.status === "completed" ||
        response.data.status === "idle" ||
        response.data.status.startsWith("error:")
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
    return "text-blue-600";
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">书签迁移</h2>

      {progress && (
        <div className="mb-4 space-y-2">
          <p className="text-lg">
            状态:{" "}
            <span
              className={`font-semibold ${getStatusColor(progress.status)}`}
            >
              {progress.status}
            </span>
          </p>
          <p>当前批次: {progress.current_batch}</p>
          <p>已获取: {progress.total_fetched} 条</p>
          <p>已删除: {progress.total_deleted} 条</p>
        </div>
      )}

      <div className="flex gap-3">
        <button
          onClick={startMigration}
          disabled={isPolling}
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isPolling ? "迁移中..." : "开始迁移"}
        </button>
        <button
          onClick={pauseMigration}
          disabled={!isPolling}
          className="bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          暂停
        </button>
      </div>
    </div>
  );
}
