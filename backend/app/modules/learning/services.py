"""
Learning services for study sessions and advanced study modes
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import re
from difflib import SequenceMatcher

from app.modules.flashcards.models import Flashcard, FlashcardSet, StudySession, StudyAttempt
from app.modules.flashcards.schemas import (
    StudySessionCreate, StudySessionUpdate, StudyAttemptCreate,
    WriteModeAnswer, WriteModeAnswerResponse, WriteModeProgress,
    SpellModeAnswer, SpellModeAnswerResponse, SpellModeProgress,
    TestSessionCreate, TestSessionResponse, TestResult, TestQuestion,
    QuestionType, StudyMode
)


class StudySessionService:
    """Service for managing study sessions"""
    
    @staticmethod
    def create_study_session(
        db: Session, 
        user_id: int, 
        session_data: StudySessionCreate
    ) -> StudySession:
        """Create a new study session"""
        study_session = StudySession(
            user_id=user_id,
            set_id=session_data.set_id,
            study_mode=session_data.study_mode.value,
            duration_seconds=session_data.duration_minutes * 60 if session_data.duration_minutes else None,
            start_time=datetime.utcnow()
        )
        
        db.add(study_session)
        db.commit()
        db.refresh(study_session)
        return study_session
    
    @staticmethod
    def get_user_study_sessions(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        set_id: Optional[int] = None,
        study_mode: Optional[str] = None
    ) -> List[StudySession]:
        """Get user's study sessions with optional filtering"""
        query = db.query(StudySession).filter(StudySession.user_id == user_id)
        
        if set_id:
            query = query.filter(StudySession.set_id == set_id)
        
        if study_mode:
            query = query.filter(StudySession.study_mode == study_mode)
        
        return query.order_by(StudySession.start_time.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_study_session_by_id(
        db: Session, 
        session_id: int, 
        user_id: int
    ) -> Optional[StudySession]:
        """Get a specific study session by ID"""
        return db.query(StudySession).filter(
            and_(
                StudySession.id == session_id,
                StudySession.user_id == user_id
            )
        ).first()
    
    @staticmethod
    def update_study_session(
        db: Session,
        session_id: int,
        user_id: int,
        update_data: StudySessionUpdate
    ) -> StudySession:
        """Update a study session"""
        study_session = StudySessionService.get_study_session_by_id(db, session_id, user_id)
        if not study_session:
            raise ValueError("Study session not found")
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(study_session, field, value)
        
        # Calculate accuracy if we have the data
        if (update_data.total_cards_studied and 
            update_data.correct_answers is not None and 
            update_data.incorrect_answers is not None):
            
            total_answers = update_data.correct_answers + update_data.incorrect_answers
            if total_answers > 0:
                study_session.accuracy_percentage = (
                    update_data.correct_answers / total_answers * 100
                )
        
        study_session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(study_session)
        return study_session


class StudyAttemptService:
    """Service for managing study attempts"""
    
    @staticmethod
    def create_study_attempt(
        db: Session,
        user_id: int,
        attempt_data: StudyAttemptCreate
    ) -> StudyAttempt:
        """Create a new study attempt"""
        study_attempt = StudyAttempt(
            user_id=user_id,
            card_id=attempt_data.card_id,
            session_id=attempt_data.session_id,
            user_answer=attempt_data.user_answer,
            is_correct=attempt_data.is_correct,
            response_time_seconds=attempt_data.response_time_seconds
        )
        
        db.add(study_attempt)
        db.commit()
        db.refresh(study_attempt)
        return study_attempt
    
    @staticmethod
    def get_session_attempts(
        db: Session,
        session_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[StudyAttempt]:
        """Get all attempts for a study session"""
        return db.query(StudyAttempt).filter(
            and_(
                StudyAttempt.session_id == session_id,
                StudyAttempt.user_id == user_id
            )
        ).order_by(StudyAttempt.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_study_attempt_by_id(
        db: Session,
        attempt_id: int,
        user_id: int
    ) -> Optional[StudyAttempt]:
        """Get a specific study attempt by ID"""
        return db.query(StudyAttempt).filter(
            and_(
                StudyAttempt.id == attempt_id,
                StudyAttempt.user_id == user_id
            )
        ).first()


class WriteModeService:
    """Service for Write Mode study sessions"""
    
    @staticmethod
    def submit_write_answer(
        db: Session,
        user_id: int,
        answer_data: WriteModeAnswer
    ) -> WriteModeAnswerResponse:
        """Submit a write mode answer and get feedback"""
        # Get the flashcard
        flashcard = db.query(Flashcard).filter(Flashcard.id == answer_data.card_id).first()
        if not flashcard:
            raise ValueError("Flashcard not found")
        
        # Calculate accuracy using fuzzy matching
        accuracy_score = WriteModeService._calculate_accuracy(
            answer_data.user_answer, 
            flashcard.back_content
        )
        
        # Determine if answer is correct (threshold: 80% accuracy)
        is_correct = accuracy_score >= 0.8
        
        # Generate feedback and suggestions
        feedback, suggestions = WriteModeService._generate_feedback(
            answer_data.user_answer,
            flashcard.back_content,
            accuracy_score
        )
        
        # Create study attempt
        study_attempt = StudyAttemptService.create_study_attempt(
            db=db,
            user_id=user_id,
            attempt_data=StudyAttemptCreate(
                card_id=answer_data.card_id,
                session_id=answer_data.session_id,
                user_answer=answer_data.user_answer,
                is_correct=is_correct,
                response_time_seconds=answer_data.response_time_seconds
            )
        )
        
        return WriteModeAnswerResponse(
            card_id=answer_data.card_id,
            user_answer=answer_data.user_answer,
            correct_answer=flashcard.back_content,
            is_correct=is_correct,
            accuracy_score=accuracy_score,
            feedback=feedback,
            suggestions=suggestions,
            response_time_seconds=answer_data.response_time_seconds or 0.0,
            created_at=study_attempt.created_at
        )
    
    @staticmethod
    def get_write_progress(
        db: Session,
        session_id: int,
        user_id: int
    ) -> WriteModeProgress:
        """Get write mode progress for a session"""
        # Get session
        session = StudySessionService.get_study_session_by_id(db, session_id, user_id)
        if not session:
            raise ValueError("Study session not found")
        
        # Get total cards in set
        total_cards = db.query(Flashcard).filter(Flashcard.set_id == session.set_id).count()
        
        # Get attempts for this session
        attempts = StudyAttemptService.get_session_attempts(db, session_id, user_id, limit=1000)
        
        cards_answered = len(attempts)
        correct_answers = sum(1 for attempt in attempts if attempt.is_correct)
        accuracy_percentage = (correct_answers / cards_answered * 100) if cards_answered > 0 else 0
        
        # Calculate average response time
        response_times = [attempt.response_time_seconds for attempt in attempts if attempt.response_time_seconds]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return WriteModeProgress(
            session_id=session_id,
            total_cards=total_cards,
            cards_answered=cards_answered,
            correct_answers=correct_answers,
            accuracy_percentage=accuracy_percentage,
            average_response_time=average_response_time,
            time_remaining_seconds=None  # Could be calculated based on session duration
        )
    
    @staticmethod
    def _calculate_accuracy(user_answer: str, correct_answer: str) -> float:
        """Calculate accuracy between user answer and correct answer"""
        # Normalize strings for comparison
        user_norm = re.sub(r'[^\w\s]', '', user_answer.lower().strip())
        correct_norm = re.sub(r'[^\w\s]', '', correct_answer.lower().strip())
        
        # Use sequence matcher for fuzzy matching
        return SequenceMatcher(None, user_norm, correct_norm).ratio()
    
    @staticmethod
    def _generate_feedback(user_answer: str, correct_answer: str, accuracy: float) -> tuple[str, List[str]]:
        """Generate feedback and suggestions based on accuracy"""
        if accuracy >= 0.9:
            feedback = "Excellent! Your answer is very close to the correct answer."
            suggestions = []
        elif accuracy >= 0.8:
            feedback = "Good! Your answer is mostly correct."
            suggestions = ["Double-check spelling and punctuation"]
        elif accuracy >= 0.6:
            feedback = "Close! You're on the right track."
            suggestions = [
                "Check for missing words",
                "Verify spelling",
                "Make sure you included all key terms"
            ]
        else:
            feedback = "Not quite right. Let's review the correct answer."
            suggestions = [
                "Read the question carefully",
                "Focus on key vocabulary terms",
                "Practice with similar questions"
            ]
        
        return feedback, suggestions
