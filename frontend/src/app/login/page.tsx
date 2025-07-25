"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function AdminLogin() {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    // Demo: Hardcoded admin credentials
    if (email === "admin@bakeaday.com" && pw === "letmein") {
      // Set cookie for middleware
      document.cookie = "bakeaday-auth=true; path=/";
      // Optionally set localStorage for client UI
      localStorage.setItem("bakeaday-auth", "true");
      router.push("/admin");
    } else {
      setError("Invalid email or password!");
    }
  }

  return (
    <section className="flex flex-col items-center justify-center min-h-[60vh]">
      <h2 className="text-2xl font-bold mb-6 text-pink-700">Admin Login</h2>
      <form onSubmit={handleLogin} className="bg-white p-6 rounded shadow-lg flex flex-col gap-4 w-80">
        <input
          type="email"
          className="border rounded px-3 py-2"
          placeholder="Email"
          required
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          type="password"
          className="border rounded px-3 py-2"
          placeholder="Password"
          required
          value={pw}
          onChange={e => setPw(e.target.value)}
        />
        {error && <div className="text-red-500 text-sm text-center">{error}</div>}
        <button className="bg-pink-500 text-white rounded-full py-2 hover:bg-pink-600" type="submit">
          Login
        </button>
      </form>
      <p className="mt-4 text-gray-500 text-sm">
        Hint: <b>admin@bakeaday.com</b> / <b>letmein</b>
      </p>
    </section>
  );
}
