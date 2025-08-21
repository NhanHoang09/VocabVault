"""
Flashcard schemas for API requests and responses
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class CardType(str, Enum):
    """Card type enumeration"""
    TEXT = "text"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_IN_BLANK = "fill_in_blank"
    IMAGE = "image"
    AUDIO = "audio"


class DifficultyLevel(str, Enum):
    """Difficulty level enumeration"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class MasteryLevel(str, Enum):
    """Mastery level enumeration"""
    NOT_LEARNED = "not_learned"
    LEARNING = "learning"
    REVIEWING = "reviewing"
    MASTERED = "mastered"


class StudyMode(str, Enum):
    """Study mode enumeration"""
    FLASHCARDS = "flashcards"
    LEARN = "learn"
    WRITE = "write"
    SPELL = "spell"
    TEST = "test"


class QuestionType(str, Enum):
    """Question type for test mode"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_IN_BLANK = "fill_in_blank"
    MATCHING = "matching"


# FlashcardSet Schemas
class FlashcardSetBase(BaseModel):
    """Base flashcard set schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    is_public: bool = False
    is_featured: bool = False


class FlashcardSetCreate(FlashcardSetBase):
    """Schema for creating a flashcard set"""
    pass


class FlashcardSetUpdate(BaseModel):
    """Schema for updating a flashcard set"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None


class FlashcardSetResponse(FlashcardSetBase):
    """Schema for flashcard set response"""
    id: int
    user_id: int
    total_cards: int = 0
    study_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FlashcardSetListResponse(BaseModel):
    """Schema for paginated flashcard sets list"""
    items: List[FlashcardSetResponse]
    total: int
    page: int
    size: int
    pages: int


# Flashcard Schemas
class FlashcardBase(BaseModel):
    """Base flashcard schema"""
    front_content: str = Field(..., min_length=1)
    back_content: str = Field(..., min_length=1)
    card_type: Optional[str] = "text"  # text, image, audio, video
    media_url: Optional[str] = None
    difficulty: Optional[str] = "medium"  # easy, medium, hard
    card_metadata: Optional[Dict[str, Any]] = {}


class FlashcardCreate(FlashcardBase):
    """Schema for creating a flashcard"""
    pass


class FlashcardUpdate(BaseModel):
    """Schema for updating a flashcard"""
    front_content: Optional[str] = Field(None, min_length=1)
    back_content: Optional[str] = Field(None, min_length=1)
    card_type: Optional[str] = None
    media_url: Optional[str] = None
    difficulty: Optional[str] = None
    card_metadata: Optional[Dict[str, Any]] = None


class FlashcardResponse(FlashcardBase):
    """Schema for flashcard response"""
    id: int
    set_id: int
    mastery_level: str = "not_learned"
    mastery_score: float = 0.0
    study_count: int = 0
    last_studied_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FlashcardSetWithCards(FlashcardSetResponse):
    """Schema for flashcard set with all cards included"""
    cards: List[FlashcardResponse] = []

    class Config:
        from_attributes = True


class FlashcardListResponse(BaseModel):
    """Schema for paginated flashcards list"""
    items: List[FlashcardResponse]
    total: int
    page: int
    size: int
    pages: int


# Study Session Schemas
class StudySessionBase(BaseModel):
    """Base schema for study session"""
    set_id: int = Field(..., description="ID of the flashcard set")
    study_mode: StudyMode = Field(..., description="Study mode")
    duration_minutes: Optional[int] = Field(None, ge=1, le=480, description="Expected duration in minutes")


class StudySessionCreate(StudySessionBase):
    """Schema for creating a study session"""
    pass


class StudySessionUpdate(BaseModel):
    """Schema for updating a study session"""
    ended_at: Optional[datetime] = None
    total_cards_studied: Optional[int] = Field(None, ge=0)
    correct_answers: Optional[int] = Field(None, ge=0)
    incorrect_answers: Optional[int] = Field(None, ge=0)
    accuracy_percentage: Optional[float] = Field(None, ge=0, le=100)


class StudySessionResponse(StudySessionBase):
    """Schema for study session response"""
    id: int
    user_id: int
    total_cards_studied: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    accuracy_percentage: float = 0.0
    start_time: datetime
    end_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Study Attempt Schemas
class StudyAttemptBase(BaseModel):
    """Base schema for study attempt"""
    card_id: int = Field(..., description="ID of the flashcard")
    session_id: int = Field(..., description="ID of the study session")
    user_answer: str = Field(..., description="User's answer")
    is_correct: bool = Field(..., description="Whether the answer is correct")
    response_time_seconds: Optional[float] = Field(None, ge=0, description="Response time in seconds")


class StudyAttemptCreate(StudyAttemptBase):
    """Schema for creating a study attempt"""
    pass


class StudyAttemptResponse(StudyAttemptBase):
    """Schema for study attempt response"""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Advanced Study Modes Schemas

# Write Mode Schemas
class WriteModeAnswer(BaseModel):
    """Schema for write mode answer"""
    card_id: int = Field(..., description="ID of the flashcard")
    user_answer: str = Field(..., description="User's written answer")
    response_time_seconds: Optional[float] = Field(None, ge=0, description="Response time in seconds")
    confidence_level: Optional[int] = Field(None, ge=1, le=5, description="User's confidence level (1-5)")


class WriteModeAnswerResponse(BaseModel):
    """Schema for write mode answer response"""
    card_id: int
    user_answer: str
    correct_answer: str
    is_correct: bool
    accuracy_score: float
    feedback: str
    suggestions: List[str] = []
    response_time_seconds: float
    created_at: datetime


class WriteModeProgress(BaseModel):
    """Schema for write mode progress"""
    session_id: int
    total_cards: int
    cards_answered: int
    correct_answers: int
    accuracy_percentage: float
    average_response_time: float
    time_remaining_seconds: Optional[int] = None


# Spell Mode Schemas
class SpellModeAnswer(BaseModel):
    """Schema for spell mode answer"""
    card_id: int = Field(..., description="ID of the flashcard")
    user_spelling: str = Field(..., description="User's spelling attempt")
    response_time_seconds: Optional[float] = Field(None, ge=0, description="Response time in seconds")
    audio_played: bool = Field(False, description="Whether audio was played")


class SpellModeAnswerResponse(BaseModel):
    """Schema for spell mode answer response"""
    card_id: int
    user_spelling: str
    correct_spelling: str
    is_correct: bool
    phonetic_feedback: str
    pronunciation_tips: List[str] = []
    response_time_seconds: float
    created_at: datetime


class SpellModeProgress(BaseModel):
    """Schema for spell mode progress"""
    session_id: int
    total_cards: int
    cards_answered: int
    correct_spellings: int
    accuracy_percentage: float
    average_response_time: float
    audio_plays_count: int


# Test Mode Schemas
class TestQuestion(BaseModel):
    """Schema for test question"""
    id: int
    question_type: QuestionType
    question_text: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: DifficultyLevel
    points: int = 1


class TestQuestionResponse(BaseModel):
    """Schema for test question response"""
    question_id: int
    user_answer: str
    is_correct: bool
    points_earned: int
    response_time_seconds: float
    explanation: Optional[str] = None


class TestSessionCreate(BaseModel):
    """Schema for creating a test session"""
    set_id: int = Field(..., description="ID of the flashcard set")
    question_count: int = Field(10, ge=5, le=50, description="Number of questions")
    time_limit_minutes: Optional[int] = Field(None, ge=5, le=120, description="Time limit in minutes")
    include_explanations: bool = Field(True, description="Include explanations in results")
    question_types: Optional[List[QuestionType]] = Field(None, description="Types of questions to include")


class TestSessionResponse(BaseModel):
    """Schema for test session response"""
    id: int
    user_id: int
    set_id: int
    question_count: int
    time_limit_minutes: Optional[int]
    include_explanations: bool
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_score: int = 0
    max_score: int = 0
    accuracy_percentage: float = 0.0
    time_taken_seconds: Optional[int] = None
    questions_answered: int = 0
    correct_answers: int = 0
    created_at: datetime


class TestResult(BaseModel):
    """Schema for test result"""
    test_session_id: int
    total_score: int
    max_score: int
    accuracy_percentage: float
    time_taken_seconds: int
    questions_answered: int
    correct_answers: int
    question_results: List[TestQuestionResponse]
    performance_analysis: Dict[str, Any]
    recommendations: List[str]


# Bulk Operations
class FlashcardBulkCreate(BaseModel):
    """Schema for bulk creating flashcards"""
    cards: List[FlashcardCreate] = Field(..., min_items=1, max_items=100)


class FlashcardBulkUpdate(BaseModel):
    """Schema for bulk updating flashcards"""
    cards: List[dict] = Field(..., min_items=1, max_items=100)  # List of {id: int, ...update_fields}


# Search and Filter Schemas
class FlashcardSetFilter(BaseModel):
    """Schema for filtering flashcard sets"""
    search: Optional[str] = Field(None, description="Search term")
    category: Optional[str] = Field(None, description="Filter by category")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    is_public: Optional[bool] = Field(None, description="Filter by public status")
    user_id: Optional[int] = Field(None, description="Filter by user ID")


class FlashcardFilter(BaseModel):
    """Schema for filtering flashcards"""
    search: Optional[str] = Field(None, description="Search term")
    card_type: Optional[CardType] = Field(None, description="Filter by card type")
    difficulty: Optional[DifficultyLevel] = Field(None, description="Filter by difficulty")
    mastery_level: Optional[MasteryLevel] = Field(None, description="Filter by mastery level")


# Statistics Schemas
class FlashcardSetStats(BaseModel):
    """Schema for flashcard set statistics"""
    total_cards: int
    mastered_cards: int
    learning_cards: int
    not_learned_cards: int
    average_mastery_score: float
    total_study_time_minutes: int
    study_sessions_count: int
    last_studied_at: Optional[datetime]


class UserFlashcardStats(BaseModel):
    """Schema for user flashcard statistics"""
    total_sets: int
    total_cards: int
    total_study_time_minutes: int
    total_study_sessions: int
    average_accuracy: float
    study_streak_days: int
    last_study_date: Optional[datetime]
