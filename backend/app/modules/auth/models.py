from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

# Models will be imported via models_registry to prevent circular imports


class User(Base):
    """User model for authentication and user management"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Gamification fields
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    study_streak_days = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(DateTime(timezone=True))
    
    # Analytics fields
    total_study_time_minutes = Column(Integer, default=0)
    total_cards_studied = Column(Integer, default=0)
    total_correct_answers = Column(Integer, default=0)
    total_incorrect_answers = Column(Integer, default=0)
    average_accuracy = Column(Float, default=0.0)
    
    # Preferences
    study_preferences = Column(JSON, default=dict)  # Preferred study modes, times, etc.
    notification_settings = Column(JSON, default=dict)  # Email, push notifications
    privacy_settings = Column(JSON, default=dict)  # Public profile, data sharing
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    flashcard_sets = relationship("FlashcardSet", back_populates="user", lazy="select")
    study_sessions = relationship("StudySession", back_populates="user", lazy="select")
    study_attempts = relationship("StudyAttempt", back_populates="user", lazy="select")
    # SetSharing relationships - user can be both shared_by and shared_with
    shared_sets = relationship("SetSharing", foreign_keys="SetSharing.shared_by", back_populates="shared_by_user", lazy="select")
    received_sets = relationship("SetSharing", foreign_keys="SetSharing.shared_with", back_populates="shared_with_user", lazy="select")
    # Analytics relationships
    analytics = relationship("UserAnalytics", back_populates="user", lazy="select")
    study_progress = relationship("StudyProgress", back_populates="user", lazy="select")
    learning_insights = relationship("LearningInsight", back_populates="user", lazy="select")
    performance_metrics = relationship("PerformanceMetric", back_populates="user", lazy="select")
    study_goals = relationship("StudyGoal", back_populates="user", lazy="select")
    learning_paths = relationship("LearningPath", back_populates="user", lazy="select")
    
    # Gamification relationships
    badges = relationship("UserBadge", back_populates="user", lazy="select")
    points_transactions = relationship("PointsTransaction", back_populates="user", lazy="select")
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user", lazy="select")
    game_sessions = relationship("GameSession", back_populates="user", lazy="select")
    user_challenges = relationship("UserChallenge", back_populates="user", lazy="select")
    
    # AI relationships
    ai_conversations = relationship("AIConversation", back_populates="user", lazy="select")
    generated_content = relationship("GeneratedContent", back_populates="user", lazy="select")
    learning_profile = relationship("LearningProfile", back_populates="user", lazy="select", uselist=False)
    adaptive_recommendations = relationship("AdaptiveRecommendation", back_populates="user", lazy="select")
    ai_tutor_sessions = relationship("AITutorSession", back_populates="user", lazy="select")
    
    # Social relationships (Phase 4)
    social_analytics = relationship("SocialAnalytics", foreign_keys="SocialAnalytics.user_id", back_populates="user", lazy="select")
    community_sets = relationship("CommunitySet", back_populates="creator", lazy="select")
    set_ratings = relationship("SetRating", back_populates="user", lazy="select")
    created_study_groups = relationship("StudyGroup", back_populates="creator", lazy="select")
    study_group_memberships = relationship("StudyGroupMember", back_populates="user", lazy="select")
    group_session_participations = relationship("GroupSessionParticipant", back_populates="user", lazy="select")
    following = relationship("UserFollow", foreign_keys="UserFollow.follower_id", back_populates="follower", lazy="select")
    followers = relationship("UserFollow", foreign_keys="UserFollow.following_id", back_populates="following", lazy="select")
    notifications = relationship("Notification", back_populates="user", lazy="select")
