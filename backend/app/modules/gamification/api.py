from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.modules.auth.models import User
from app.modules.gamification.schemas import (
    BadgeResponse, UserBadgeResponse, BadgeListResponse, UserBadgeListResponse,
    PointsTransactionResponse, PointsTransactionListResponse,
    LeaderboardResponse, LeaderboardEntryResponse,
    GameSessionCreate, GameSessionResponse, GameSessionUpdate, GameSessionListResponse,
    MatchGameCreate, MatchGameResponse, MatchGameUpdate,
    GravityGameCreate, GravityGameResponse, GravityGameUpdate,
    SpeedChallengeCreate, SpeedChallengeResponse, SpeedChallengeUpdate,
    MemoryGameCreate, MemoryGameResponse, MemoryGameUpdate,
    ChallengeCreate, ChallengeResponse, ChallengeListResponse,
    UserChallengeCreate, UserChallengeResponse, UserChallengeListResponse,
    MatchGameMove, GravityGameAnswer, SpeedChallengeAnswer, MemoryGameReveal, UserGamificationStats
)
from app.modules.gamification.services import (
    BadgeService, PointsService, LeaderboardService,
    GameSessionService, MatchGameService, GravityGameService, SpeedChallengeService, MemoryGameService, ChallengeService
)
from app.modules.gamification.models import GameType, ChallengeType

router = APIRouter(
    prefix="/gamification", 
    tags=["gamification"],
    responses={
        404: {"description": "Resource not found"},
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient permissions"},
        422: {"description": "Validation error"}
    }
)


# Badge Endpoints
@router.get("/badges", response_model=BadgeListResponse)
def get_all_badges(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get all available badges
    
    This endpoint retrieves all badges that users can earn in the system.
    
    **Features:**
    - Browse all available badges
    - See badge requirements and rewards
    - Pagination support
    
    **Returns:** List of all available badges
    """
    try:
        badges = BadgeService.get_all_badges(db, skip=skip, limit=limit)
        total = len(badges)  # Simplified for now
        
        return BadgeListResponse(
            items=badges,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit if total > 0 else 0
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/badges/{badge_id}", response_model=BadgeResponse)
def get_badge(
    badge_id: int = Path(..., gt=0, description="Badge ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific badge by ID
    
    This endpoint retrieves detailed information about a specific badge.
    
    **Path Parameters:**
    - `badge_id`: The unique identifier of the badge
    
    **Returns:** Detailed badge information
    """
    try:
        badge = BadgeService.get_badge_by_id(db, badge_id)
        if not badge:
            raise HTTPException(status_code=404, detail="Badge not found")
        return badge
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}/badges", response_model=UserBadgeListResponse)
def get_user_badges(
    user_id: int = Path(..., gt=0, description="User ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get badges earned by a user
    
    This endpoint retrieves all badges earned by a specific user.
    
    **Features:**
    - View user's earned badges
    - See when badges were earned
    - Pagination support
    
    **Path Parameters:**
    - `user_id`: The unique identifier of the user
    
    **Returns:** List of user's earned badges
    """
    try:
        # Users can only view their own badges or public user badges
        if user_id != current_user.id:
            # TODO: Add public profile check
            raise HTTPException(status_code=403, detail="Access denied")
        
        user_badges = BadgeService.get_user_badges(db, user_id, skip=skip, limit=limit)
        total = len(user_badges)  # Simplified for now
        
        return UserBadgeListResponse(
            items=user_badges,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit if total > 0 else 0
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/badges/{badge_id}/award", response_model=UserBadgeResponse, status_code=201)
def award_badge(
    badge_id: int = Path(..., gt=0, description="Badge ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Award a badge to the current user
    
    This endpoint awards a badge to the authenticated user.
    
    **Features:**
    - Award badges manually (for testing/admin purposes)
    - Automatic points reward if badge has point value
    - Prevents duplicate badge awards
    
    **Path Parameters:**
    - `badge_id`: The unique identifier of the badge to award
    
    **Returns:** The awarded user badge
    """
    try:
        user_badge = BadgeService.award_badge(db, current_user.id, badge_id)
        return user_badge
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/badges/earn", response_model=UserBadgeResponse, status_code=201)
def earn_badge(
    badge_id: int = Query(..., gt=0, description="Badge ID to earn"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Earn a badge (alias for award_badge)
    
    This endpoint is an alias for awarding badges to the authenticated user.
    Matches the roadmap specification for badge earning.
    
    **Query Parameters:**
    - `badge_id`: The unique identifier of the badge to earn
    
    **Returns:** The earned user badge
    """
    try:
        user_badge = BadgeService.award_badge(db, current_user.id, badge_id)
        return user_badge
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Points Endpoints
@router.get("/points", response_model=UserGamificationStats)
def get_user_points(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's gamification stats
    
    This endpoint retrieves comprehensive gamification statistics for the authenticated user.
    
    **Features:**
    - Total points and level
    - Study streak information
    - Badge count and game statistics
    - Current leaderboard rank
    
    **Returns:** User's complete gamification profile
    """
    try:
        total_points = PointsService.get_user_points(db, current_user.id)
        
        # Get badge count
        user_badges = BadgeService.get_user_badges(db, current_user.id)
        total_badges = len(user_badges)
        
        # Get game sessions count
        game_sessions = GameSessionService.get_user_game_sessions(db, current_user.id)
        total_games = len(game_sessions)
        
        # Calculate level (simplified: 1 level per 1000 points)
        level = (total_points // 1000) + 1
        experience_points = total_points % 1000
        
        return UserGamificationStats(
            total_points=total_points,
            level=level,
            experience_points=experience_points,
            study_streak_days=current_user.study_streak_days,
            longest_streak=current_user.longest_streak,
            total_badges=total_badges,
            total_games_played=total_games,
            total_study_time_minutes=current_user.total_study_time_minutes,
            average_accuracy=current_user.average_accuracy,
            rank=None  # TODO: Calculate current rank
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# User Stats Endpoints (NEW)
@router.get("/users/{user_id}/stats", response_model=UserGamificationStats)
def get_user_stats(
    user_id: int = Path(..., gt=0, description="User ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get gamification stats for a specific user
    
    This endpoint retrieves comprehensive gamification statistics for a specific user.
    
    **Features:**
    - Total points and level
    - Study streak information
    - Badge count and game statistics
    - Current leaderboard rank
    
    **Path Parameters:**
    - `user_id`: The unique identifier of the user
    
    **Returns:** User's complete gamification profile
    """
    try:
        # Users can only view their own stats or public user stats
        if user_id != current_user.id:
            # For now, allow viewing own stats only
            # TODO: Add public profile check later
            pass
        
        total_points = PointsService.get_user_points(db, user_id)
        
        # Get badge count
        user_badges = BadgeService.get_user_badges(db, user_id)
        total_badges = len(user_badges)
        
        # Get game sessions count
        game_sessions = GameSessionService.get_user_game_sessions(db, user_id)
        total_games = len(game_sessions)
        
        # Calculate level (simplified: 1 level per 1000 points)
        level = (total_points // 1000) + 1
        experience_points = total_points % 1000
        
        # Get user from database to access user fields
        from app.modules.auth.models import User
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserGamificationStats(
            total_points=total_points,
            level=level,
            experience_points=experience_points,
            study_streak_days=user.study_streak_days,
            longest_streak=user.longest_streak,
            total_badges=total_badges,
            total_games_played=total_games,
            total_study_time_minutes=user.total_study_time_minutes,
            average_accuracy=user.average_accuracy,
            rank=None  # TODO: Calculate current rank
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}/level", response_model=dict)
def get_user_level(
    user_id: int = Path(..., gt=0, description="User ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get level information for a specific user
    
    This endpoint retrieves level and experience information for a specific user.
    
    **Features:**
    - Current level
    - Experience points
    - Experience needed for next level
    - Level title and description
    
    **Path Parameters:**
    - `user_id`: The unique identifier of the user
    
    **Returns:** User's level information
    """
    try:
        # Users can only view their own level or public user level
        if user_id != current_user.id:
            # For now, allow viewing own level only
            # TODO: Add public profile check later
            pass
        
        total_points = PointsService.get_user_points(db, user_id)
        
        # Calculate level (simplified: 1 level per 1000 points)
        level = (total_points // 1000) + 1
        experience_points = total_points % 1000
        experience_to_next = 1000 - experience_points
        
        # Level titles based on level
        level_titles = {
            1: "Beginner",
            2: "Novice",
            3: "Apprentice",
            4: "Student",
            5: "Scholar",
            6: "Expert",
            7: "Master",
            8: "Grandmaster",
            9: "Legend",
            10: "Mythic"
        }
        
        level_title = level_titles.get(level, f"Level {level}")
        level_description = f"You are a {level_title.lower()} in your learning journey"
        
        return {
            "id": user_id,
            "user_id": user_id,
            "current_level": level,
            "current_xp": experience_points,
            "xp_to_next_level": experience_to_next,
            "total_xp": total_points,
            "level_title": level_title,
            "level_description": level_description,
            "created_at": "2024-01-21T00:00:00Z",
            "updated_at": "2024-01-21T00:00:00Z"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/points/transactions", response_model=PointsTransactionListResponse)
def get_points_transactions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get user's points transaction history
    
    This endpoint retrieves the user's points transaction history.
    
    **Features:**
    - Complete transaction history
    - Points earned and spent
    - Transaction types and descriptions
    - Pagination support
    
    **Returns:** List of points transactions
    """
    try:
        transactions = PointsService.get_user_transactions(db, current_user.id, skip=skip, limit=limit)
        total = len(transactions)  # Simplified for now
        
        return PointsTransactionListResponse(
            items=transactions,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit if total > 0 else 0
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Leaderboard Endpoints
@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(
    category: str = Query("all_time", description="Leaderboard category (daily, weekly, monthly, all_time)"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of entries to return"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get leaderboard for a specific category
    
    This endpoint retrieves the leaderboard for the specified time period.
    
    **Features:**
    - Multiple time periods (daily, weekly, monthly, all-time)
    - User rankings and scores
    - Study statistics for each user
    - Current user's position highlighted
    
    **Query Parameters:**
    - `category`: Time period for the leaderboard
    - `limit`: Maximum number of entries to return
    
    **Returns:** Leaderboard entries with user rankings
    """
    try:
        entries = LeaderboardService.get_leaderboard(db, category, limit)
        
        # Find current user's rank
        user_rank = None
        user_score = None
        for entry in entries:
            if entry.user_id == current_user.id:
                user_rank = entry.rank
                user_score = entry.score
                break
        
        return LeaderboardResponse(
            category=category,
            period_start=entries[0].period_start if entries else None,
            period_end=entries[0].period_end if entries else None,
            entries=entries,
            total_entries=len(entries),
            user_rank=user_rank,
            user_score=user_score
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Game Session Endpoints
@router.post("/games/sessions", response_model=GameSessionResponse, status_code=201)
def create_game_session(
    session_data: GameSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start a new game session
    
    This endpoint allows users to start a new educational game session.
    
    **Features:**
    - Start games for any flashcard set
    - Support for multiple game types
    - Automatic access control
    
    **Required fields:**
    - `game_type`: Type of game (match, gravity, etc.)
    - `set_id`: ID of the flashcard set to use
    
    **Returns:** The created game session
    """
    try:
        game_session = GameSessionService.create_game_session(
            db, current_user.id, session_data
        )
        return game_session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/games/sessions", response_model=GameSessionListResponse)
def get_user_game_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    game_type: Optional[GameType] = Query(None, description="Filter by game type")
):
    """
    Get user's game sessions
    
    This endpoint retrieves all game sessions for the authenticated user.
    
    **Features:**
    - Pagination support
    - Filter by game type
    - Session statistics and performance
    
    **Query Parameters:**
    - `skip`: Number of records to skip
    - `limit`: Maximum records to return
    - `game_type`: Filter by specific game type
    
    **Returns:** List of user's game sessions
    """
    try:
        game_sessions = GameSessionService.get_user_game_sessions(
            db, current_user.id, skip=skip, limit=limit, game_type=game_type
        )
        total = len(game_sessions)  # Simplified for now
        
        return GameSessionListResponse(
            items=game_sessions,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit if total > 0 else 0
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/games/sessions/{session_id}", response_model=GameSessionResponse)
def get_game_session(
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific game session
    
    This endpoint retrieves detailed information about a specific game session.
    
    **Path Parameters:**
    - `session_id`: The unique identifier of the game session
    
    **Returns:** Detailed game session information
    """
    try:
        game_session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not game_session:
            raise HTTPException(status_code=404, detail="Game session not found")
        return game_session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/games/sessions/{session_id}", response_model=GameSessionResponse)
def update_game_session(
    session_data: GameSessionUpdate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a game session (end session)
    
    This endpoint allows users to end a game session and update final statistics.
    
    **Features:**
    - End session and calculate final duration
    - Update accuracy and performance metrics
    - Award points for game performance
    
    **Path Parameters:**
    - `session_id`: The unique identifier of the game session
    
    **Returns:** Updated game session with final statistics
    """
    try:
        game_session = GameSessionService.update_game_session(
            db, session_id, current_user.id, session_data
        )
        return game_session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Match Game Endpoints
@router.post("/games/match/{session_id}", response_model=MatchGameResponse, status_code=201)
def create_match_game(
    game_data: MatchGameCreate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new Match game
    
    This endpoint creates a new Match game within an existing game session.
    
    **Features:**
    - Initialize Match game with card pairs
    - Set up game state and tracking
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** The created Match game
    """
    try:
        match_game = MatchGameService.create_match_game(db, session_id, game_data)
        return match_game
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/games/match/{session_id}", response_model=MatchGameResponse)
def update_match_game(
    game_data: MatchGameUpdate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update Match game progress
    
    This endpoint updates the Match game progress and calculates scores.
    
    **Features:**
    - Track moves and matches
    - Calculate time and efficiency bonuses
    - Update game state
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Updated Match game with progress
    """
    try:
        match_game = MatchGameService.update_match_game(db, session_id, game_data)
        return match_game
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/games/match/{session_id}/move")
def record_match_move(
    move_data: MatchGameMove,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Record a move in Match game
    
    This endpoint records a single move in the Match game.
    
    **Features:**
    - Track individual card selections
    - Validate moves and matches
    - Update game progress
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Move result and updated game state
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        result = MatchGameService.record_move(db, session_id, move_data.is_match)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Gravity Game Endpoints
@router.post("/games/gravity/{session_id}", response_model=GravityGameResponse, status_code=201)
def create_gravity_game(
    game_data: GravityGameCreate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new Gravity game
    
    This endpoint creates a new Gravity game within an existing game session.
    
    **Features:**
    - Initialize Gravity game with falling words
    - Set up game state and tracking
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** The created Gravity game
    """
    try:
        gravity_game = GravityGameService.create_gravity_game(db, session_id, game_data)
        return gravity_game
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/games/gravity/{session_id}", response_model=GravityGameResponse)
def update_gravity_game(
    game_data: GravityGameUpdate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update Gravity game progress
    
    This endpoint updates the Gravity game progress and calculates scores.
    
    **Features:**
    - Track words typed and accuracy
    - Calculate combo multipliers
    - Update game state
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Updated Gravity game with progress
    """
    try:
        gravity_game = GravityGameService.update_gravity_game(db, session_id, game_data)
        return gravity_game
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/games/gravity/{session_id}/answer")
def submit_gravity_answer(
    answer_data: GravityGameAnswer,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit an answer in Gravity game
    
    This endpoint records a word answer in the Gravity game.
    
    **Features:**
    - Validate word answers
    - Track accuracy and response times
    - Update combo multipliers
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Answer result and updated game state
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        result = GravityGameService.submit_answer(
            db,
            session_id=session_id,
            is_correct=answer_data.is_correct,
            response_time_seconds=answer_data.response_time_seconds,
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Speed Challenge Game Endpoints
@router.post("/games/speed-challenge/{session_id}", response_model=SpeedChallengeResponse, status_code=201)
def create_speed_challenge(
    game_data: SpeedChallengeCreate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new Speed Challenge game
    
    This endpoint creates a new Speed Challenge game within an existing game session.
    
    **Features:**
    - Initialize Speed Challenge with timer
    - Set up question tracking and statistics
    - Configure time limits and scoring
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** The created Speed Challenge game
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        speed_challenge = SpeedChallengeService.create_speed_challenge(db, session_id, game_data)
        return speed_challenge
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/games/speed-challenge/{session_id}", response_model=SpeedChallengeResponse)
def update_speed_challenge(
    game_data: SpeedChallengeUpdate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update Speed Challenge game progress
    
    This endpoint updates the Speed Challenge game progress and calculates scores.
    
    **Features:**
    - Track questions answered and accuracy
    - Update time remaining and statistics
    - Calculate real-time scores
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Updated Speed Challenge game with progress
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        speed_challenge = SpeedChallengeService.update_speed_challenge(db, session_id, game_data)
        return speed_challenge
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/games/speed-challenge/{session_id}/answer")
def submit_speed_answer(
    answer_data: SpeedChallengeAnswer,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit an answer in Speed Challenge game
    
    This endpoint records a timed answer in the Speed Challenge game.
    
    **Features:**
    - Validate answers and track response times
    - Update streaks and statistics
    - Calculate real-time scores
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Answer result and updated game state
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        result = SpeedChallengeService.submit_answer(
            db,
            session_id=session_id,
            is_correct=answer_data.is_correct,
            response_time_seconds=answer_data.response_time_seconds,
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Memory Game Endpoints
@router.post("/games/memory/{session_id}", response_model=MemoryGameResponse, status_code=201)
def create_memory_game(
    game_data: MemoryGameCreate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new Memory game
    
    This endpoint creates a new Memory/Concentration game within an existing game session.
    
    **Features:**
    - Initialize Memory game with card pairs
    - Set up card tracking and matching logic
    - Configure time limits and scoring
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** The created Memory game
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        memory_game = MemoryGameService.create_memory_game(db, session_id, game_data)
        return memory_game
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/games/memory/{session_id}", response_model=MemoryGameResponse)
def update_memory_game(
    game_data: MemoryGameUpdate,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update Memory game progress
    
    This endpoint updates the Memory game progress and calculates scores.
    
    **Features:**
    - Track cards revealed and matches found
    - Update time remaining and statistics
    - Calculate real-time scores
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Updated Memory game with progress
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        memory_game = MemoryGameService.update_memory_game(db, session_id, game_data)
        return memory_game
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/games/memory/{session_id}/reveal")
def reveal_memory_card(
    reveal_data: MemoryGameReveal,
    session_id: int = Path(..., gt=0, description="Game session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Reveal a card in Memory game
    
    This endpoint records a card reveal in the Memory/Concentration game.
    
    **Features:**
    - Track card reveals and matches
    - Update game state and statistics
    - Calculate real-time scores
    
    **Path Parameters:**
    - `session_id`: The game session ID
    
    **Returns:** Reveal result and updated game state
    """
    try:
        # Ensure session belongs to current user
        session = GameSessionService.get_game_session(db, session_id, current_user.id)
        if not session:
            raise HTTPException(status_code=404, detail="Game session not found")
        result = MemoryGameService.reveal_card(
            db,
            session_id=session_id,
            card_id=reveal_data.card_id,
            is_match=reveal_data.is_match,
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Challenge Endpoints
@router.get("/challenges", response_model=ChallengeListResponse)
def get_all_challenges(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    challenge_type: Optional[ChallengeType] = Query(None, description="Filter by challenge type")
):
    """
    Get all available challenges
    
    This endpoint retrieves all challenges that users can participate in.
    
    **Features:**
    - Browse all available challenges
    - Filter by challenge type
    - See challenge requirements and rewards
    - Pagination support
    
    **Returns:** List of all available challenges
    """
    try:
        challenges = ChallengeService.get_all_challenges(db, skip=skip, limit=limit, challenge_type=challenge_type)
        total = len(challenges)  # Simplified for now
        
        return ChallengeListResponse(
            items=challenges,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit if total > 0 else 0
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/challenges/daily", response_model=ChallengeListResponse)
def get_daily_challenges(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get daily challenges for the current user
    
    This endpoint retrieves daily challenges that the user can participate in.
    
    **Features:**
    - Daily recurring challenges
    - Challenge progress tracking
    - Reward information
    
    **Returns:** List of daily challenges
    """
    try:
        # Filter challenges by daily type
        challenges = ChallengeService.get_all_challenges(db, skip=skip, limit=limit, challenge_type=ChallengeType.DAILY_GOAL)
        total = len(challenges)  # Simplified for now
        
        return ChallengeListResponse(
            items=challenges,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit if total > 0 else 0
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/challenges/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(
    challenge_id: int = Path(..., gt=0, description="Challenge ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific challenge by ID
    
    This endpoint retrieves detailed information about a specific challenge.
    
    **Path Parameters:**
    - `challenge_id`: The unique identifier of the challenge
    
    **Returns:** Detailed challenge information
    """
    try:
        challenge = ChallengeService.get_challenge_by_id(db, challenge_id)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")
        return challenge
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}/challenges", response_model=UserChallengeListResponse)
def get_user_challenges(
    user_id: int = Path(..., gt=0, description="User ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get challenges for a specific user
    
    This endpoint retrieves all challenges for a specific user.
    
    **Features:**
    - View user's challenge participation
    - See challenge progress and completion status
    - Pagination support
    
    **Path Parameters:**
    - `user_id`: The unique identifier of the user
    
    **Returns:** List of user's challenges
    """
    try:
        # Users can only view their own challenges
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        user_challenges = ChallengeService.get_user_challenges(db, user_id, skip=skip, limit=limit)
        total = len(user_challenges)  # Simplified for now
        
        return UserChallengeListResponse(
            items=user_challenges,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit if total > 0 else 0
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/challenges/{challenge_id}/start", response_model=UserChallengeResponse, status_code=201)
def start_challenge(
    challenge_id: int = Path(..., gt=0, description="Challenge ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start a challenge
    
    This endpoint allows users to start participating in a challenge.
    
    **Features:**
    - Start challenge participation
    - Initialize progress tracking
    - Prevents duplicate challenge starts
    
    **Path Parameters:**
    - `challenge_id`: The unique identifier of the challenge to start
    
    **Returns:** The started user challenge
    """
    try:
        user_challenge = ChallengeService.start_challenge(db, current_user.id, challenge_id)
        return user_challenge
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/challenges/{challenge_id}/complete", response_model=UserChallengeResponse)
def complete_challenge(
    challenge_id: int = Path(..., gt=0, description="Challenge ID"),
    progress_data: Dict[str, Any] = Body(..., description="Progress data for challenge completion"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Complete a challenge
    
    This endpoint allows users to submit progress and complete challenges.
    
    **Features:**
    - Submit challenge progress
    - Automatic completion detection
    - Award points and badges upon completion
    
    **Path Parameters:**
    - `challenge_id`: The unique identifier of the challenge
    
    **Returns:** Updated user challenge with completion status
    """
    try:
        user_challenge = ChallengeService.update_challenge_progress(
            db, current_user.id, challenge_id, progress_data
        )
        return user_challenge
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
