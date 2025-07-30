"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function OrdersPage() {
  type Order = {
    id: number;
    customer_name: string;
    customer_email?: string;
    total: number;
    created_at: string;
    items: {
      id: number;
      order_id: number;
      product_id: number;
      quantity: number;
      price: number;
    }[];
  };
  const [loading, setLoading] = useState(true);
  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState("");
  const router = useRouter();

  // Protect route
  useEffect(() => {
    fetch("/api/admin/hello", { credentials: "include" })
      .then((res) => {
        if (!res.ok) router.replace("/admin-signin");
        else setLoading(false);
      })
      .catch(() => router.replace("/admin-signin"));
  }, [router]);

  useEffect(() => {
    if (!loading) {
      fetch("/api/admin/orders/", { credentials: "include" })
        .then((res) => res.json())
        .then(data => {
          if (Array.isArray(data)) setOrders(data);
          else setOrders([]);
        })
        .catch(() => setError("Could not load orders"));
    }
  }, [loading]);

  if (loading) return <div>Loading...</div>;

  return (
    <section className="min-h-[80vh] flex flex-col items-center py-16 bg-yellow-50">
      <div className="w-full max-w-4xl bg-white rounded-2xl shadow-2xl p-10">
        <button
          className="mb-8 text-pink-600 underline"
          onClick={() => router.push("/admin")}
        >
          ← Back to Dashboard
        </button>
        <h2 className="text-3xl font-bold text-pink-700 mb-6">Orders</h2>
        {error && <div className="text-red-500">{error}</div>}
        {Array.isArray(orders) && orders.length === 0 ? (
          <div>No orders found.</div>
        ) : Array.isArray(orders) ? (
          <table className="w-full border mt-2">
            <thead>
              <tr className="bg-pink-100">
                <th className="px-4 py-2">Customer</th>
                <th className="px-4 py-2">Total</th>
                <th className="px-4 py-2">Created At</th>
                {/* Add more columns/actions here */}
              </tr>
            </thead>
            <tbody>
              {orders.map((o) => (
                <tr key={o.id} className="hover:bg-pink-50">
                  <td className="border px-4 py-2">{o.customer_name}</td>
                  <td className="border px-4 py-2">${o.total?.toFixed?.(2) ?? o.total}</td>
                  <td className="border px-4 py-2">{o.created_at}</td>
                  {/* Add View/Delete buttons here */}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="text-red-500">Unexpected response from server.</div>
        )}
      </div>
    </section>
  );
}
