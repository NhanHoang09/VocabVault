from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MasteryLevel(str, Enum):
    """Mastery level enumeration"""
    NOT_LEARNED = "NOT_LEARNED"
    LEARNING = "LEARNING"
    WELL_LEARNED = "WELL_LEARNED"
    MASTERED = "MASTERED"


class StudyMode(str, Enum):
    """Study mode enumeration"""
    FLASHCARDS = "flashcards"
    LEARN = "learn"
    WRITE = "write"
    SPELL = "spell"
    TEST = "test"


# Base Progress Schemas
class ProgressBase(BaseModel):
    """Base schema for progress data"""
    total_cards: int = Field(..., description="Total number of cards")
    cards_studied: int = Field(..., description="Number of cards studied")
    correct_answers: int = Field(..., description="Number of correct answers")
    incorrect_answers: int = Field(..., description="Number of incorrect answers")
    accuracy_rate: float = Field(..., description="Overall accuracy rate (0.0 to 1.0)")
    total_study_time_minutes: int = Field(..., description="Total study time in minutes")


class MasteryDistribution(BaseModel):
    """Mastery level distribution"""
    not_learned: int = Field(..., description="Number of cards not learned")
    learning: int = Field(..., description="Number of cards being learned")
    well_learned: int = Field(..., description="Number of well-learned cards")
    mastered: int = Field(..., description="Number of mastered cards")


# User Progress Response
class UserProgressResponse(ProgressBase):
    """Schema for user progress response"""
    user_id: int
    total_sets: int = Field(..., description="Total number of flashcard sets")
    active_sets: int = Field(..., description="Number of sets with recent activity")
    study_sessions_count: int = Field(..., description="Total number of study sessions")
    current_streak_days: int = Field(..., description="Current study streak in days")
    longest_streak_days: int = Field(..., description="Longest study streak in days")
    mastery_distribution: MasteryDistribution
    average_session_duration_minutes: float = Field(..., description="Average session duration")
    last_study_date: Optional[datetime] = Field(None, description="Last study session date")


# Set Progress Response
class SetProgressResponse(ProgressBase):
    """Schema for set progress response"""
    set_id: int
    set_title: str = Field(..., description="Flashcard set title")
    cards_in_set: int = Field(..., description="Total cards in the set")
    mastery_distribution: MasteryDistribution
    study_sessions_count: int = Field(..., description="Number of study sessions for this set")
    last_studied: Optional[datetime] = Field(None, description="Last study session date")
    average_session_duration_minutes: float = Field(..., description="Average session duration")
    study_mode_breakdown: Dict[str, int] = Field(..., description="Breakdown by study mode")


# Daily Statistics
class DailyStatsResponse(BaseModel):
    """Schema for daily statistics response"""
    date: str = Field(..., description="Date of the statistics (YYYY-MM-DD)")
    study_time_minutes: int = Field(..., description="Study time in minutes")
    sessions_count: int = Field(..., description="Number of study sessions")
    cards_studied: int = Field(..., description="Number of cards studied")
    correct_answers: int = Field(..., description="Number of correct answers")
    incorrect_answers: int = Field(..., description="Number of incorrect answers")
    accuracy_rate: float = Field(..., description="Daily accuracy rate")
    study_mode_breakdown: Dict[str, int] = Field(..., description="Breakdown by study mode")
    sets_studied: List[int] = Field(..., description="List of set IDs studied")


# Weekly Statistics
class WeeklyStatsResponse(BaseModel):
    """Schema for weekly statistics response"""
    week_start: str = Field(..., description="Week start date (YYYY-MM-DD)")
    week_end: str = Field(..., description="Week end date (YYYY-MM-DD)")
    total_study_time_minutes: int = Field(..., description="Total study time for the week")
    total_sessions: int = Field(..., description="Total study sessions for the week")
    total_cards_studied: int = Field(..., description="Total cards studied for the week")
    average_accuracy: float = Field(..., description="Average accuracy for the week")
    study_mode_breakdown: Dict[str, int] = Field(..., description="Breakdown by study mode")
    sets_studied: List[int] = Field(..., description="List of set IDs studied")


# Monthly Statistics
class MonthlyStatsResponse(BaseModel):
    """Schema for monthly statistics response"""
    year: int = Field(..., description="Year")
    month: int = Field(..., description="Month (1-12)")
    total_study_time_minutes: int = Field(..., description="Total study time for the month")
    total_sessions: int = Field(..., description="Total study sessions for the month")
    total_cards_studied: int = Field(..., description="Total cards studied for the month")
    average_accuracy: float = Field(..., description="Average accuracy for the month")
    study_mode_breakdown: Dict[str, int] = Field(..., description="Breakdown by study mode")
    sets_studied: List[int] = Field(..., description="List of set IDs studied")


# Streak Information
class StreakInfo(BaseModel):
    """Schema for streak information"""
    current_streak_days: int = Field(..., description="Current streak in days")
    longest_streak_days: int = Field(..., description="Longest streak in days")
    streak_start_date: Optional[str] = Field(None, description="Current streak start date (YYYY-MM-DD)")
    longest_streak_start_date: Optional[str] = Field(None, description="Longest streak start date (YYYY-MM-DD)")
    longest_streak_end_date: Optional[str] = Field(None, description="Longest streak end date (YYYY-MM-DD)")
    next_milestone_days: int = Field(..., description="Days until next milestone")
    milestone_target: int = Field(..., description="Next milestone target")


class LearningPathResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    current_step: int
    total_steps: int
    progress_percentage: float
    is_completed: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# Phase 4: Social Features Schemas
class SocialAnalyticsBase(BaseModel):
    interaction_type: str
    target_user_id: Optional[int] = None
    target_set_id: Optional[int] = None
    interaction_data: Optional[Dict[str, Any]] = None


class SocialAnalyticsCreate(SocialAnalyticsBase):
    pass


class SocialAnalyticsResponse(SocialAnalyticsBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommunitySetBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    tags: Optional[List[str]] = None
    difficulty_level: str = "medium"
    language: Optional[str] = None
    is_public: bool = True


class CommunitySetCreate(CommunitySetBase):
    original_set_id: int


class CommunitySetUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty_level: Optional[str] = None
    language: Optional[str] = None
    is_public: Optional[bool] = None


class CommunitySetResponse(CommunitySetBase):
    id: int
    original_set_id: int
    creator_id: int
    is_featured: bool
    view_count: int
    import_count: int
    rating: float
    rating_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class SetRatingBase(BaseModel):
    rating: int  # 1-5 stars
    review: Optional[str] = None


class SetRatingCreate(SetRatingBase):
    community_set_id: int


class SetRatingUpdate(BaseModel):
    rating: Optional[int] = None
    review: Optional[str] = None


class SetRatingResponse(SetRatingBase):
    id: int
    user_id: int
    community_set_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class StudyGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = True
    max_members: int = 50


class StudyGroupCreate(StudyGroupBase):
    pass


class StudyGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    max_members: Optional[int] = None


class StudyGroupResponse(StudyGroupBase):
    id: int
    creator_id: int
    current_members: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class StudyGroupMemberBase(BaseModel):
    role: str = "member"


class StudyGroupMemberCreate(StudyGroupMemberBase):
    group_id: int


class StudyGroupMemberResponse(StudyGroupMemberBase):
    id: int
    group_id: int
    user_id: int
    joined_at: datetime

    class Config:
        from_attributes = True


class GroupStudySessionBase(BaseModel):
    session_type: str  # collaborative, competitive, review
    set_id: Optional[int] = None


class GroupStudySessionCreate(GroupStudySessionBase):
    group_id: int


class GroupStudySessionUpdate(BaseModel):
    end_time: Optional[datetime] = None
    session_data: Optional[Dict[str, Any]] = None


class GroupStudySessionResponse(GroupStudySessionBase):
    id: int
    group_id: int
    start_time: datetime
    end_time: Optional[datetime]
    session_data: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class GroupSessionParticipantBase(BaseModel):
    performance_data: Optional[Dict[str, Any]] = None


class GroupSessionParticipantCreate(GroupSessionParticipantBase):
    session_id: int


class GroupSessionParticipantUpdate(BaseModel):
    left_at: Optional[datetime] = None
    performance_data: Optional[Dict[str, Any]] = None


class GroupSessionParticipantResponse(GroupSessionParticipantBase):
    id: int
    session_id: int
    user_id: int
    joined_at: datetime
    left_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserFollowBase(BaseModel):
    following_id: int


class UserFollowCreate(UserFollowBase):
    pass


class UserFollowResponse(UserFollowBase):
    id: int
    follower_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    notification_type: str
    title: str
    message: str
    data: Optional[Dict[str, Any]] = None


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# List response schemas
class CommunitySetListResponse(BaseModel):
    sets: List[CommunitySetResponse]
    total: int
    page: int
    size: int


class StudyGroupListResponse(BaseModel):
    groups: List[StudyGroupResponse]
    total: int
    page: int
    size: int


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    page: int
    size: int
    unread_count: int


# Advanced Analytics Schemas
class AdvancedAnalyticsResponse(BaseModel):
    study_trends: Dict[str, Any]
    social_interactions: Dict[str, Any]
    community_engagement: Dict[str, Any]
    learning_effectiveness: Dict[str, Any]
    recommendations: List[Dict[str, Any]]


class SocialInsightsResponse(BaseModel):
    total_followers: int
    total_following: int
    sets_shared: int
    sets_imported: int
    community_rating: float
    group_participation: int
    recent_activity: List[Dict[str, Any]]


class CommunityStatsResponse(BaseModel):
    total_community_sets: int
    total_ratings: int
    average_rating: float
    most_popular_categories: List[Dict[str, Any]]
    trending_sets: List[CommunitySetResponse]
    user_contributions: Dict[str, Any]
