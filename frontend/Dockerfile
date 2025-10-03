# ---- Base ----
FROM node:20-alpine AS base
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1

# ---- Deps layer (cacheable) ----
FROM base AS deps
COPY package.json package-lock.json* ./
RUN npm ci

# ---- Dev ----
# Code will be bind-mounted in dev; keep node_modules in a container volume.
FROM deps AS dev
ENV CHOKIDAR_USEPOLLING=true
EXPOSE 3000
# On first run, if volume is empty, install deps; then start dev server
CMD [ "sh", "-c", "[ -d node_modules ] || npm ci && npm run dev" ]

# ---- Build (prod artifact) ----
FROM base AS builder
COPY package.json package-lock.json* ./
RUN npm i
COPY . .
# Optional (recommended) for slimmer prod: set output: 'standalone' in next.config.js
# module.exports = { output: 'standalone' }
RUN npm run build

# ---- Prod ----
# If you use 'standalone', prefer this minimal runtime:
# FROM node:20-alpine AS prod
# WORKDIR /app
# ENV NODE_ENV=production
# COPY --from=builder /app/.next/standalone ./
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/.next/static ./.next/static
# EXPOSE 3000
# USER node
# CMD ["node","server.js"]

# Fallback: regular 'next start' (works without standalone)
FROM node:20-alpine AS prod
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app ./
EXPOSE 3000
# Least-privileged user (safer in prod)
USER node
CMD ["npm","run","start"]
