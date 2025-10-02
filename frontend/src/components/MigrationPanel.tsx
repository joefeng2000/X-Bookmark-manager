// frontend/src/components/MigrationPanel.tsx
"use client";

import { useState, useEffect } from "react";
import apiClient from "@/lib/api";

interface Progress {
  total_fetched: number;
  total_deleted: number;
  current_batch: number;
  status: string;
}

export default function MigrationPanel() {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [isPolling, setIsPolling] = useState(false);

  useEffect(() => {
    if (isPolling) {
      const interval = setInterval(fetchProgress, 2000);
      return () => clearInterval(interval);
    }
  }, [isPolling]);

  const fetchProgress = async () => {
    try {
      const response = await apiClient.get("/api/bookmarks/sync/status");
      setProgress(response.data);

      if (
        response.data.status === "completed" ||
        response.data.status === "idle"
      ) {
        setIsPolling(false);
      }
    } catch (error) {
      console.error("Failed to fetch progress:", error);
    }
  };

  const startMigration = async () => {
    try {
      await apiClient.post("/api/bookmarks/sync/start");
      setIsPolling(true);
    } catch (error) {
      console.error("Failed to start migration:", error);
    }
  };

  const pauseMigration = async () => {
    try {
      await apiClient.post("/api/bookmarks/sync/pause");
      setIsPolling(false);
    } catch (error) {
      console.error("Failed to pause migration:", error);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">书签迁移</h2>

      {progress && (
        <div className="mb-4 space-y-2">
          <p className="text-lg">
            状态: <span className="font-semibold">{progress.status}</span>
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
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          开始迁移
        </button>
        <button
          onClick={pauseMigration}
          disabled={!isPolling}
          className="bg-orange-500 text-white px-6 py-2 rounded hover:bg-orange-600 disabled:bg-gray-400"
        >
          暂停
        </button>
      </div>
    </div>
  );
}
