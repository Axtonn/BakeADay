"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";

const slides = [
  { src: "/images/cake.jpg", caption: "Custom Cakes" },
  { src: "/images/cookies.jpg", caption: "Fresh Cookies" },
  { src: "/images/bread.jpg", caption: "Daily Bakes" },
];

export default function Slideshow() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % slides.length);
    }, 4000); // auto change every 4s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative w-full h-[80vh] overflow-hidden">
      <AnimatePresence>
        <motion.div
          key={index}
          className="absolute inset-0"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 1 }}
        >
          <Image
            src={slides[index].src}
            alt={slides[index].caption}
            fill
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
            <h2 className="text-white text-4xl md:text-6xl font-bold drop-shadow-lg">
              {slides[index].caption}
            </h2>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
