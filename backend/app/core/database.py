from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        # Import all models from modules to ensure they are registered
        from app.modules.auth.models import User
        
        # Import flashcard models
        from app.modules.flashcards.models import (
            FlashcardSet, Flashcard, StudySession, StudyAttempt, SetSharing
        )
        
        # Import gamification models
        from app.modules.gamification.models import (
            Badge, UserBadge, GameSession, Leaderboard, Challenge, UserChallenge, LearningStreak
        )
        
        # Import AI models
        from app.modules.ai.models import (
            AIConversation, AIMessage, ContentGeneration,
            LearningRecommendation, AdaptiveLearningProfile, PronunciationAnalysis
        )
        
        # Import analytics models
        from app.modules.analytics.models import (
            UserAnalytics, StudyProgress, LearningInsight,
            PerformanceMetric, StudyGoal, LearningPath
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise
