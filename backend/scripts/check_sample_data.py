#!/usr/bin/env python3
"""
Simple script to check sample data in database
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.core.database import SessionLocal

def check_sample_data():
    """Check sample data in database"""
    print("🔍 Checking sample data in database...")
    
    db = SessionLocal()
    try:
        # Check users
        result = db.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.fetchone()[0]
        print(f"👥 Users: {user_count}")
        
        # Check flashcard sets
        result = db.execute(text("SELECT COUNT(*) FROM flashcard_sets"))
        set_count = result.fetchone()[0]
        print(f"📚 Flashcard Sets: {set_count}")
        
        # Check flashcards
        result = db.execute(text("SELECT COUNT(*) FROM flashcards"))
        card_count = result.fetchone()[0]
        print(f"🃏 Flashcards: {card_count}")
        
        # Show some sample users
        print("\n📋 Sample Users:")
        result = db.execute(text("SELECT email, username, full_name FROM users LIMIT 5"))
        for row in result.fetchall():
            print(f"  - {row[0]} ({row[1]}) - {row[2]}")
        
        # Show some sample flashcard sets
        print("\n📚 Sample Flashcard Sets:")
        result = db.execute(text("SELECT title, category, total_cards FROM flashcard_sets LIMIT 5"))
        for row in result.fetchall():
            print(f"  - {row[0]} ({row[1]}) - {row[2]} cards")
        
        print("\n✅ Sample data check completed!")
        
    except Exception as e:
        print(f"❌ Error checking data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_sample_data()
