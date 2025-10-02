// frontend/src/components/TwitterAuth.tsx
"use client";

import { useState, useEffect } from "react";
import apiClient from "@/lib/api";
import { getErrorMessage } from "@/lib/errorHandler";

export default function TwitterAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log("[TwitterAuth] Component mounted");

    // 检查localStorage中是否有token
    const storedToken = localStorage.getItem("twitter_access_token");
    console.log(
      "[TwitterAuth] Stored token:",
      storedToken ? "exists" : "not found"
    );

    if (storedToken) {
      initializeWithToken(storedToken);
    }

    const handleMessage = async (event: MessageEvent) => {
      console.log("[TwitterAuth] Received message:", event.data);
      console.log("[TwitterAuth] Message origin:", event.origin);
      console.log("[TwitterAuth] Window origin:", window.location.origin);

      // 安全检查：确保消息来自预期的源
      if (event.origin !== window.location.origin) {
        console.warn("[TwitterAuth] Message from unexpected origin, ignoring");
        return;
      }

      if (event.data.type === "twitter_auth_success") {
        console.log("[TwitterAuth] Auth success! Saving token");
        const token = event.data.access_token;
        localStorage.setItem("twitter_access_token", token);
        if (event.data.refresh_token) {
          localStorage.setItem(
            "twitter_refresh_token",
            event.data.refresh_token
          );
        }
        await initializeWithToken(token);
        console.log("[TwitterAuth] Token initialized, stopping loading");
        setLoading(false);
      } else if (event.data.type === "twitter_auth_error") {
        console.error("[TwitterAuth] Auth error:", event.data.message);
        setError(event.data.message || "授权失败");
        setLoading(false);
      }
    };

    window.addEventListener("message", handleMessage);
    console.log("[TwitterAuth] Message listener added");

    return () => {
      console.log("[TwitterAuth] Component unmounting, removing listener");
      window.removeEventListener("message", handleMessage);
    };
  }, []);

  const initializeWithToken = async (token: string) => {
    console.log("[TwitterAuth] Initializing with token");
    try {
      setLoading(true);
      await apiClient.post("/api/auth/set-token", null, {
        params: { access_token: token },
      });
      setAccessToken(token);
      setIsAuthenticated(true);
      setError(null);
      console.log("[TwitterAuth] Token initialized successfully");
    } catch (err) {
      const errorMsg = getErrorMessage(err);
      console.error("[TwitterAuth] Failed to initialize token:", err);
      setError("初始化Token失败: " + errorMsg);
      localStorage.removeItem("twitter_access_token");
      localStorage.removeItem("twitter_refresh_token");
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    console.log("[TwitterAuth] Login button clicked");
    try {
      setLoading(true);
      setError(null);

      console.log("[TwitterAuth] Fetching authorization URL...");
      const response = await apiClient.get("/api/auth/twitter/login");
      console.log("[TwitterAuth] Got authorization URL");

      const authUrl = response.data.authorization_url;

      if (!authUrl) {
        throw new Error("No authorization URL received");
      }

      // 计算窗口位置（居中显示）
      const width = 600;
      const height = 700;
      const left = window.screen.width / 2 - width / 2;
      const top = window.screen.height / 2 - height / 2;

      console.log("[TwitterAuth] Opening auth window...");
      // 在新窗口打开授权页面
      const authWindow = window.open(
        authUrl,
        "Twitter Authorization",
        `width=${width},height=${height},left=${left},top=${top}`
      );

      if (!authWindow) {
        console.error("[TwitterAuth] Failed to open auth window");
        setError("无法打开授权窗口，请检查浏览器弹窗设置");
        setLoading(false);
      } else {
        console.log("[TwitterAuth] Auth window opened successfully");
        // 保持loading状态，直到收到回调消息
      }
    } catch (err) {
      const errorMsg = getErrorMessage(err);
      console.error("[TwitterAuth] Login failed:", err);
      setError("获取授权链接失败: " + errorMsg);
      setLoading(false);
    }
  };

  const handleLogout = () => {
    console.log("[TwitterAuth] Logging out");
    localStorage.removeItem("twitter_access_token");
    localStorage.removeItem("twitter_refresh_token");
    setAccessToken(null);
    setIsAuthenticated(false);
  };

  console.log(
    "[TwitterAuth] Render - authenticated:",
    isAuthenticated,
    "loading:",
    loading
  );

  return (
    <div className="mb-6 p-6 bg-white border border-gray-200 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Twitter 账号授权</h2>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700">
          {error}
        </div>
      )}

      {!isAuthenticated ? (
        <div>
          <p className="mb-4 text-gray-600">
            ⚠️ 使用书签管理功能前，需要先授权您的Twitter账号
          </p>
          <button
            onClick={handleLogin}
            disabled={loading}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
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
                正在授权...
              </>
            ) : (
              <>
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                </svg>
                授权 Twitter 账号
              </>
            )}
          </button>
          <p className="mt-3 text-sm text-gray-500">
            点击后将在新窗口打开Twitter授权页面
          </p>
        </div>
      ) : (
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <svg
                className="w-6 h-6 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <div>
              <p className="text-green-600 font-semibold">✓ 已授权</p>
              <p className="text-sm text-gray-500">现在可以使用所有功能</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="text-red-500 hover:text-red-700 px-4 py-2 border border-red-300 rounded hover:bg-red-50"
          >
            退出授权
          </button>
        </div>
      )}
    </div>
  );
}
