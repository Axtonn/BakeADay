export default function LoggedOutPage() {
  return (
    <section className="flex flex-col items-center justify-center min-h-[70vh] bg-yellow-50">
      <div className="bg-white p-8 rounded-xl shadow-lg text-center">
        <h1 className="text-3xl font-bold text-pink-700 mb-4">You have been logged out.</h1>
        <p className="text-pink-900 mb-4">Thanks for visiting A Bake A Day!</p>
        <a
          href="/"
          className="bg-pink-500 text-white px-6 py-2 rounded-full hover:bg-pink-600 transition"
        >
          Back to Home
        </a>
      </div>
    </section>
  );
}
