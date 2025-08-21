"""
AI Module Schemas
Pydantic schemas for AI conversation, content generation, and adaptive learning
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ConversationContextType(str, Enum):
    """Types of conversation context"""
    GENERAL = "general"
    STUDY_HELP = "study_help"
    FLASHCARD_EXPLANATION = "flashcard_explanation"
    CONTENT_GENERATION = "content_generation"


class ContentType(str, Enum):
    """Types of AI-generated content"""
    FLASHCARD_SET = "flashcard_set"
    EXPLANATION = "explanation"
    QUIZ = "quiz"
    STUDY_PLAN = "study_plan"
    RECOMMENDATION = "recommendation"


class RecommendationType(str, Enum):
    """Types of adaptive recommendations"""
    STUDY_MODE = "study_mode"
    DIFFICULTY = "difficulty"
    CONTENT = "content"
    TIMING = "timing"


class TutorSessionType(str, Enum):
    """Types of AI tutor sessions"""
    GUIDED_STUDY = "guided_study"
    REVIEW = "review"
    PRACTICE = "practice"
    ASSESSMENT = "assessment"


# AI Conversation Schemas
class AIConversationBase(BaseModel):
    """Base schema for AI conversations"""
    title: str = Field(..., min_length=1, max_length=255)
    context_type: ConversationContextType = ConversationContextType.GENERAL
    context_data: Optional[Dict[str, Any]] = None


class AIConversationCreate(AIConversationBase):
    """Schema for creating a new AI conversation"""
    pass


class AIConversationUpdate(BaseModel):
    """Schema for updating an AI conversation"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None


class AIConversationResponse(AIConversationBase):
    """Schema for AI conversation response"""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# AI Message Schemas
class AIMessageBase(BaseModel):
    """Base schema for AI messages"""
    content: str = Field(..., min_length=1)
    message_metadata: Optional[Dict[str, Any]] = None


class AIMessageCreate(AIMessageBase):
    """Schema for creating a new AI message"""
    role: str = Field(..., pattern="^(user|assistant|system)$")


class AIMessageResponse(AIMessageBase):
    """Schema for AI message response"""
    id: int
    conversation_id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationWithMessages(AIConversationResponse):
    """Schema for conversation with messages"""
    messages: List[AIMessageResponse] = []


# Content Generation Schemas
class ContentGenerationRequest(BaseModel):
    """Schema for content generation requests"""
    content_type: ContentType
    source_text: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    context_data: Optional[Dict[str, Any]] = None


class ContentGenerationResponse(BaseModel):
    """Schema for content generation response"""
    id: int
    user_id: int
    content_type: ContentType
    source_text: Optional[str] = None
    generated_data: Dict[str, Any]
    generation_metadata: Optional[Dict[str, Any]] = None
    is_imported: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Learning Profile Schemas
class LearningProfileBase(BaseModel):
    """Base schema for learning profiles"""
    preferred_study_mode: str = Field(default="flashcards")
    preferred_difficulty: str = Field(default="adaptive")
    study_session_duration: int = Field(default=15, ge=5, le=120)
    daily_study_goal: int = Field(default=50, ge=1, le=1000)


class LearningProfileCreate(LearningProfileBase):
    """Schema for creating a learning profile"""
    pass


class LearningProfileUpdate(BaseModel):
    """Schema for updating a learning profile"""
    preferred_study_mode: Optional[str] = None
    preferred_difficulty: Optional[str] = None
    study_session_duration: Optional[int] = Field(None, ge=5, le=120)
    daily_study_goal: Optional[int] = Field(None, ge=1, le=1000)


class LearningProfileResponse(LearningProfileBase):
    """Schema for learning profile response"""
    id: int
    user_id: int
    average_response_time: Optional[float] = None
    accuracy_rate: Optional[float] = None
    retention_rate: Optional[float] = None
    learning_speed: Optional[float] = None
    recommended_difficulty: str
    recommended_study_mode: str
    next_review_time: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Adaptive Recommendation Schemas
class AdaptiveRecommendationBase(BaseModel):
    """Base schema for adaptive recommendations"""
    recommendation_type: RecommendationType
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    priority: int = Field(default=1, ge=1, le=5)
    data: Optional[Dict[str, Any]] = None


class AdaptiveRecommendationCreate(AdaptiveRecommendationBase):
    """Schema for creating an adaptive recommendation"""
    expires_at: Optional[datetime] = None


class AdaptiveRecommendationUpdate(BaseModel):
    """Schema for updating an adaptive recommendation"""
    is_applied: Optional[bool] = None


class AdaptiveRecommendationResponse(AdaptiveRecommendationBase):
    """Schema for adaptive recommendation response"""
    id: int
    user_id: int
    is_applied: bool
    expires_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# AI Tutor Session Schemas
class AITutorSessionBase(BaseModel):
    """Base schema for AI tutor sessions"""
    session_type: TutorSessionType
    difficulty_level: str = Field(default="medium")
    target_accuracy: float = Field(default=0.8, ge=0.1, le=1.0)


class AITutorSessionCreate(AITutorSessionBase):
    """Schema for creating an AI tutor session"""
    set_id: Optional[int] = None


class AITutorSessionUpdate(BaseModel):
    """Schema for updating an AI tutor session"""
    current_accuracy: Optional[float] = Field(None, ge=0.0, le=1.0)
    cards_studied: Optional[int] = Field(None, ge=0)
    is_completed: Optional[bool] = None
    session_data: Optional[Dict[str, Any]] = None


class AITutorSessionResponse(AITutorSessionBase):
    """Schema for AI tutor session response"""
    id: int
    user_id: int
    set_id: Optional[int] = None
    current_accuracy: Optional[float] = None
    cards_studied: int
    total_cards: Optional[int] = None
    is_completed: bool
    session_data: Optional[Dict[str, Any]] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# AI Service Schemas
class AIChatRequest(BaseModel):
    """Schema for AI chat requests"""
    message: str = Field(..., min_length=1)
    conversation_id: Optional[int] = None
    context_type: ConversationContextType = ConversationContextType.GENERAL
    context_data: Optional[Dict[str, Any]] = None


class AIChatResponse(BaseModel):
    """Schema for AI chat response"""
    conversation_id: int
    message: AIMessageResponse
    response: AIMessageResponse


class FlashcardGenerationRequest(BaseModel):
    """Schema for flashcard generation requests"""
    source_text: str = Field(..., min_length=10)
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty: str = Field(default="medium")
    num_cards: int = Field(default=10, ge=1, le=50)


class StudyPlanGenerationRequest(BaseModel):
    """Schema for study plan generation requests"""
    set_id: int
    study_duration_minutes: int = Field(default=30, ge=5, le=180)
    target_accuracy: float = Field(default=0.8, ge=0.5, le=1.0)
    preferred_mode: Optional[str] = None


class LearningInsightRequest(BaseModel):
    """Schema for learning insight requests"""
    user_id: int
    time_period_days: int = Field(default=7, ge=1, le=90)


# Response schemas for lists
class AIConversationListResponse(BaseModel):
    """Schema for list of AI conversations"""
    conversations: List[AIConversationResponse]
    total: int
    page: int
    size: int


class GeneratedContentListResponse(BaseModel):
    """Schema for list of generated content"""
    content: List[ContentGenerationResponse]
    total: int
    page: int
    size: int


class AdaptiveRecommendationListResponse(BaseModel):
    """Schema for list of adaptive recommendations"""
    recommendations: List[AdaptiveRecommendationResponse]
    total: int
    page: int
    size: int


class AITutorSessionListResponse(BaseModel):
    """Schema for list of AI tutor sessions"""
    sessions: List[AITutorSessionResponse]
    total: int
    page: int
    size: int
