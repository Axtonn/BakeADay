# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN npm install @vercel/analytics


# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .
COPY alembic ./alembic
COPY alembic.ini ./

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
