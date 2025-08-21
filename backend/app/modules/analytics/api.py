from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_pagination_params
from app.modules.auth.models import User
from app.modules.analytics.schemas import (
    UserProgressResponse, SetProgressResponse,
    DailyStatsResponse, WeeklyStatsResponse, MonthlyStatsResponse, StreakInfo
)
from app.modules.analytics.services import AnalyticsService

router = APIRouter(
    prefix="/analytics", 
    tags=["analytics"],
    responses={
        404: {"description": "Resource not found"},
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient permissions"},
        422: {"description": "Validation error"}
    }
)


@router.get("/progress", response_model=UserProgressResponse)
def get_user_progress(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's overall learning progress
    
    This endpoint provides comprehensive progress statistics for the authenticated user.
    
    **Features:**
    - Overall study statistics
    - Mastery level distribution
    - Learning streak information
    - Performance trends
    
    **Returns:** Complete user progress overview
    """
    try:
        progress = AnalyticsService.get_user_progress(db, current_user.id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sets/{set_id}/progress", response_model=SetProgressResponse)
def get_set_progress(
    set_id: int = Path(..., gt=0, description="Flashcard set ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get progress for a specific flashcard set
    
    This endpoint provides detailed progress statistics for a specific flashcard set.
    
    **Features:**
    - Set-specific study statistics
    - Card mastery distribution
    - Study session history
    - Performance metrics
    
    **Path Parameters:**
    - `set_id`: The unique identifier of the flashcard set
    
    **Returns:** Detailed set progress information
    """
    try:
        progress = AnalyticsService.get_set_progress(db, current_user.id, set_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/stats/daily", response_model=DailyStatsResponse)
def get_daily_stats(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (default: today)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get daily study statistics
    
    This endpoint provides study statistics for a specific day.
    
    **Features:**
    - Daily study time
    - Cards studied
    - Accuracy rates
    - Study sessions count
    
    **Query Parameters:**
    - `date`: Date in YYYY-MM-DD format (default: today)
    
    **Returns:** Daily study statistics
    """
    try:
        if date:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            target_date = datetime.now().date()
        
        stats = AnalyticsService.get_daily_stats(db, current_user.id, target_date)
        return stats
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stats/weekly", response_model=WeeklyStatsResponse)
def get_weekly_stats(
    week_start: Optional[str] = Query(None, description="Week start date in YYYY-MM-DD format"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get weekly study statistics
    
    This endpoint provides study statistics for a specific week.
    
    **Features:**
    - Weekly study time
    - Daily breakdown
    - Progress trends
    - Achievement tracking
    
    **Query Parameters:**
    - `week_start`: Week start date in YYYY-MM-DD format (default: current week)
    
    **Returns:** Weekly study statistics with daily breakdown
    """
    try:
        if week_start:
            start_date = datetime.strptime(week_start, "%Y-%m-%d").date()
        else:
            # Get current week start (Monday)
            today = datetime.now().date()
            start_date = today - timedelta(days=today.weekday())
        
        stats = AnalyticsService.get_weekly_stats(db, current_user.id, start_date)
        return stats
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stats/monthly", response_model=MonthlyStatsResponse)
def get_monthly_stats(
    year: Optional[int] = Query(None, description="Year (default: current year)"),
    month: Optional[int] = Query(None, description="Month 1-12 (default: current month)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get monthly study statistics
    
    This endpoint provides study statistics for a specific month.
    
    **Features:**
    - Monthly study time
    - Weekly breakdown
    - Progress trends
    - Goal tracking
    
    **Query Parameters:**
    - `year`: Year (default: current year)
    - `month`: Month 1-12 (default: current month)
    
    **Returns:** Monthly study statistics with weekly breakdown
    """
    try:
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")
        
        stats = AnalyticsService.get_monthly_stats(db, current_user.id, year, month)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mastery", response_model=Dict[str, Any])
def get_mastery_distribution(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get mastery level distribution
    
    This endpoint provides the distribution of cards across different mastery levels.
    
    **Features:**
    - Mastery level breakdown
    - Progress visualization data
    - Learning efficiency metrics
    
    **Returns:** Mastery level distribution statistics
    """
    try:
        mastery_data = AnalyticsService.get_mastery_distribution(db, current_user.id)
        return mastery_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/streaks", response_model=Dict[str, Any])
def get_study_streaks(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get study streak information
    
    This endpoint provides information about the user's study streaks.
    
    **Features:**
    - Current streak
    - Longest streak
    - Streak history
    - Streak goals
    
    **Returns:** Study streak statistics
    """
    try:
        streak_data = AnalyticsService.get_study_streaks(db, current_user.id)
        return streak_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Additional endpoints for frontend compatibility
@router.get("/user", response_model=UserProgressResponse)
def get_user_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user analytics (alias for /progress)
    
    This endpoint provides comprehensive progress statistics for the authenticated user.
    
    **Features:**
    - Overall study statistics
    - Mastery level distribution
    - Learning streak information
    - Performance trends
    
    **Returns:** Complete user progress overview
    """
    try:
        progress = AnalyticsService.get_user_progress(db, current_user.id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/study", response_model=Dict[str, Any])
def get_study_analytics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get study analytics
    
    This endpoint provides comprehensive study analytics for the authenticated user.
    
    **Features:**
    - Study session statistics
    - Performance metrics
    - Learning patterns
    - Study recommendations
    
    **Returns:** Study analytics data
    """
    try:
        # Combine multiple analytics data
        progress = AnalyticsService.get_user_progress(db, current_user.id)
        mastery_data = AnalyticsService.get_mastery_distribution(db, current_user.id)
        streak_data = AnalyticsService.get_study_streaks(db, current_user.id)
        
        return {
            "progress": progress,
            "mastery": mastery_data,
            "streaks": streak_data,
            "study_sessions": {
                "total_sessions": 0,  # TODO: Implement
                "average_duration": 0,  # TODO: Implement
                "total_cards_studied": 0,  # TODO: Implement
                "average_accuracy": 0,  # TODO: Implement
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
