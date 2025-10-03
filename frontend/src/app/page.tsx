"use client";

import Link from "next/link";
import HeroSlideshow from "./components/Slideshow";
import { FadeInSection } from "./components/FadeInSection";

export default function HomePage() {
  return (
    <>
      {/* Slideshow */}
      <HeroSlideshow />

      {/* Welcome Section */}
      <section className="flex flex-col items-center justify-center py-16 px-4 bg-gradient-to-br from-pink-50 to-yellow-50">
        <div className="text-center max-w-2xl">
          <h1 className="text-5xl font-extrabold mb-4 text-pink-700 drop-shadow">
            Welcome to
            <br />
            <span className="text-6xl px-2">A Bake A Day!</span>
          </h1>

          <blockquote className="italic text-2xl text-yellow-700 mb-6 font-semibold">
            “Bake Day Brighter”
          </blockquote>

          <p className="text-xl text-pink-800 mb-8 font-medium">
            Bringing a little sweetness to your every day.
            <br />
            Order custom cakes, cookies, and bakes—crafted fresh, delivered fast!
          </p>

          <Link href="/order">
            <button className="bg-pink-500 text-white px-6 py-3 rounded-full text-lg shadow hover:bg-pink-600 transition">
              Order Now
            </button>
          </Link>
        </div>
      </section>

      {/* Story Section with fade-in */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-4xl mx-auto">
          <FadeInSection direction="left">
            <h2 className="text-4xl font-playfair mb-6">Our Story</h2>
          </FadeInSection>

          <FadeInSection direction="right">
            <p className="text-lg text-gray-700 mb-8">
              BakeADay was born to bring sweetness and joy into every home. We
              craft our cakes, cookies, and bakes with love and only the finest
              ingredients.
            </p>
          </FadeInSection>

          <FadeInSection direction="up">
            <img
              src="/images/lamington.jpg"
              alt="Lamington"
              className="rounded-xl shadow-lg"
            />
          </FadeInSection>
        </div>
      </section>
    </>
  );
}
