"use client";
import Link from "next/dist/client/link";
import { useEffect, useState } from "react";

type Product = {
  id: number;
  name: string;
  price: number;
  description?: string;
  image_url?: string;
  in_stock: number;
};

const emptyProduct: Omit<Product, "id"> = {
  name: "",
  price: 0,
  description: "",
  image_url: "",
  in_stock: 0,
};

export default function AdminProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState<Product | null>(null);
  const [form, setForm] = useState(emptyProduct);
  const [msg, setMsg] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [, setImgPreview] = useState<string | undefined>(undefined);

  // Load products on mount
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/products/`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error("Could not load products");
        return res.json();
      })
      .then(data => {
        if (Array.isArray(data)) setProducts(data);
        else if (Array.isArray(data.products)) setProducts(data.products);
        else setProducts([]);
      })
      .catch(() => setError("Could not load products"))
      .finally(() => setLoading(false));
  }, []);

  // Handle form changes
  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  // Handle file change
  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    setImageFile(file ?? null);
    if (file) setImgPreview(URL.createObjectURL(file));
    else setImgPreview(undefined);
  }

  // Create or update product (with image upload)
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMsg("");

    let imageUrl = form.image_url;
    // If a new image file is selected, upload it first
    if (imageFile) {
      const data = new FormData();
      data.append("file", imageFile);
      const uploadRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/products/upload`, {
        method: "POST",
        credentials: "include",
        body: data,
      });
      if (uploadRes.ok) {
        const { url } = await uploadRes.json();
        imageUrl = url;
      } else {
        setMsg("Image upload failed.");
        return;
      }
    }
    const method = editing ? "PUT" : "POST";
    const url = editing
      ? `${process.env.NEXT_PUBLIC_API_URL}/admin/products/${editing.id}`
      : `${process.env.NEXT_PUBLIC_API_URL}/admin/products/`;
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        ...form,
        price: parseFloat(String(form.price)),
        in_stock: parseInt(String(form.in_stock)),
        image_url: imageUrl,
      }),
    });
    if (res.ok) {
      setMsg(editing ? "Product updated!" : "Product added!");
      setForm(emptyProduct);
      setEditing(null);
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/products/`, { credentials: "include" })
        .then((res) => res.json())
        .then(setProducts);
    } else {
      setMsg("Failed to save product.");
    }
  }

  // Edit product
  function handleEdit(p: Product) {
    setEditing(p);
    setForm({ ...p });
    setImgPreview(p.image_url ? `${p.image_url}` : undefined);
    setImageFile(null);
  }

  // Delete product
  async function handleDelete(id: number) {
    if (!confirm("Are you sure?")) return;
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/products/${id}`, {
      method: "DELETE",
      credentials: "include",
    });
    if (res.ok) {
      setProducts(products.filter((p) => p.id !== id));
    } else {
      setMsg("Failed to delete.");
    }
  }

  if (loading) return <div>Loading...</div>;

  return (
    <section className="max-w-3xl mx-auto py-10">
      <Link href="/admin" className="text-pink-600 underline">&larr; Back to Dashboard</Link>
      <h2 className="text-3xl font-bold text-pink-700 my-6">Products</h2>
      {error && <div className="text-red-500">{error}</div>}
      <form onSubmit={handleSubmit} className="bg-pink-50 rounded-xl shadow-md p-6 mb-10">
         <h3 className="font-semibold text-lg mb-3">{editing ? "Edit Product" : "Add Product"}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <div>
            <label className="block mb-1 font-lipstick text-pink-500 font-bold italic tracking-wide">Name</label>
            <input
              name="name"
              placeholder="Name"
              className="cotton-candy"
              value={form.name}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-lipstick text-pink-500 font-bold italic tracking-wide">Price</label>
            <input
              name="price"
              type="number"
              step="0.01"
              placeholder="0"
              className="cotton-candy"
              value={form.price}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-lipstick text-pink-500 font-bold italic tracking-wide">Stock</label>
            <input
              name="in_stock"
              type="number"
              placeholder="0"
              className="cotton-candy"
              value={form.in_stock}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-lipstick text-pink-500 font-bold italic tracking-wide">Image URL (optional)</label>
            <input
              name="image_url"
              placeholder="Image URL (optional)"
              className="cotton-candy"
              value={form.image_url}
              onChange={handleChange}
            />
          </div>
          <div className="md:col-span-2">
            <label className="block mb-1 font-lipstick text-pink-500 font-bold italic tracking-wide">Image File (optional)</label>
            <input
              type="file"
              accept="image/*"
              className="cotton-candy"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) setImageFile(e.target.files[0]);
              }}
            />
          </div>
          <div className="md:col-span-2">
            <label className="block mb-1 font-lipstick text-pink-500 font-bold italic tracking-wide">Description</label>
            <textarea
              name="description"
              placeholder="Description"
              className="cotton-candy"
              value={form.description}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="flex gap-2 mt-4">
          <button className="bg-pink-500 text-white px-6 py-2 rounded-lg font-bold shadow hover:bg-pink-600 transition" type="submit">
            {editing ? "Update" : "Add"}
          </button>
          {editing && (
            <button
              type="button"
              className="px-4 py-2 rounded border"
              onClick={() => {
                setEditing(null);
                setForm(emptyProduct);
              }}
            >
              Cancel
            </button>
          )}
        </div>
        {msg && <div className="mt-2 text-green-700">{msg}</div>}
      </form>

      <ul>
        {products.length === 0 ? (
          <div>No products found.</div>
        ) : (
          products.map((product) => (
            <li key={product.id} className="mb-6 border-b pb-4 flex flex-col md:flex-row items-center md:items-start gap-6">
              {product.image_url && (
                <img
                  src={product.image_url.startsWith("http") ? product.image_url : `${product.image_url}`}
                  alt={product.name}
                  className="w-24 h-24 object-contain rounded bg-white border"
                />
              )}
              <div className="flex-1">
                <div className="font-bold text-lg text-pink-700">{product.name}</div>
                <div className="text-pink-800 mb-1">${product.price.toFixed(2)}</div>
                <div className="text-gray-600 mb-1">{product.description}</div>
                <div className="text-sm text-gray-500">Stock: {product.in_stock}</div>
              </div>
              <div className="flex flex-col gap-2">
                <button
                  className="bg-pink-400 text-white rounded px-3 py-1 hover:bg-pink-600"
                  onClick={() => handleEdit(product)}
                >
                  Edit
                </button>
                <button
                  className="bg-red-400 text-white rounded px-3 py-1 hover:bg-red-600"
                  onClick={() => handleDelete(product.id)}
                >
                  Delete
                </button>
              </div>
            </li>
          ))
        )}
      </ul>
    </section>
  );
}
