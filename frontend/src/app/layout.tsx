// src/app/layout.tsx
"use client";
import { ClerkProvider } from "@clerk/nextjs";
import { usePathname } from "next/navigation";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  // If current path starts with /admin, hide the main Navbar and Footer
  const isAdmin = pathname.startsWith("/admin");

  return (
    <html lang="en">
      <ClerkProvider>
        <body className="min-h-screen flex flex-col">
          {!isAdmin && <Navbar />}
          <main className="flex-1">{children}</main>
          {!isAdmin && <Footer />}
        </body>
      </ClerkProvider>
    </html>
  );
}