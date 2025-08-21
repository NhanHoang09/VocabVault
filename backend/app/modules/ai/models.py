"""
AI Module Models
Models for AI conversation, content generation, and adaptive learning features
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime
from typing import Optional, Dict, Any


class AIConversation(Base):
    """AI conversation sessions between users and AI tutor"""
    __tablename__ = "ai_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    context_type = Column(String(50), nullable=False, default="general")  # general, study_help, flashcard_explanation
    context_data = Column(JSON, nullable=True)  # Additional context like flashcard_id, set_id, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ai_conversations")
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AIConversation(id={self.id}, user_id={self.user_id}, title='{self.title}')>"


class AIMessage(Base):
    """Individual messages in AI conversations"""
    __tablename__ = "ai_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON, nullable=True)  # Additional data like tokens used, model used, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("AIConversation", back_populates="messages")
    
    def __repr__(self):
        return f"<AIMessage(id={self.id}, conversation_id={self.conversation_id}, role='{self.role}')>"


class GeneratedContent(Base):
    """AI-generated content like flashcards, explanations, etc."""
    __tablename__ = "generated_content"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content_type = Column(String(50), nullable=False)  # flashcard_set, explanation, quiz, etc.
    source_text = Column(Text, nullable=True)  # Original text used for generation
    generated_data = Column(JSON, nullable=False)  # The generated content
    generation_metadata = Column(JSON, nullable=True)  # Generation parameters, model used, etc.
    is_imported = Column(Boolean, default=False)  # Whether user has imported this content
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="generated_content")
    
    def __repr__(self):
        return f"<GeneratedContent(id={self.id}, user_id={self.user_id}, type='{self.content_type}')>"


class LearningProfile(Base):
    """User's adaptive learning profile and preferences"""
    __tablename__ = "learning_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Learning style preferences
    preferred_study_mode = Column(String(50), default="flashcards")  # flashcards, write, spell, test, games
    preferred_difficulty = Column(String(20), default="adaptive")  # easy, medium, hard, adaptive
    study_session_duration = Column(Integer, default=15)  # minutes
    daily_study_goal = Column(Integer, default=50)  # cards per day
    
    # Learning analytics
    average_response_time = Column(Float, nullable=True)  # seconds
    accuracy_rate = Column(Float, nullable=True)  # percentage
    retention_rate = Column(Float, nullable=True)  # percentage
    learning_speed = Column(Float, nullable=True)  # cards per minute
    
    # AI recommendations
    recommended_difficulty = Column(String(20), default="medium")
    recommended_study_mode = Column(String(50), default="flashcards")
    next_review_time = Column(DateTime(timezone=True), nullable=True)
    
    # Profile metadata
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="learning_profile")
    
    def __repr__(self):
        return f"<LearningProfile(user_id={self.user_id}, preferred_mode='{self.preferred_study_mode}')>"


class AdaptiveRecommendation(Base):
    """AI-generated learning recommendations"""
    __tablename__ = "adaptive_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recommendation_type = Column(String(50), nullable=False)  # study_mode, difficulty, content, timing
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Integer, default=1)  # 1-5, higher is more important
    data = Column(JSON, nullable=True)  # Additional recommendation data
    is_applied = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="adaptive_recommendations")
    
    def __repr__(self):
        return f"<AdaptiveRecommendation(id={self.id}, user_id={self.user_id}, type='{self.recommendation_type}')>"


class AITutorSession(Base):
    """AI tutor study sessions with personalized guidance"""
    __tablename__ = "ai_tutor_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id", ondelete="CASCADE"), nullable=True)
    session_type = Column(String(50), nullable=False)  # guided_study, review, practice, assessment
    difficulty_level = Column(String(20), nullable=False, default="medium")
    target_accuracy = Column(Float, default=0.8)  # 80% target accuracy
    current_accuracy = Column(Float, nullable=True)
    cards_studied = Column(Integer, default=0)
    total_cards = Column(Integer, nullable=True)
    is_completed = Column(Boolean, default=False)
    session_data = Column(JSON, nullable=True)  # Session-specific data
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="ai_tutor_sessions")
    flashcard_set = relationship("FlashcardSet", back_populates="ai_tutor_sessions")
    
    def __repr__(self):
        return f"<AITutorSession(id={self.id}, user_id={self.user_id}, type='{self.session_type}')>"
