// frontend/src/app/auth/callback/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

export default function AuthCallback() {
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<"processing" | "success" | "error">(
    "processing"
  );
  const [message, setMessage] = useState("正在处理授权回调...");

  useEffect(() => {
    const code = searchParams.get("code");
    const state = searchParams.get("state");
    const error = searchParams.get("error");

    console.log("[AuthCallback] Params:", {
      code: code?.substring(0, 20),
      state: state?.substring(0, 20),
      error,
    });

    if (error) {
      setStatus("error");
      setMessage(`授权失败: ${error}`);

      if (window.opener) {
        console.log("[AuthCallback] Sending error to opener");
        window.opener.postMessage(
          {
            type: "twitter_auth_error",
            message: error,
          },
          window.location.origin
        );
      }

      setTimeout(() => window.close(), 3000);
      return;
    }

    if (!code || !state) {
      setStatus("error");
      setMessage("缺少必要的授权参数");
      setTimeout(() => window.close(), 3000);
      return;
    }

    console.log("[AuthCallback] Calling backend callback endpoint");

    // 调用后端callback接口
    fetch(`http://localhost:8000/api/auth/callback?code=${code}&state=${state}`)
      .then(async (res) => {
        console.log("[AuthCallback] Backend response status:", res.status);

        if (!res.ok) {
          const error = await res.json();
          throw new Error(error.detail || "授权回调失败");
        }
        return res.json();
      })
      .then((data) => {
        console.log(
          "[AuthCallback] Success! Token received:",
          data.access_token?.substring(0, 20)
        );

        setStatus("success");
        setMessage("授权成功！正在关闭窗口...");

        // 通过postMessage发送token给父窗口
        if (window.opener) {
          console.log("[AuthCallback] Sending success message to opener");
          window.opener.postMessage(
            {
              type: "twitter_auth_success",
              access_token: data.access_token,
              refresh_token: data.refresh_token,
              expires_in: data.expires_in,
            },
            window.location.origin
          );

          console.log(
            "[AuthCallback] Message sent, closing window in 2 seconds"
          );
        } else {
          console.warn("[AuthCallback] No opener window found!");
        }

        // 2秒后关闭窗口
        setTimeout(() => {
          console.log("[AuthCallback] Closing window");
          window.close();
        }, 2000);
      })
      .catch((err) => {
        console.error("[AuthCallback] Callback error:", err);
        setStatus("error");
        setMessage(`授权失败: ${err.message}`);

        if (window.opener) {
          window.opener.postMessage(
            {
              type: "twitter_auth_error",
              message: err.message,
            },
            window.location.origin
          );
        }

        setTimeout(() => window.close(), 3000);
      });
  }, [searchParams]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <div className="flex flex-col items-center">
          {status === "processing" && (
            <>
              <svg
                className="animate-spin h-12 w-12 text-blue-500 mb-4"
                viewBox="0 0 24 24"
              >
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
              <p className="text-lg text-gray-700">{message}</p>
            </>
          )}

          {status === "success" && (
            <>
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <svg
                  className="w-10 h-10 text-green-600"
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
              <p className="text-lg text-green-600 font-semibold">{message}</p>
            </>
          )}

          {status === "error" && (
            <>
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
                <svg
                  className="w-10 h-10 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </div>
              <p className="text-lg text-red-600">{message}</p>
              <p className="text-sm text-gray-500 mt-2">窗口将自动关闭</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
