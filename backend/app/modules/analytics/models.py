from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class AnalyticsType(str, enum.Enum):
    """Types of analytics data"""
    DAILY_STUDY = "daily_study"
    WEEKLY_PROGRESS = "weekly_progress"
    MONTHLY_REPORT = "monthly_report"
    PERFORMANCE_TREND = "performance_trend"
    LEARNING_INSIGHTS = "learning_insights"


class UserAnalytics(Base):
    """User analytics data"""
    __tablename__ = "user_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    analytics_type = Column(Enum(AnalyticsType), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    data = Column(JSON, nullable=False)  # Analytics data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="analytics")


class StudyProgress(Base):
    """Detailed study progress tracking"""
    __tablename__ = "study_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    study_time_minutes = Column(Integer, default=0)
    cards_studied = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    accuracy_rate = Column(Float, default=0.0)
    mastery_gained = Column(Float, default=0.0)
    study_sessions = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="study_progress")
    set = relationship("FlashcardSet", back_populates="progress")


class LearningInsight(Base):
    """AI-generated learning insights"""
    __tablename__ = "learning_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    insight_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    data = Column(JSON)  # Insight-specific data
    priority = Column(Integer, default=1)  # 1-5 priority
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="learning_insights")


class PerformanceMetric(Base):
    """Performance metrics tracking"""
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String)  # percentage, count, time, etc.
    context = Column(JSON)  # Additional context
    date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="performance_metrics")


class StudyGoal(Base):
    """User study goals"""
    __tablename__ = "study_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    goal_type = Column(String, nullable=False)  # daily, weekly, monthly
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    unit = Column(String)  # minutes, cards, sessions, etc.
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_completed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="study_goals")


class LearningPath(Base):
    """Personalized learning paths"""
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    path_data = Column(JSON, nullable=False)  # Learning path structure
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, default=0)
    progress_percentage = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="learning_paths")


# Phase 4: Advanced Analytics Models
class SocialAnalytics(Base):
    """Social interaction analytics"""
    __tablename__ = "social_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interaction_type = Column(String, nullable=False)  # share, import, collaborate, follow
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=True)
    interaction_data = Column(JSON, nullable=True)  # Additional interaction details
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="social_analytics")
    target_user = relationship("User", foreign_keys=[target_user_id])


class CommunitySet(Base):
    """Community-shared flashcard sets"""
    __tablename__ = "community_sets"

    id = Column(Integer, primary_key=True, index=True)
    original_set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)  # language, subject, topic
    tags = Column(JSON, nullable=True)  # Array of tags
    difficulty_level = Column(String, default="medium")  # easy, medium, hard
    language = Column(String, nullable=True)  # Language of the set
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    import_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    original_set = relationship("FlashcardSet")
    creator = relationship("User", back_populates="community_sets")
    ratings = relationship("SetRating", back_populates="community_set", cascade="all, delete-orphan")


class SetRating(Base):
    """User ratings for community sets"""
    __tablename__ = "set_ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    community_set_id = Column(Integer, ForeignKey("community_sets.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="set_ratings")
    community_set = relationship("CommunitySet", back_populates="ratings")


class StudyGroup(Base):
    """Study groups for collaborative learning"""
    __tablename__ = "study_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=True)
    max_members = Column(Integer, default=50)
    current_members = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="created_study_groups")
    members = relationship("StudyGroupMember", back_populates="group")
    sessions = relationship("GroupStudySession", back_populates="group")


class StudyGroupMember(Base):
    """Study group membership"""
    __tablename__ = "study_group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member")  # creator, admin, member
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    group = relationship("StudyGroup", back_populates="members")
    user = relationship("User", back_populates="study_group_memberships")


class GroupStudySession(Base):
    """Group study sessions"""
    __tablename__ = "group_study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=False)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=True)
    session_type = Column(String, nullable=False)  # collaborative, competitive, review
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    session_data = Column(JSON, nullable=True)  # Session-specific data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    group = relationship("StudyGroup", back_populates="sessions")
    set = relationship("FlashcardSet")
    participants = relationship("GroupSessionParticipant", back_populates="session")


class GroupSessionParticipant(Base):
    """Participants in group study sessions"""
    __tablename__ = "group_session_participants"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("group_study_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)
    performance_data = Column(JSON, nullable=True)  # Individual performance in session

    # Relationships
    session = relationship("GroupStudySession", back_populates="participants")
    user = relationship("User", back_populates="group_session_participations")


class UserFollow(Base):
    """User following relationships"""
    __tablename__ = "user_follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")


class Notification(Base):
    """User notifications"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notification_type = Column(String, nullable=False)  # follow, share, achievement, reminder
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)  # Additional notification data
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications") 
