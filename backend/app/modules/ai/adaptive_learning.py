"""
Adaptive Learning Service
AI-powered adaptive learning features including learning profiles and recommendations
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from app.core.config import settings
from app.modules.ai.models import LearningProfile, AdaptiveRecommendation
from app.modules.flashcards.models import StudySession, StudyAttempt
from app.modules.analytics.models import UserAnalytics, StudyProgress
from app.core.exceptions import VocabularyVaultException

logger = logging.getLogger(__name__)


class AdaptiveLearningService:
    """Service for adaptive learning features"""
    
    @staticmethod
    def create_or_update_learning_profile(
        db: Session, 
        user_id: int,
        preferred_study_mode: str = "flashcards",
        preferred_difficulty: str = "adaptive",
        study_session_duration: int = 15,
        daily_study_goal: int = 50
    ) -> LearningProfile:
        """Create or update user's learning profile"""
        profile = db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
        
        if profile:
            # Update existing profile
            profile.preferred_study_mode = preferred_study_mode
            profile.preferred_difficulty = preferred_difficulty
            profile.study_session_duration = study_session_duration
            profile.daily_study_goal = daily_study_goal
        else:
            # Create new profile
            profile = LearningProfile(
                user_id=user_id,
                preferred_study_mode=preferred_study_mode,
                preferred_difficulty=preferred_difficulty,
                study_session_duration=study_session_duration,
                daily_study_goal=daily_study_goal
            )
            db.add(profile)
        
        db.commit()
        db.refresh(profile)
        return profile
    
    @staticmethod
    def get_learning_profile(db: Session, user_id: int) -> Optional[LearningProfile]:
        """Get user's learning profile"""
        return db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
    
    @staticmethod
    def analyze_learning_patterns(db: Session, user_id: int) -> Dict[str, Any]:
        """Analyze user's learning patterns and update profile"""
        # Get recent study data
        recent_attempts = db.query(StudyAttempt).filter(
            and_(
                StudyAttempt.user_id == user_id,
                StudyAttempt.created_at >= datetime.now() - timedelta(days=30)
            )
        ).all()
        
        if not recent_attempts:
            return {"message": "No recent study data available"}
        
        # Calculate metrics
        total_attempts = len(recent_attempts)
        correct_attempts = len([a for a in recent_attempts if a.is_correct])
        accuracy_rate = correct_attempts / total_attempts if total_attempts > 0 else 0
        
        # Calculate average response time
        response_times = [a.response_time_seconds for a in recent_attempts if a.response_time_seconds]
        average_response_time = sum(response_times) / len(response_times) if response_times else None
        
        # Analyze study modes
        recent_sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.start_time >= datetime.now() - timedelta(days=30)
            )
        ).all()
        
        mode_performance = {}
        for session in recent_sessions:
            mode = session.study_mode
            if mode not in mode_performance:
                mode_performance[mode] = {"sessions": 0, "total_accuracy": 0}
            mode_performance[mode]["sessions"] += 1
            mode_performance[mode]["total_accuracy"] += session.accuracy_rate or 0
        
        # Find best performing mode
        best_mode = "flashcards"  # default
        best_accuracy = 0
        for mode, data in mode_performance.items():
            if data["sessions"] > 0:
                avg_accuracy = data["total_accuracy"] / data["sessions"]
                if avg_accuracy > best_accuracy:
                    best_accuracy = avg_accuracy
                    best_mode = mode
        
        # Determine recommended difficulty
        if accuracy_rate >= 0.9:
            recommended_difficulty = "hard"
        elif accuracy_rate >= 0.7:
            recommended_difficulty = "medium"
        else:
            recommended_difficulty = "easy"
        
        # Calculate learning speed (cards per minute)
        total_study_time = sum(s.duration_seconds or 0 for s in recent_sessions)
        total_cards_studied = sum(s.cards_studied or 0 for s in recent_sessions)
        learning_speed = (total_cards_studied / (total_study_time / 60)) if total_study_time > 0 else None
        
        # Calculate retention rate (based on repeated attempts)
        retention_data = AdaptiveLearningService._calculate_retention_rate(db, user_id)
        
        # Update learning profile
        profile = db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
        
        if profile:
            profile.accuracy_rate = accuracy_rate
            profile.average_response_time = average_response_time
            profile.recommended_difficulty = recommended_difficulty
            profile.recommended_study_mode = best_mode
            profile.learning_speed = learning_speed
            profile.retention_rate = retention_data.get("retention_rate")
            db.commit()
        
        return {
            "accuracy_rate": accuracy_rate,
            "average_response_time": average_response_time,
            "recommended_difficulty": recommended_difficulty,
            "recommended_study_mode": best_mode,
            "learning_speed": learning_speed,
            "retention_rate": retention_data.get("retention_rate"),
            "mode_performance": mode_performance,
            "study_consistency": retention_data.get("study_consistency")
        }
    
    @staticmethod
    def _calculate_retention_rate(db: Session, user_id: int) -> Dict[str, Any]:
        """Calculate retention rate based on repeated card attempts"""
        # Get cards that have been attempted multiple times
        repeated_attempts = db.query(
            StudyAttempt.card_id,
            func.count(StudyAttempt.id).label('attempt_count'),
            func.avg(StudyAttempt.is_correct.cast(func.Integer)).label('avg_accuracy')
        ).filter(
            StudyAttempt.user_id == user_id
        ).group_by(StudyAttempt.card_id).having(
            func.count(StudyAttempt.id) > 1
        ).all()
        
        if not repeated_attempts:
            return {"retention_rate": None, "study_consistency": "low"}
        
        # Calculate retention rate
        total_accuracy = sum(attempt.avg_accuracy for attempt in repeated_attempts)
        retention_rate = total_accuracy / len(repeated_attempts) if repeated_attempts else 0
        
        # Determine study consistency
        avg_attempts = sum(attempt.attempt_count for attempt in repeated_attempts) / len(repeated_attempts)
        if avg_attempts >= 5:
            consistency = "high"
        elif avg_attempts >= 3:
            consistency = "medium"
        else:
            consistency = "low"
        
        return {
            "retention_rate": retention_rate,
            "study_consistency": consistency,
            "avg_attempts_per_card": avg_attempts
        }
    
    @staticmethod
    def generate_recommendations(db: Session, user_id: int) -> List[AdaptiveRecommendation]:
        """Generate personalized learning recommendations"""
        # Analyze current patterns
        analysis = AdaptiveLearningService.analyze_learning_patterns(db, user_id)
        
        recommendations = []
        
        # Check if user needs to adjust study mode
        profile = db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
        
        if profile and profile.recommended_study_mode != profile.preferred_study_mode:
            recommendation = AdaptiveRecommendation(
                user_id=user_id,
                recommendation_type="study_mode",
                title="Try a Different Study Mode",
                description=f"Based on your performance, you might benefit from using {profile.recommended_study_mode} mode instead of {profile.preferred_study_mode}.",
                priority=3,
                data={"recommended_mode": profile.recommended_study_mode}
            )
            recommendations.append(recommendation)
        
        # Check accuracy and suggest difficulty adjustment
        if analysis.get("accuracy_rate", 0) < 0.6:
            recommendation = AdaptiveRecommendation(
                user_id=user_id,
                recommendation_type="difficulty",
                title="Consider Easier Content",
                description="Your recent accuracy is below 60%. Try reviewing easier cards to build confidence.",
                priority=4,
                data={"current_accuracy": analysis.get("accuracy_rate")}
            )
            recommendations.append(recommendation)
        elif analysis.get("accuracy_rate", 0) > 0.9:
            recommendation = AdaptiveRecommendation(
                user_id=user_id,
                recommendation_type="difficulty",
                title="Ready for a Challenge",
                description="You're doing great! Consider trying more difficult content to keep learning.",
                priority=2,
                data={"current_accuracy": analysis.get("accuracy_rate")}
            )
            recommendations.append(recommendation)
        
        # Check study consistency
        recent_sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.start_time >= datetime.now() - timedelta(days=7)
            )
        ).count()
        
        if recent_sessions < 3:
            recommendation = AdaptiveRecommendation(
                user_id=user_id,
                recommendation_type="timing",
                title="Increase Study Frequency",
                description="You've studied less than 3 times this week. Regular practice helps retention.",
                priority=5,
                data={"sessions_this_week": recent_sessions}
            )
            recommendations.append(recommendation)
        
        # Check learning speed
        learning_speed = analysis.get("learning_speed")
        if learning_speed and learning_speed < 2:  # Less than 2 cards per minute
            recommendation = AdaptiveRecommendation(
                user_id=user_id,
                recommendation_type="timing",
                title="Take Your Time",
                description="You're learning at a slower pace. This is fine - focus on understanding rather than speed.",
                priority=2,
                data={"learning_speed": learning_speed}
            )
            recommendations.append(recommendation)
        
        # Check retention rate
        retention_rate = analysis.get("retention_rate")
        if retention_rate and retention_rate < 0.7:
            recommendation = AdaptiveRecommendation(
                user_id=user_id,
                recommendation_type="content",
                title="Review More Frequently",
                description="Your retention rate suggests you might benefit from more frequent reviews.",
                priority=3,
                data={"retention_rate": retention_rate}
            )
            recommendations.append(recommendation)
        
        # Save recommendations
        for rec in recommendations:
            db.add(rec)
        
        db.commit()
        
        return recommendations
    
    @staticmethod
    def get_user_recommendations(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[AdaptiveRecommendation]:
        """Get user's recommendations"""
        return db.query(AdaptiveRecommendation).filter(
            and_(
                AdaptiveRecommendation.user_id == user_id,
                AdaptiveRecommendation.is_applied == False,
                (AdaptiveRecommendation.expires_at.is_(None) | 
                 AdaptiveRecommendation.expires_at > datetime.now())
            )
        ).order_by(desc(AdaptiveRecommendation.priority), desc(AdaptiveRecommendation.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def mark_recommendation_applied(
        db: Session, 
        user_id: int, 
        recommendation_id: int
    ) -> AdaptiveRecommendation:
        """Mark a recommendation as applied"""
        recommendation = db.query(AdaptiveRecommendation).filter(
            and_(
                AdaptiveRecommendation.id == recommendation_id,
                AdaptiveRecommendation.user_id == user_id
            )
        ).first()
        
        if not recommendation:
            raise VocabularyVaultException(
                status_code=404,
                detail="Recommendation not found"
            )
        
        recommendation.is_applied = True
        db.commit()
        db.refresh(recommendation)
        
        return recommendation
    
    @staticmethod
    def get_learning_insights(db: Session, user_id: int) -> Dict[str, Any]:
        """Get comprehensive learning insights for the user"""
        # Get learning profile
        profile = db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
        
        if not profile:
            return {"message": "No learning profile found. Complete some study sessions first."}
        
        # Analyze patterns
        analysis = AdaptiveLearningService.analyze_learning_patterns(db, user_id)
        
        # Get recent progress
        recent_progress = db.query(StudyProgress).filter(
            and_(
                StudyProgress.user_id == user_id,
                StudyProgress.created_at >= datetime.now() - timedelta(days=30)
            )
        ).order_by(desc(StudyProgress.created_at)).limit(10).all()
        
        # Calculate trends
        if len(recent_progress) >= 2:
            first_accuracy = recent_progress[-1].accuracy_rate or 0
            last_accuracy = recent_progress[0].accuracy_rate or 0
            accuracy_trend = "improving" if last_accuracy > first_accuracy else "declining" if last_accuracy < first_accuracy else "stable"
        else:
            accuracy_trend = "insufficient_data"
        
        # Get study streak
        study_streak = AdaptiveLearningService._calculate_study_streak(db, user_id)
        
        return {
            "profile": {
                "preferred_study_mode": profile.preferred_study_mode,
                "preferred_difficulty": profile.preferred_difficulty,
                "study_session_duration": profile.study_session_duration,
                "daily_study_goal": profile.daily_study_goal
            },
            "performance": {
                "accuracy_rate": analysis.get("accuracy_rate"),
                "average_response_time": analysis.get("average_response_time"),
                "learning_speed": analysis.get("learning_speed"),
                "retention_rate": analysis.get("retention_rate"),
                "accuracy_trend": accuracy_trend
            },
            "recommendations": {
                "recommended_difficulty": analysis.get("recommended_difficulty"),
                "recommended_study_mode": analysis.get("recommended_study_mode")
            },
            "study_habits": {
                "study_streak": study_streak,
                "mode_performance": analysis.get("mode_performance"),
                "study_consistency": analysis.get("study_consistency")
            }
        }
    
    @staticmethod
    def _calculate_study_streak(db: Session, user_id: int) -> int:
        """Calculate current study streak in days"""
        # Get all study sessions for the user
        sessions = db.query(StudySession).filter(
            StudySession.user_id == user_id
        ).order_by(desc(StudySession.start_time)).all()
        
        if not sessions:
            return 0
        
        # Calculate streak
        current_date = datetime.now().date()
        streak = 0
        
        for i in range(30):  # Check last 30 days
            check_date = current_date - timedelta(days=i)
            has_study_session = any(
                session.start_time.date() == check_date 
                for session in sessions
            )
            
            if has_study_session:
                streak += 1
            else:
                break
        
        return streak
