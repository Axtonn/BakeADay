"use client";
import { useRouter } from "next/navigation";

export default function AdminNavbar() {
  const router = useRouter();
  const handleLogout = async () => {
    await fetch("/api/admin/logout", {
      method: "POST",
      credentials: "include",
    });
    router.push("/admin-signin");
  };

  return (
    <nav className="flex justify-between items-center px-8 py-4 bg-pink-100 shadow">
      <a href="/admin" className="text-2xl font-extrabold text-pink-700 flex items-center gap-2">
        <span role="img" aria-label="cupcake">🧁</span> Admin Panel
      </a>
      <button
        onClick={handleLogout}
        className="ml-6 bg-white text-pink-600 border border-pink-400 rounded-full px-5 py-2 font-semibold hover:bg-pink-600 hover:text-white transition"
      >
        Logout
      </button>
    </nav>
  );
}
