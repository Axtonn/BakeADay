"use client";
import { useState } from "react";
import Chatbot from "../components/Chatbot";

export default function ContactPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("");

    const res = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, message }),
    });

    const result = await res.json();
    if (result.ok) {
      setStatus("Message sent successfully!");
      setEmail("");
      setMessage("");
    } else {
      setStatus(result.error || "Failed to send message.");
    }
  }

  return (
    <>
      <section className="py-12 px-4 min-h-[80vh] flex flex-col items-center bg-pink-50">
        <h2 className="text-3xl font-bold text-pink-700 mb-4">Contact & Chat</h2>
        <p className="mb-6 text-pink-900 text-lg text-center max-w-xl">
          Questions about ingredients, orders, or custom requests?  
          Chat with our AI assistant or send us a message below!
        </p>
        <div className="w-full max-w-lg">
          <Chatbot />
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-white shadow-lg rounded-lg p-6 w-full max-w-lg mt-8 space-y-4"
        >
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Your Email</label>
            <input
              type="email"
              className="w-full border rounded px-3 py-2"
              placeholder="you@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Message</label>
            <textarea
              className="w-full border rounded px-3 py-2"
              rows={4}
              placeholder="How can we help you?"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
            />
          </div>
          {status && <p className="text-sm text-center text-pink-700">{status}</p>}
          <button
            type="submit"
            className="bg-pink-500 text-white px-5 py-2 rounded-full shadow hover:bg-pink-600 transition"
          >
            Send Message
          </button>
        </form>
      </section>

      {/* ✅ Footer */}
      <footer className="bg-pink-100 text-pink-700 py-4 text-center border-t border-pink-200">
        <p className="font-semibold mb-1">Connect with us:</p>
        <div className="flex justify-center gap-6 text-sm">
          <a
            href="https://wa.me/61406823507"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline"
          >
            A Bake A Day Whatsapp
          </a>
          <a
            href="https://www.instagram.com/a.bakeaday?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline"
          >
            A Bake A Day Instagram
          </a>
        </div>
      </footer>
    </>
  );
}
