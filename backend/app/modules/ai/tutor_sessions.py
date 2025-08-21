"""
AI Tutor Session Service
AI-powered guided study sessions with personalized learning plans
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from app.core.config import settings
from app.modules.ai.models import AITutorSession, LearningProfile
from app.modules.flashcards.models import FlashcardSet, Flashcard, StudySession, StudyAttempt
from app.core.exceptions import VocabularyVaultException

logger = logging.getLogger(__name__)


class AITutorSessionService:
    """Service for AI tutor sessions"""
    
    @staticmethod
    def create_tutor_session(
        db: Session,
        user_id: int,
        session_type: str,
        set_id: Optional[int] = None,
        difficulty_level: str = "medium",
        target_accuracy: float = 0.8
    ) -> AITutorSession:
        """Create a new AI tutor session"""
        session = AITutorSession(
            user_id=user_id,
            set_id=set_id,
            session_type=session_type,
            difficulty_level=difficulty_level,
            target_accuracy=target_accuracy
        )
        
        if set_id:
            # Get total cards in set
            total_cards = db.query(Flashcard).filter(Flashcard.set_id == set_id).count()
            session.total_cards = total_cards
        
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_tutor_session(
        db: Session, 
        session_id: int, 
        user_id: int
    ) -> Optional[AITutorSession]:
        """Get a tutor session by ID for a specific user"""
        return db.query(AITutorSession).filter(
            and_(
                AITutorSession.id == session_id,
                AITutorSession.user_id == user_id
            )
        ).first()
    
    @staticmethod
    def get_user_tutor_sessions(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[AITutorSession]:
        """Get all tutor sessions for a user"""
        return db.query(AITutorSession).filter(
            AITutorSession.user_id == user_id
        ).order_by(desc(AITutorSession.started_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_session_progress(
        db: Session,
        session_id: int,
        user_id: int,
        current_accuracy: Optional[float] = None,
        cards_studied: Optional[int] = None,
        is_completed: bool = False
    ) -> AITutorSession:
        """Update AI tutor session progress"""
        session = db.query(AITutorSession).filter(
            and_(
                AITutorSession.id == session_id,
                AITutorSession.user_id == user_id
            )
        ).first()
        
        if not session:
            raise VocabularyVaultException(
                status_code=404,
                detail="Tutor session not found"
            )
        
        if current_accuracy is not None:
            session.current_accuracy = current_accuracy
        if cards_studied is not None:
            session.cards_studied = cards_studied
        if is_completed:
            session.is_completed = True
            session.completed_at = datetime.now()
        
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_guided_study_plan(
        db: Session,
        session_id: int,
        user_id: int
    ) -> Dict[str, Any]:
        """Get a guided study plan for an AI tutor session"""
        session = db.query(AITutorSession).filter(
            and_(
                AITutorSession.id == session_id,
                AITutorSession.user_id == user_id
            )
        ).first()
        
        if not session:
            raise VocabularyVaultException(
                status_code=404,
                detail="Tutor session not found"
            )
        
        # Get user's learning profile
        profile = db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
        
        # Generate study plan based on session type
        if session.session_type == "guided_study":
            plan = AITutorSessionService._create_guided_study_plan(session, profile)
        elif session.session_type == "review":
            plan = AITutorSessionService._create_review_plan(session, profile)
        elif session.session_type == "practice":
            plan = AITutorSessionService._create_practice_plan(session, profile)
        else:
            plan = AITutorSessionService._create_assessment_plan(session, profile)
        
        return plan
    
    @staticmethod
    def _create_guided_study_plan(session: AITutorSession, profile: Optional[LearningProfile]) -> Dict[str, Any]:
        """Create a guided study plan"""
        return {
            "session_type": "guided_study",
            "target_accuracy": session.target_accuracy,
            "difficulty_level": session.difficulty_level,
            "phases": [
                {
                    "phase": "introduction",
                    "description": "Let's start with an overview of what we'll learn today",
                    "duration_minutes": 2,
                    "mode": "flashcards",
                    "objectives": ["Familiarize with new concepts", "Set learning goals"]
                },
                {
                    "phase": "learning",
                    "description": "Focus on understanding new concepts",
                    "duration_minutes": 10,
                    "mode": "learn",
                    "objectives": ["Learn new vocabulary", "Understand definitions"]
                },
                {
                    "phase": "practice",
                    "description": "Practice what you've learned",
                    "duration_minutes": 8,
                    "mode": "write",
                    "objectives": ["Apply knowledge", "Build confidence"]
                },
                {
                    "phase": "review",
                    "description": "Review and reinforce learning",
                    "duration_minutes": 5,
                    "mode": "flashcards",
                    "objectives": ["Reinforce memory", "Check understanding"]
                }
            ],
            "tips": [
                "Take your time to understand each concept",
                "Don't worry about making mistakes - they help you learn",
                "Ask for explanations if something isn't clear",
                "Take short breaks between phases if needed"
            ],
            "success_criteria": f"Achieve {session.target_accuracy * 100}% accuracy and complete all phases"
        }
    
    @staticmethod
    def _create_review_plan(session: AITutorSession, profile: Optional[LearningProfile]) -> Dict[str, Any]:
        """Create a review plan"""
        return {
            "session_type": "review",
            "target_accuracy": session.target_accuracy,
            "difficulty_level": session.difficulty_level,
            "phases": [
                {
                    "phase": "warmup",
                    "description": "Start with familiar cards to build confidence",
                    "duration_minutes": 3,
                    "mode": "flashcards",
                    "objectives": ["Build confidence", "Warm up memory"]
                },
                {
                    "phase": "review",
                    "description": "Review cards that need reinforcement",
                    "duration_minutes": 12,
                    "mode": "spell",
                    "objectives": ["Reinforce difficult concepts", "Improve retention"]
                },
                {
                    "phase": "test",
                    "description": "Test your knowledge",
                    "duration_minutes": 10,
                    "mode": "test",
                    "objectives": ["Assess understanding", "Identify weak areas"]
                }
            ],
            "tips": [
                "Focus on cards you've struggled with before",
                "Use different study modes to reinforce learning",
                "Take breaks if you need them",
                "Review incorrect answers carefully"
            ],
            "success_criteria": f"Maintain {session.target_accuracy * 100}% accuracy across all phases"
        }
    
    @staticmethod
    def _create_practice_plan(session: AITutorSession, profile: Optional[LearningProfile]) -> Dict[str, Any]:
        """Create a practice plan"""
        return {
            "session_type": "practice",
            "target_accuracy": session.target_accuracy,
            "difficulty_level": session.difficulty_level,
            "phases": [
                {
                    "phase": "practice",
                    "description": "Practice with various study modes",
                    "duration_minutes": 15,
                    "mode": "mixed",
                    "objectives": ["Improve skills", "Build confidence"]
                },
                {
                    "phase": "assessment",
                    "description": "Quick assessment of your progress",
                    "duration_minutes": 10,
                    "mode": "test",
                    "objectives": ["Measure progress", "Identify areas for improvement"]
                }
            ],
            "tips": [
                "Try different study modes to find what works best",
                "Focus on accuracy over speed",
                "Review incorrect answers carefully",
                "Celebrate your progress"
            ],
            "success_criteria": f"Complete practice session and achieve {session.target_accuracy * 100}% accuracy"
        }
    
    @staticmethod
    def _create_assessment_plan(session: AITutorSession, profile: Optional[LearningProfile]) -> Dict[str, Any]:
        """Create an assessment plan"""
        return {
            "session_type": "assessment",
            "target_accuracy": session.target_accuracy,
            "difficulty_level": session.difficulty_level,
            "phases": [
                {
                    "phase": "assessment",
                    "description": "Comprehensive assessment of your knowledge",
                    "duration_minutes": 20,
                    "mode": "test",
                    "objectives": ["Evaluate knowledge", "Measure progress"]
                },
                {
                    "phase": "review",
                    "description": "Review your performance and areas for improvement",
                    "duration_minutes": 5,
                    "mode": "analysis",
                    "objectives": ["Understand results", "Plan next steps"]
                }
            ],
            "tips": [
                "Take your time and think carefully about each answer",
                "Don't rush - accuracy is more important than speed",
                "Use this assessment to identify areas for improvement",
                "Stay calm and focused throughout the assessment"
            ],
            "success_criteria": f"Complete assessment and review results thoroughly"
        }
    
    @staticmethod
    def get_session_recommendations(
        db: Session,
        user_id: int,
        set_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get personalized session recommendations"""
        # Get user's learning profile
        profile = db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
        
        if not profile:
            return {
                "recommended_session_type": "guided_study",
                "recommended_difficulty": "medium",
                "reason": "No learning profile available"
            }
        
        # Get recent performance
        recent_sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.start_time >= datetime.now() - timedelta(days=7)
            )
        ).all()
        
        if not recent_sessions:
            return {
                "recommended_session_type": "guided_study",
                "recommended_difficulty": "medium",
                "reason": "No recent study sessions"
            }
        
        # Calculate average accuracy
        avg_accuracy = sum(s.accuracy_rate or 0 for s in recent_sessions) / len(recent_sessions)
        
        # Determine recommended session type
        if avg_accuracy < 0.6:
            recommended_type = "guided_study"
            reason = "Low accuracy suggests need for guided learning"
        elif avg_accuracy < 0.8:
            recommended_type = "practice"
            reason = "Moderate accuracy - practice will help improve"
        else:
            recommended_type = "assessment"
            reason = "High accuracy - ready for assessment"
        
        # Determine recommended difficulty
        if avg_accuracy < 0.5:
            recommended_difficulty = "easy"
        elif avg_accuracy < 0.8:
            recommended_difficulty = "medium"
        else:
            recommended_difficulty = "hard"
        
        return {
            "recommended_session_type": recommended_type,
            "recommended_difficulty": recommended_difficulty,
            "reason": reason,
            "current_accuracy": avg_accuracy,
            "recent_sessions_count": len(recent_sessions)
        }
    
    @staticmethod
    def complete_session(
        db: Session,
        session_id: int,
        user_id: int,
        final_accuracy: float,
        total_cards_studied: int,
        session_data: Optional[Dict[str, Any]] = None
    ) -> AITutorSession:
        """Complete an AI tutor session"""
        session = AITutorSessionService.update_session_progress(
            db, session_id, user_id,
            current_accuracy=final_accuracy,
            cards_studied=total_cards_studied,
            is_completed=True
        )
        
        # Add session data if provided
        if session_data:
            session.session_data = session_data
            db.commit()
            db.refresh(session)
        
        return session
    
    @staticmethod
    def get_session_analytics(
        db: Session,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get analytics for tutor sessions"""
        # Get sessions in the specified time period
        sessions = db.query(AITutorSession).filter(
            and_(
                AITutorSession.user_id == user_id,
                AITutorSession.started_at >= datetime.now() - timedelta(days=days)
            )
        ).all()
        
        if not sessions:
            return {
                "total_sessions": 0,
                "completed_sessions": 0,
                "average_accuracy": 0,
                "session_types": {},
                "message": f"No tutor sessions in the last {days} days"
            }
        
        # Calculate metrics
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s.is_completed])
        completed_accuracies = [s.current_accuracy for s in sessions if s.is_completed and s.current_accuracy is not None]
        average_accuracy = sum(completed_accuracies) / len(completed_accuracies) if completed_accuracies else 0
        
        # Session types breakdown
        session_types = {}
        for session in sessions:
            session_type = session.session_type
            if session_type not in session_types:
                session_types[session_type] = {"count": 0, "completed": 0, "avg_accuracy": 0}
            session_types[session_type]["count"] += 1
            if session.is_completed:
                session_types[session_type]["completed"] += 1
                if session.current_accuracy is not None:
                    session_types[session_type]["avg_accuracy"] += session.current_accuracy
        
        # Calculate averages for session types
        for session_type in session_types:
            if session_types[session_type]["completed"] > 0:
                session_types[session_type]["avg_accuracy"] /= session_types[session_type]["completed"]
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "completion_rate": completed_sessions / total_sessions if total_sessions > 0 else 0,
            "average_accuracy": average_accuracy,
            "session_types": session_types,
            "period_days": days
        }
