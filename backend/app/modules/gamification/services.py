from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
from app.modules.gamification.models import (
    Badge, UserBadge, PointsTransaction, LeaderboardEntry,
    GameSession, MatchGame, GravityGame, SpeedChallenge, MemoryGame, 
    Challenge, UserChallenge, BadgeType, GameType, ChallengeType
)
from app.modules.gamification.schemas import (
    BadgeCreate, PointsTransactionCreate, GameSessionCreate,
    GameSessionUpdate, MatchGameCreate, MatchGameUpdate,
    GravityGameCreate, GravityGameUpdate,
    SpeedChallengeCreate, SpeedChallengeUpdate,
    MemoryGameCreate, MemoryGameUpdate
)
from app.modules.auth.models import User
from app.modules.flashcards.models import FlashcardSet, Flashcard
from app.core.exceptions import VocabularyVaultException

logger = logging.getLogger(__name__)


class BadgeService:
    """Service for managing badges and user achievements"""
    
    @staticmethod
    def get_all_badges(db: Session, skip: int = 0, limit: int = 100) -> List[Badge]:
        """Get all available badges"""
        return db.query(Badge).filter(Badge.is_active == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_badge_by_id(db: Session, badge_id: int) -> Optional[Badge]:
        """Get a specific badge by ID"""
        return db.query(Badge).filter(Badge.id == badge_id, Badge.is_active == True).first()
    
    @staticmethod
    def get_user_badges(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[UserBadge]:
        """Get badges earned by a user"""
        return db.query(UserBadge).filter(UserBadge.user_id == user_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def award_badge(db: Session, user_id: int, badge_id: int, context_data: Optional[Dict] = None) -> UserBadge:
        """Award a badge to a user"""
        # Check if user already has this badge
        existing_badge = db.query(UserBadge).filter(
            UserBadge.user_id == user_id,
            UserBadge.badge_id == badge_id
        ).first()
        
        if existing_badge:
            raise VocabularyVaultException("User already has this badge", status_code=400)
        
        # Get badge details
        badge = BadgeService.get_badge_by_id(db, badge_id)
        if not badge:
            raise VocabularyVaultException("Badge not found", status_code=404)
        
        # Create user badge
        user_badge = UserBadge(
            user_id=user_id,
            badge_id=badge_id,
            context_data=context_data
        )
        db.add(user_badge)
        
        # Award points if badge has point reward
        if badge.points_reward > 0:
            PointsService.add_points(
                db, user_id, badge.points_reward, "badge", 
                f"Earned badge: {badge.name}", badge_id, "badge"
            )
        
        db.commit()
        db.refresh(user_badge)
        return user_badge
    
    @staticmethod
    def check_and_award_study_streak_badges(db: Session, user_id: int, current_streak: int):
        """Check and award study streak badges"""
        streak_badges = db.query(Badge).filter(
            Badge.badge_type == BadgeType.STUDY_STREAK,
            Badge.is_active == True
        ).all()
        
        for badge in streak_badges:
            required_streak = badge.criteria.get("study_streak", 0)
            if current_streak >= required_streak:
                try:
                    BadgeService.award_badge(
                        db, user_id, badge.id, 
                        {"study_streak": current_streak}
                    )
                except VocabularyVaultException as e:
                    if "already has this badge" not in str(e):
                        raise e

    @staticmethod
    def check_and_award_perfect_score_badges(db: Session, user_id: int, accuracy_rate: float, session_id: int):
        """Check and award perfect score badges"""
        if accuracy_rate >= 1.0:  # 100% accuracy
            perfect_badges = db.query(Badge).filter(
                Badge.badge_type == BadgeType.PERFECT_SCORE,
                Badge.is_active == True
            ).all()
            
            for badge in perfect_badges:
                try:
                    BadgeService.award_badge(
                        db, user_id, badge.id,
                        {"accuracy_rate": accuracy_rate, "session_id": session_id}
                    )
                except VocabularyVaultException as e:
                    if "already has this badge" not in str(e):
                        raise e

    @staticmethod
    def check_and_award_speed_demon_badges(db: Session, user_id: int, duration_seconds: int, cards_studied: int):
        """Check and award speed demon badges"""
        if cards_studied > 0:
            cards_per_minute = (cards_studied / duration_seconds) * 60 if duration_seconds > 0 else 0
            
            speed_badges = db.query(Badge).filter(
                Badge.badge_type == BadgeType.SPEED_DEMON,
                Badge.is_active == True
            ).all()
            
            for badge in speed_badges:
                required_speed = badge.criteria.get("cards_per_minute", 0)
                if cards_per_minute >= required_speed:
                    try:
                        BadgeService.award_badge(
                            db, user_id, badge.id,
                            {"cards_per_minute": cards_per_minute, "duration_seconds": duration_seconds}
                        )
                    except VocabularyVaultException as e:
                        if "already has this badge" not in str(e):
                            raise e


class PointsService:
    """Service for managing user points and transactions"""
    
    @staticmethod
    def get_user_points(db: Session, user_id: int) -> int:
        """Get user's total points"""
        user = db.query(User).filter(User.id == user_id).first()
        return user.total_points if user else 0
    
    @staticmethod
    def add_points(
        db: Session, user_id: int, points: int, transaction_type: str, 
        description: str, reference_id: Optional[int] = None, 
        reference_type: Optional[str] = None
    ) -> PointsTransaction:
        """Add points to user account"""
        if points <= 0:
            raise VocabularyVaultException("Points must be positive", status_code=400)
        
        # Create transaction
        transaction = PointsTransaction(
            user_id=user_id,
            points=points,
            transaction_type=transaction_type,
            description=description,
            reference_id=reference_id,
            reference_type=reference_type
        )
        db.add(transaction)
        
        # Update user's total points
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.total_points += points
        
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def deduct_points(
        db: Session, user_id: int, points: int, transaction_type: str,
        description: str, reference_id: Optional[int] = None,
        reference_type: Optional[str] = None
    ) -> PointsTransaction:
        """Deduct points from user account"""
        if points <= 0:
            raise VocabularyVaultException("Points must be positive", status_code=400)
        
        # Check if user has enough points
        current_points = PointsService.get_user_points(db, user_id)
        if current_points < points:
            raise VocabularyVaultException("Insufficient points", status_code=400)
        
        # Create transaction
        transaction = PointsTransaction(
            user_id=user_id,
            points=-points,  # Negative for deduction
            transaction_type=transaction_type,
            description=description,
            reference_id=reference_id,
            reference_type=reference_type
        )
        db.add(transaction)
        
        # Update user's total points
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.total_points -= points
        
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def get_user_transactions(
        db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[PointsTransaction]:
        """Get user's points transaction history"""
        return db.query(PointsTransaction).filter(
            PointsTransaction.user_id == user_id
        ).order_by(desc(PointsTransaction.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def award_study_points(
        db: Session, user_id: int, correct_answers: int, 
        incorrect_answers: int, study_time_minutes: int,
        session_id: Optional[int] = None
    ) -> int:
        """Award points for study session"""
        # Base points: 10 points per correct answer, 2 points per incorrect answer
        base_points = (correct_answers * 10) + (incorrect_answers * 2)
        
        # Time bonus: 1 point per minute of study time
        time_bonus = study_time_minutes
        
        # Accuracy bonus: 50% bonus for 90%+ accuracy
        total_answers = correct_answers + incorrect_answers
        if total_answers > 0:
            accuracy = correct_answers / total_answers
            if accuracy >= 0.9:
                accuracy_bonus = int(base_points * 0.5)
            elif accuracy >= 0.8:
                accuracy_bonus = int(base_points * 0.25)
            else:
                accuracy_bonus = 0
        else:
            accuracy_bonus = 0
        
        total_points = base_points + time_bonus + accuracy_bonus
        
        if total_points > 0:
            PointsService.add_points(
                db, user_id, total_points, "study",
                f"Study session: {correct_answers} correct, {incorrect_answers} incorrect",
                session_id, "study_session"
            )
        
        return total_points


class LeaderboardService:
    """Service for managing leaderboards"""
    
    @staticmethod
    def get_leaderboard(
        db: Session, category: str = "all_time", limit: int = 50
    ) -> List[LeaderboardEntry]:
        """Get leaderboard for a specific category"""
        now = datetime.utcnow()
        
        if category == "daily":
            period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            period_end = period_start + timedelta(days=1)
        elif category == "weekly":
            period_start = now - timedelta(days=now.weekday())
            period_start = period_start.replace(hour=0, minute=0, second=0, microsecond=0)
            period_end = period_start + timedelta(days=7)
        elif category == "monthly":
            period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                period_end = now.replace(year=now.year + 1, month=1, day=1)
            else:
                period_end = now.replace(month=now.month + 1, day=1)
        else:  # all_time
            period_start = datetime(2020, 1, 1)  # Arbitrary start date
            period_end = now + timedelta(days=1)
        
        return db.query(LeaderboardEntry).filter(
            LeaderboardEntry.category == category,
            LeaderboardEntry.period_start == period_start,
            LeaderboardEntry.period_end == period_end
        ).order_by(desc(LeaderboardEntry.score)).limit(limit).all()
    
    @staticmethod
    def update_user_leaderboard_entry(
        db: Session, user_id: int, category: str, score: int,
        study_time_minutes: int = 0, cards_studied: int = 0,
        games_played: int = 0, badges_earned: int = 0
    ):
        """Update or create user's leaderboard entry"""
        now = datetime.utcnow()
        
        if category == "daily":
            period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            period_end = period_start + timedelta(days=1)
        elif category == "weekly":
            period_start = now - timedelta(days=now.weekday())
            period_start = period_start.replace(hour=0, minute=0, second=0, microsecond=0)
            period_end = period_start + timedelta(days=7)
        elif category == "monthly":
            period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if now.month == 12:
                period_end = now.replace(year=now.year + 1, month=1, day=1)
            else:
                period_end = now.replace(month=now.month + 1, day=1)
        else:  # all_time
            period_start = datetime(2020, 1, 1)
            period_end = now + timedelta(days=1)
        
        # Find existing entry
        entry = db.query(LeaderboardEntry).filter(
            LeaderboardEntry.user_id == user_id,
            LeaderboardEntry.category == category,
            LeaderboardEntry.period_start == period_start,
            LeaderboardEntry.period_end == period_end
        ).first()
        
        if entry:
            # Update existing entry
            entry.score = score
            entry.study_time_minutes = study_time_minutes
            entry.cards_studied = cards_studied
            entry.games_played = games_played
            entry.badges_earned = badges_earned
            entry.updated_at = now
        else:
            # Create new entry
            entry = LeaderboardEntry(
                user_id=user_id,
                category=category,
                period_start=period_start,
                period_end=period_end,
                score=score,
                study_time_minutes=study_time_minutes,
                cards_studied=cards_studied,
                games_played=games_played,
                badges_earned=badges_earned
            )
            db.add(entry)
        
        db.commit()
        db.refresh(entry)
        return entry


class GameSessionService:
    """Service for managing game sessions"""
    
    @staticmethod
    def create_game_session(
        db: Session, user_id: int, session_data: GameSessionCreate
    ) -> GameSession:
        """Create a new game session"""
        # Verify flashcard set exists and user has access
        flashcard_set = db.query(FlashcardSet).filter(
            FlashcardSet.id == session_data.set_id
        ).first()
        
        if not flashcard_set:
            raise VocabularyVaultException("Flashcard set not found", status_code=404)
        
        if not flashcard_set.is_public and flashcard_set.user_id != user_id:
            raise VocabularyVaultException("Access denied", status_code=403)
        
        game_session = GameSession(
            user_id=user_id,
            game_type=session_data.game_type,
            set_id=session_data.set_id,
            max_score=session_data.max_score,
            game_data=session_data.game_data
        )
        
        db.add(game_session)
        db.commit()
        db.refresh(game_session)
        return game_session
    
    @staticmethod
    def get_game_session(
        db: Session, session_id: int, user_id: int
    ) -> Optional[GameSession]:
        """Get a specific game session"""
        return db.query(GameSession).filter(
            GameSession.id == session_id,
            GameSession.user_id == user_id
        ).first()
    
    @staticmethod
    def update_game_session(
        db: Session, session_id: int, user_id: int, update_data: GameSessionUpdate
    ) -> GameSession:
        """Update a game session (end session)"""
        game_session = GameSessionService.get_game_session(db, session_id, user_id)
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(game_session, field, value)
        
        # Set end time if not provided
        if not game_session.end_time:
            game_session.end_time = datetime.utcnow()
        
        # Calculate duration if not provided
        if not game_session.duration_seconds and game_session.end_time:
            duration = game_session.end_time - game_session.start_time
            game_session.duration_seconds = int(duration.total_seconds())
        
        # Calculate accuracy rate if not provided
        if game_session.accuracy_rate is None and game_session.cards_played > 0:
            game_session.accuracy_rate = game_session.correct_answers / game_session.cards_played
        
        # Award points for game performance
        if game_session.score > 0:
            PointsService.add_points(
                db, user_id, game_session.score, "game",
                f"Game session: {game_session.game_type.value}",
                session_id, "game_session"
            )
        
        # Update leaderboards for all categories
        try:
            study_time_minutes = (game_session.duration_seconds or 0) // 60
            LeaderboardService.update_user_leaderboard_entry(
                db,
                user_id=user_id,
                category="daily",
                score=game_session.score,
                study_time_minutes=study_time_minutes,
                cards_studied=game_session.cards_played,
                games_played=1,
                badges_earned=0,
            )
            LeaderboardService.update_user_leaderboard_entry(
                db,
                user_id=user_id,
                category="weekly",
                score=game_session.score,
                study_time_minutes=study_time_minutes,
                cards_studied=game_session.cards_played,
                games_played=1,
                badges_earned=0,
            )
            LeaderboardService.update_user_leaderboard_entry(
                db,
                user_id=user_id,
                category="monthly",
                score=game_session.score,
                study_time_minutes=study_time_minutes,
                cards_studied=game_session.cards_played,
                games_played=1,
                badges_earned=0,
            )
            LeaderboardService.update_user_leaderboard_entry(
                db,
                user_id=user_id,
                category="all_time",
                score=game_session.score,
                study_time_minutes=study_time_minutes,
                cards_studied=game_session.cards_played,
                games_played=1,
                badges_earned=0,
            )
        except Exception as leaderboard_error:
            logger.warning(f"Failed to update leaderboard for game session {session_id}: {leaderboard_error}")
        
        db.commit()
        db.refresh(game_session)
        return game_session
    
    @staticmethod
    def get_user_game_sessions(
        db: Session, user_id: int, skip: int = 0, limit: int = 100,
        game_type: Optional[GameType] = None
    ) -> List[GameSession]:
        """Get user's game sessions"""
        query = db.query(GameSession).filter(GameSession.user_id == user_id)
        
        if game_type:
            query = query.filter(GameSession.game_type == game_type)
        
        return query.order_by(desc(GameSession.created_at)).offset(skip).limit(limit).all()


class MatchGameService:
    """Service for managing Match game sessions"""
    
    @staticmethod
    def create_match_game(
        db: Session, session_id: int, game_data: MatchGameCreate
    ) -> MatchGame:
        """Create a new Match game"""
        # Verify game session exists
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        match_game = MatchGame(
            session_id=session_id,
            total_pairs=game_data.total_pairs,
            game_state=game_data.game_state
        )
        
        db.add(match_game)
        db.commit()
        db.refresh(match_game)
        return match_game
    
    @staticmethod
    def update_match_game(
        db: Session, session_id: int, update_data: MatchGameUpdate
    ) -> MatchGame:
        """Update Match game progress"""
        match_game = db.query(MatchGame).filter(MatchGame.session_id == session_id).first()
        if not match_game:
            raise VocabularyVaultException("Match game not found", status_code=404)
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(match_game, field, value)
        
        db.commit()
        db.refresh(match_game)
        return match_game
    
    @staticmethod
    def record_move(
        db: Session, session_id: int, is_match: bool
    ) -> dict:
        """Record a move in a Match game and update session score/stats"""
        match_game = db.query(MatchGame).filter(MatchGame.session_id == session_id).first()
        if not match_game:
            raise VocabularyVaultException("Match game not found", status_code=404)
        
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        # Update move counters
        match_game.moves_count += 1
        if is_match:
            match_game.matches_found += 1
            game_session.correct_answers += 1
        else:
            game_session.incorrect_answers += 1
        
        game_session.cards_played += 1
        
        # Compute current duration
        now = datetime.utcnow()
        duration_seconds = int((now - (game_session.start_time or now)).total_seconds())
        
        # Calculate score snapshot
        score_parts = MatchGameService.calculate_match_score(
            matches_found=match_game.matches_found,
            total_pairs=match_game.total_pairs,
            moves_count=match_game.moves_count,
            duration_seconds=duration_seconds,
        )
        game_session.score = max(game_session.score, score_parts["total_score"])  # keep the best
        
        db.commit()
        db.refresh(match_game)
        db.refresh(game_session)
        
        return {
            "session_id": session_id,
            "moves_count": match_game.moves_count,
            "matches_found": match_game.matches_found,
            "is_match": is_match,
            "score": game_session.score,
        }
    
    @staticmethod
    def calculate_match_score(
        matches_found: int, total_pairs: int, moves_count: int, 
        duration_seconds: int
    ) -> Dict[str, int]:
        """Calculate Match game score"""
        # Base score: 100 points per match
        base_score = matches_found * 100
        
        # Efficiency bonus: fewer moves = more points
        if total_pairs > 0:
            efficiency_ratio = matches_found / moves_count if moves_count > 0 else 1
            efficiency_bonus = int(base_score * efficiency_ratio * 0.5)
        else:
            efficiency_bonus = 0
        
        # Time bonus: faster completion = more points
        if duration_seconds > 0:
            time_bonus = max(0, 1000 - (duration_seconds * 2))  # Max 1000 points, decreases with time
        else:
            time_bonus = 0
        
        # Perfect game bonus
        perfect_bonus = 500 if matches_found == total_pairs else 0
        
        total_score = base_score + efficiency_bonus + time_bonus + perfect_bonus
        
        return {
            "base_score": base_score,
            "efficiency_bonus": efficiency_bonus,
            "time_bonus": time_bonus,
            "perfect_bonus": perfect_bonus,
            "total_score": total_score
        }


class GravityGameService:
    """Service for managing Gravity game sessions"""
    
    @staticmethod
    def create_gravity_game(
        db: Session, session_id: int, game_data: GravityGameCreate
    ) -> GravityGame:
        """Create a new Gravity game"""
        # Verify game session exists
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        gravity_game = GravityGame(
            session_id=session_id,
            game_state=game_data.game_state
        )
        
        db.add(gravity_game)
        db.commit()
        db.refresh(gravity_game)
        return gravity_game
    
    @staticmethod
    def update_gravity_game(
        db: Session, session_id: int, update_data: GravityGameUpdate
    ) -> GravityGame:
        """Update Gravity game progress"""
        gravity_game = db.query(GravityGame).filter(GravityGame.session_id == session_id).first()
        if not gravity_game:
            raise VocabularyVaultException("Gravity game not found", status_code=404)
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(gravity_game, field, value)
        
        db.commit()
        db.refresh(gravity_game)
        return gravity_game
    
    @staticmethod
    def submit_answer(
        db: Session, session_id: int, is_correct: bool, response_time_seconds: Optional[float] = None
    ) -> dict:
        """Process a gravity game answer and update session score/stats"""
        gravity_game = db.query(GravityGame).filter(GravityGame.session_id == session_id).first()
        if not gravity_game:
            raise VocabularyVaultException("Gravity game not found", status_code=404)
        
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        # Update counters
        gravity_game.words_typed += 1
        if is_correct:
            gravity_game.words_correct += 1
            game_session.correct_answers += 1
            # increase combo gradually, cap at 5.0
            gravity_game.combo_multiplier = min((gravity_game.combo_multiplier or 1.0) + 0.1, 5.0)
        else:
            gravity_game.words_incorrect += 1
            game_session.incorrect_answers += 1
            gravity_game.combo_multiplier = 1.0
        
        if int(gravity_game.combo_multiplier) > (gravity_game.max_combo or 0):
            gravity_game.max_combo = int(gravity_game.combo_multiplier)
        
        game_session.cards_played += 1
        
        # Compute current duration
        now = datetime.utcnow()
        duration_seconds = int((now - (game_session.start_time or now)).total_seconds())
        
        # Calculate score snapshot
        score_parts = GravityGameService.calculate_gravity_score(
            words_correct=gravity_game.words_correct,
            words_incorrect=gravity_game.words_incorrect,
            max_combo=gravity_game.max_combo,
            duration_seconds=duration_seconds,
        )
        game_session.score = max(game_session.score, score_parts["total_score"])  # keep the best
        
        db.commit()
        db.refresh(gravity_game)
        db.refresh(game_session)
        
        return {
            "session_id": session_id,
            "is_correct": is_correct,
            "words_typed": gravity_game.words_typed,
            "words_correct": gravity_game.words_correct,
            "words_incorrect": gravity_game.words_incorrect,
            "combo_multiplier": gravity_game.combo_multiplier,
            "max_combo": gravity_game.max_combo,
            "score": game_session.score,
            "response_time_seconds": response_time_seconds,
        }
    
    @staticmethod
    def calculate_gravity_score(
        words_correct: int, words_incorrect: int, max_combo: int, 
        duration_seconds: int
    ) -> Dict[str, int]:
        """Calculate Gravity game score"""
        # Base score: 100 points per correct word
        base_score = words_correct * 100
        
        # Combo bonus: longer combos = more points
        combo_bonus = max_combo * 50
        
        # Speed bonus: faster typing = more points
        if duration_seconds > 0:
            speed_bonus = max(0, int(500 - (duration_seconds * 10))) # Max 500 points, decreases with time
        else:
            speed_bonus = 0
        
        # Accuracy bonus: 100% accuracy = 500 bonus points
        total_answers = words_correct + words_incorrect
        if total_answers > 0:
            accuracy = words_correct / total_answers
            accuracy_bonus = int(500 * accuracy)
        else:
            accuracy_bonus = 0
        
        total_score = base_score + combo_bonus + speed_bonus + accuracy_bonus
        
        return {
            "base_score": base_score,
            "combo_bonus": combo_bonus,
            "speed_bonus": speed_bonus,
            "accuracy_bonus": accuracy_bonus,
            "total_score": total_score
        }


class SpeedChallengeService:
    """Service for managing Speed Challenge game sessions"""
    
    @staticmethod
    def create_speed_challenge(
        db: Session, session_id: int, game_data: SpeedChallengeCreate
    ) -> SpeedChallenge:
        """Create a new Speed Challenge game"""
        # Verify game session exists
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        speed_challenge = SpeedChallenge(
            session_id=session_id,
            total_questions=game_data.total_questions,
            time_limit_seconds=game_data.time_limit_seconds,
            time_remaining_seconds=game_data.time_limit_seconds,
            game_state=game_data.game_state
        )
        
        db.add(speed_challenge)
        db.commit()
        db.refresh(speed_challenge)
        return speed_challenge
    
    @staticmethod
    def update_speed_challenge(
        db: Session, session_id: int, update_data: SpeedChallengeUpdate
    ) -> SpeedChallenge:
        """Update Speed Challenge game progress"""
        speed_challenge = db.query(SpeedChallenge).filter(SpeedChallenge.session_id == session_id).first()
        if not speed_challenge:
            raise VocabularyVaultException("Speed Challenge game not found", status_code=404)
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(speed_challenge, field, value)
        
        db.commit()
        db.refresh(speed_challenge)
        return speed_challenge
    
    @staticmethod
    def submit_answer(
        db: Session, session_id: int, is_correct: bool, response_time_seconds: float
    ) -> dict:
        """Process a Speed Challenge answer and update game state"""
        speed_challenge = db.query(SpeedChallenge).filter(SpeedChallenge.session_id == session_id).first()
        if not speed_challenge:
            raise VocabularyVaultException("Speed Challenge game not found", status_code=404)
        
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        # Update counters
        speed_challenge.questions_answered += 1
        if is_correct:
            speed_challenge.correct_answers += 1
            game_session.correct_answers += 1
            speed_challenge.streak_count += 1
        else:
            speed_challenge.incorrect_answers += 1
            game_session.incorrect_answers += 1
            speed_challenge.streak_count = 0
        
        # Update max streak
        if speed_challenge.streak_count > speed_challenge.max_streak:
            speed_challenge.max_streak = speed_challenge.streak_count
        
        # Update response time statistics
        if speed_challenge.fastest_response_time is None or response_time_seconds < speed_challenge.fastest_response_time:
            speed_challenge.fastest_response_time = response_time_seconds
        
        if speed_challenge.slowest_response_time is None or response_time_seconds > speed_challenge.slowest_response_time:
            speed_challenge.slowest_response_time = response_time_seconds
        
        # Calculate average response time
        total_response_time = speed_challenge.average_response_time * (speed_challenge.questions_answered - 1) + response_time_seconds
        speed_challenge.average_response_time = total_response_time / speed_challenge.questions_answered
        
        game_session.cards_played += 1
        
        # Calculate score snapshot
        score_parts = SpeedChallengeService.calculate_speed_challenge_score(
            correct_answers=speed_challenge.correct_answers,
            incorrect_answers=speed_challenge.incorrect_answers,
            total_questions=speed_challenge.total_questions,
            time_remaining_seconds=speed_challenge.time_remaining_seconds or 0,
            max_streak=speed_challenge.max_streak,
            average_response_time=speed_challenge.average_response_time
        )
        game_session.score = max(game_session.score, score_parts["total_score"])
        
        db.commit()
        db.refresh(speed_challenge)
        db.refresh(game_session)
        
        return {
            "session_id": session_id,
            "is_correct": is_correct,
            "questions_answered": speed_challenge.questions_answered,
            "correct_answers": speed_challenge.correct_answers,
            "incorrect_answers": speed_challenge.incorrect_answers,
            "streak_count": speed_challenge.streak_count,
            "max_streak": speed_challenge.max_streak,
            "average_response_time": speed_challenge.average_response_time,
            "score": game_session.score,
            "response_time_seconds": response_time_seconds,
        }
    
    @staticmethod
    def calculate_speed_challenge_score(
        correct_answers: int, incorrect_answers: int, total_questions: int,
        time_remaining_seconds: int, max_streak: int, average_response_time: float
    ) -> Dict[str, int]:
        """Calculate Speed Challenge game score"""
        # Base score: 100 points per correct answer, -20 points per incorrect answer
        base_score = (correct_answers * 100) - (incorrect_answers * 20)
        
        # Time bonus: more time remaining = more points
        time_bonus = int(time_remaining_seconds * 2)  # 2 points per second remaining
        
        # Speed bonus: faster average response time = more points
        if average_response_time > 0:
            speed_bonus = max(0, int(500 - (average_response_time * 100)))  # Max 500 points, decreases with time
        else:
            speed_bonus = 0
        
        # Streak bonus: longer streaks = more points
        streak_bonus = max_streak * 50
        
        # Completion bonus: finish all questions = 1000 points
        completion_bonus = 1000 if (correct_answers + incorrect_answers) >= total_questions else 0
        
        # Accuracy bonus: 100% accuracy = 500 bonus points
        total_answers = correct_answers + incorrect_answers
        if total_answers > 0:
            accuracy = correct_answers / total_answers
            accuracy_bonus = int(500 * accuracy)
        else:
            accuracy_bonus = 0
        
        total_score = base_score + time_bonus + speed_bonus + streak_bonus + completion_bonus + accuracy_bonus
        
        return {
            "base_score": base_score,
            "time_bonus": time_bonus,
            "speed_bonus": speed_bonus,
            "streak_bonus": streak_bonus,
            "completion_bonus": completion_bonus,
            "accuracy_bonus": accuracy_bonus,
            "total_score": total_score
        }


class MemoryGameService:
    """Service for managing Memory/Concentration game sessions"""
    
    @staticmethod
    def create_memory_game(
        db: Session, session_id: int, game_data: MemoryGameCreate
    ) -> MemoryGame:
        """Create a new Memory game"""
        # Verify game session exists
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        memory_game = MemoryGame(
            session_id=session_id,
            total_cards=game_data.total_cards,
            time_limit_seconds=game_data.time_limit_seconds,
            time_remaining_seconds=game_data.time_limit_seconds,
            revealed_cards=[],
            matched_pairs=[],
            game_state=game_data.game_state
        )
        
        db.add(memory_game)
        db.commit()
        db.refresh(memory_game)
        return memory_game
    
    @staticmethod
    def update_memory_game(
        db: Session, session_id: int, update_data: MemoryGameUpdate
    ) -> MemoryGame:
        """Update Memory game progress"""
        memory_game = db.query(MemoryGame).filter(MemoryGame.session_id == session_id).first()
        if not memory_game:
            raise VocabularyVaultException("Memory game not found", status_code=404)
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(memory_game, field, value)
        
        db.commit()
        db.refresh(memory_game)
        return memory_game
    
    @staticmethod
    def reveal_card(
        db: Session, session_id: int, card_id: int, is_match: bool
    ) -> dict:
        """Process a card reveal in Memory game"""
        memory_game = db.query(MemoryGame).filter(MemoryGame.session_id == session_id).first()
        if not memory_game:
            raise VocabularyVaultException("Memory game not found", status_code=404)
        
        game_session = db.query(GameSession).filter(GameSession.id == session_id).first()
        if not game_session:
            raise VocabularyVaultException("Game session not found", status_code=404)
        
        # Update revealed cards
        if card_id not in memory_game.revealed_cards:
            memory_game.revealed_cards.append(card_id)
            memory_game.cards_revealed += 1
        
        # Update moves count
        memory_game.moves_count += 1
        
        # Handle match
        if is_match:
            memory_game.matches_found += 1
            game_session.correct_answers += 1
            
            # Add to matched pairs (simplified - assumes pairs are consecutive reveals)
            if len(memory_game.revealed_cards) >= 2:
                # Get the last two revealed cards as a pair
                last_two = memory_game.revealed_cards[-2:]
                if last_two not in memory_game.matched_pairs:
                    memory_game.matched_pairs.append(last_two)
        else:
            game_session.incorrect_answers += 1
        
        game_session.cards_played += 1
        
        # Calculate score snapshot
        score_parts = MemoryGameService.calculate_memory_game_score(
            matches_found=memory_game.matches_found,
            total_cards=memory_game.total_cards,
            moves_count=memory_game.moves_count,
            time_remaining_seconds=memory_game.time_remaining_seconds or 0
        )
        game_session.score = max(game_session.score, score_parts["total_score"])
        
        db.commit()
        db.refresh(memory_game)
        db.refresh(game_session)
        
        return {
            "session_id": session_id,
            "card_id": card_id,
            "is_match": is_match,
            "cards_revealed": memory_game.cards_revealed,
            "matches_found": memory_game.matches_found,
            "moves_count": memory_game.moves_count,
            "revealed_cards": memory_game.revealed_cards,
            "matched_pairs": memory_game.matched_pairs,
            "score": game_session.score,
        }
    
    @staticmethod
    def calculate_memory_game_score(
        matches_found: int, total_cards: int, moves_count: int, time_remaining_seconds: int
    ) -> Dict[str, int]:
        """Calculate Memory game score"""
        # Base score: 200 points per match
        base_score = matches_found * 200
        
        # Efficiency bonus: fewer moves = more points
        if total_cards > 0:
            efficiency_ratio = matches_found / moves_count if moves_count > 0 else 1
            efficiency_bonus = int(base_score * efficiency_ratio * 0.5)
        else:
            efficiency_bonus = 0
        
        # Time bonus: more time remaining = more points
        time_bonus = int(time_remaining_seconds * 1)  # 1 point per second remaining
        
        # Completion bonus: find all pairs = 1000 points
        total_pairs = total_cards // 2
        completion_bonus = 1000 if matches_found >= total_pairs else 0
        
        # Perfect game bonus: complete with minimal moves
        if matches_found >= total_pairs and moves_count <= total_pairs * 2:
            perfect_bonus = 500
        else:
            perfect_bonus = 0
        
        total_score = base_score + efficiency_bonus + time_bonus + completion_bonus + perfect_bonus
        
        return {
            "base_score": base_score,
            "efficiency_bonus": efficiency_bonus,
            "time_bonus": time_bonus,
            "completion_bonus": completion_bonus,
            "perfect_bonus": perfect_bonus,
            "total_score": total_score
        }


class ChallengeService:
    """Service for managing challenges and user participation"""
    
    @staticmethod
    def get_all_challenges(
        db: Session, skip: int = 0, limit: int = 100, 
        challenge_type: Optional[ChallengeType] = None
    ) -> List[Challenge]:
        """Get all available challenges"""
        query = db.query(Challenge).filter(Challenge.is_active == True)
        
        if challenge_type:
            query = query.filter(Challenge.challenge_type == challenge_type)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_challenge_by_id(db: Session, challenge_id: int) -> Optional[Challenge]:
        """Get a specific challenge by ID"""
        return db.query(Challenge).filter(
            Challenge.id == challenge_id, 
            Challenge.is_active == True
        ).first()
    
    @staticmethod
    def get_user_challenges(
        db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[UserChallenge]:
        """Get challenges for a specific user"""
        return db.query(UserChallenge).filter(
            UserChallenge.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def start_challenge(
        db: Session, user_id: int, challenge_id: int
    ) -> UserChallenge:
        """Start a challenge for a user"""
        # Check if challenge exists and is active
        challenge = ChallengeService.get_challenge_by_id(db, challenge_id)
        if not challenge:
            raise VocabularyVaultException("Challenge not found", status_code=404)
        
        # Check if user already started this challenge
        existing = db.query(UserChallenge).filter(
            UserChallenge.user_id == user_id,
            UserChallenge.challenge_id == challenge_id,
            UserChallenge.is_completed == False,
            UserChallenge.is_failed == False
        ).first()
        
        if existing:
            raise VocabularyVaultException("User already started this challenge", status_code=400)
        
        user_challenge = UserChallenge(
            user_id=user_id,
            challenge_id=challenge_id,
            progress_data={}
        )
        
        db.add(user_challenge)
        db.commit()
        db.refresh(user_challenge)
        return user_challenge
    
    @staticmethod
    def update_challenge_progress(
        db: Session, user_id: int, challenge_id: int, progress_data: Dict[str, Any]
    ) -> UserChallenge:
        """Update user's challenge progress"""
        user_challenge = db.query(UserChallenge).filter(
            UserChallenge.user_id == user_id,
            UserChallenge.challenge_id == challenge_id,
            UserChallenge.is_completed == False,
            UserChallenge.is_failed == False
        ).first()
        
        if not user_challenge:
            raise VocabularyVaultException("User challenge not found", status_code=404)
        
        # Update progress data
        user_challenge.progress_data.update(progress_data)
        
        # Check if challenge is completed
        challenge = user_challenge.challenge
        if ChallengeService._check_challenge_completion(challenge, progress_data):
            user_challenge.is_completed = True
            user_challenge.completed_at = datetime.utcnow()
            
            # Award points
            if challenge.reward_points > 0:
                PointsService.add_points(
                    db, user_id, challenge.reward_points, "challenge",
                    f"Completed challenge: {challenge.name}",
                    challenge_id, "challenge"
                )
            
            # Award badge if specified
            if challenge.reward_badge_id:
                try:
                    BadgeService.award_badge(
                        db, user_id, challenge.reward_badge_id,
                        {"challenge_id": challenge_id, "challenge_name": challenge.name}
                    )
                except VocabularyVaultException as e:
                    if "already has this badge" not in str(e):
                        raise e
        
        db.commit()
        db.refresh(user_challenge)
        return user_challenge
    
    @staticmethod
    def _check_challenge_completion(challenge: Challenge, progress_data: Dict[str, Any]) -> bool:
        """Check if a challenge is completed based on progress data"""
        criteria = challenge.criteria
        
        if challenge.challenge_type == ChallengeType.STUDY_STREAK:
            required_streak = criteria.get("study_streak", 0)
            current_streak = progress_data.get("study_streak", 0)
            return current_streak >= required_streak
        
        elif challenge.challenge_type == ChallengeType.PERFECT_SCORE:
            required_accuracy = criteria.get("accuracy", 1.0)
            current_accuracy = progress_data.get("accuracy", 0.0)
            return current_accuracy >= required_accuracy
        
        elif challenge.challenge_type == ChallengeType.SPEED_RUN:
            required_time = criteria.get("time_seconds", 0)
            current_time = progress_data.get("time_seconds", float('inf'))
            return current_time <= required_time
        
        elif challenge.challenge_type == ChallengeType.DAILY_GOAL:
            required_cards = criteria.get("cards_studied", 0)
            current_cards = progress_data.get("cards_studied", 0)
            return current_cards >= required_cards
        
        elif challenge.challenge_type == ChallengeType.WEEKLY_GOAL:
            required_sessions = criteria.get("study_sessions", 0)
            current_sessions = progress_data.get("study_sessions", 0)
            return current_sessions >= required_sessions
        
        elif challenge.challenge_type == ChallengeType.GAME_MASTER:
            required_games = criteria.get("games_played", 0)
            current_games = progress_data.get("games_played", 0)
            return current_games >= required_games
        
        elif challenge.challenge_type == ChallengeType.SOCIAL_SHARER:
            required_shares = criteria.get("sets_shared", 0)
            current_shares = progress_data.get("sets_shared", 0)
            return current_shares >= required_shares
        
        return False
    
