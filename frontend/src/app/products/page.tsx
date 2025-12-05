"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";

type Product = {
  id: number;
  name: string;
  description?: string;
  price: number;
  image_url?: string;
  in_stock: number;
};

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const router = useRouter();

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/products`)
      .then((res) => res.json())
      .then(setProducts);
  }, []);

  return (
    <section className="py-12 px-4 bg-yellow-50 min-h-[80vh]">
      <h2 className="text-3xl font-bold text-pink-700 mb-6 text-center">Our Menu</h2>
      <div className="grid gap-8 md:grid-cols-3 sm:grid-cols-2 grid-cols-1 max-w-5xl mx-auto">
        {products.map((item) => (
          <div key={item.id} className="bg-white rounded-lg shadow-lg p-6 flex flex-col items-center">
            {item.image_url && <Image src={item.image_url} alt={item.name} className="h-32 mb-4" />}
            <div className="font-bold text-lg">{item.name}</div>
            <div className="mb-2 text-pink-700">${item.price.toFixed(2)}</div>
            <div className="text-sm mb-3">{item.description}</div>
            <button
              className="bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600"
              onClick={() => router.push(`/products/${item.id}`)}
            >
              View Details
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}
