// frontend/src/app/page.tsx
import TwitterAuth from "@/components/TwitterAuth";
import MigrationPanel from "@/components/MigrationPanel";
import BookmarkList from "@/components/BookmarkList";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 text-center">X 书签管理器</h1>

        {/* 授权组件 - 应该显示在最上面 */}
        <TwitterAuth />

        {/* 迁移面板 */}
        <MigrationPanel />

        {/* 书签列表 */}
        <BookmarkList />
      </div>
    </main>
  );
}
