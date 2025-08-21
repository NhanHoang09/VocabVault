#!/bin/bash

echo "🐳 Setting up Docker environment for My Vocabulary Vault Backend..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    echo "   Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed."
    echo "   Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Create .env file from env.docker if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from env.docker..."
    cp env.docker .env
    echo "✅ .env file created successfully!"
else
    echo "⚠️  .env file already exists. Skipping creation."
fi

# Start Docker services
echo "🚀 Starting Docker services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker-compose -f docker-compose.dev.yml exec -T postgres pg_isready -U vocabulary_user -d vocabulary_vault; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done

echo "✅ PostgreSQL is ready!"

# Run database migrations
echo "🗄️  Running database migrations..."
cd backend
alembic upgrade head

echo "✅ Docker setup complete!"
echo ""
echo "📋 Services running:"
echo "   🐘 PostgreSQL: localhost:5432"
echo "   🔴 Redis: localhost:6379"
echo "   🗄️  PgAdmin: http://localhost:5050"
echo "   📚 Backend API: http://localhost:8000"
echo ""
echo "🔑 PgAdmin credentials:"
echo "   Email: admin@vocabularyvault.com"
echo "   Password: admin123"
echo ""
echo "🗄️  Database credentials:"
echo "   Database: vocabulary_vault"
echo "   Username: vocabulary_user"
echo "   Password: vocabulary_password"
echo ""
echo "🛑 To stop services: docker-compose -f docker-compose.dev.yml down"
echo "🔄 To restart services: docker-compose -f docker-compose.dev.yml restart"
