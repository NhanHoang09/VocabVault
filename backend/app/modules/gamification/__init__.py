"""
Gamification Module

This module handles all gamification features including:
- Badge system
- Points and achievements
- Leaderboards
- Educational games (Match, Gravity)
- Game sessions and statistics
"""

from .models import *
from .schemas import *
from .services import *
from .api import router

__all__ = [
    # Models
    "Badge", "UserBadge", "PointsTransaction", "LeaderboardEntry",
    "GameSession", "MatchGame", "GravityGame",
    
    # Schemas
    "BadgeCreate", "BadgeResponse", "UserBadgeResponse",
    "PointsTransactionCreate", "PointsTransactionResponse",
    "LeaderboardEntryResponse", "LeaderboardResponse",
    "GameSessionCreate", "GameSessionResponse",
    "MatchGameCreate", "MatchGameResponse",
    "GravityGameCreate", "GravityGameResponse",
    
    # Services
    "BadgeService", "PointsService", "LeaderboardService",
    "GameSessionService", "MatchGameService", "GravityGameService",
    
    # API Router
    "router"
]
