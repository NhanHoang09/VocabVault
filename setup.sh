#!/bin/bash

echo "🚀 Setting up My Vocabulary Vault..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. Please install it first."
    echo "   On macOS: brew install postgresql"
    echo "   On Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    echo "   On Windows: Download from https://www.postgresql.org/download/"
fi

echo "📦 Setting up Backend..."

# Backend setup
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit backend/.env with your database credentials"
fi

echo "📦 Setting up Frontend..."

# Frontend setup
cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env.local file if it doesn't exist
if [ ! -f .env.local ]; then
    echo "Creating .env.local file..."
    cp env.example .env.local
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your database credentials"
echo "2. Create PostgreSQL database: createdb vocabulary_vault"
echo "3. Run database migrations: cd backend && alembic upgrade head"
echo "4. Start backend: cd backend && python run.py"
echo "5. Start frontend: cd frontend && npm run dev"
echo ""
echo "🌐 Backend will be available at: http://localhost:8000"
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "📚 API Documentation: http://localhost:8000/docs"
