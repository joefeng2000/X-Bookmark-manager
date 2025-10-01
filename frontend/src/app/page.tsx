"use client";

import { useEffect, useState } from "react";
import apiClient from "@/lib/api";

export default function Home() {
  const [apiStatus, setApiStatus] = useState<string>("检查中...");

  useEffect(() => {
    // console.log("ENV:", process.env.NEXT_PUBLIC_API_URL);
    // console.log("BASE:", apiClient.defaults.baseURL);
    apiClient
      .get("/health")
      .then((res) => setApiStatus(`后端连接成功: ${res.data.status}`))
      .catch(() => setApiStatus("后端连接失败"));
  }, []);

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-4">X Bookmark Manager</h1>
      <p className="text-lg">{apiStatus}</p>
    </main>
  );
}
