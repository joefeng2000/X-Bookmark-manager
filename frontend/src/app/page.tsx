// frontend/src/app/page.tsx
import MigrationPanel from "@/components/MigrationPanel";
import BookmarkList from "@/components/BookmarkList";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 text-center">X 书签管理器</h1>
        <MigrationPanel />
        <BookmarkList />
      </div>
    </main>
  );
}
