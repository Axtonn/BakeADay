"use client";

import { useState } from "react";

type BaseType = "cake" | "cheesecake";

const cakeOptions = {
  sizes: ["6-inch", "8-inch", "10-inch"],
  flavors: ["Vanilla", "Chocolate", "Matcha", "Red Velvet", "Lemon"],
  fillings: ["None", "Fresh cream", "Ganache", "Berry compote", "Custard"],
  toppings: ["Berries", "Edible flowers", "Chocolate shards", "Candied citrus", "Pistachio crumble"],
};

const cheesecakeOptions = {
  sizes: ["6-inch", "8-inch"],
  flavors: ["Classic Basque", "Matcha Basque", "Chocolate Basque", "Coffee Basque"],
  toppings: ["None", "Salted caramel", "Berry compote", "Whipped cream", "Toasted nuts"],
};

export default function OrderPage() {
  const [base, setBase] = useState<BaseType>("cake");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [size, setSize] = useState("");
  const [flavor, setFlavor] = useState("");
  const [filling, setFilling] = useState("");
  const [topping, setTopping] = useState("");
  const [message, setMessage] = useState("");
  const [servings, setServings] = useState("");
  const [date, setDate] = useState("");
  const [deliveryType, setDeliveryType] = useState<"pickup" | "delivery">("pickup");
  const [status, setStatus] = useState("");

  const sizes = base === "cake" ? cakeOptions.sizes : cheesecakeOptions.sizes;
  const flavors = base === "cake" ? cakeOptions.flavors : cheesecakeOptions.flavors;
  const fillings = base === "cake" ? cakeOptions.fillings : ["None"];
  const toppings = base === "cake" ? cakeOptions.toppings : cheesecakeOptions.toppings;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("");

    const summary = `
Base: ${base === "cake" ? "Custom Cake" : "Basque Cheesecake"}
Size: ${size}
Flavor: ${flavor}
Filling: ${filling}
Topping: ${topping}
Servings: ${servings}
Delivery: ${deliveryType}
Requested Date: ${date}
Custom Message: ${message}
Customer: ${name} (${email}${phone ? ", " + phone : ""})
    `.trim();

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, message: summary }),
    });
    if (res.ok) {
      setStatus("Order submitted! We'll confirm details by email.");
      setName("");
      setEmail("");
      setPhone("");
      setSize("");
      setFlavor("");
      setFilling("");
      setTopping("");
      setMessage("");
      setServings("");
      setDate("");
      setDeliveryType("pickup");
    } else {
      setStatus("Failed to submit order. Please try again.");
    }
  };

  return (
    <section className="py-12 px-4 min-h-[80vh] flex flex-col items-center bg-gradient-to-br from-yellow-50 to-pink-50">
      <h2 className="text-3xl font-bold text-pink-700 mb-6">Custom Order</h2>
      <div className="bg-white shadow-xl rounded-2xl p-6 w-full max-w-3xl grid gap-6">
        <div className="flex gap-4">
          <button
            className={`flex-1 px-4 py-3 rounded-xl border ${base === "cake" ? "border-pink-500 bg-pink-50" : "border-gray-200"}`}
            onClick={() => setBase("cake")}
          >
            Custom Cake
          </button>
          <button
            className={`flex-1 px-4 py-3 rounded-xl border ${base === "cheesecake" ? "border-pink-500 bg-pink-50" : "border-gray-200"}`}
            onClick={() => setBase("cheesecake")}
          >
            Basque Cheesecake
          </button>
        </div>

        <form className="grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
          <div className="md:col-span-2">
            <label className="block mb-1 font-semibold text-pink-800">Name</label>
            <input className="w-full border rounded px-3 py-2" required value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Email</label>
            <input type="email" className="w-full border rounded px-3 py-2" required value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Phone (optional)</label>
            <input className="w-full border rounded px-3 py-2" value={phone} onChange={(e) => setPhone(e.target.value)} />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Size</label>
            <select className="w-full border rounded px-3 py-2" required value={size} onChange={(e) => setSize(e.target.value)}>
              <option value="">Select size</option>
              {sizes.map((s) => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Flavor</label>
            <select className="w-full border rounded px-3 py-2" required value={flavor} onChange={(e) => setFlavor(e.target.value)}>
              <option value="">Select flavor</option>
              {flavors.map((f) => <option key={f}>{f}</option>)}
            </select>
          </div>
          {base === "cake" && (
            <div>
              <label className="block mb-1 font-semibold text-pink-800">Filling</label>
              <select className="w-full border rounded px-3 py-2" required value={filling} onChange={(e) => setFilling(e.target.value)}>
                <option value="">Select filling</option>
                {fillings.map((f) => <option key={f}>{f}</option>)}
              </select>
            </div>
          )}
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Topping</label>
            <select className="w-full border rounded px-3 py-2" required value={topping} onChange={(e) => setTopping(e.target.value)}>
              <option value="">Select topping</option>
              {toppings.map((t) => <option key={t}>{t}</option>)}
            </select>
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Servings</label>
            <input className="w-full border rounded px-3 py-2" placeholder="e.g., 8-10" value={servings} onChange={(e) => setServings(e.target.value)} />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Delivery / Pickup</label>
            <select className="w-full border rounded px-3 py-2" value={deliveryType} onChange={(e) => setDeliveryType(e.target.value as "pickup" | "delivery")}>
              <option value="pickup">Pickup</option>
              <option value="delivery">Delivery</option>
            </select>
          </div>
          <div>
            <label className="block mb-1 font-semibold text-pink-800">Requested Date</label>
            <input type="date" className="w-full border rounded px-3 py-2" value={date} onChange={(e) => setDate(e.target.value)} />
          </div>
          <div className="md:col-span-2">
            <label className="block mb-1 font-semibold text-pink-800">Custom writing / notes</label>
            <textarea className="w-full border rounded px-3 py-2" rows={3} placeholder="Add message on cake, flavors tweaks, allergies..." value={message} onChange={(e) => setMessage(e.target.value)} />
          </div>
          <div className="md:col-span-2 flex justify-end gap-3">
            <button type="submit" className="bg-pink-500 text-white px-5 py-2 rounded-full shadow hover:bg-pink-600 transition">
              Submit Custom Order
            </button>
          </div>
        </form>
        {status && <div className="text-center text-pink-700 font-semibold">{status}</div>}
      </div>
    </section>
  );
}
