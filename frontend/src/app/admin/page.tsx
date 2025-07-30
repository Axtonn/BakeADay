"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import AdminNavbar from "../components/AdminNavbar";

export default function AdminDashboard() {
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check admin session
  useEffect(() => {
    fetch("${process.env.NEXT_PUBLIC_API_URL}/admin/hello", { credentials: "include" })
      .then((res) => {
        if (!res.ok) router.replace("/admin-signin");
        else setLoading(false);
      })
      .catch(() => router.replace("/admin-signin"));
  }, [router]);

  if (loading) return <div>Loading...</div>;

  return (
    <>
      <AdminNavbar />
      <section className="min-h-[80vh] flex flex-col items-center py-16 bg-yellow-50">
        <div className="w-full max-w-5xl bg-white rounded-2xl shadow-2xl p-10">
          <div className="border-b pb-6 mb-10">
            <h2 className="text-4xl font-extrabold text-pink-700">Admin Dashboard</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-pink-50 rounded-2xl p-8 min-h-[320px] shadow-lg flex flex-col items-center transition-transform hover:scale-105 duration-200">
              <span className="text-7xl mb-4">🧁</span>
              <div className="font-bold text-xl mb-2 text-pink-700">Products</div>
              <div className="text-pink-700 mb-6 text-center">View &amp; Edit Menu</div>
              <button
                className="bg-pink-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-pink-600 transition"
                onClick={() => router.push("/admin/products")}
              >
                Manage
              </button>
            </div>
            <div className="bg-pink-50 rounded-2xl p-8 min-h-[320px] shadow-lg flex flex-col items-center transition-transform hover:scale-105 duration-200">
              <span className="text-7xl mb-4">📦</span>
              <div className="font-bold text-xl mb-2 text-pink-700">Orders</div>
              <div className="text-pink-700 mb-6 text-center">See Current &amp; Past Orders</div>
              <button
                className="bg-pink-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-pink-600 transition"
                onClick={() => router.push("/admin/orders")}
              >
                Manage
              </button>
            </div>
            <div className="bg-pink-50 rounded-2xl p-8 min-h-[320px] shadow-lg flex flex-col items-center transition-transform hover:scale-105 duration-200">
              <span className="text-7xl mb-4">📈</span>
              <div className="font-bold text-xl mb-2 text-pink-700">Analytics</div>
              <div className="text-pink-700 mb-6 text-center">Sales &amp; Site Traffic</div>
              <button
                className="bg-pink-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-pink-600 transition"
                onClick={() => router.push("/admin/analytics")}
              >
                View
              </button>
            </div>
          </div>
          <div className="mt-10 text-right text-sm text-gray-400">
            Signed in as <b>admin</b>
          </div>
        </div>
      </section>
    </>
  );
}
