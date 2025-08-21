from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, JSON, Float, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class BadgeType(str, enum.Enum):
    """Types of badges users can earn"""
    STUDY_STREAK = "study_streak"
    PERFECT_SCORE = "perfect_score"
    SPEED_DEMON = "speed_demon"
    MASTER_LEARNER = "master_learner"
    GAME_CHAMPION = "game_champion"
    SOCIAL_BUTTERFLY = "social_butterfly"
    CREATOR = "creator"
    EXPLORER = "explorer"
    # Additional badge types for comprehensive gamification
    PERFECT_GAME = "perfect_game"  # Perfect score in games
    FAST_LEARNER = "fast_learner"  # Quick study sessions
    CONSISTENT_STUDIER = "consistent_studier"  # Regular study habits


class GameType(str, enum.Enum):
    """Types of educational games"""
    MATCH = "match"
    GRAVITY = "gravity"
    SPEED_CHALLENGE = "speed_challenge"
    MEMORY = "memory"


class Badge(Base):
    """Badge definitions - available badges in the system"""
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    badge_type = Column(Enum(BadgeType), nullable=False, name="achievement_type")
    icon_url = Column(String)  # URL to badge icon
    points_reward = Column(Integer, default=0)  # Points awarded for earning this badge
    criteria = Column(JSON)  # Criteria for earning the badge (e.g., {"study_streak": 7})
    rarity = Column(String, default="common")  # common, rare, epic, legendary
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    """User's earned badges"""
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    context_data = Column(JSON)  # Additional data about how the badge was earned

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")

    # Unique constraint to prevent duplicate badges
    __table_args__ = (
        Index('idx_user_badge_unique', 'user_id', 'badge_id', unique=True),
    )


class PointsTransaction(Base):
    """Points transaction history"""
    __tablename__ = "points_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, nullable=False)  # Can be positive (earned) or negative (spent)
    transaction_type = Column(String, nullable=False)  # study, game, badge, bonus, penalty
    description = Column(Text, nullable=False)
    reference_id = Column(Integer)  # ID of related entity (study session, game, badge, etc.)
    reference_type = Column(String)  # Type of reference (study_session, game_session, badge, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="points_transactions")


class LeaderboardEntry(Base):
    """Leaderboard entries for different categories"""
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)  # daily, weekly, monthly, all_time
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    score = Column(Integer, default=0)  # Total score for the period
    rank = Column(Integer)  # Current rank in the leaderboard
    study_time_minutes = Column(Integer, default=0)
    cards_studied = Column(Integer, default=0)
    games_played = Column(Integer, default=0)
    badges_earned = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="leaderboard_entries")

    # Index for efficient leaderboard queries
    __table_args__ = (
        Index('idx_leaderboard_category_period', 'category', 'period_start', 'period_end'),
        Index('idx_leaderboard_user_category', 'user_id', 'category'),
    )


class GameSession(Base):
    """Base game session model"""
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_type = Column(Enum(GameType), nullable=False)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    score = Column(Integer, default=0)
    max_score = Column(Integer, default=0)
    accuracy_rate = Column(Float)
    cards_played = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    game_data = Column(JSON)  # Game-specific data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="game_sessions")
    set = relationship("FlashcardSet", back_populates="game_sessions")
    match_game = relationship("MatchGame", back_populates="session", uselist=False, cascade="all, delete-orphan")
    gravity_game = relationship("GravityGame", back_populates="session", uselist=False, cascade="all, delete-orphan")
    speed_challenge = relationship("SpeedChallenge", back_populates="session", uselist=False, cascade="all, delete-orphan")
    memory_game = relationship("MemoryGame", back_populates="session", uselist=False, cascade="all, delete-orphan")


class MatchGame(Base):
    """Match game specific data"""
    __tablename__ = "match_games"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    moves_count = Column(Integer, default=0)
    matches_found = Column(Integer, default=0)
    total_pairs = Column(Integer, default=0)
    time_bonus = Column(Integer, default=0)  # Bonus points for speed
    perfect_match_bonus = Column(Integer, default=0)  # Bonus for perfect game
    game_state = Column(JSON)  # Current game state (cards, positions, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("GameSession", back_populates="match_game")


class GravityGame(Base):
    """Gravity game specific data"""
    __tablename__ = "gravity_games"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    words_typed = Column(Integer, default=0)
    words_correct = Column(Integer, default=0)
    words_incorrect = Column(Integer, default=0)
    combo_multiplier = Column(Float, default=1.0)  # Current combo multiplier
    max_combo = Column(Integer, default=0)  # Maximum combo achieved
    time_bonus = Column(Integer, default=0)  # Bonus points for speed
    game_state = Column(JSON)  # Current game state (falling words, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("GameSession", back_populates="gravity_game")


class SpeedChallenge(Base):
    """Speed Challenge game specific data"""
    __tablename__ = "speed_challenges"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    total_questions = Column(Integer, default=0)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    time_limit_seconds = Column(Integer, default=60)  # Default 60 seconds
    time_remaining_seconds = Column(Integer)
    average_response_time = Column(Float, default=0.0)
    fastest_response_time = Column(Float)
    slowest_response_time = Column(Float)
    streak_count = Column(Integer, default=0)  # Current correct answer streak
    max_streak = Column(Integer, default=0)  # Maximum streak achieved
    game_state = Column(JSON)  # Current game state (questions, timer, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("GameSession", back_populates="speed_challenge")


class MemoryGame(Base):
    """Memory/Concentration game specific data"""
    __tablename__ = "memory_games"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    total_cards = Column(Integer, default=0)
    cards_revealed = Column(Integer, default=0)
    matches_found = Column(Integer, default=0)
    moves_count = Column(Integer, default=0)
    time_limit_seconds = Column(Integer, default=300)  # Default 5 minutes
    time_remaining_seconds = Column(Integer)
    revealed_cards = Column(JSON)  # Array of currently revealed card IDs
    matched_pairs = Column(JSON)  # Array of matched card pairs
    game_state = Column(JSON)  # Current game state (card positions, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("GameSession", back_populates="memory_game")


class ChallengeType(str, enum.Enum):
    """Types of challenges users can participate in"""
    STUDY_STREAK = "study_streak"
    PERFECT_SCORE = "perfect_score"
    SPEED_RUN = "speed_run"
    DAILY_GOAL = "daily_goal"
    WEEKLY_GOAL = "weekly_goal"
    GAME_MASTER = "game_master"
    SOCIAL_SHARER = "social_sharer"


class Challenge(Base):
    """Challenge definitions - available challenges in the system"""
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    challenge_type = Column(Enum(ChallengeType), nullable=False)
    criteria = Column(JSON)  # Criteria for completing the challenge
    reward_points = Column(Integer, default=0)  # Points awarded for completion
    reward_badge_id = Column(Integer, ForeignKey("badges.id"))  # Badge awarded for completion
    duration_days = Column(Integer, default=1)  # Challenge duration in days
    is_active = Column(Boolean, default=True)
    is_recurring = Column(Boolean, default=False)  # Daily/weekly recurring challenges
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    reward_badge = relationship("Badge")
    user_challenges = relationship("UserChallenge", back_populates="challenge")


class UserChallenge(Base):
    """User's challenge participation and progress"""
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    progress_data = Column(JSON)  # Current progress towards challenge completion
    is_completed = Column(Boolean, default=False)
    is_failed = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="user_challenges")
    challenge = relationship("Challenge", back_populates="user_challenges")

    # Unique constraint to prevent duplicate challenge participation
    __table_args__ = (
        Index('idx_user_challenge_unique', 'user_id', 'challenge_id', unique=True),
    )
