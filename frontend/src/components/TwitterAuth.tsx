// frontend/src/components/TwitterAuth.tsx
"use client";

import { useState, useEffect } from "react";
import apiClient from "@/lib/api";

export default function TwitterAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  useEffect(() => {
    // 检查localStorage中是否有token
    const storedToken = localStorage.getItem("twitter_access_token");
    if (storedToken) {
      initializeWithToken(storedToken);
    }
  }, []);

  const initializeWithToken = async (token: string) => {
    try {
      await apiClient.post("/api/auth/set-token", null, {
        params: { access_token: token },
      });
      setAccessToken(token);
      setIsAuthenticated(true);
    } catch (error) {
      console.error("Failed to initialize with token:", error);
      localStorage.removeItem("twitter_access_token");
    }
  };

  const handleLogin = async () => {
    try {
      const response = await apiClient.get("/api/auth/twitter/login");
      const authUrl = response.data.authorization_url;

      // 在新窗口打开授权页面
      const authWindow = window.open(
        authUrl,
        "Twitter Authorization",
        "width=600,height=700"
      );

      // 监听回调消息
      window.addEventListener("message", async (event) => {
        if (event.data.type === "twitter_auth_success") {
          const token = event.data.access_token;
          localStorage.setItem("twitter_access_token", token);
          await initializeWithToken(token);
          authWindow?.close();
        }
      });
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded">
      {!isAuthenticated ? (
        <>
          <p className="mb-2">请先授权Twitter账号以访问书签</p>
          <button
            onClick={handleLogin}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            授权Twitter账号
          </button>
        </>
      ) : (
        <p className="text-green-600">✓ 已授权，可以开始使用</p>
      )}
    </div>
  );
}
