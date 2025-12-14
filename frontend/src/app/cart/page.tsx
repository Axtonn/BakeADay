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
  const [deliveryType, setDeliveryType] = useState<"pickup" | "delivery">("pickup");
  const [deliveryAddress, setDeliveryAddress] = useState("");
  const [scheduledDate, setScheduledDate] = useState("");
  const [note, setNote] = useState("");
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
    if (deliveryType === "delivery" && !deliveryAddress) {
      setMsg("Please provide a delivery address.");
      return;
    }
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
        delivery_type: deliveryType,
        delivery_address: deliveryType === "delivery" ? deliveryAddress : null,
        scheduled_date: scheduledDate || null,
        note,
      }),
    });
    if (res.ok) {
      setMsg("hooray! We've received your order. See you then!");
      setCart([]);
      localStorage.removeItem(cartKey);
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
      const err = await res.json().catch(() => ({}));
      setMsg(err?.detail || "Checkout failed.");
    }
  };

  return (
    <section className="py-12 px-4 min-h-[80vh] flex flex-col items-center bg-gradient-to-br from-yellow-50 to-pink-50">
      <h2 className="text-3xl font-bold text-pink-700 mb-6">Your Cart</h2>
      {cart.length === 0 ? (
        <div className="text-pink-800 bg-white px-4 py-3 rounded-xl shadow">Your cart is empty.</div>
      ) : (
        <div className="w-full max-w-5xl grid md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-4">
            {cart.map((item) => (
              <div key={item.id} className="bg-white rounded-xl shadow p-4 flex gap-4 items-center">
                <div className="w-20 h-20 rounded-lg bg-pink-50 flex items-center justify-center overflow-hidden">
                  {item.image_url ? (
                    <img src={item.image_url} alt={item.name} className="w-full h-full object-cover" />
                  ) : (
                    <span className="text-pink-400 text-sm">No image</span>
                  )}
                </div>
                <div className="flex-1">
                  <div className="font-bold text-pink-800 text-lg">{item.name}</div>
                  <div className="text-sm text-gray-600">Quantity: {item.quantity}</div>
                  <div className="text-pink-700 font-semibold">${(item.price * item.quantity).toFixed(2)}</div>
                </div>
              </div>
            ))}
            <div className="bg-white rounded-xl shadow p-4 flex justify-between text-lg font-bold text-pink-800">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
          </div>
          <form className="bg-white shadow-lg rounded-xl p-6 space-y-4" onSubmit={handleCheckout}>
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
            <div>
              <label className="block mb-1 font-semibold text-pink-800">Pickup or Delivery</label>
              <select
                className="w-full border rounded px-3 py-2"
                value={deliveryType}
                onChange={(e) => setDeliveryType(e.target.value as "pickup" | "delivery")}
              >
                <option value="pickup">Pickup</option>
                <option value="delivery">Delivery</option>
              </select>
            </div>
            {deliveryType === "delivery" && (
              <div>
                <label className="block mb-1 font-semibold text-pink-800">Delivery address</label>
                <input
                  className="w-full border rounded px-3 py-2"
                  placeholder="Street, suburb, state, postcode"
                  value={deliveryAddress}
                  onChange={(e) => setDeliveryAddress(e.target.value)}
                  required
                />
              </div>
            )}
            <div>
              <label className="block mb-1 font-semibold text-pink-800">Preferred date</label>
              <input
                type="date"
                className="w-full border rounded px-3 py-2"
                value={scheduledDate}
                onChange={(e) => setScheduledDate(e.target.value)}
              />
            </div>
            <div>
              <label className="block mb-1 font-semibold text-pink-800">Notes</label>
              <textarea
                className="w-full border rounded px-3 py-2"
                rows={3}
                placeholder="Allergies, delivery instructions, etc."
                value={note}
                onChange={(e) => setNote(e.target.value)}
              />
            </div>
            <button
              type="submit"
              className="w-full bg-pink-500 text-white px-5 py-3 rounded-full shadow hover:bg-pink-600 transition"
            >
              Checkout
            </button>
            {msg && <div className="text-pink-700 mt-2 font-semibold text-sm">{msg}</div>}
          </form>
        </div>
      )}
    </section>
  );
}
