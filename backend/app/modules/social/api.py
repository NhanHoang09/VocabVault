"""
Social Module API
API endpoints for social features, community sets, study groups, and notifications
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.modules.auth.models import User
from app.modules.analytics import schemas
from app.modules.analytics.services import (
    SocialAnalyticsService, CommunityService, StudyGroupService, 
    NotificationService, AdvancedAnalyticsService
)

router = APIRouter(
    prefix="/social",
    tags=["social"],
    responses={
        404: {"description": "Resource not found"},
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient permissions"},
        422: {"description": "Validation error"}
    }
)


# Community Sets Endpoints
@router.post(
    "/community-sets",
    response_model=schemas.CommunitySetResponse,
    summary="Create community set",
    description="Share a flashcard set with the community"
)
async def create_community_set(
    community_set: schemas.CommunitySetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a community set"""
    try:
        return CommunityService.create_community_set(
            db=db,
            user_id=current_user.id,
            original_set_id=community_set.original_set_id,
            title=community_set.title,
            description=community_set.description,
            category=community_set.category,
            tags=community_set.tags,
            difficulty_level=community_set.difficulty_level,
            language=community_set.language,
            is_public=community_set.is_public
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/community-sets",
    response_model=schemas.CommunitySetListResponse,
    summary="Get community sets",
    description="Browse community-shared flashcard sets"
)
async def get_community_sets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    language: Optional[str] = Query(None, description="Filter by language"),
    featured_only: bool = Query(False, description="Show only featured sets"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get community sets with filters"""
    try:
        sets = CommunityService.get_community_sets(
            db=db,
            skip=skip,
            limit=limit,
            category=category,
            difficulty=difficulty,
            language=language,
            featured_only=featured_only
        )
        total = len(sets)  # In a real app, you'd get total count separately
        
        return schemas.CommunitySetListResponse(
            sets=sets,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/community-sets/{set_id}/rate",
    response_model=schemas.SetRatingResponse,
    summary="Rate community set",
    description="Rate and review a community set"
)
async def rate_community_set(
    rating_data: schemas.SetRatingCreate,
    set_id: int = Path(..., gt=0, description="Community set ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Rate a community set"""
    try:
        return CommunityService.rate_set(
            db=db,
            user_id=current_user.id,
            community_set_id=set_id,
            rating=rating_data.rating,
            review=rating_data.review
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Study Groups Endpoints
@router.post(
    "/study-groups",
    response_model=schemas.StudyGroupResponse,
    summary="Create study group",
    description="Create a new study group"
)
async def create_study_group(
    group: schemas.StudyGroupCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a study group"""
    try:
        return StudyGroupService.create_study_group(
            db=db,
            creator_id=current_user.id,
            name=group.name,
            description=group.description,
            is_public=group.is_public,
            max_members=group.max_members
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/study-groups/{group_id}/join",
    response_model=schemas.StudyGroupMemberResponse,
    summary="Join study group",
    description="Join an existing study group"
)
async def join_study_group(
    group_id: int = Path(..., gt=0, description="Study group ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Join a study group"""
    try:
        return StudyGroupService.join_study_group(
            db=db,
            user_id=current_user.id,
            group_id=group_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/study-groups",
    response_model=schemas.StudyGroupListResponse,
    summary="Get user study groups",
    description="Get study groups for the current user"
)
async def get_user_study_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get study groups for the user"""
    try:
        groups = StudyGroupService.get_user_study_groups(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        total = len(groups)  # In a real app, you'd get total count separately
        
        return schemas.StudyGroupListResponse(
            groups=groups,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Notifications Endpoints
@router.get(
    "/notifications",
    response_model=schemas.NotificationListResponse,
    summary="Get user notifications",
    description="Get notifications for the current user"
)
async def get_user_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False, description="Show only unread notifications"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    try:
        notifications, total = NotificationService.get_user_notifications(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            unread_only=unread_only
        )
        
        # Get unread count
        unread_notifications, unread_count = NotificationService.get_user_notifications(
            db=db,
            user_id=current_user.id,
            unread_only=True
        )
        
        return schemas.NotificationListResponse(
            notifications=notifications,
            total=total,
            page=skip // limit + 1,
            size=limit,
            unread_count=unread_count
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/notifications/{notification_id}/read",
    response_model=schemas.NotificationResponse,
    summary="Mark notification as read",
    description="Mark a notification as read"
)
async def mark_notification_read(
    notification_id: int = Path(..., gt=0, description="Notification ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    try:
        return NotificationService.mark_notification_read(
            db=db,
            notification_id=notification_id,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Social Analytics Endpoints
@router.get(
    "/analytics",
    response_model=schemas.SocialInsightsResponse,
    summary="Get social insights",
    description="Get social interaction analytics for the user"
)
async def get_social_insights(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get social insights for the user"""
    try:
        social_analytics = SocialAnalyticsService.get_user_social_analytics(
            db=db,
            user_id=current_user.id,
            days=days
        )
        
        # Get community stats
        community_stats = CommunityService._get_user_community_stats(db, current_user.id, days)
        
        # Get group participation
        user_groups = StudyGroupService.get_user_study_groups(db, current_user.id)
        group_participation = len(user_groups)
        
        # Get recent activity (placeholder)
        recent_activity = []
        
        return schemas.SocialInsightsResponse(
            total_followers=0,  # Placeholder
            total_following=0,  # Placeholder
            sets_shared=community_stats.get("sets_shared", 0),
            sets_imported=community_stats.get("sets_imported", 0),
            community_rating=community_stats.get("average_rating", 0.0),
            group_participation=group_participation,
            recent_activity=recent_activity
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Advanced Analytics Endpoints
@router.get(
    "/advanced-analytics",
    response_model=schemas.AdvancedAnalyticsResponse,
    summary="Get advanced analytics",
    description="Get comprehensive analytics including social and community data"
)
async def get_advanced_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get advanced analytics for the user"""
    try:
        return AdvancedAnalyticsService.get_advanced_analytics(
            db=db,
            user_id=current_user.id,
            days=days
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
