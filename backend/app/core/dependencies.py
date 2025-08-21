from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.modules.auth.models import User
from app.core.config import settings


class PaginationParams:
    """Pagination parameters for API endpoints"""
    
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(
            settings.DEFAULT_PAGE_SIZE, 
            ge=1, 
            le=settings.MAX_PAGE_SIZE,
            description="Page size"
        )
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size


class SearchParams:
    """Search parameters for API endpoints"""
    
    def __init__(
        self,
        search: Optional[str] = Query(None, description="Search term"),
        sort_by: Optional[str] = Query(None, description="Sort field"),
        sort_order: Optional[str] = Query(
            "asc", 
            regex="^(asc|desc)$",
            description="Sort order (asc or desc)"
        )
    ):
        self.search = search
        self.sort_by = sort_by
        self.sort_order = sort_order


def get_pagination_params() -> PaginationParams:
    """Get pagination parameters"""
    return PaginationParams()


def get_search_params() -> SearchParams:
    """Get search parameters"""
    return SearchParams()


def get_current_user_optional(
    current_user: Optional[User] = Depends(get_current_active_user)
) -> Optional[User]:
    """Get current user (optional - for endpoints that can work with or without auth)"""
    return current_user


def require_active_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require active user permissions"""
    return current_user


def require_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require superuser permissions"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser access required"
        )
    return current_user


def get_db_session() -> Generator[Session, None, None]:
    """Get database session"""
    return get_db()
