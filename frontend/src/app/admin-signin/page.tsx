"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AdminSignIn() {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("${process.env.NEXT_PUBLIC_API_URL}/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password: pw }),
        credentials: "include", // This sends/receives cookies!
      });

      if (res.ok) {
        // Optionally: check response, redirect to admin dashboard
        router.push("/admin");
      } else {
        const data = await res.json();
        setError(data?.error || "Invalid password");
      }
    } catch (err) {
      setError("Network/server error.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-yellow-50">
      <h2 className="text-3xl font-bold mb-8 text-pink-700">Admin Portal Sign In</h2>
      <form className="bg-white rounded shadow-xl p-8 flex flex-col gap-4 w-96" onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Admin Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="border px-4 py-2 rounded"
          required
        />
        <input
          type="password"
          placeholder="Admin Password"
          value={pw}
          onChange={e => setPw(e.target.value)}
          className="border px-4 py-2 rounded"
          required
        />
        {error && <div className="text-red-500 text-center">{error}</div>}
        <button
          className="bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600"
          type="submit"
          disabled={loading}
        >
          {loading ? "Signing In..." : "Sign In"}
        </button>
        <button
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded w-full"
          onClick={() => router.push("/")}
          style={{ marginTop: "8px" }}
        >
          Back to Home
        </button>
      </form>
      
      <p className="mt-6 text-sm text-gray-400">Admins only.</p>
    </div>
  );
}
