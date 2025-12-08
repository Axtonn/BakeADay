"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function AnalyticsPage() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<{ total_orders?: number; total_sales?: number } | null>(null);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    // Check admin session
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/hello`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) router.replace("/admin-signin");
        else setLoading(false);
      })
      .catch(() => router.replace("/admin-signin"));
  }, [router]);

  useEffect(() => {
    if (!loading) {
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/analytics/`, { credentials: "include" })
        .then((res) => {
          if (!res.ok) throw new Error("Could not load analytics");
          return res.json();
        })
        .then(setStats)
        .catch(() => setError("Could not load analytics."));
    }
  }, [loading]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-600">{error}</div>;
  if (!stats) return <div>Loading analytics...</div>;

  return (
    <section className="min-h-[80vh] flex flex-col items-center py-16 bg-yellow-50">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-2xl p-10">
        <button
          className="mb-8 text-pink-600 underline"
          onClick={() => router.push("/admin")}
        >
          ← Back to Dashboard
        </button>
        <h2 className="text-3xl font-bold text-pink-700 mb-8">Analytics</h2>
        <div className="grid grid-cols-2 gap-8 mb-8">
          <div className="bg-pink-50 rounded-xl p-8 flex flex-col items-center shadow">
            <span className="text-4xl mb-2">📦</span>
            <div className="text-gray-500">Total Orders</div>
            <div className="text-2xl font-bold text-pink-700">
              {typeof stats.total_orders === "number"
                ? stats.total_orders.toLocaleString()
                : "N/A"}
            </div>
          </div>
          <div className="bg-pink-50 rounded-xl p-8 flex flex-col items-center shadow">
            <span className="text-4xl mb-2">💵</span>
            <div className="text-gray-500">Total Sales</div>
            <div className="text-2xl font-bold text-pink-700">
              {typeof stats.total_sales === "number"
                ? stats.total_sales.toLocaleString("en-AU", { style: "currency", currency: "AUD" })
                : "N/A"}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
