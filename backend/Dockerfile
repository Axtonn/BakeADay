# syntax=docker/dockerfile:1.6

# ---- Base ----
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# ---- Deps (cacheable) ----
FROM base AS deps
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# ---- Dev ----
# Code will be bind-mounted in dev; we just need deps + reload.
FROM deps AS dev
ENV WATCHFILES_FORCE_POLLING=true \
    PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", \
     "--reload-exclude", ".venv", "--reload-exclude", "venv", "--reload-exclude", "__pycache__"]

# ---- Prod ----
FROM deps AS prod
# Copy sources + Alembic
COPY . /app
ENV PYTHONPATH=/app
EXPOSE 8000
# Create unprivileged user
RUN useradd -u 10001 -m appuser
USER appuser
# Gunicorn + Uvicorn workers for prod
CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","app.main:app", \
     "-b","0.0.0.0:8000","--workers","2","--threads","4","--timeout","60"]
