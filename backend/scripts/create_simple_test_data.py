#!/usr/bin/env python3
"""
Simple script to create test data for My Vocabulary Vault
Creates sample users, flashcard sets, and flashcards for testing
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.security import SecurityManager
import app.models_registry  # Import all models to ensure relationships are loaded
from app.modules.auth.models import User
from app.modules.flashcards.models import FlashcardSet, Flashcard
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_users(db: Session):
    """Create test users directly"""
    logger.info("Creating test users...")
    
    # Test user 1: John Doe
    john = User(
        email="john.doe@example.com",
        username="johndoe",
        full_name="John Doe",
        hashed_password=SecurityManager.get_password_hash("password123"),
        is_active=True,
        is_superuser=False
    )
    
    # Test user 2: Jane Smith
    jane = User(
        email="jane.smith@example.com", 
        username="janesmith",
        full_name="Jane Smith",
        hashed_password=SecurityManager.get_password_hash("password123"),
        is_active=True,
        is_superuser=False
    )
    
    # Test user 3: Admin user
    admin = User(
        email="admin@vocabularyvault.com",
        username="admin",
        full_name="System Administrator",
        hashed_password=SecurityManager.get_password_hash("admin123"),
        is_active=True,
        is_superuser=True
    )
    
    users = []
    for user in [john, jane, admin]:
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user.email).first()
            if existing_user:
                logger.info(f"User {user.email} already exists, skipping...")
                users.append(existing_user)
                continue
            
            # Create new user
            db.add(user)
            db.commit()
            db.refresh(user)
            users.append(user)
            logger.info(f"Created user: {user.email}")
            
        except Exception as e:
            logger.error(f"Error creating user {user.email}: {e}")
            db.rollback()
    
    return users

def create_flashcard_sets(db: Session, users: list):
    """Create sample flashcard sets"""
    logger.info("Creating flashcard sets...")
    
    # Sample flashcard sets data
    sets_data = [
        {
            "title": "Basic English Vocabulary",
            "description": "Essential English words for beginners",
            "category": "English",
            "tags": ["beginner", "vocabulary", "english"],
            "is_public": True,
            "is_featured": True,
            "user_id": users[0].id  # John Doe
        },
        {
            "title": "Programming Terms",
            "description": "Common programming terminology and concepts",
            "category": "Programming",
            "tags": ["programming", "tech", "computer-science"],
            "is_public": True,
            "is_featured": False,
            "user_id": users[0].id  # John Doe
        },
        {
            "title": "Spanish Basics",
            "description": "Basic Spanish vocabulary for travelers",
            "category": "Spanish",
            "tags": ["spanish", "travel", "beginner"],
            "is_public": True,
            "is_featured": False,
            "user_id": users[1].id  # Jane Smith
        },
        {
            "title": "Math Formulas",
            "description": "Important mathematical formulas and equations",
            "category": "Mathematics",
            "tags": ["math", "formulas", "education"],
            "is_public": False,
            "is_featured": False,
            "user_id": users[1].id  # Jane Smith
        },
        {
            "title": "Science Terms",
            "description": "Scientific terminology and definitions",
            "category": "Science",
            "tags": ["science", "biology", "chemistry", "physics"],
            "is_public": True,
            "is_featured": True,
            "user_id": users[2].id  # Admin
        }
    ]
    
    flashcard_sets = []
    for set_data in sets_data:
        try:
            flashcard_set = FlashcardSet(
                user_id=set_data["user_id"],
                title=set_data["title"],
                description=set_data["description"],
                category=set_data["category"],
                tags=set_data["tags"],
                is_public=set_data["is_public"],
                is_featured=set_data["is_featured"]
            )
            db.add(flashcard_set)
            db.commit()
            db.refresh(flashcard_set)
            flashcard_sets.append(flashcard_set)
            logger.info(f"Created flashcard set: {flashcard_set.title}")
            
        except Exception as e:
            logger.error(f"Error creating flashcard set {set_data['title']}: {e}")
            db.rollback()
    
    return flashcard_sets

def create_flashcards(db: Session, flashcard_sets: list):
    """Create sample flashcards for each set"""
    logger.info("Creating flashcards...")
    
    # Sample flashcards data
    flashcards_data = {
        "Basic English Vocabulary": [
            {"front": "Hello", "back": "Xin chào", "difficulty": "easy"},
            {"front": "Goodbye", "back": "Tạm biệt", "difficulty": "easy"},
            {"front": "Thank you", "back": "Cảm ơn", "difficulty": "easy"},
            {"front": "Please", "back": "Làm ơn", "difficulty": "easy"},
            {"front": "Sorry", "back": "Xin lỗi", "difficulty": "easy"},
            {"front": "Yes", "back": "Có", "difficulty": "easy"},
            {"front": "No", "back": "Không", "difficulty": "easy"},
            {"front": "Water", "back": "Nước", "difficulty": "medium"},
            {"front": "Food", "back": "Thức ăn", "difficulty": "medium"},
            {"front": "House", "back": "Nhà", "difficulty": "medium"}
        ],
        "Programming Terms": [
            {"front": "Variable", "back": "A container that stores data values", "difficulty": "easy"},
            {"front": "Function", "back": "A reusable block of code that performs a specific task", "difficulty": "medium"},
            {"front": "Loop", "back": "A programming construct that repeats a block of code", "difficulty": "medium"},
            {"front": "Array", "back": "A data structure that stores multiple values in a single variable", "difficulty": "medium"},
            {"front": "Object", "back": "An instance of a class that contains data and methods", "difficulty": "hard"},
            {"front": "Class", "back": "A blueprint for creating objects with properties and methods", "difficulty": "hard"},
            {"front": "API", "back": "Application Programming Interface - a set of rules for building software", "difficulty": "medium"},
            {"front": "Database", "back": "An organized collection of structured information or data", "difficulty": "medium"},
            {"front": "Algorithm", "back": "A step-by-step procedure for solving a problem", "difficulty": "hard"},
            {"front": "Debugging", "back": "The process of finding and fixing errors in code", "difficulty": "medium"}
        ],
        "Spanish Basics": [
            {"front": "Hola", "back": "Hello", "difficulty": "easy"},
            {"front": "Adiós", "back": "Goodbye", "difficulty": "easy"},
            {"front": "Gracias", "back": "Thank you", "difficulty": "easy"},
            {"front": "Por favor", "back": "Please", "difficulty": "easy"},
            {"front": "Lo siento", "back": "Sorry", "difficulty": "easy"},
            {"front": "Sí", "back": "Yes", "difficulty": "easy"},
            {"front": "No", "back": "No", "difficulty": "easy"},
            {"front": "Agua", "back": "Water", "difficulty": "medium"},
            {"front": "Comida", "back": "Food", "difficulty": "medium"},
            {"front": "Casa", "back": "House", "difficulty": "medium"}
        ],
        "Math Formulas": [
            {"front": "Area of Circle", "back": "A = πr²", "difficulty": "medium"},
            {"front": "Pythagorean Theorem", "back": "a² + b² = c²", "difficulty": "medium"},
            {"front": "Quadratic Formula", "back": "x = (-b ± √(b² - 4ac)) / 2a", "difficulty": "hard"},
            {"front": "Slope Formula", "back": "m = (y₂ - y₁) / (x₂ - x₁)", "difficulty": "medium"},
            {"front": "Distance Formula", "back": "d = √((x₂ - x₁)² + (y₂ - y₁)²)", "difficulty": "medium"}
        ],
        "Science Terms": [
            {"front": "Atom", "back": "The smallest unit of matter that retains the properties of an element", "difficulty": "medium"},
            {"front": "Molecule", "back": "A group of atoms bonded together", "difficulty": "medium"},
            {"front": "Cell", "back": "The basic structural and functional unit of all living organisms", "difficulty": "medium"},
            {"front": "DNA", "back": "Deoxyribonucleic acid - the molecule that carries genetic information", "difficulty": "hard"},
            {"front": "Photosynthesis", "back": "The process by which plants convert sunlight into energy", "difficulty": "medium"},
            {"front": "Gravity", "back": "A force that attracts objects toward each other", "difficulty": "easy"},
            {"front": "Evolution", "back": "The process of change in all forms of life over generations", "difficulty": "medium"},
            {"front": "Ecosystem", "back": "A community of living organisms and their environment", "difficulty": "medium"}
        ]
    }
    
    total_cards = 0
    for flashcard_set in flashcard_sets:
        set_title = flashcard_set.title
        if set_title in flashcards_data:
            cards_data = flashcards_data[set_title]
            for card_data in cards_data:
                try:
                    flashcard = Flashcard(
                        set_id=flashcard_set.id,
                        front_content=card_data["front"],
                        back_content=card_data["back"],
                        card_type="text",
                        difficulty=card_data["difficulty"],
                        card_metadata={"created_by": "test_script"}
                    )
                    db.add(flashcard)
                    total_cards += 1
                    
                except Exception as e:
                    logger.error(f"Error creating flashcard: {e}")
                    db.rollback()
            
            # Update total_cards count for the set
            try:
                flashcard_set.total_cards = len(cards_data)
                db.commit()
                logger.info(f"Created {len(cards_data)} cards for set: {set_title}")
            except Exception as e:
                logger.error(f"Error updating card count for set {set_title}: {e}")
                db.rollback()
    
    logger.info(f"Total flashcards created: {total_cards}")

def main():
    """Main function to create all test data"""
    logger.info("Starting test data creation...")
    
    db = SessionLocal()
    try:
        # Create test users
        users = create_test_users(db)
        
        if not users:
            logger.error("No users created, cannot proceed")
            return
        
        # Create flashcard sets
        flashcard_sets = create_flashcard_sets(db, users)
        
        # Create flashcards
        create_flashcards(db, flashcard_sets)
        
        logger.info("✅ Test data creation completed successfully!")
        logger.info(f"Created {len(users)} users")
        logger.info(f"Created {len(flashcard_sets)} flashcard sets")
        
        # Print login credentials
        logger.info("\n📋 Test User Credentials:")
        logger.info("1. John Doe - john.doe@example.com / password123")
        logger.info("2. Jane Smith - jane.smith@example.com / password123")
        logger.info("3. Admin - admin@vocabularyvault.com / admin123")
        
        logger.info("\n🔗 API Endpoints:")
        logger.info("- Health Check: http://localhost:8000/health")
        logger.info("- API Docs: http://localhost:8000/docs")
        logger.info("- Login: POST http://localhost:8000/api/v1/auth/login")
        
    except Exception as e:
        logger.error(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
