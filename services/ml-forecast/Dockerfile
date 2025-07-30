# ================================
# 1. Base image
# ================================
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ================================
# 2. Install system dependencies
# ================================
# Prophet needs gcc, g++, and pystan compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ================================
# 3. Install dependencies
# ================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ================================
# 4. Copy application
# ================================
COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# ================================
# 5. Run application
# ================================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
