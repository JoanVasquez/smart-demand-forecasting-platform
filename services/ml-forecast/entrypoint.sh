#!/bin/sh
set -e

echo "⏳ Waiting for Kafka broker..."
until nc -z kafka 9092; do
  echo "Kafka is unavailable - sleeping"
  sleep 2
done
echo "✅ Kafka broker is up."

echo "🚀 Starting FastAPI (Schema will be checked asynchronously)..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
