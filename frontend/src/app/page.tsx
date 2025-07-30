"use client";
import Link from "next/dist/client/link";

export default function HomePage() {
  return (
    <section className="flex flex-col items-center justify-center py-16 px-4 bg-gradient-to-br from-pink-50 to-yellow-50 min-h-[80vh]">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-extrabold mb-4 text-pink-700 drop-shadow">
          Welcome to
          <br />
          <br />
          <span className="text-6xl rounded px-2">A Bake A Day!</span>
        </h1>
        <br />
        <blockquote className="italic text-2xl sm:text-3xl text-yellow-700 mb-6 font-semibold">
          “Bake A Day Brighter”
        </blockquote>
        <p className="text-xl sm:text-2xl text-pink-800 mb-8 font-medium">
          Bringing a little sweetness to your every day. <br />
          Order custom cakes, cookies, and bakes—crafted fresh, delivered fast!
        </p>
        <Link href="/order">
          <button className="bg-pink-500 text-white px-6 py-3 rounded-full text-lg shadow hover:bg-pink-600 hover:scale-105 transition">
            Order Now
          </button>
        </Link>
      </div>
      

    </section>
  );
}
