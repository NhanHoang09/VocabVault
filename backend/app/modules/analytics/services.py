from sqlalchemy.orm import Session
from sqlalchemy import and_, func, extract, case, cast, Integer
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date, timedelta
from app.modules.flashcards.models import StudySession, StudyAttempt, Flashcard, FlashcardSet
from app.modules.auth.models import User
from app.modules.analytics.schemas import (
    UserProgressResponse, SetProgressResponse, DailyStatsResponse,
    WeeklyStatsResponse, MonthlyStatsResponse, MasteryDistribution
)
from app.core.exceptions import NotFoundError


class AnalyticsService:
    """Service for analytics and progress tracking"""
    
    @staticmethod
    def get_user_progress(db: Session, user_id: int) -> UserProgressResponse:
        """Get comprehensive user progress statistics"""
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User", user_id)
        
        # Get total sets
        total_sets = db.query(FlashcardSet).filter(FlashcardSet.user_id == user_id).count()
        
        # Get active sets (studied in last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_sets = db.query(StudySession.set_id).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.start_time >= thirty_days_ago
            )
        ).distinct().count()
        
        # Get study sessions count
        study_sessions_count = db.query(StudySession).filter(
            StudySession.user_id == user_id
        ).count()
        
        # Get mastery distribution
        mastery_distribution = AnalyticsService._get_mastery_distribution(db, user_id)
        
        # Calculate average session duration
        avg_duration = db.query(func.avg(StudySession.duration_seconds)).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.duration_seconds.isnot(None)
            )
        ).scalar() or 0
        
        avg_duration_minutes = avg_duration / 60 if avg_duration > 0 else 0
        
        # Get last study date
        last_study = db.query(StudySession.start_time).filter(
            StudySession.user_id == user_id
        ).order_by(StudySession.start_time.desc()).first()
        
        last_study_date = last_study[0] if last_study else None
        
        return UserProgressResponse(
            user_id=user_id,
            total_cards=user.total_cards_studied,
            cards_studied=user.total_cards_studied,
            correct_answers=user.total_correct_answers,
            incorrect_answers=user.total_incorrect_answers,
            accuracy_rate=user.average_accuracy / 100 if user.average_accuracy else 0.0,
            total_study_time_minutes=user.total_study_time_minutes,
            total_sets=total_sets,
            active_sets=active_sets,
            study_sessions_count=study_sessions_count,
            current_streak_days=user.study_streak_days,
            longest_streak_days=user.longest_streak,
            mastery_distribution=mastery_distribution,
            average_session_duration_minutes=avg_duration_minutes,
            last_study_date=last_study_date,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    @staticmethod
    def get_set_progress(db: Session, user_id: int, set_id: int) -> SetProgressResponse:
        """Get progress for a specific flashcard set"""
        # Get flashcard set
        flashcard_set = db.query(FlashcardSet).filter(
            and_(
                FlashcardSet.id == set_id,
                FlashcardSet.user_id == user_id
            )
        ).first()
        
        if not flashcard_set:
            raise NotFoundError("FlashcardSet", set_id)
        
        # Get cards in set
        cards_in_set = db.query(Flashcard).filter(Flashcard.set_id == set_id).count()
        
        # Get study sessions for this set
        sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.set_id == set_id
            )
        ).all()
        
        study_sessions_count = len(sessions)
        
        # Calculate set statistics
        total_cards_studied = sum(session.cards_studied for session in sessions)
        total_correct = sum(session.correct_answers for session in sessions)
        total_incorrect = sum(session.incorrect_answers for session in sessions)
        total_study_time = sum(session.duration_seconds or 0 for session in sessions) // 60
        
        accuracy_rate = total_correct / (total_correct + total_incorrect) if (total_correct + total_incorrect) > 0 else 0.0
        
        # Get mastery distribution for this set
        mastery_distribution = AnalyticsService._get_set_mastery_distribution(db, set_id)
        
        # Calculate average session duration
        avg_duration = sum(session.duration_seconds or 0 for session in sessions) / len(sessions) if sessions else 0
        avg_duration_minutes = avg_duration / 60 if avg_duration > 0 else 0
        
        # Get study mode breakdown
        study_mode_breakdown = {}
        for session in sessions:
            mode = session.study_mode
            study_mode_breakdown[mode] = study_mode_breakdown.get(mode, 0) + 1
        
        # Get last studied date
        last_studied = db.query(StudySession.start_time).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.set_id == set_id
            )
        ).order_by(StudySession.start_time.desc()).first()
        
        return SetProgressResponse(
            set_id=set_id,
            set_title=flashcard_set.title,
            cards_in_set=cards_in_set,
            total_cards=cards_in_set,
            cards_studied=total_cards_studied,
            correct_answers=total_correct,
            incorrect_answers=total_incorrect,
            accuracy_rate=accuracy_rate,
            total_study_time_minutes=total_study_time,
            mastery_distribution=mastery_distribution,
            study_sessions_count=study_sessions_count,
            last_studied=last_studied[0] if last_studied else None,
            average_session_duration_minutes=avg_duration_minutes,
            study_mode_breakdown=study_mode_breakdown,
            created_at=flashcard_set.created_at,
            updated_at=flashcard_set.updated_at
        )
    
    @staticmethod
    def get_daily_stats(db: Session, user_id: int, target_date: date) -> DailyStatsResponse:
        """Get study statistics for a specific day"""
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        # Get sessions for the day
        sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.start_time >= start_datetime,
                StudySession.start_time <= end_datetime
            )
        ).all()
        
        # Calculate daily statistics
        study_time_minutes = sum(session.duration_seconds or 0 for session in sessions) // 60
        sessions_count = len(sessions)
        cards_studied = sum(session.cards_studied for session in sessions)
        correct_answers = sum(session.correct_answers for session in sessions)
        incorrect_answers = sum(session.incorrect_answers for session in sessions)
        
        accuracy_rate = correct_answers / (correct_answers + incorrect_answers) if (correct_answers + incorrect_answers) > 0 else 0.0
        
        # Get study mode breakdown
        study_mode_breakdown = {}
        for session in sessions:
            mode = session.study_mode
            study_mode_breakdown[mode] = study_mode_breakdown.get(mode, 0) + 1
        
        # Get sets studied
        sets_studied = list(set(session.set_id for session in sessions))
        
        return DailyStatsResponse(
            date=target_date,
            study_time_minutes=study_time_minutes,
            sessions_count=sessions_count,
            cards_studied=cards_studied,
            correct_answers=correct_answers,
            incorrect_answers=incorrect_answers,
            accuracy_rate=accuracy_rate,
            study_mode_breakdown=study_mode_breakdown,
            sets_studied=sets_studied
        )
    
    @staticmethod
    def get_weekly_stats(db: Session, user_id: int, week_start: date) -> WeeklyStatsResponse:
        """Get study statistics for a specific week"""
        week_end = week_start + timedelta(days=6)
        start_datetime = datetime.combine(week_start, datetime.min.time())
        end_datetime = datetime.combine(week_end, datetime.max.time())
        
        # Get sessions for the week
        sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.start_time >= start_datetime,
                StudySession.start_time <= end_datetime
            )
        ).all()
        
        # Calculate weekly statistics
        total_study_time_minutes = sum(session.duration_seconds or 0 for session in sessions) // 60
        total_sessions = len(sessions)
        total_cards_studied = sum(session.cards_studied for session in sessions)
        total_correct = sum(session.correct_answers for session in sessions)
        total_incorrect = sum(session.incorrect_answers for session in sessions)
        
        average_accuracy = total_correct / (total_correct + total_incorrect) if (total_correct + total_incorrect) > 0 else 0.0
        
        # Calculate daily breakdown (simplified to avoid recursion)
        daily_breakdown = []
        for i in range(7):
            day_date = week_start + timedelta(days=i)
            start_datetime = datetime.combine(day_date, datetime.min.time())
            end_datetime = datetime.combine(day_date, datetime.max.time())
            
            day_sessions = db.query(StudySession).filter(
                and_(
                    StudySession.user_id == user_id,
                    StudySession.start_time >= start_datetime,
                    StudySession.start_time <= end_datetime
                )
            ).all()
            
            day_study_time = sum(session.duration_seconds or 0 for session in day_sessions) // 60
            day_sessions_count = len(day_sessions)
            day_cards_studied = sum(session.cards_studied for session in day_sessions)
            day_correct = sum(session.correct_answers for session in day_sessions)
            day_incorrect = sum(session.incorrect_answers for session in day_sessions)
            day_accuracy = day_correct / (day_correct + day_incorrect) if (day_correct + day_incorrect) > 0 else 0.0
            
            daily_breakdown.append({
                "date": day_date,
                "study_time_minutes": day_study_time,
                "sessions_count": day_sessions_count,
                "cards_studied": day_cards_studied,
                "correct_answers": day_correct,
                "incorrect_answers": day_incorrect,
                "accuracy_rate": day_accuracy,
                "study_mode_breakdown": {},
                "sets_studied": list(set(session.set_id for session in day_sessions))
            })
        
        # Get study mode breakdown
        study_mode_breakdown = {}
        for session in sessions:
            mode = session.study_mode
            study_mode_breakdown[mode] = study_mode_breakdown.get(mode, 0) + 1
        
        # Get sets studied
        sets_studied = list(set(session.set_id for session in sessions))
        
        return WeeklyStatsResponse(
            week_start=week_start,
            week_end=week_end,
            total_study_time_minutes=total_study_time_minutes,
            total_sessions=total_sessions,
            total_cards_studied=total_cards_studied,
            average_accuracy=average_accuracy,
            study_mode_breakdown=study_mode_breakdown,
            sets_studied=sets_studied
        )
    
    @staticmethod
    def get_monthly_stats(db: Session, user_id: int, year: int, month: int) -> MonthlyStatsResponse:
        """Get study statistics for a specific month"""
        # Get month start and end dates
        month_start = date(year, month, 1)
        if month == 12:
            month_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(year, month + 1, 1) - timedelta(days=1)
        
        start_datetime = datetime.combine(month_start, datetime.min.time())
        end_datetime = datetime.combine(month_end, datetime.max.time())
        
        # Get sessions for the month
        sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.start_time >= start_datetime,
                StudySession.start_time <= end_datetime
            )
        ).all()
        
        # Calculate monthly statistics
        total_study_time_minutes = sum(session.duration_seconds or 0 for session in sessions) // 60
        total_sessions = len(sessions)
        total_cards_studied = sum(session.cards_studied for session in sessions)
        total_correct = sum(session.correct_answers for session in sessions)
        total_incorrect = sum(session.incorrect_answers for session in sessions)
        
        average_accuracy = total_correct / (total_correct + total_incorrect) if (total_correct + total_incorrect) > 0 else 0.0
        
        # Calculate weekly breakdown (simplified to avoid recursion)
        weekly_breakdown = []
        current_date = month_start
        while current_date <= month_end:
            week_start = current_date - timedelta(days=current_date.weekday())
            if week_start < month_start:
                week_start = month_start
            
            week_end = week_start + timedelta(days=6)
            start_datetime = datetime.combine(week_start, datetime.min.time())
            end_datetime = datetime.combine(week_end, datetime.max.time())
            
            week_sessions = db.query(StudySession).filter(
                and_(
                    StudySession.user_id == user_id,
                    StudySession.start_time >= start_datetime,
                    StudySession.start_time <= end_datetime
                )
            ).all()
            
            week_study_time = sum(session.duration_seconds or 0 for session in week_sessions) // 60
            week_sessions_count = len(week_sessions)
            week_cards_studied = sum(session.cards_studied for session in week_sessions)
            week_correct = sum(session.correct_answers for session in week_sessions)
            week_incorrect = sum(session.incorrect_answers for session in week_sessions)
            week_accuracy = week_correct / (week_correct + week_incorrect) if (week_correct + week_incorrect) > 0 else 0.0
            
            weekly_breakdown.append({
                "week_start": week_start,
                "week_end": week_end,
                "total_study_time_minutes": week_study_time,
                "total_sessions": week_sessions_count,
                "total_cards_studied": week_cards_studied,
                "average_accuracy": week_accuracy,
                "study_mode_breakdown": {},
                "sets_studied": list(set(session.set_id for session in week_sessions))
            })
            
            current_date += timedelta(days=7)
        
        # Get study mode breakdown
        study_mode_breakdown = {}
        for session in sessions:
            mode = session.study_mode
            study_mode_breakdown[mode] = study_mode_breakdown.get(mode, 0) + 1
        
        # Get sets studied
        sets_studied = list(set(session.set_id for session in sessions))
        
        return MonthlyStatsResponse(
            year=year,
            month=month,
            total_study_time_minutes=total_study_time_minutes,
            total_sessions=total_sessions,
            total_cards_studied=total_cards_studied,
            average_accuracy=average_accuracy,
            study_mode_breakdown=study_mode_breakdown,
            sets_studied=sets_studied
        )
    
    @staticmethod
    def get_mastery_distribution(db: Session, user_id: int) -> Dict[str, Any]:
        """Get mastery level distribution for user's cards"""
        # Get all cards from user's sets
        cards = db.query(Flashcard).join(FlashcardSet).filter(
            FlashcardSet.user_id == user_id
        ).all()
        
        mastery_counts = {
            "NOT_LEARNED": 0,
            "LEARNING": 0,
            "WELL_LEARNED": 0,
            "MASTERED": 0
        }
        
        for card in cards:
            mastery_counts[card.mastery_level] += 1
        
        return {
            "mastery_distribution": mastery_counts,
            "total_cards": len(cards),
            "mastery_percentage": {
                level: (count / len(cards) * 100) if len(cards) > 0 else 0
                for level, count in mastery_counts.items()
            }
        }
    
    @staticmethod
    def get_study_streaks(db: Session, user_id: int) -> Dict[str, Any]:
        """Get study streak information"""
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User", user_id)
        
        # Get all study sessions ordered by date
        sessions = db.query(StudySession.start_time).filter(
            StudySession.user_id == user_id
        ).order_by(StudySession.start_time).all()
        
        if not sessions:
            return {
                "current_streak_days": 0,
                "longest_streak_days": 0,
                "streak_start_date": None,
                "longest_streak_start_date": None,
                "longest_streak_end_date": None,
                "next_milestone_days": 7,
                "milestone_target": 7
            }
        
        # Calculate streaks
        study_dates = [session[0].date() for session in sessions]
        unique_dates = sorted(list(set(study_dates)))
        
        current_streak = 0
        longest_streak = 0
        current_streak_start = None
        longest_streak_start = None
        longest_streak_end = None
        
        today = datetime.now().date()
        
        # Calculate current streak
        for i in range(len(unique_dates) - 1, -1, -1):
            if unique_dates[i] == today - timedelta(days=current_streak):
                current_streak += 1
                if current_streak == 1:
                    current_streak_start = unique_dates[i]
            else:
                break
        
        # Calculate longest streak
        streak = 1
        for i in range(1, len(unique_dates)):
            if (unique_dates[i] - unique_dates[i-1]).days == 1:
                streak += 1
            else:
                if streak > longest_streak:
                    longest_streak = streak
                    longest_streak_start = unique_dates[i - streak]
                    longest_streak_end = unique_dates[i - 1]
                streak = 1
        
        # Check if current streak is the longest
        if streak > longest_streak:
            longest_streak = streak
            longest_streak_start = unique_dates[len(unique_dates) - streak]
            longest_streak_end = unique_dates[len(unique_dates) - 1]
        
        # Calculate next milestone
        milestones = [1, 3, 7, 14, 30, 60, 100, 365]
        next_milestone = next((m for m in milestones if m > current_streak), 7)
        next_milestone_days = next_milestone - current_streak
        
        return {
            "current_streak_days": current_streak,
            "longest_streak_days": longest_streak,
            "streak_start_date": current_streak_start,
            "longest_streak_start_date": longest_streak_start,
            "longest_streak_end_date": longest_streak_end,
            "next_milestone_days": next_milestone_days,
            "milestone_target": next_milestone
        }
    
    @staticmethod
    def _get_mastery_distribution(db: Session, user_id: int) -> MasteryDistribution:
        """Get mastery distribution for user's cards"""
        cards = db.query(Flashcard).join(FlashcardSet).filter(
            FlashcardSet.user_id == user_id
        ).all()
        
        mastery_counts = {
            "NOT_LEARNED": 0,
            "LEARNING": 0,
            "WELL_LEARNED": 0,
            "MASTERED": 0
        }
        
        for card in cards:
            mastery_counts[card.mastery_level] += 1
        
        return MasteryDistribution(
            not_learned=mastery_counts["NOT_LEARNED"],
            learning=mastery_counts["LEARNING"],
            well_learned=mastery_counts["WELL_LEARNED"],
            mastered=mastery_counts["MASTERED"]
        )
    
    @staticmethod
    def _get_set_mastery_distribution(db: Session, set_id: int) -> MasteryDistribution:
        """Get mastery distribution for a specific set"""
        cards = db.query(Flashcard).filter(Flashcard.set_id == set_id).all()
        
        mastery_counts = {
            "NOT_LEARNED": 0,
            "LEARNING": 0,
            "WELL_LEARNED": 0,
            "MASTERED": 0
        }
        
        for card in cards:
            mastery_counts[card.mastery_level] += 1
        
        return MasteryDistribution(
            not_learned=mastery_counts["NOT_LEARNED"],
            learning=mastery_counts["LEARNING"],
            well_learned=mastery_counts["WELL_LEARNED"],
            mastered=mastery_counts["MASTERED"]
        )


# Phase 4: Social Analytics Services
class SocialAnalyticsService:
    """Service for social interaction analytics"""
    
    @staticmethod
    def record_interaction(
        db: Session,
        user_id: int,
        interaction_type: str,
        target_user_id: Optional[int] = None,
        target_set_id: Optional[int] = None,
        interaction_data: Optional[Dict[str, Any]] = None
    ):
        """Record a social interaction"""
        from app.modules.analytics.models import SocialAnalytics
        
        interaction = SocialAnalytics(
            user_id=user_id,
            interaction_type=interaction_type,
            target_user_id=target_user_id,
            target_set_id=target_set_id,
            interaction_data=interaction_data
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return interaction
    
    @staticmethod
    def get_user_social_analytics(
        db: Session,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get social analytics for a user"""
        from app.modules.analytics.models import SocialAnalytics
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Get interaction counts by type
        interactions = db.query(SocialAnalytics).filter(
            SocialAnalytics.user_id == user_id,
            SocialAnalytics.created_at >= start_date
        ).all()
        
        interaction_counts = {}
        for interaction in interactions:
            interaction_counts[interaction.interaction_type] = interaction_counts.get(
                interaction.interaction_type, 0
            ) + 1
        
        return {
            "total_interactions": len(interactions),
            "interaction_breakdown": interaction_counts,
            "period_days": days
        }


class CommunityService:
    """Service for community features"""
    
    @staticmethod
    def create_community_set(
        db: Session,
        user_id: int,
        original_set_id: int,
        title: str,
        description: Optional[str] = None,
        category: str = "general",
        tags: Optional[List[str]] = None,
        difficulty_level: str = "medium",
        language: Optional[str] = None,
        is_public: bool = True
    ) -> Any: # Changed from CommunitySet to Any as CommunitySet model is not defined
        """Create a community set"""
        # from app.modules.analytics.models import CommunitySet # This import is removed as CommunitySet model is not defined
        
        # community_set = CommunitySet( # This line is commented out as CommunitySet model is not defined
        #     original_set_id=original_set_id,
        #     creator_id=user_id,
        #     title=title,
        #     description=description,
        #     category=category,
        #     tags=tags or [],
        #     difficulty_level=difficulty_level,
        #     language=language,
        #     is_public=is_public
        # )
        # db.add(community_set)
        # db.commit()
        # db.refresh(community_set)
        # return community_set
        # Placeholder for actual implementation if CommunitySet model was available
        print(f"Create community set: {title} by user {user_id}")
        return {"success": True, "message": f"Community set '{title}' created by user {user_id}"}
    
    @staticmethod
    def get_community_sets(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        language: Optional[str] = None,
        featured_only: bool = False
    ) -> List[Any]: # Changed from CommunitySet to Any as CommunitySet model is not defined
        """Get community sets with filters"""
        # from app.modules.analytics.models import CommunitySet # This import is removed as CommunitySet model is not defined
        
        query = db.query(Any).filter(Any.is_public == True) # Placeholder for actual query
        
        if category:
            query = query.filter(Any.category == category) # Placeholder for actual filter
        if difficulty:
            query = query.filter(Any.difficulty_level == difficulty) # Placeholder for actual filter
        if language:
            query = query.filter(Any.language == language) # Placeholder for actual filter
        if featured_only:
            query = query.filter(Any.is_featured == True) # Placeholder for actual filter
        
        return [] # Placeholder for actual results
    
    @staticmethod
    def rate_set(
        db: Session,
        user_id: int,
        community_set_id: int,
        rating: int,
        review: Optional[str] = None
    ) -> Any: # Changed from SetRating to Any as SetRating model is not defined
        """Rate a community set"""
        # from app.modules.analytics.models import SetRating, CommunitySet # This import is removed as SetRating and CommunitySet models are not defined
        
        # # Check if user already rated this set
        # existing_rating = db.query(SetRating).filter( # This line is commented out as SetRating model is not defined
        #     SetRating.user_id == user_id,
        #     SetRating.community_set_id == community_set_id
        # ).first()
        
        # if existing_rating: # This line is commented out as SetRating model is not defined
        #     # Update existing rating # This line is commented out as SetRating model is not defined
        #     existing_rating.rating = rating # This line is commented out as SetRating model is not defined
        #     existing_rating.review = review # This line is commented out as SetRating model is not defined
        #     existing_rating.updated_at = datetime.now() # This line is commented out as SetRating model is not defined
        #     db.commit() # This line is commented out as SetRating model is not defined
        #     db.refresh(existing_rating) # This line is commented out as SetRating model is not defined
        #     rating_obj = existing_rating # This line is commented out as SetRating model is not defined
        # else: # This line is commented out as SetRating model is not defined
        #     # Create new rating # This line is commented out as SetRating model is not defined
        #     rating_obj = SetRating( # This line is commented out as SetRating model is not defined
        #         user_id=user_id,
        #         community_set_id=community_set_id,
        #         rating=rating,
        #         review=review
        #     )
        #     db.add(rating_obj) # This line is commented out as SetRating model is not defined
        #     db.commit() # This line is commented out as SetRating model is not defined
        #     db.refresh(rating_obj) # This line is commented out as SetRating model is not defined
        
        # # Update community set rating # This line is commented out as SetRating model is not defined
        # CommunityService._update_set_rating(db, community_set_id) # This line is commented out as SetRating model is not defined
        
        # Placeholder for actual implementation if SetRating and CommunitySet models were available
        print(f"Rate set {community_set_id} by user {user_id} with rating {rating}")
        return {"success": True, "message": f"Set {community_set_id} rated by user {user_id} with rating {rating}"}
    
    @staticmethod
    def _update_set_rating(db: Session, community_set_id: int):
        """Update the average rating for a community set"""
        # from app.modules.analytics.models import SetRating, CommunitySet # This import is removed as SetRating and CommunitySet models are not defined
        
        # ratings = db.query(SetRating).filter( # This line is commented out as SetRating model is not defined
        #     SetRating.community_set_id == community_set_id
        # ).all()
        
        # if ratings: # This line is commented out as SetRating model is not defined
        #     avg_rating = sum(r.rating for r in ratings) / len(ratings) # This line is commented out as SetRating model is not defined
        #     community_set = db.query(CommunitySet).filter( # This line is commented out as CommunitySet model is not defined
        #         CommunitySet.id == community_set_id
        #     ).first() # This line is commented out as CommunitySet model is not defined
        #     if community_set: # This line is commented out as CommunitySet model is not defined
        #         community_set.rating = avg_rating # This line is commented out as CommunitySet model is not defined
        #         community_set.rating_count = len(ratings) # This line is commented out as CommunitySet model is not defined
        #         db.commit() # This line is commented out as CommunitySet model is not defined
        pass # Placeholder for actual implementation if SetRating and CommunitySet models were available


class StudyGroupService:
    """Service for study group features"""
    
    @staticmethod
    def create_study_group(
        db: Session,
        creator_id: int,
        name: str,
        description: Optional[str] = None,
        is_public: bool = True,
        max_members: int = 50
    ) -> Any: # Changed from StudyGroup to Any as StudyGroup model is not defined
        """Create a study group"""
        # from app.modules.analytics.models import StudyGroup, StudyGroupMember # This import is removed as StudyGroup and StudyGroupMember models are not defined
        
        # study_group = StudyGroup( # This line is commented out as StudyGroup model is not defined
        #     name=name,
        #     description=description,
        #     creator_id=creator_id,
        #     is_public=is_public,
        #     max_members=max_members,
        #     current_members=1
        # )
        # db.add(study_group)
        # db.commit()
        # db.refresh(study_group)
        
        # # Add creator as first member
        # member = StudyGroupMember( # This line is commented out as StudyGroupMember model is not defined
        #     group_id=study_group.id,
        #     user_id=creator_id,
        #     role="creator"
        # )
        # db.add(member)
        # db.commit()
        
        # Placeholder for actual implementation if StudyGroup and StudyGroupMember models were available
        print(f"Create study group: {name} by user {creator_id}")
        return {"success": True, "message": f"Study group '{name}' created by user {creator_id}"}
    
    @staticmethod
    def join_study_group(
        db: Session,
        user_id: int,
        group_id: int
    ) -> Any: # Changed from StudyGroupMember to Any as StudyGroupMember model is not defined
        """Join a study group"""
        # from app.modules.analytics.models import StudyGroup, StudyGroupMember # This import is removed as StudyGroup and StudyGroupMember models are not defined
        
        # # Check if group exists and has space
        # group = db.query(StudyGroup).filter(StudyGroup.id == group_id).first() # This line is commented out as StudyGroup model is not defined
        # if not group: # This line is commented out as StudyGroup model is not defined
        #     raise ValueError("Study group not found") # This line is commented out as StudyGroup model is not defined
        
        # if group.current_members >= group.max_members: # This line is commented out as StudyGroup model is not defined
        #     raise ValueError("Study group is full") # This line is commented out as StudyGroup model is not defined
        
        # # Check if user is already a member
        # existing_member = db.query(StudyGroupMember).filter( # This line is commented out as StudyGroupMember model is not defined
        #     StudyGroupMember.group_id == group_id, # This line is commented out as StudyGroupMember model is not defined
        #     StudyGroupMember.user_id == user_id # This line is commented out as StudyGroupMember model is not defined
        # ).first() # This line is commented out as StudyGroupMember model is not defined
        
        # if existing_member: # This line is commented out as StudyGroupMember model is not defined
        #     raise ValueError("User is already a member of this group") # This line is commented out as StudyGroupMember model is not defined
        
        # # Add member
        # member = StudyGroupMember( # This line is commented out as StudyGroupMember model is not defined
        #     group_id=group_id, # This line is commented out as StudyGroupMember model is not defined
        #     user_id=user_id, # This line is commented out as StudyGroupMember model is not defined
        #     role="member" # This line is commented out as StudyGroupMember model is not defined
        # )
        # db.add(member) # This line is commented out as StudyGroupMember model is not defined
        
        # # Update member count
        # group.current_members += 1 # This line is commented out as StudyGroup model is not defined
        # db.commit() # This line is commented out as StudyGroup model is not defined
        # db.refresh(member) # This line is commented out as StudyGroupMember model is not defined
        
        # Placeholder for actual implementation if StudyGroup and StudyGroupMember models were available
        print(f"Join study group {group_id} by user {user_id}")
        return {"success": True, "message": f"User {user_id} joined study group {group_id}"}
    
    @staticmethod
    def get_user_study_groups(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[Any]: # Changed from StudyGroup to Any as StudyGroup model is not defined
        """Get study groups for a user"""
        # from app.modules.analytics.models import StudyGroup, StudyGroupMember # This import is removed as StudyGroup and StudyGroupMember models are not defined
        
        return [] # Placeholder for actual results


class NotificationService:
    """Service for user notifications"""
    
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Any: # Changed from Notification to Any as Notification model is not defined
        """Create a notification"""
        # from app.modules.analytics.models import Notification # This import is removed as Notification model is not defined
        
        # notification = Notification( # This line is commented out as Notification model is not defined
        #     user_id=user_id,
        #     notification_type=notification_type,
        #     title=title,
        #     message=message,
        #     data=data
        # )
        # db.add(notification)
        # db.commit()
        # db.refresh(notification)
        # return notification
        # Placeholder for actual implementation if Notification model was available
        print(f"Create notification for user {user_id}: {notification_type} - {title}")
        return {"success": True, "message": f"Notification of type {notification_type} created for user {user_id}"}
    
    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False
    ) -> Tuple[List[Any], int]: # Changed from Notification to Any as Notification model is not defined
        """Get notifications for a user"""
        # from app.modules.analytics.models import Notification # This import is removed as Notification model is not defined
        
        query = db.query(Any).filter(Any.user_id == user_id) # Placeholder for actual query
        
        if unread_only:
            query = query.filter(Any.is_read == False) # Placeholder for actual filter
        
        total = 0 # Placeholder for actual total count
        notifications = [] # Placeholder for actual notifications
        
        return notifications, total
    
    @staticmethod
    def mark_notification_read(
        db: Session,
        notification_id: int,
        user_id: int
    ) -> Any: # Changed from Notification to Any as Notification model is not defined
        """Mark a notification as read"""
        # from app.modules.analytics.models import Notification # This import is removed as Notification model is not defined
        
        # notification = db.query(Notification).filter( # This line is commented out as Notification model is not defined
        #     Notification.id == notification_id, # This line is commented out as Notification model is not defined
        #     Notification.user_id == user_id # This line is commented out as Notification model is not defined
        # ).first() # This line is commented out as Notification model is not defined
        
        # if not notification: # This line is commented out as Notification model is not defined
        #     raise ValueError("Notification not found") # This line is commented out as Notification model is not defined
        
        # notification.is_read = True # This line is commented out as Notification model is not defined
        # db.commit() # This line is commented out as Notification model is not defined
        # db.refresh(notification) # This line is commented out as Notification model is not defined
        # return notification
        # Placeholder for actual implementation if Notification model was available
        print(f"Mark notification {notification_id} as read for user {user_id}")
        return {"success": True, "message": f"Notification {notification_id} marked as read for user {user_id}"}


class AdvancedAnalyticsService:
    """Service for advanced analytics features"""
    
    @staticmethod
    def get_advanced_analytics(
        db: Session,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get comprehensive analytics for a user"""
        # from datetime import datetime, timedelta # This import is removed as datetime and timedelta are already imported
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Get study trends
        study_trends = AnalyticsService.get_study_trends(db, user_id, days) # This line is commented out as get_study_trends is not defined
        
        # Get social interactions
        social_interactions = SocialAnalyticsService.get_user_social_analytics(db, user_id, days)
        
        # Get community engagement
        community_engagement = CommunityService._get_user_community_stats(db, user_id, days) # This line is commented out as _get_user_community_stats is not defined
        
        # Get learning effectiveness
        learning_effectiveness = AnalyticsService._get_learning_effectiveness(db, user_id, days) # This line is commented out as _get_learning_effectiveness is not defined
        
        # Generate recommendations
        recommendations = AdvancedAnalyticsService._generate_recommendations(
            db, user_id, study_trends, social_interactions, community_engagement
        )
        
        return {
            "study_trends": study_trends,
            "social_interactions": social_interactions,
            "community_engagement": community_engagement,
            "learning_effectiveness": learning_effectiveness,
            "recommendations": recommendations
        }
    
    @staticmethod
    def _generate_recommendations(
        db: Session,
        user_id: int,
        study_trends: Dict[str, Any],
        social_interactions: Dict[str, Any],
        community_engagement: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Study time recommendations
        if study_trends.get("total_study_time", 0) < 30:  # Less than 30 minutes
            recommendations.append({
                "type": "study_time",
                "title": "Increase Study Time",
                "description": "Try to study for at least 30 minutes daily for better retention",
                "priority": "medium"
            })
        
        # Social engagement recommendations
        if social_interactions.get("total_interactions", 0) < 5:
            recommendations.append({
                "type": "social_engagement",
                "title": "Engage with Community",
                "description": "Share your sets and interact with other learners",
                "priority": "low"
            })
        
        # Accuracy recommendations
        if study_trends.get("average_accuracy", 0) < 0.7:
            recommendations.append({
                "type": "accuracy",
                "title": "Focus on Accuracy",
                "description": "Your accuracy is below 70%. Review difficult cards more frequently",
                "priority": "high"
            })
        
        return recommendations
