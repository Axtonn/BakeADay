"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Image from "next/image";
import { useUser } from "@clerk/nextjs";

// Shared types (put in types.ts for reuse if you like)
type Product = {
  id: number;
  name: string;
  description?: string;
  price: number;
  image_url?: string;
  in_stock: number;
};
type Review = {
  id: number;
  user_name: string;
  rating: number;
  comment?: string;
  created_at: string;
};
// For submitting a new review (only fields you send!)
type ReviewCreate = {
  user_name: string;
  rating: number;
  comment?: string;
};

const apiBase = process.env.NEXT_PUBLIC_API_URL;
const resolveImage = (url?: string) => {
  if (!url) return undefined;
  if (url.startsWith("http")) return url;
  return `${apiBase}${url}`;
};

export default function ProductDetailPage() {
  const { id } = useParams();
  const { isSignedIn, user } = useUser();
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [cartMsg, setCartMsg] = useState("");
  const [reviewMsg, setReviewMsg] = useState("");
  const [reviewImage, setReviewImage] = useState<File | null>(null);
  const [reviewImgPreview, setReviewImgPreview] = useState<string | undefined>(undefined);

  // Only the fields needed for submitting
  const [review, setReview] = useState<ReviewCreate>({
    user_name: "",
    rating: 5,
    comment: "",
  });

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/products/${id}`)
      .then((res) => res.ok ? res.json() : null)
      .then(setProduct);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/reviews/product/${id}`)
      .then((res) => res.ok ? res.json() : [])
      .then(setReviews);
  }, [id]);


  const handleAddToCart = () => {
    if (!product) return;
    if (!isSignedIn) {
      window.location.href = "/sign-in";
      return;
    }
    const userId = user?.id || "unknown";
    const cartKey = `cart_${userId}`;
    const cart: (Product & { quantity: number })[] = JSON.parse(localStorage.getItem(cartKey) || "[]");
    const idx = cart.findIndex((item) => item.id === product.id);
    if (idx > -1) {
      cart[idx].quantity += quantity;
    } else {
      cart.push({ ...product, quantity });
    }
    localStorage.setItem(cartKey, JSON.stringify(cart));
    setCartMsg("Added to cart!");
  };

  
  function handleReviewFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    setReviewImage(file ?? null);
    if (file) setReviewImgPreview(URL.createObjectURL(file));
    else setReviewImgPreview(undefined);
  }

  const handleReviewSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      let image_url = "";
      if (reviewImage) {
        const formData = new FormData();
        formData.append("file", reviewImage);
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/reviews/upload`, {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        if (res.ok && data.image_url) {
          image_url = data.image_url;
        }
      }
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/reviews/product/${id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...review,
        image_url,
      }),
    });
    if (res.ok) {
      setReviewMsg("Review submitted!");
      setReview({ user_name: "", rating: 5, comment: "" });
      // Reload reviews
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/reviews/product/${id}`)
        .then((res) => res.json())
        .then(setReviews);
    } else {
      setReviewMsg("Failed to submit review.");
    }
  };

  if (!product) return <div>Loading...</div>;

  return (
    <section className="py-10 px-4 min-h-[80vh] bg-yellow-50">
      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-8 flex flex-col md:flex-row gap-8">
        {product.image_url ? (
          <Image
            src={resolveImage(product.image_url) || ""}
            alt={product.name}
            width={80}
            height={80}
            className="object-cover"
            unoptimized
          />
        ) : (
          <div className="w-60 h-60 flex items-center justify-center bg-gray-100 text-gray-400">
            No Image
          </div>
        )}
        <div className="flex-1 flex flex-col gap-4">
          <h2 className="text-2xl font-bold text-pink-700">{product.name}</h2>
          <div className="text-lg text-pink-700">${product.price.toFixed(2)}</div>
          <div className="text-gray-600">{product.description}</div>
          <div className="flex items-center gap-2">
            <label>Quantity:</label>
            <input
              type="number"
              min="1"
              max={product.in_stock}
              value={quantity}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuantity(Number(e.target.value))}
              className="border rounded w-20 px-2 py-1"
            />
            <button
              className="bg-pink-500 text-white px-4 py-2 rounded hover:bg-pink-600 ml-2"
              onClick={handleAddToCart}
            >
              Add to Cart
            </button>
          </div>
          {cartMsg && <div className="text-green-600">{cartMsg}</div>}
          <hr className="my-4" />
          <div>
            <h3 className="font-bold mb-2 text-lg">Reviews</h3>
            {(!Array.isArray(reviews) || reviews.length === 0) ? (
              <div>No reviews yet.</div>
            ) : (
              <ul>
                {reviews.map((rev) => (
                  <li key={rev.id} className="mb-2">
                    <b>{rev.user_name}</b> ({rev.rating}/5): {rev.comment}
                  </li>
                ))}
              </ul>
            )}
            <form className="mt-4 space-y-2" onSubmit={handleReviewSubmit}>
              <div>
                <input
                  type="text"
                  placeholder="Your name"
                  className="border rounded px-2 py-1"
                  value={review.user_name}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setReview((r) => ({ ...r, user_name: e.target.value }))
                  }
                  required
                />
              </div>
              <div>
                <input
                  type="number"
                  min={1}
                  max={5}
                  className="border rounded w-16 px-2 py-1"
                  value={review.rating}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setReview((r) => ({ ...r, rating: Number(e.target.value) }))
                  }
                  required
                />{" "}
                /5 Rating
              </div>
              <div>
                <input type="file" accept="image/*" onChange={handleReviewFileChange} />
                {reviewImgPreview && (
                  <Image
                    src={reviewImgPreview}
                    alt="Review Preview"
                    width={96}
                    height={96}
                    className="w-24 h-24 mt-2 object-cover"
                    unoptimized
                  />
                )}
              </div>
              <div>
                <textarea
                  className="border rounded w-full px-2 py-1"
                  placeholder="Write a review..."
                  value={review.comment}
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
                    setReview((r) => ({ ...r, comment: e.target.value }))
                  }
                />
              </div>
              <button className="bg-pink-500 text-white px-3 py-1 rounded" type="submit">
                Submit Review
              </button>
              {reviewMsg && <div className="text-green-600">{reviewMsg}</div>}
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}
