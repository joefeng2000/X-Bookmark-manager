// frontend/src/components/BookmarkList.tsx
"use client";

import { useState, useEffect } from "react";
import apiClient from "@/lib/api";
import Image from "next/image";

interface Bookmark {
  tweet_id: string;
  text: string;
  author_name: string;
  author_handle: string;
  author_avatar_url: string;
  created_at: string;
  bookmarked_at: string;
  original_url: string;
  media_urls: string[];
  local_tags: string[];
  local_notes: string;
}

export default function BookmarkList() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async (searchTerm = "") => {
    try {
      setLoading(true);
      const params = searchTerm ? { search: searchTerm } : {};
      const response = await apiClient.get("/api/bookmarks", { params });
      setBookmarks(response.data.bookmarks);
    } catch (error) {
      console.error("Failed to fetch bookmarks:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchBookmarks(search);
  };

  const deleteBookmark = async (tweetId: string) => {
    if (!confirm("确定要删除此书签吗?")) return;

    try {
      await apiClient.delete(`/api/bookmarks/${tweetId}`);
      setBookmarks(bookmarks.filter((b) => b.tweet_id !== tweetId));
    } catch (error) {
      console.error("Failed to delete bookmark:", error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">加载中...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <form onSubmit={handleSearch} className="mb-6">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="搜索书签内容或作者..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg"
        />
      </form>

      <div className="space-y-4">
        {bookmarks.map((bookmark) => (
          <div
            key={bookmark.tweet_id}
            className="border rounded-lg p-4 hover:shadow-md transition"
          >
            <div className="flex items-start gap-3">
              <Image
                src={bookmark.author_avatar_url}
                alt={bookmark.author_name}
                className="w-12 h-12 rounded-full"
              />
              <div className="flex-1">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold">{bookmark.author_name}</h3>
                    <p className="text-gray-500 text-sm">
                      @{bookmark.author_handle}
                    </p>
                  </div>
                  <button
                    onClick={() => deleteBookmark(bookmark.tweet_id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    删除
                  </button>
                </div>
                <p className="mt-2 text-gray-800">{bookmark.text}</p>
                {bookmark.media_urls.length > 0 && (
                  <div className="mt-2 flex gap-2">
                    {bookmark.media_urls.map((url, idx) => (
                      <Image
                        key={idx}
                        src={url}
                        alt=""
                        className="w-24 h-24 object-cover rounded"
                      />
                    ))}
                  </div>
                )}
                <div className="mt-3 flex gap-2">
                  <a
                    href={bookmark.original_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline text-sm"
                  >
                    查看原推文
                  </a>
                  <span className="text-gray-400 text-sm">
                    • {new Date(bookmark.bookmarked_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
