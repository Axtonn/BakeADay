# ---- Base ----
# Use current LTS Alpine to reduce known vulnerabilities
FROM node:22-alpine AS base
# Pull latest security patches for the base image
RUN apk --no-cache upgrade
# Build tooling needed for npm installs that compile native deps
RUN apk add --no-cache libc6-compat python3 make g++
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1

# ---- Deps layer (cacheable) ----
FROM base AS deps
COPY package.json package-lock.json* ./
# Use legacy peer deps to satisfy Clerk peer requirements without downgrading Next
RUN npm ci --legacy-peer-deps

# ---- Dev ----
# Code will be bind-mounted in dev; keep node_modules in a container volume.
FROM deps AS dev
ENV CHOKIDAR_USEPOLLING=true
EXPOSE 3000
# On first run, if volume is empty, install deps; then start dev server
CMD [ "sh", "-c", "[ -d ./node_modules ] || npm ci && npm run dev" ]

# ---- Build (prod artifact) ----
FROM base AS builder
COPY package.json package-lock.json* ./
# npx fix-react2shell-next is not in deps and was failing the build; remove it
RUN npm ci --legacy-peer-deps
COPY . .
# Optional (recommended) for slimmer prod: set output: 'standalone' in next.config.js
# module.exports = { output: 'standalone' }
RUN npm run build

# ---- Prod ----
# If you use 'standalone', prefer this minimal runtime:
# FROM node:22-alpine AS prod
# WORKDIR /app
# ENV NODE_ENV=production
# COPY --from=builder /app/.next/standalone ./
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/.next/static ./.next/static
# EXPOSE 3000
# USER node
# CMD ["node","server.js"]

# Fallback: regular 'next start' (works without standalone)
FROM node:22-alpine AS prod
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app ./
EXPOSE 3000
# Least-privileged user (safer in prod)
USER node
CMD ["npm","run","start"]
