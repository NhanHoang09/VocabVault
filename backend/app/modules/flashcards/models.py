from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class CardType(str, enum.Enum):
    """Types of flashcard content"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"


class DifficultyLevel(str, enum.Enum):
    """Card difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class MasteryLevel(str, enum.Enum):
    """Mastery levels for cards"""
    NOT_LEARNED = "not_learned"
    LEARNING = "learning"
    REVIEWING = "reviewing"
    MASTERED = "mastered"


class StudyMode(str, enum.Enum):
    """Available study modes"""
    FLASHCARDS = "flashcards"
    LEARN = "learn"
    WRITE = "write"
    SPELL = "spell"
    TEST = "test"
    MATCH = "match"
    GRAVITY = "gravity"


class FlashcardSet(Base):
    """Flashcard set model - equivalent to Quizlet set"""
    __tablename__ = "flashcard_sets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # e.g., "Programming", "Languages", "Science"
    tags = Column(JSON)  # Array of tags
    is_public = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    total_cards = Column(Integer, default=0)
    study_count = Column(Integer, default=0)  # How many times this set has been studied
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="flashcard_sets")
    cards = relationship("Flashcard", back_populates="set", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="set", cascade="all, delete-orphan")
    game_sessions = relationship("GameSession", back_populates="set", cascade="all, delete-orphan")
    sharing = relationship("SetSharing", back_populates="set", cascade="all, delete-orphan")
    progress = relationship("StudyProgress", back_populates="set")
    ai_tutor_sessions = relationship("AITutorSession", back_populates="flashcard_set", cascade="all, delete-orphan")


class Flashcard(Base):
    """Individual flashcard model"""
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    front_content = Column(Text, nullable=False)  # Question/term
    back_content = Column(Text, nullable=False)   # Answer/definition
    card_type = Column(Enum(CardType), default=CardType.TEXT)
    media_url = Column(String)  # URL to image/audio/video
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    mastery_level = Column(Enum(MasteryLevel), default=MasteryLevel.NOT_LEARNED)
    mastery_score = Column(Float, default=0.0)  # 0.0 to 1.0
    review_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    last_reviewed_at = Column(DateTime(timezone=True))
    next_review_at = Column(DateTime(timezone=True))
    card_metadata = Column(JSON)  # Additional card data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    set = relationship("FlashcardSet", back_populates="cards")
    study_attempts = relationship("StudyAttempt", back_populates="card")


class StudySession(Base):
    """Study session tracking"""
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    study_mode = Column(Enum(StudyMode), nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    cards_studied = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    accuracy_rate = Column(Float)
    session_data = Column(JSON)  # Detailed session data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="study_sessions")
    set = relationship("FlashcardSet", back_populates="study_sessions")
    attempts = relationship("StudyAttempt", back_populates="session")


class StudyAttempt(Base):
    """Individual study attempt for a card"""
    __tablename__ = "study_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("flashcards.id"), nullable=False)
    user_answer = Column(Text)
    is_correct = Column(Boolean)
    response_time_seconds = Column(Float)
    confidence_level = Column(Integer)  # 1-5 scale
    attempt_number = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="study_attempts")
    session = relationship("StudySession", back_populates="attempts")
    card = relationship("Flashcard", back_populates="study_attempts")


class SetSharing(Base):
    """Flashcard set sharing permissions"""
    __tablename__ = "set_sharings"

    id = Column(Integer, primary_key=True, index=True)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    shared_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    shared_with = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_level = Column(String, default="view")  # view, edit, admin
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    set = relationship("FlashcardSet", back_populates="sharing")
    shared_by_user = relationship("User", foreign_keys=[shared_by], back_populates="shared_sets")
    shared_with_user = relationship("User", foreign_keys=[shared_with], back_populates="received_sets") 
