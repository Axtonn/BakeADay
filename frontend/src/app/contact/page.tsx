import Chatbot from "../components/Chatbot";

export default function ContactPage() {
  return (
    <section className="py-12 px-4 min-h-[80vh] flex flex-col items-center bg-pink-50">
      <h2 className="text-3xl font-bold text-pink-700 mb-4">Contact & Chat</h2>
      <p className="mb-6 text-pink-900 text-lg text-center max-w-xl">
        Questions about ingredients, orders, or custom requests?  
        Chat with our AI assistant or send us a message below!
      </p>
      <div className="w-full max-w-lg">
        <Chatbot />
      </div>
      <form className="bg-white shadow-lg rounded-lg p-6 w-full max-w-lg mt-8 space-y-4">
        <div>
          <label className="block mb-1 font-semibold text-pink-800">Your Email</label>
          <input type="email" className="w-full border rounded px-3 py-2" placeholder="you@email.com" required />
        </div>
        <div>
          <label className="block mb-1 font-semibold text-pink-800">Message</label>
          <textarea className="w-full border rounded px-3 py-2" rows={4} placeholder="How can we help you?" required />
        </div>
        <button
          type="submit"
          className="bg-pink-500 text-white px-5 py-2 rounded-full shadow hover:bg-pink-600 transition"
        >
          Send Message
        </button>
      </form>
    </section>
  );
}
