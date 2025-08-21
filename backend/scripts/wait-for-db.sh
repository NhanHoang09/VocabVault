#!/bin/bash

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."

until pg_isready -h localhost -p 5432 -U vocabulary_user -d vocabulary_vault; do
    echo "PostgreSQL is not ready yet. Waiting..."
    sleep 2
done

echo "✅ PostgreSQL is ready!"

# Optional: Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."

until redis-cli -h localhost -p 6379 ping; do
    echo "Redis is not ready yet. Waiting..."
    sleep 2
done

echo "✅ Redis is ready!"
echo "🚀 All services are ready!"
