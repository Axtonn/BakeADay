"use client";

import Link from "next/link";
import HeroSlideshow from "./components/Slideshow";
import { FadeInSection } from "./components/FadeInSection";
import Image from "next/image";

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
            <button className="bg-pink-500 text-white px-6 py-3 rounded-full text-lg shadow hover:bg-pink-600 transition hover:scale-110 active:animate-bounce">
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
              ingredients. Whether you are celebrating a special occasion or just
              want to treat yourself, we are here to make your day a little sweeter.
            </p>
            <section className="py-16 px-6 bg-gradient-to-br from-yellow-50 to-pink-50">
              <div className="max-w-6xl mx-auto">
                <h3 className="text-3xl font-playfair mb-8 text-pink-700 text-center">
                  Meet Our Founders
                </h3>

                {/* Founder 1: details left, image covers right half */}
                <div className="mb-12">
                  <div className="grid grid-cols-1 lg:grid-cols-2 items-center gap-6">
                    <FadeInSection direction="left">
                      <div className="text-left px-4 lg:px-0">
                        <h4 className="text-2xl font-playfair text-pink-800 mb-2">
                          Ava Thompson
                        </h4>
                        <p className="text-sm uppercase tracking-wider text-yellow-700 font-semibold mb-4">
                          Co-founder & Head Pastry Chef
                        </p>
                        <p className="text-lg text-gray-700 mb-4">
                          Ava brings a decade of artisan baking experience and a love for
                          playful flavors. Her creations mix classic technique with a
                          contemporary twist—always made from scratch.
                        </p>
                        <p className="text-lg text-gray-700">
                          When she is not in the kitchen, Ava designs seasonal menus and
                          teaches community baking classes.
                        </p>
                      </div>
                    </FadeInSection>

                    <FadeInSection direction="right">
                      <div className="relative h-64 lg:h-80">
                        <div className="absolute inset-2 left-1/2 rounded-xl overflow-hidden shadow-lg">
                          <Image
                            src="/images/founder/male.png"
                            alt="Axton Cahyadi"
                            width={640}
                            height={512}
                            className="w-full h-full object-cover"
                          />
                        </div>
                      </div>
                    </FadeInSection>
                  </div>
                </div>

                {/* Founder 2: details right, image covers left half */}
                <div>
                  <div className="grid grid-cols-1 lg:grid-cols-2 items-center gap-6">
                    <FadeInSection direction="left">
                      <div className="relative h-64 lg:h-80">
                        <div className="absolute inset-2 right-1/2 rounded-xl overflow-hidden shadow-lg">
                          <Image
                            src="/images/founder/female.png"
                            alt="Ashleen Leandra"
                            width={640}
                            height={512}
                            className="w-full h-full object-cover"
                          />
                        </div>
                      </div>
                    </FadeInSection>

                    <FadeInSection direction="right">
                      <div className="text-left px-4 lg:px-0">
                        <h4 className="text-2xl font-playfair text-pink-800 mb-2">
                          Marco Rivera
                        </h4>
                        <p className="text-sm uppercase tracking-wider text-yellow-700 font-semibold mb-4">
                          Co-founder & Operations
                        </p>
                        <p className="text-lg text-gray-700 mb-4">
                          Marco manages day-to-day operations and ensures every order
                          arrives fresh. His focus on quality control and logistics keeps
                          the bakery running smoothly.
                        </p>
                        <p className="text-lg text-gray-700">
                          Outside the bakery, Marco is an avid urban gardener and recipe
                          collaborator with Ava.
                        </p>
                      </div>
                    </FadeInSection>
                  </div>
                </div>
              </div>
            </section>
          </FadeInSection>

          <FadeInSection direction="up">
            <Image
              src="/images/items/slideshow/bottom.jpg"
              alt="bake"
              width={1200}
              height={800}
              className="rounded-xl shadow-lg"
            />
          </FadeInSection>
        </div>
      </section>
    </>
  );
}
