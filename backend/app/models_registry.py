"""
Models Registry - Centralized model import management
This file ensures proper import order and prevents circular dependencies
"""
from typing import List, Type
from sqlalchemy.ext.declarative import DeclarativeMeta

# Import order is important to prevent circular dependencies
# 1. First import base models (User)
# 2. Then import dependent models
# 3. Finally configure relationships

# Step 1: Import base models
from app.modules.auth.models import User

# Step 2: Import flashcard models
from app.modules.flashcards.models import (
    FlashcardSet, Flashcard, StudySession, StudyAttempt, SetSharing
)

# Step 3: Import analytics models
from app.modules.analytics.models import (
    UserAnalytics, StudyProgress, LearningInsight,
    PerformanceMetric, StudyGoal, LearningPath
)

# Step 4: Import gamification models
from app.modules.gamification.models import (
    Badge, UserBadge, PointsTransaction, LeaderboardEntry,
    GameSession, MatchGame, GravityGame
)

# Step 5: Import AI models
from app.modules.ai.models import (
    AIConversation, AIMessage, GeneratedContent, LearningProfile,
    AdaptiveRecommendation, AITutorSession
)

# Step 6: Import Phase 4 Analytics & Social models
from app.modules.analytics.models import (
    SocialAnalytics, CommunitySet, SetRating, StudyGroup, StudyGroupMember,
    GroupStudySession, GroupSessionParticipant, UserFollow, Notification
)

# Registry of all models
ALL_MODELS: List[Type] = [
    # Auth models
    User,
    
    # Flashcard models
    FlashcardSet, Flashcard, StudySession, StudyAttempt, SetSharing,
    
    # Analytics models
    UserAnalytics, StudyProgress, LearningInsight, PerformanceMetric, 
    StudyGoal, LearningPath,
    
    # Gamification models
    Badge, UserBadge, PointsTransaction, LeaderboardEntry,
    GameSession, MatchGame, GravityGame,
    
    # AI models
    AIConversation, AIMessage, GeneratedContent, LearningProfile,
    AdaptiveRecommendation, AITutorSession,
    
    # Phase 4: Analytics & Social models
    SocialAnalytics, CommunitySet, SetRating, StudyGroup, StudyGroupMember,
    GroupStudySession, GroupSessionParticipant, UserFollow, Notification,
]

def test_relationships():
    """Test that all relationships can be accessed without errors"""
    from app.core.database import SessionLocal
    
    issues = []
    
    try:
        db = SessionLocal()
        
        for model in ALL_MODELS:
            if not hasattr(model, '__tablename__'):
                continue
                
            # Try to query the model
            try:
                result = db.query(model).first()
                # This will trigger relationship loading if any
            except Exception as e:
                issues.append(f"Error querying {model.__name__}: {str(e)}")
        
        db.close()
        
    except Exception as e:
        issues.append(f"Database connection error: {str(e)}")
    
    if issues:
        import logging
        logger = logging.getLogger(__name__)
        logger.error("Relationship test issues found:")
        for issue in issues:
            logger.error(f"  - {issue}")
        return False
    
    return True

def validate_foreign_keys():
    """Validate that all relationships have proper foreign keys"""
    from sqlalchemy import inspect
    
    issues = []
    
    for model in ALL_MODELS:
        if not hasattr(model, '__tablename__'):
            continue
            
        mapper = inspect(model)
        
        for relationship_name, relationship in mapper.relationships.items():
            # Check if relationship has proper foreign keys
            if hasattr(relationship, 'foreign_keys') and not relationship.foreign_keys:
                issues.append(f"Model {model.__name__}.{relationship_name} has no foreign keys")
            
            # Check if target model exists
            try:
                target_model = relationship.mapper.class_
                if target_model not in ALL_MODELS:
                    issues.append(f"Model {model.__name__}.{relationship_name} targets unknown model {target_model.__name__}")
            except Exception as e:
                issues.append(f"Model {model.__name__}.{relationship_name} has invalid target: {str(e)}")
    
    if issues:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning("Foreign key validation issues found:")
        for issue in issues:
            logger.warning(f"  - {issue}")
        return False
    
    return True

def get_all_models() -> List[Type]:
    """Get all registered models"""
    return ALL_MODELS

def register_models():
    """Register all models with SQLAlchemy"""
    # This function ensures all models are properly registered
    # when the application starts
    from app.core.database import Base
    from sqlalchemy import inspect
    
    # Get all tables that should be created
    tables_to_create = []
    for model in ALL_MODELS:
        if hasattr(model, '__tablename__'):
            tables_to_create.append(model.__tablename__)
    
    # Log registered models for debugging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Registered {len(ALL_MODELS)} models: {tables_to_create}")
    
    return ALL_MODELS
