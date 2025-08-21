from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class BadgeType(str, Enum):
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


class GameType(str, Enum):
    MATCH = "match"
    GRAVITY = "gravity"
    # TODO: Add when implemented
    # SPEED_CHALLENGE = "speed_challenge"
    # MEMORY = "memory"


# Badge Schemas
class BadgeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Badge name")
    description: str = Field(..., min_length=1, max_length=500, description="Badge description")
    badge_type: BadgeType = Field(..., description="Type of badge")
    icon_url: Optional[str] = Field(None, description="URL to badge icon")
    points_reward: int = Field(0, ge=0, description="Points awarded for earning this badge")
    criteria: Dict[str, Any] = Field(default_factory=dict, description="Criteria for earning the badge")
    rarity: str = Field("common", description="Badge rarity (common, rare, epic, legendary)")
    is_active: bool = Field(True, description="Whether the badge is active")


class BadgeCreate(BadgeBase):
    pass


class BadgeResponse(BadgeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBadgeResponse(BaseModel):
    id: int
    user_id: int
    badge: BadgeResponse
    earned_at: datetime
    context_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# Points Schemas
class PointsTransactionBase(BaseModel):
    points: int = Field(..., description="Points amount (positive for earned, negative for spent)")
    transaction_type: str = Field(..., description="Type of transaction")
    description: str = Field(..., min_length=1, max_length=200, description="Transaction description")
    reference_id: Optional[int] = Field(None, description="ID of related entity")
    reference_type: Optional[str] = Field(None, description="Type of reference entity")


class PointsTransactionCreate(PointsTransactionBase):
    pass


class PointsTransactionResponse(PointsTransactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Leaderboard Schemas
class LeaderboardEntryResponse(BaseModel):
    id: int
    user_id: int
    username: str
    full_name: Optional[str] = None
    category: str
    period_start: datetime
    period_end: datetime
    score: int
    rank: Optional[int] = None
    study_time_minutes: int
    cards_studied: int
    games_played: int
    badges_earned: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    category: str
    period_start: datetime
    period_end: datetime
    entries: List[LeaderboardEntryResponse]
    total_entries: int
    user_rank: Optional[int] = None
    user_score: Optional[int] = None


# Game Session Schemas
class GameSessionBase(BaseModel):
    game_type: GameType = Field(..., description="Type of game")
    set_id: int = Field(..., gt=0, description="Flashcard set ID")
    max_score: int = Field(0, ge=0, description="Maximum possible score")
    game_data: Optional[Dict[str, Any]] = Field(None, description="Game-specific data")


class GameSessionCreate(GameSessionBase):
    pass


class GameSessionUpdate(BaseModel):
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = Field(None, ge=0, description="Session duration in seconds")
    score: Optional[int] = Field(None, ge=0, description="Final score")
    accuracy_rate: Optional[float] = Field(None, ge=0, le=1, description="Accuracy rate (0-1)")
    cards_played: Optional[int] = Field(None, ge=0, description="Number of cards played")
    correct_answers: Optional[int] = Field(None, ge=0, description="Number of correct answers")
    incorrect_answers: Optional[int] = Field(None, ge=0, description="Number of incorrect answers")
    game_data: Optional[Dict[str, Any]] = Field(None, description="Updated game data")


class GameSessionResponse(GameSessionBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    score: int
    accuracy_rate: Optional[float] = None
    cards_played: int
    correct_answers: int
    incorrect_answers: int
    created_at: datetime

    class Config:
        from_attributes = True


# Match Game Schemas
class MatchGameBase(BaseModel):
    total_pairs: int = Field(..., gt=0, description="Total number of pairs to match")
    game_state: Optional[Dict[str, Any]] = Field(None, description="Current game state")


class MatchGameCreate(MatchGameBase):
    pass


class MatchGameUpdate(BaseModel):
    moves_count: Optional[int] = Field(None, ge=0, description="Number of moves made")
    matches_found: Optional[int] = Field(None, ge=0, description="Number of matches found")
    time_bonus: Optional[int] = Field(None, ge=0, description="Time bonus points")
    perfect_match_bonus: Optional[int] = Field(None, ge=0, description="Perfect match bonus")
    game_state: Optional[Dict[str, Any]] = Field(None, description="Updated game state")


class MatchGameResponse(MatchGameBase):
    id: int
    session_id: int
    moves_count: int
    matches_found: int
    time_bonus: int
    perfect_match_bonus: int
    created_at: datetime

    class Config:
        from_attributes = True


# Gravity Game Schemas
class GravityGameBase(BaseModel):
    game_state: Optional[Dict[str, Any]] = Field(None, description="Current game state")


class GravityGameCreate(GravityGameBase):
    pass


class GravityGameUpdate(BaseModel):
    words_typed: Optional[int] = Field(None, ge=0, description="Total words typed")
    words_correct: Optional[int] = Field(None, ge=0, description="Correctly typed words")
    words_incorrect: Optional[int] = Field(None, ge=0, description="Incorrectly typed words")
    combo_multiplier: Optional[float] = Field(None, ge=1.0, description="Current combo multiplier")
    max_combo: Optional[int] = Field(None, ge=0, description="Maximum combo achieved")
    time_bonus: Optional[int] = Field(None, ge=0, description="Time bonus points")
    game_state: Optional[Dict[str, Any]] = Field(None, description="Updated game state")


class GravityGameResponse(GravityGameBase):
    id: int
    session_id: int
    words_typed: int
    words_correct: int
    words_incorrect: int
    combo_multiplier: float
    max_combo: int
    time_bonus: int
    created_at: datetime

    class Config:
        from_attributes = True


# Speed Challenge Game Schemas
class SpeedChallengeBase(BaseModel):
    total_questions: int = Field(..., gt=0, description="Total number of questions")
    time_limit_seconds: int = Field(60, ge=10, le=300, description="Time limit in seconds")
    game_state: Optional[Dict[str, Any]] = Field(None, description="Current game state")


class SpeedChallengeCreate(SpeedChallengeBase):
    pass


class SpeedChallengeUpdate(BaseModel):
    questions_answered: Optional[int] = Field(None, ge=0, description="Number of questions answered")
    correct_answers: Optional[int] = Field(None, ge=0, description="Number of correct answers")
    incorrect_answers: Optional[int] = Field(None, ge=0, description="Number of incorrect answers")
    time_remaining_seconds: Optional[int] = Field(None, ge=0, description="Time remaining in seconds")
    average_response_time: Optional[float] = Field(None, ge=0, description="Average response time")
    fastest_response_time: Optional[float] = Field(None, ge=0, description="Fastest response time")
    slowest_response_time: Optional[float] = Field(None, ge=0, description="Slowest response time")
    streak_count: Optional[int] = Field(None, ge=0, description="Current streak count")
    max_streak: Optional[int] = Field(None, ge=0, description="Maximum streak achieved")
    game_state: Optional[Dict[str, Any]] = Field(None, description="Updated game state")


class SpeedChallengeResponse(SpeedChallengeBase):
    id: int
    session_id: int
    questions_answered: int
    correct_answers: int
    incorrect_answers: int
    time_remaining_seconds: Optional[int]
    average_response_time: float
    fastest_response_time: Optional[float]
    slowest_response_time: Optional[float]
    streak_count: int
    max_streak: int
    created_at: datetime

    class Config:
        from_attributes = True


# Speed Challenge Answer Schema
class SpeedChallengeAnswer(BaseModel):
    question_id: int = Field(..., gt=0, description="Question ID")
    answer: str = Field(..., min_length=1, description="User's answer")
    is_correct: bool = Field(..., description="Whether the answer is correct")
    response_time_seconds: float = Field(..., ge=0, description="Response time in seconds")


# Memory Game Schemas
class MemoryGameBase(BaseModel):
    total_cards: int = Field(..., gt=0, description="Total number of cards")
    time_limit_seconds: int = Field(300, ge=60, le=600, description="Time limit in seconds")
    game_state: Optional[Dict[str, Any]] = Field(None, description="Current game state")


class MemoryGameCreate(MemoryGameBase):
    pass


class MemoryGameUpdate(BaseModel):
    cards_revealed: Optional[int] = Field(None, ge=0, description="Number of cards revealed")
    matches_found: Optional[int] = Field(None, ge=0, description="Number of matches found")
    moves_count: Optional[int] = Field(None, ge=0, description="Number of moves made")
    time_remaining_seconds: Optional[int] = Field(None, ge=0, description="Time remaining in seconds")
    revealed_cards: Optional[List[int]] = Field(None, description="Currently revealed card IDs")
    matched_pairs: Optional[List[List[int]]] = Field(None, description="Matched card pairs")
    game_state: Optional[Dict[str, Any]] = Field(None, description="Updated game state")


class MemoryGameResponse(MemoryGameBase):
    id: int
    session_id: int
    cards_revealed: int
    matches_found: int
    moves_count: int
    time_remaining_seconds: Optional[int]
    revealed_cards: List[int]
    matched_pairs: List[List[int]]
    created_at: datetime

    class Config:
        from_attributes = True


# Memory Game Reveal Schema
class MemoryGameReveal(BaseModel):
    card_id: int = Field(..., gt=0, description="Card ID to reveal")
    is_match: bool = Field(..., description="Whether this reveals a match")


# Challenge Schemas
class ChallengeType(str, Enum):
    STUDY_STREAK = "study_streak"
    PERFECT_SCORE = "perfect_score"
    SPEED_RUN = "speed_run"
    DAILY_GOAL = "daily_goal"
    WEEKLY_GOAL = "weekly_goal"
    GAME_MASTER = "game_master"
    SOCIAL_SHARER = "social_sharer"


class ChallengeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Challenge name")
    description: str = Field(..., min_length=1, max_length=500, description="Challenge description")
    challenge_type: ChallengeType = Field(..., description="Type of challenge")
    criteria: Dict[str, Any] = Field(default_factory=dict, description="Criteria for completing the challenge")
    reward_points: int = Field(0, ge=0, description="Points awarded for completion")
    reward_badge_id: Optional[int] = Field(None, description="Badge ID awarded for completion")
    duration_days: int = Field(1, ge=1, le=365, description="Challenge duration in days")
    is_active: bool = Field(True, description="Whether the challenge is active")
    is_recurring: bool = Field(False, description="Whether the challenge is recurring")


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeResponse(ChallengeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserChallengeBase(BaseModel):
    challenge_id: int = Field(..., gt=0, description="Challenge ID")
    progress_data: Optional[Dict[str, Any]] = Field(None, description="Current progress data")


class UserChallengeCreate(UserChallengeBase):
    pass


class UserChallengeResponse(UserChallengeBase):
    id: int
    user_id: int
    challenge: ChallengeResponse
    started_at: datetime
    completed_at: Optional[datetime]
    is_completed: bool
    is_failed: bool

    class Config:
        from_attributes = True


class ChallengeListResponse(BaseModel):
    items: List[ChallengeResponse]
    total: int
    page: int
    size: int
    pages: int


class UserChallengeListResponse(BaseModel):
    items: List[UserChallengeResponse]
    total: int
    page: int
    size: int
    pages: int


# Game Move Schemas
class MatchGameMove(BaseModel):
    card1_id: int = Field(..., gt=0, description="First card ID")
    card2_id: int = Field(..., gt=0, description="Second card ID")
    is_match: bool = Field(..., description="Whether the cards match")


class GravityGameAnswer(BaseModel):
    word: str = Field(..., min_length=1, description="Typed word")
    is_correct: bool = Field(..., description="Whether the word is correct")
    response_time_seconds: Optional[float] = Field(None, ge=0, description="Response time")


# User Stats Schemas
class UserGamificationStats(BaseModel):
    total_points: int
    level: int
    experience_points: int
    study_streak_days: int
    longest_streak: int
    total_badges: int
    total_games_played: int
    total_study_time_minutes: int
    average_accuracy: float
    rank: Optional[int] = None


# List Response Schemas
class BadgeListResponse(BaseModel):
    items: List[BadgeResponse]
    total: int
    page: int
    size: int
    pages: int


class UserBadgeListResponse(BaseModel):
    items: List[UserBadgeResponse]
    total: int
    page: int
    size: int
    pages: int


class PointsTransactionListResponse(BaseModel):
    items: List[PointsTransactionResponse]
    total: int
    page: int
    size: int
    pages: int


class GameSessionListResponse(BaseModel):
    items: List[GameSessionResponse]
    total: int
    page: int
    size: int
    pages: int
