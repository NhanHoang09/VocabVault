#!/bin/bash

# Script to create gamification sample data
# This script runs the Python script to create sample data for testing

set -e

echo "🎮 Creating Gamification Sample Data..."
echo "======================================"

# Change to backend directory
cd "$(dirname "$0")/.."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if database is running
echo "🔍 Checking database connection..."
python -c "
import sys
sys.path.append('.')
from app.core.database import get_db
try:
    db = next(get_db())
    db.execute('SELECT 1')
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    sys.exit(1)
"

# Run the sample data creation script
echo "📊 Creating sample data..."
python scripts/create_gamification_sample_data.py

echo ""
echo "✅ Gamification sample data creation completed!"
echo ""
echo "📋 Sample data includes:"
echo "   - 8 badges (First Steps, Streak Master, Speed Demon, etc.)"
echo "   - 5 challenges (Weekly Study Streak, Speed Runner, etc.)"
echo "   - Game sessions for all 4 game types"
echo "   - Points transactions and user badges"
echo "   - Leaderboard entries for all categories"
echo "   - User challenges with various progress states"
echo ""
echo "🚀 You can now test the gamification API endpoints!"
