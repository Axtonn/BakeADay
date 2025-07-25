export default function OrderPage() {
  return (
    <section className="py-12 px-4 min-h-[80vh] flex flex-col items-center bg-gradient-to-br from-yellow-50 to-pink-50">
      <h2 className="text-3xl font-bold text-pink-700 mb-6">Place Your Order</h2>
      <form className="bg-white shadow-lg rounded-lg p-6 w-full max-w-md space-y-4">
        <div>
          <label className="block mb-1 font-semibold text-pink-800">Name</label>
          <input type="text" className="w-full border rounded px-3 py-2" placeholder="Your name" required />
        </div>
        <div>
          <label className="block mb-1 font-semibold text-pink-800">Contact Email</label>
          <input type="email" className="w-full border rounded px-3 py-2" placeholder="you@email.com" required />
        </div>
        <div>
          <label className="block mb-1 font-semibold text-pink-800">Order Details</label>
          <textarea className="w-full border rounded px-3 py-2" placeholder="What would you like to order?" rows={4} required />
        </div>
        <button
          type="submit"
          className="bg-pink-500 text-white px-5 py-2 rounded-full shadow hover:bg-pink-600 transition"
        >
          Submit Order
        </button>
      </form>
      <p className="mt-6 text-sm text-gray-700 text-center">
        After submitting, you’ll receive a confirmation email with payment and delivery details.
      </p>
    </section>
  );
}
