"use client";

import { useEffect } from "react";
import { useSearchParams } from "next/navigation";

export default function AuthCallback() {
  const searchParams = useSearchParams();

  useEffect(() => {
    const code = searchParams.get("code");
    const state = searchParams.get("state");

    if (code && state) {
      // 调用后端callback接口
      fetch(
        `http://localhost:8000/api/auth/callback?code=${code}&state=${state}`
      )
        .then((res) => res.json())
        .then((data) => {
          // 通过postMessage发送token给父窗口
          if (window.opener) {
            window.opener.postMessage(
              {
                type: "twitter_auth_success",
                access_token: data.access_token,
                refresh_token: data.refresh_token,
              },
              "*"
            );
          }
        })
        .catch((err) => {
          console.error("Callback error:", err);
        });
    }
  }, [searchParams]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <p className="text-lg">正在处理授权回调...</p>
    </div>
  );
}
