"""
Main models file - Centralized import of all models
This file ensures all models are properly imported and registered
"""

# Import all models to ensure they are registered
from app.modules.auth.models import User

from app.modules.flashcards.models import (
    FlashcardSet, Flashcard, StudySession, StudyAttempt, SetSharing
)

from app.modules.analytics.models import (
    UserAnalytics, StudyProgress, LearningInsight,
    PerformanceMetric, StudyGoal, LearningPath
)

# Export all models for easy access
__all__ = [
    # Auth models
    "User",
    
    # Flashcard models
    "FlashcardSet", "Flashcard", "StudySession", "StudyAttempt", "SetSharing",
    
    # Analytics models
    "UserAnalytics", "StudyProgress", "LearningInsight", 
    "PerformanceMetric", "StudyGoal", "LearningPath",
]
