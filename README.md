﻿### 🥐 **BakeADay** — “Bake a Day Brighter”
**One-liner**:  
An AI-powered, cloud-native baking website for a solo startup baker to showcase products, interact with customers, accept orders, and manage deliveries with intelligent automation.

---

### ✅ **Real-World Use Case**
As a solo baker launching a startup, you need a professional platform to display your creations, engage customers with intelligent assistance, accept payments, and manage deliveries—all without relying on third-party platforms like Etsy or UberEats.

---

### 🛠️ **Full Tech Stack**
| Layer              | Tools/Tech                                                                 |
|-------------------|------------------------------------------------------------------------------|
| **Frontend**       | Next.js + TailwindCSS + ShadCN UI                                          |
| **Backend**        | FastAPI + PostgreSQL + OpenAI API + NGINX                                           |
| **Auth**           | Clerk / Auth0 (with Google sign-in)                                        |
| **AI Chatbot**     | OpenAI GPT-4 (via free wrapper or API key)                                 |
| **Deployment**     | Docker + Docker Compose + Kubernetes (for future scaling)                  |
| **CI/CD**          | GitHub Actions + Render / Railway / Fly.io                                 |
| **Cloud Hosting**  | Render for MVP, scale to AWS (can start with Render for MVP)                                 |
| **Storage**        | AWS S3 (product photos, menu images), Supabase (optional backend + auth)  |
| **Payments**       | Stripe API (credit card, Apple Pay, etc.)                                  |
| **Delivery Radius**| Google Maps Distance Matrix API                                            |

---

### 🔍 **Advanced Features**
- **AI Chatbot**: Answers baking product questions, order tracking, ingredient substitutions.
- **Payment System**: Stripe checkout, invoicing, email receipts, order logs.
- **Delivery Checker**: Uses Google Maps API to check if an address is within your delivery radius.
- **Product Dashboard**: Admin-only backend for managing your offerings, photos, and pricing.
- **Real-Time Chat**: Customer support chat with fallback to email.
- **Order Timeline**: Tracks order from "Received" → "Baking" → "Out for Delivery" → "Delivered".

---

### 💼 **Resume Pitch**
> Built and deployed a full-stack, production-ready eCommerce platform for a baking startup with AI customer support, Google Maps-based delivery verification, and Stripe payment integration. Architected using FastAPI, Next.js, Typescript, PostgreSQL, Docker, and OpenAI APIs with a focus on scalability and automation.
