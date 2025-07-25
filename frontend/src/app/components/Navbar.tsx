"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { UserButton, useUser, SignInButton } from "@clerk/nextjs";

type CartItem = {
  id: number;
  name: string;
  price: number;
  quantity: number;
};

export default function Navbar() {
  const [cartCount, setCartCount] = useState(0);
  const { isLoaded, isSignedIn } = useUser();
  const router = useRouter();

  // Update cart count when cart changes (localStorage)
  useEffect(() => {
    const updateCartCount = () => {
      const cart: CartItem[] = JSON.parse(localStorage.getItem("cart") || "[]");
      setCartCount(cart.reduce((acc, item) => acc + item.quantity, 0));
    };
    updateCartCount();
    window.addEventListener("storage", updateCartCount);
    return () => window.removeEventListener("storage", updateCartCount);
  }, []);

  return (
    <nav className="flex justify-between items-center px-6 py-3 bg-pink-100 shadow">
      <a href="/" className="text-3xl font-extrabold text-pink-700 flex items-center gap-2">
        <span role="img" aria-label="cupcake">🧁</span> A Bake A Day
      </a>
      <div className="flex items-center gap-6">
        <a href="/products" className="font-semibold text-pink-700 hover:underline">Menu</a>
        <a href="/order" className="font-semibold text-pink-700 hover:underline">Order</a>
        <a href="/cart" className="relative font-semibold text-pink-700 hover:underline flex items-center">
          <span>Cart</span>
          {cartCount > 0 && (
            <span className="ml-1 bg-pink-500 text-white rounded-full text-xs px-2 py-0.5 font-bold">
              {cartCount}
            </span>
          )}
        </a>
        <a href="/contact" className="font-semibold text-pink-700 hover:underline">Contact</a>
        <a href="/admin" className="font-bold text-pink-800 underline">Admin</a>
        {isLoaded && (
          !isSignedIn ? (
            <SignInButton mode="modal">
              <button className="ml-2 bg-white text-pink-600 border border-pink-400 rounded-full px-4 py-1 font-semibold hover:bg-pink-600 hover:text-white transition">
                Sign in
              </button>
            </SignInButton>
          ) : (
            <UserButton afterSignOutUrl="/" />
          )
        )}
      </div>
    </nav>
  );
}
