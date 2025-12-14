"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useUser } from "@clerk/nextjs";

type Product = {
  id: number;
  name: string;
  description?: string;
  price: number;
  image_url?: string;
  in_stock: number;
};


export default function CartPage() {
  type CartItem = Product & { quantity: number };
  const [cart, setCart] = useState<CartItem[]>([]);
  const [msg, setMsg] = useState("");
  const [customer, setCustomer] = useState({ name: "", email: "" });
  const router = useRouter();
  const { isSignedIn, user } = useUser();

  const cartKey = user?.id ? `cart_${user.id}` : "cart_guest";

  useEffect(() => {
    if (!isSignedIn) {
      router.replace("/sign-in?redirect_url=/cart");
      return;
    }
    setCart(JSON.parse(localStorage.getItem(cartKey) || "[]"));
  }, [cartKey, isSignedIn, router]);

  const total = cart.reduce((t, p) => t + p.price * p.quantity, 0);

  const handleCheckout = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!customer.name || !customer.email || cart.length === 0) return;
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        customer_name: customer.name,
        customer_email: customer.email,
        items: cart.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price,
        })),
        total,
      }),
    });
    if (res.ok) {
      setMsg("hooray! We've received your order. See you then!");
      setCart([]);
      localStorage.removeItem(cartKey);
      // trigger a lightweight confetti animation
      const confetti = document.createElement("div");
      confetti.className = "confetti-container";
      confetti.innerHTML = `
        <div class="confetti left">🎉</div>
        <div class="confetti right">🎉</div>
      `;
      document.body.appendChild(confetti);
      setTimeout(() => {
        confetti.remove();
        router.push("/");
      }, 1800);
    } else {
      setMsg("Checkout failed.");
    }
  };

  return (
    <section className="py-12 px-4 min-h-[80vh] flex flex-col items-center bg-yellow-50">
      <h2 className="text-3xl font-bold text-pink-700 mb-6">Cart & Checkout</h2>
      {cart.length === 0 ? (
        <div>Your cart is empty.</div>
      ) : (
        <form
          className="bg-white shadow-lg rounded-lg p-6 w-full max-w-md space-y-4"
          onSubmit={handleCheckout}
        >
          <div>
            <b>Items:</b>
            <ul className="mb-2">
              {cart.map((item) => (
                <li key={item.id}>
                  {item.name} x {item.quantity} = ${item.price * item.quantity}
                </li>
              ))}
            </ul>
            <div className="font-bold">Total: ${total.toFixed(2)}</div>
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Name</label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              placeholder="Your name"
              required
              value={customer.name}
              onChange={(e) => setCustomer((c) => ({ ...c, name: e.target.value }))}
            />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Email</label>
            <input
              type="email"
              className="w-full border rounded px-3 py-2"
              placeholder="you@email.com"
              required
              value={customer.email}
              onChange={(e) => setCustomer((c) => ({ ...c, email: e.target.value }))}
            />
          </div>
          <button
            type="submit"
            className="bg-pink-500 text-white px-5 py-2 rounded-full shadow hover:bg-pink-600 transition"
          >
            Checkout
          </button>
          {msg && <div className="text-green-600 mt-2">{msg}</div>}
        </form>
      )}
    </section>
  );
}
