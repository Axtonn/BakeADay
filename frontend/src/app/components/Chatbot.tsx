"use client";
import { useState } from "react";

export default function Chatbot() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! I'm BakeADay Bot. Ask me anything about our products or orders!" }
  ]);

  function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input) return;
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
    // Here you’ll call your AI backend in the future!
    setTimeout(() => setMessages(msgs => [...msgs, { sender: "bot", text: "I'm just a demo bot for now. 😊" }]), 600);
  }

  return (
    <div className="border rounded-2xl p-4 bg-yellow-50 shadow min-h-[200px]">
      <div className="mb-3 h-36 overflow-y-auto flex flex-col gap-2">
        {messages.map((m, i) => (
          <div key={i} className={m.sender === "bot" ? "text-pink-700" : "text-pink-900 text-right"}>
            <span className="block bg-pink-100 px-3 py-1 rounded-lg inline-block max-w-xs">{m.text}</span>
          </div>
        ))}
      </div>
      <form className="flex gap-2" onSubmit={handleSend}>
        <input
          className="flex-1 border rounded px-2 py-1"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message…"
        />
        <button className="bg-pink-500 text-white px-3 py-1 rounded" type="submit">
          Send
        </button>
      </form>
    </div>
  );
}
