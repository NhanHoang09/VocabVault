"""
Flashcard services for business logic
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from fastapi import HTTPException, status

from app.modules.flashcards.models import FlashcardSet, Flashcard, StudySession, StudyAttempt
from app.modules.flashcards.schemas import (
    FlashcardSetCreate, FlashcardSetUpdate, FlashcardCreate, FlashcardUpdate,
    StudySessionCreate, StudySessionUpdate, StudyAttemptCreate,
    FlashcardSetFilter, FlashcardFilter, MasteryLevel, DifficultyLevel
)
from app.modules.auth.models import User
from app.core.exceptions import NotFoundError, AuthorizationError


class FlashcardSetService:
    """Service for flashcard set operations"""
    
    @staticmethod
    def create_flashcard_set(db: Session, user_id: int, set_data: FlashcardSetCreate) -> FlashcardSet:
        """Create a new flashcard set"""
        flashcard_set = FlashcardSet(
            user_id=user_id,
            title=set_data.title,
            description=set_data.description,
            category=set_data.category,
            tags=set_data.tags,
            is_public=set_data.is_public,
            is_featured=set_data.is_featured
        )
        db.add(flashcard_set)
        db.commit()
        db.refresh(flashcard_set)
        return flashcard_set
    
    @staticmethod
    def get_user_flashcard_sets(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[FlashcardSet]:
        """Get flashcard sets for a user with optional filtering"""
        query = db.query(FlashcardSet).filter(FlashcardSet.user_id == user_id)
        
        if search:
            query = query.filter(
                or_(
                    FlashcardSet.title.ilike(f"%{search}%"),
                    FlashcardSet.description.ilike(f"%{search}%")
                )
            )
        
        if category:
            query = query.filter(FlashcardSet.category == category)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_public_flashcard_sets(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[FlashcardSet]:
        """Get public flashcard sets"""
        query = db.query(FlashcardSet).filter(FlashcardSet.is_public == True)
        
        if search:
            query = query.filter(
                or_(
                    FlashcardSet.title.ilike(f"%{search}%"),
                    FlashcardSet.description.ilike(f"%{search}%")
                )
            )
        
        if category:
            query = query.filter(FlashcardSet.category == category)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_flashcard_set_by_id(db: Session, set_id: int, user_id: Optional[int] = None) -> FlashcardSet:
        """Get a flashcard set by ID with optional user ownership check"""
        query = db.query(FlashcardSet).filter(FlashcardSet.id == set_id)
        
        if user_id:
            # Check if user owns the set or if it's public
            query = query.filter(
                or_(
                    FlashcardSet.user_id == user_id,
                    FlashcardSet.is_public == True
                )
            )
        
        flashcard_set = query.first()
        if not flashcard_set:
            raise NotFoundError("Flashcard set", set_id)
        
        return flashcard_set
    
    @staticmethod
    def update_flashcard_set(
        db: Session, 
        set_id: int, 
        user_id: int, 
        update_data: FlashcardSetUpdate
    ) -> FlashcardSet:
        """Update a flashcard set"""
        flashcard_set = FlashcardSetService.get_flashcard_set_by_id(db, set_id, user_id)
        
        # Check ownership
        if flashcard_set.user_id != user_id:
            raise AuthorizationError("You can only update your own flashcard sets")
        
        # Update fields
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(flashcard_set, field, value)
        
        db.commit()
        db.refresh(flashcard_set)
        return flashcard_set
    
    @staticmethod
    def delete_flashcard_set(db: Session, set_id: int, user_id: int) -> bool:
        """Delete a flashcard set"""
        flashcard_set = FlashcardSetService.get_flashcard_set_by_id(db, set_id, user_id)
        
        # Check ownership
        if flashcard_set.user_id != user_id:
            raise AuthorizationError("You can only delete your own flashcard sets")
        
        db.delete(flashcard_set)
        db.commit()
        return True
    
    @staticmethod
    def get_flashcard_set_with_cards(db: Session, set_id: int, user_id: Optional[int] = None) -> FlashcardSet:
        """Get a flashcard set with all its cards"""
        flashcard_set = FlashcardSetService.get_flashcard_set_by_id(db, set_id, user_id)
        # Cards will be loaded via relationship
        return flashcard_set


class FlashcardService:
    """Service for flashcard operations"""
    
    @staticmethod
    def create_flashcard(
        db: Session, 
        set_id: int, 
        user_id: int, 
        card_data: FlashcardCreate
    ) -> Flashcard:
        """Create a new flashcard in a set"""
        # Verify set ownership
        flashcard_set = FlashcardSetService.get_flashcard_set_by_id(db, set_id, user_id)
        if flashcard_set.user_id != user_id:
            raise AuthorizationError("You can only add cards to your own sets")
        
        flashcard = Flashcard(
            set_id=set_id,
            front_content=card_data.front_content,
            back_content=card_data.back_content,
            card_type=card_data.card_type,
            media_url=card_data.media_url,
            difficulty=card_data.difficulty,
            card_metadata=card_data.card_metadata
        )
        
        db.add(flashcard)
        db.commit()
        db.refresh(flashcard)
        
        # Update set total_cards count
        flashcard_set.total_cards = db.query(Flashcard).filter(Flashcard.set_id == set_id).count()
        db.commit()
        
        return flashcard
    
    @staticmethod
    def get_flashcards_in_set(
        db: Session, 
        set_id: int, 
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Flashcard]:
        """Get all flashcards in a set"""
        # Verify set access
        FlashcardSetService.get_flashcard_set_by_id(db, set_id, user_id)
        
        return db.query(Flashcard).filter(
            Flashcard.set_id == set_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_flashcard_by_id(db: Session, card_id: int, user_id: Optional[int] = None) -> Flashcard:
        """Get a flashcard by ID"""
        query = db.query(Flashcard).filter(Flashcard.id == card_id)
        flashcard = query.first()
        
        if not flashcard:
            raise NotFoundError("Flashcard", card_id)
        
        # Check access to the set
        if user_id:
            FlashcardSetService.get_flashcard_set_by_id(db, flashcard.set_id, user_id)
        
        return flashcard
    
    @staticmethod
    def update_flashcard(
        db: Session, 
        card_id: int, 
        user_id: int, 
        update_data: FlashcardUpdate
    ) -> Flashcard:
        """Update a flashcard"""
        flashcard = FlashcardService.get_flashcard_by_id(db, card_id, user_id)
        
        # Check set ownership
        flashcard_set = FlashcardSetService.get_flashcard_set_by_id(db, flashcard.set_id, user_id)
        if flashcard_set.user_id != user_id:
            raise AuthorizationError("You can only update cards in your own sets")
        
        # Update fields
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(flashcard, field, value)
        
        db.commit()
        db.refresh(flashcard)
        return flashcard
    
    @staticmethod
    def delete_flashcard(db: Session, card_id: int, user_id: int) -> bool:
        """Delete a flashcard"""
        flashcard = FlashcardService.get_flashcard_by_id(db, card_id, user_id)
        
        # Check set ownership
        flashcard_set = FlashcardSetService.get_flashcard_set_by_id(db, flashcard.set_id, user_id)
        if flashcard_set.user_id != user_id:
            raise AuthorizationError("You can only delete cards from your own sets")
        
        set_id = flashcard.set_id
        db.delete(flashcard)
        db.commit()
        
        # Update set total_cards count
        flashcard_set.total_cards = db.query(Flashcard).filter(Flashcard.set_id == set_id).count()
        db.commit()
        
        return True
