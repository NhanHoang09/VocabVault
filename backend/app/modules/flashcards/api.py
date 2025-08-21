from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_pagination_params
from app.modules.auth.models import User
from app.modules.flashcards.schemas import (
    FlashcardSetCreate, FlashcardSetUpdate, FlashcardSetResponse, FlashcardSetListResponse,
    FlashcardCreate, FlashcardUpdate, FlashcardResponse, FlashcardSetWithCards
)
from app.modules.flashcards.services import FlashcardSetService, FlashcardService

router = APIRouter(
    prefix="/flashcards", 
    tags=["flashcards"],
    responses={
        404: {"description": "Resource not found"},
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient permissions"},
        422: {"description": "Validation error"}
    }
)


# FlashcardSet Endpoints
@router.post("/sets", response_model=FlashcardSetResponse, status_code=201)
def create_flashcard_set(
    set_data: FlashcardSetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new flashcard set
    
    This endpoint allows authenticated users to create a new flashcard set.
    
    **Features:**
    - Create sets with title, description, category, and tags
    - Set visibility (public/private)
    - Mark sets as featured
    
    **Required fields:**
    - `title`: Set title (1-200 characters)
    - `description`: Optional description
    - `category`: Optional category for organization
    - `tags`: Optional list of tags for easy searching
    - `is_public`: Whether the set is publicly visible
    - `is_featured`: Whether to mark as featured
    
    **Returns:** The created flashcard set with all details
    """
    try:
        flashcard_set = FlashcardSetService.create_flashcard_set(
            db=db, 
            user_id=current_user.id, 
            set_data=set_data
        )
        return flashcard_set
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sets", response_model=FlashcardSetListResponse)
def get_user_flashcard_sets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for title or description"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Get current user's flashcard sets with optional filtering
    
    This endpoint retrieves all flashcard sets owned by the authenticated user.
    
    **Features:**
    - Pagination support (skip/limit)
    - Search functionality (title and description)
    - Category filtering
    - Returns paginated results with metadata
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum records to return (default: 100, max: 1000)
    - `search`: Search term for title or description
    - `category`: Filter by specific category
    
    **Returns:** Paginated list of flashcard sets with total count and pagination info
    """
    try:
        flashcard_sets = FlashcardSetService.get_user_flashcard_sets(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            search=search,
            category=category
        )
        
        # Get total count for pagination
        total = len(flashcard_sets)  # Simplified for now
        pages = (total + limit - 1) // limit if total > 0 else 0
        
        return FlashcardSetListResponse(
            items=flashcard_sets,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=pages
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sets/public", response_model=FlashcardSetListResponse)
def get_public_flashcard_sets(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search term for title or description"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Get public flashcard sets
    
    This endpoint retrieves all publicly available flashcard sets from the community.
    
    **Features:**
    - Browse community-created flashcard sets
    - Pagination support (skip/limit)
    - Search functionality (title and description)
    - Category filtering
    - No authentication required
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum records to return (default: 100, max: 1000)
    - `search`: Search term for title or description
    - `category`: Filter by specific category
    
    **Returns:** Paginated list of public flashcard sets with total count and pagination info
    """
    try:
        flashcard_sets = FlashcardSetService.get_public_flashcard_sets(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            category=category
        )
        
        # Get total count for pagination
        total = len(flashcard_sets)  # Simplified for now
        pages = (total + limit - 1) // limit if total > 0 else 0
        
        return FlashcardSetListResponse(
            items=flashcard_sets,
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=pages
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sets/{set_id}", response_model=FlashcardSetResponse)
def get_flashcard_set(
    set_id: int = Path(..., gt=0, description="Flashcard set ID"),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific flashcard set by ID
    
    This endpoint retrieves a specific flashcard set by its ID.
    
    **Access Control:**
    - Users can access their own sets
    - Users can access public sets
    - Private sets are only accessible to their owners
    
    **Path Parameters:**
    - `set_id`: The unique identifier of the flashcard set
    
    **Returns:** Flashcard set details without cards
    """
    try:
        flashcard_set = FlashcardSetService.get_flashcard_set_by_id(
            db=db, 
            set_id=set_id, 
            user_id=current_user.id if current_user else None
        )
        return flashcard_set
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/sets/{set_id}/with-cards", response_model=FlashcardSetWithCards)
def get_flashcard_set_with_cards(
    set_id: int = Path(..., gt=0, description="Flashcard set ID"),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a flashcard set with all its cards
    
    This endpoint retrieves a flashcard set along with all its cards in one request.
    
    **Features:**
    - Complete set information
    - All cards in the set
    - Card metadata and progress tracking
    - Perfect for study sessions
    
    **Access Control:**
    - Users can access their own sets
    - Users can access public sets
    - Private sets are only accessible to their owners
    
    **Path Parameters:**
    - `set_id`: The unique identifier of the flashcard set
    
    **Returns:** Flashcard set with all cards included
    """
    try:
        flashcard_set = FlashcardSetService.get_flashcard_set_with_cards(
            db=db, 
            set_id=set_id, 
            user_id=current_user.id if current_user else None
        )
        return flashcard_set
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/sets/{set_id}", response_model=FlashcardSetResponse)
def update_flashcard_set(
    set_data: FlashcardSetUpdate,
    set_id: int = Path(..., gt=0, description="Flashcard set ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a flashcard set
    
    This endpoint allows users to update their own flashcard sets.
    
    **Features:**
    - Update title, description, category, and tags
    - Change visibility settings (public/private)
    - Mark/unmark as featured
    - Partial updates supported (only send fields to update)
    
    **Access Control:**
    - Only set owners can update their sets
    
    **Path Parameters:**
    - `set_id`: The unique identifier of the flashcard set
    
    **Returns:** Updated flashcard set details
    """
    try:
        flashcard_set = FlashcardSetService.update_flashcard_set(
            db=db,
            set_id=set_id,
            user_id=current_user.id,
            update_data=set_data
        )
        return flashcard_set
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/sets/{set_id}", status_code=204)
def delete_flashcard_set(
    set_id: int = Path(..., gt=0, description="Flashcard set ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a flashcard set
    
    This endpoint allows users to permanently delete their own flashcard sets.
    
    **⚠️ Warning:**
    - This action is irreversible
    - All cards in the set will be deleted
    - Study progress will be lost
    
    **Access Control:**
    - Only set owners can delete their sets
    
    **Path Parameters:**
    - `set_id`: The unique identifier of the flashcard set
    
    **Returns:** 204 No Content on successful deletion
    """
    try:
        FlashcardSetService.delete_flashcard_set(
            db=db,
            set_id=set_id,
            user_id=current_user.id
        )
        return {"message": "Flashcard set deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Flashcard Endpoints
@router.post("/sets/{set_id}/cards", response_model=FlashcardResponse, status_code=201)
def create_flashcard(
    card_data: FlashcardCreate,
    set_id: int = Path(..., gt=0, description="Flashcard set ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new flashcard in a set
    
    This endpoint allows users to add new flashcards to their own sets.
    
    **Features:**
    - Create text, image, audio, or video cards
    - Set difficulty levels (easy, medium, hard)
    - Add custom metadata
    - Automatic card counting
    
    **Required fields:**
    - `front_content`: Question or prompt (1+ characters)
    - `back_content`: Answer or explanation (1+ characters)
    
    **Optional fields:**
    - `card_type`: Type of card (text, image, audio, video)
    - `media_url`: URL to media content
    - `difficulty`: Card difficulty (easy, medium, hard)
    - `card_metadata`: Additional metadata as JSON
    
    **Access Control:**
    - Only set owners can add cards to their sets
    
    **Path Parameters:**
    - `set_id`: The unique identifier of the flashcard set
    
    **Returns:** The created flashcard with all details
    """
    try:
        flashcard = FlashcardService.create_flashcard(
            db=db,
            set_id=set_id,
            user_id=current_user.id,
            card_data=card_data
        )
        return flashcard
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sets/{set_id}/cards", response_model=List[FlashcardResponse])
def get_flashcards_in_set(
    set_id: int = Path(..., gt=0, description="Flashcard set ID"),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get all flashcards in a set
    
    This endpoint retrieves all flashcards within a specific set.
    
    **Features:**
    - Pagination support for large sets
    - Card metadata and progress tracking
    - Mastery level information
    - Review statistics
    
    **Access Control:**
    - Users can access cards in their own sets
    - Users can access cards in public sets
    - Private sets are only accessible to their owners
    
    **Path Parameters:**
    - `set_id`: The unique identifier of the flashcard set
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum records to return (default: 100, max: 1000)
    
    **Returns:** List of flashcards with progress tracking data
    """
    try:
        flashcards = FlashcardService.get_flashcards_in_set(
            db=db,
            set_id=set_id,
            user_id=current_user.id if current_user else None,
            skip=skip,
            limit=limit
        )
        return flashcards
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/cards/{card_id}", response_model=FlashcardResponse)
def get_flashcard(
    card_id: int = Path(..., gt=0, description="Flashcard ID"),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific flashcard by ID
    
    This endpoint retrieves a specific flashcard by its unique ID.
    
    **Features:**
    - Complete card information
    - Progress tracking data
    - Mastery level and statistics
    - Media content URLs
    
    **Access Control:**
    - Users can access cards in their own sets
    - Users can access cards in public sets
    - Private sets are only accessible to their owners
    
    **Path Parameters:**
    - `card_id`: The unique identifier of the flashcard
    
    **Returns:** Complete flashcard details with progress tracking
    """
    try:
        flashcard = FlashcardService.get_flashcard_by_id(
            db=db,
            card_id=card_id,
            user_id=current_user.id if current_user else None
        )
        return flashcard
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/cards/{card_id}", response_model=FlashcardResponse)
def update_flashcard(
    card_data: FlashcardUpdate,
    card_id: int = Path(..., gt=0, description="Flashcard ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a flashcard
    
    This endpoint allows users to update flashcards in their own sets.
    
    **Features:**
    - Update front and back content
    - Change card type and media URLs
    - Modify difficulty levels
    - Update custom metadata
    - Partial updates supported
    
    **Access Control:**
    - Only set owners can update cards in their sets
    
    **Path Parameters:**
    - `card_id`: The unique identifier of the flashcard
    
    **Returns:** Updated flashcard details
    """
    try:
        flashcard = FlashcardService.update_flashcard(
            db=db,
            card_id=card_id,
            user_id=current_user.id,
            update_data=card_data
        )
        return flashcard
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/cards/{card_id}", status_code=204)
def delete_flashcard(
    card_id: int = Path(..., gt=0, description="Flashcard ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a flashcard
    
    This endpoint allows users to permanently delete flashcards from their own sets.
    
    **⚠️ Warning:**
    - This action is irreversible
    - Study progress for this card will be lost
    - Card count in the set will be updated automatically
    
    **Access Control:**
    - Only set owners can delete cards from their sets
    
    **Path Parameters:**
    - `card_id`: The unique identifier of the flashcard
    
    **Returns:** 204 No Content on successful deletion
    """
    try:
        FlashcardService.delete_flashcard(
            db=db,
            card_id=card_id,
            user_id=current_user.id
        )
        return {"message": "Flashcard deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
