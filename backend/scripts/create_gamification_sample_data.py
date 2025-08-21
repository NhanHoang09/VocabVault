#!/usr/bin/env python3
"""
Script to create sample data for the gamification system
This script creates sample badges, challenges, and game data for testing
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, get_db
import app.models_registry  # Import all models to ensure relationships are loaded
from app.modules.gamification.models import (
    Badge, UserBadge, PointsTransaction, LeaderboardEntry,
    GameSession, MatchGame, GravityGame, SpeedChallenge, MemoryGame,
    Challenge, UserChallenge, BadgeType, GameType, ChallengeType
)
from app.modules.auth.models import User
from app.modules.flashcards.models import FlashcardSet


def create_sample_badges(db: Session):
    """Create sample badges"""
    print("Creating sample badges...")
    
    badges_data = [
        {
            "name": "First Steps",
            "description": "Complete your first study session",
            "badge_type": BadgeType.STUDY_STREAK,
            "icon_url": "https://example.com/badges/first-steps.png",
            "points_reward": 50,
            "criteria": {"study_sessions": 1},
            "rarity": "common"
        },
        {
            "name": "Streak Master",
            "description": "Maintain a 7-day study streak",
            "badge_type": BadgeType.STUDY_STREAK,
            "icon_url": "https://example.com/badges/streak-master.png",
            "points_reward": 200,
            "criteria": {"study_streak_days": 7},
            "rarity": "rare"
        },
        {
            "name": "Speed Demon",
            "description": "Complete a speed challenge in under 30 seconds",
            "badge_type": BadgeType.SPEED_DEMON,
            "icon_url": "https://example.com/badges/speed-demon.png",
            "points_reward": 300,
            "criteria": {"speed_challenge_time": 30},
            "rarity": "epic"
        },
        {
            "name": "Perfect Memory",
            "description": "Complete a memory game with 100% accuracy",
            "badge_type": BadgeType.PERFECT_GAME,
            "icon_url": "https://example.com/badges/perfect-memory.png",
            "points_reward": 400,
            "criteria": {"memory_game_accuracy": 1.0},
            "rarity": "legendary"
        },
        {
            "name": "Gravity Master",
            "description": "Type 50 words correctly in gravity game",
            "badge_type": BadgeType.GAME_CHAMPION,
            "icon_url": "https://example.com/badges/gravity-master.png",
            "points_reward": 250,
            "criteria": {"gravity_words_correct": 50},
            "rarity": "uncommon"
        },
        {
            "name": "Match Maker",
            "description": "Complete 10 match games",
            "badge_type": BadgeType.GAME_CHAMPION,
            "icon_url": "https://example.com/badges/match-maker.png",
            "points_reward": 150,
            "criteria": {"match_games_completed": 10},
            "rarity": "common"
        },
        {
            "name": "Fast Learner",
            "description": "Complete 5 study sessions in one day",
            "badge_type": BadgeType.FAST_LEARNER,
            "icon_url": "https://example.com/badges/fast-learner.png",
            "points_reward": 100,
            "criteria": {"study_sessions_per_day": 5},
            "rarity": "uncommon"
        },
        {
            "name": "Consistent Studier",
            "description": "Study for 30 consecutive days",
            "badge_type": BadgeType.CONSISTENT_STUDIER,
            "icon_url": "https://example.com/badges/consistent-studier.png",
            "points_reward": 500,
            "criteria": {"study_streak_days": 30},
            "rarity": "legendary"
        }
    ]
    
    badges = []
    for badge_data in badges_data:
        badge = Badge(**badge_data)
        db.add(badge)
        badges.append(badge)
    
    db.commit()
    print(f"Created {len(badges)} badges")
    return badges


def create_sample_challenges(db: Session):
    """Create sample challenges"""
    print("Creating sample challenges...")
    
    challenges_data = [
        {
            "name": "Weekly Study Streak",
            "description": "Study for 7 consecutive days",
            "challenge_type": ChallengeType.STUDY_STREAK,
            "criteria": {"study_days": 7},
            "reward_points": 200,
            "duration_days": 7,
            "is_recurring": True
        },
        {
            "name": "Speed Runner",
            "description": "Complete 5 speed challenges",
            "challenge_type": ChallengeType.SPEED_RUN,
            "criteria": {"speed_challenges_completed": 5},
            "reward_points": 150,
            "duration_days": 14,
            "is_recurring": False
        },
        {
            "name": "Game Master",
            "description": "Play all 4 types of games",
            "challenge_type": ChallengeType.GAME_MASTER,
            "criteria": {"game_types_played": ["match", "gravity", "speed_challenge", "memory"]},
            "reward_points": 300,
            "duration_days": 30,
            "is_recurring": False
        },
        {
            "name": "Daily Goal",
            "description": "Study for at least 30 minutes today",
            "challenge_type": ChallengeType.DAILY_GOAL,
            "criteria": {"study_time_minutes": 30},
            "reward_points": 50,
            "duration_days": 1,
            "is_recurring": True
        },
        {
            "name": "Perfect Score",
            "description": "Achieve 100% accuracy in any game",
            "challenge_type": ChallengeType.PERFECT_SCORE,
            "criteria": {"game_accuracy": 1.0},
            "reward_points": 250,
            "duration_days": 7,
            "is_recurring": False
        }
    ]
    
    challenges = []
    for challenge_data in challenges_data:
        challenge = Challenge(**challenge_data)
        db.add(challenge)
        challenges.append(challenge)
    
    db.commit()
    print(f"Created {len(challenges)} challenges")
    return challenges


def create_sample_game_sessions(db: Session, users, flashcard_sets):
    """Create sample game sessions and game data"""
    print("Creating sample game sessions...")
    
    game_types = [GameType.MATCH, GameType.GRAVITY, GameType.SPEED_CHALLENGE, GameType.MEMORY]
    
    sessions = []
    for user in users:
        # Create 2-5 game sessions per user
        num_sessions = random.randint(2, 5)
        
        for i in range(num_sessions):
            game_type = random.choice(game_types)
            set_id = random.choice(flashcard_sets).id
            
            # Random session data
            start_time = datetime.now() - timedelta(days=random.randint(1, 30))
            duration_seconds = random.randint(300, 1800)  # 5-30 minutes
            end_time = start_time + timedelta(seconds=duration_seconds)
            
            # Random performance data
            cards_played = random.randint(10, 50)
            correct_answers = random.randint(cards_played // 2, cards_played)
            accuracy_rate = correct_answers / cards_played if cards_played > 0 else 0
            score = int(correct_answers * 10 * accuracy_rate)
            
            session = GameSession(
                user_id=user.id,
                game_type=game_type,
                set_id=set_id,
                start_time=start_time,
                end_time=end_time,
                duration_seconds=duration_seconds,
                score=score,
                max_score=cards_played * 10,
                accuracy_rate=accuracy_rate,
                cards_played=cards_played,
                correct_answers=correct_answers,
                incorrect_answers=cards_played - correct_answers
            )
            
            db.add(session)
            sessions.append(session)
    
    db.commit()
    
    # Create specific game data for each session
    for session in sessions:
        if session.game_type == GameType.MATCH:
            match_game = MatchGame(
                session_id=session.id,
                moves_count=random.randint(20, 60),
                matches_found=session.cards_played // 2,
                total_pairs=session.cards_played // 2,
                time_bonus=random.randint(50, 200),
                perfect_match_bonus=100 if session.accuracy_rate == 1.0 else 0
            )
            db.add(match_game)
            
        elif session.game_type == GameType.GRAVITY:
            gravity_game = GravityGame(
                session_id=session.id,
                words_typed=session.cards_played,
                words_correct=session.correct_answers,
                words_incorrect=session.incorrect_answers,
                combo_multiplier=random.uniform(1.0, 5.0),
                max_combo=random.randint(5, 20),
                time_bonus=random.randint(100, 500)
            )
            db.add(gravity_game)
            
        elif session.game_type == GameType.SPEED_CHALLENGE:
            speed_challenge = SpeedChallenge(
                session_id=session.id,
                total_questions=session.cards_played,
                questions_answered=session.cards_played,
                correct_answers=session.correct_answers,
                incorrect_answers=session.incorrect_answers,
                time_limit_seconds=300,
                time_remaining_seconds=random.randint(30, 180),
                average_response_time=random.uniform(2.0, 8.0),
                fastest_response_time=random.uniform(1.0, 3.0),
                slowest_response_time=random.uniform(5.0, 15.0),
                streak_count=random.randint(3, 10),
                max_streak=random.randint(5, 15)
            )
            db.add(speed_challenge)
            
        elif session.game_type == GameType.MEMORY:
            memory_game = MemoryGame(
                session_id=session.id,
                total_cards=session.cards_played,
                cards_revealed=session.cards_played,
                matches_found=session.cards_played // 2,
                moves_count=random.randint(30, 80),
                time_limit_seconds=600,
                time_remaining_seconds=random.randint(100, 400)
            )
            db.add(memory_game)
    
    db.commit()
    print(f"Created {len(sessions)} game sessions with game data")
    return sessions


def create_sample_points_transactions(db: Session, users, sessions):
    """Create sample points transactions"""
    print("Creating sample points transactions...")
    
    transactions = []
    for user in users:
        # Create 5-15 transactions per user
        num_transactions = random.randint(5, 15)
        
        for i in range(num_transactions):
            # Random transaction data
            points = random.randint(10, 100)
            transaction_types = ["study", "game", "badge", "bonus", "challenge"]
            transaction_type = random.choice(transaction_types)
            
            descriptions = {
                "study": "Study session completed",
                "game": "Game session completed",
                "badge": "Badge earned",
                "bonus": "Bonus points awarded",
                "challenge": "Challenge completed"
            }
            
            transaction = PointsTransaction(
                user_id=user.id,
                points=points,
                transaction_type=transaction_type,
                description=descriptions[transaction_type],
                reference_id=random.randint(1, 100),
                reference_type=transaction_type
            )
            
            db.add(transaction)
            transactions.append(transaction)
    
    db.commit()
    print(f"Created {len(transactions)} points transactions")
    return transactions


def create_sample_user_badges(db: Session, users, badges):
    """Create sample user badges"""
    print("Creating sample user badges...")
    
    user_badges = []
    for user in users:
        # Award 2-4 badges per user
        num_badges = random.randint(2, 4)
        user_badges_to_award = random.sample(badges, min(num_badges, len(badges)))
        
        for badge in user_badges_to_award:
            user_badge = UserBadge(
                user_id=user.id,
                badge_id=badge.id,
                context_data={"earned_at": datetime.now().isoformat()}
            )
            
            db.add(user_badge)
            user_badges.append(user_badge)
    
    db.commit()
    print(f"Created {len(user_badges)} user badges")
    return user_badges


def create_sample_leaderboard_entries(db: Session, users):
    """Create sample leaderboard entries"""
    print("Creating sample leaderboard entries...")
    
    categories = ["daily", "weekly", "monthly", "all_time"]
    entries = []
    
    for user in users:
        for category in categories:
            # Random leaderboard data
            score = random.randint(100, 5000)
            rank = random.randint(1, 50)
            study_time_minutes = random.randint(30, 480)
            cards_studied = random.randint(20, 200)
            games_played = random.randint(1, 20)
            badges_earned = random.randint(1, 8)
            
            # Set period dates
            now = datetime.now()
            if category == "daily":
                period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                period_end = period_start + timedelta(days=1)
            elif category == "weekly":
                period_start = now - timedelta(days=now.weekday())
                period_start = period_start.replace(hour=0, minute=0, second=0, microsecond=0)
                period_end = period_start + timedelta(days=7)
            elif category == "monthly":
                period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                period_end = (period_start + timedelta(days=32)).replace(day=1)
            else:  # all_time
                period_start = datetime(2024, 1, 1)
                period_end = now + timedelta(days=365)
            
            entry = LeaderboardEntry(
                user_id=user.id,
                category=category,
                period_start=period_start,
                period_end=period_end,
                score=score,
                rank=rank,
                study_time_minutes=study_time_minutes,
                cards_studied=cards_studied,
                games_played=games_played,
                badges_earned=badges_earned
            )
            
            db.add(entry)
            entries.append(entry)
    
    db.commit()
    print(f"Created {len(entries)} leaderboard entries")
    return entries


def create_sample_user_challenges(db: Session, users, challenges):
    """Create sample user challenges"""
    print("Creating sample user challenges...")
    
    user_challenges = []
    for user in users:
        # Start 2-4 challenges per user
        num_challenges = random.randint(2, 4)
        user_challenges_to_start = random.sample(challenges, min(num_challenges, len(challenges)))
        
        for challenge in user_challenges_to_start:
            # Random progress data
            progress_data = {
                "current_progress": random.randint(0, 100),
                "target": 100,
                "last_updated": datetime.now().isoformat()
            }
            
            # Some challenges are completed
            is_completed = random.choice([True, False])
            completed_at = datetime.now() if is_completed else None
            
            user_challenge = UserChallenge(
                user_id=user.id,
                challenge_id=challenge.id,
                progress_data=progress_data,
                is_completed=is_completed,
                completed_at=completed_at
            )
            
            db.add(user_challenge)
            user_challenges.append(user_challenge)
    
    db.commit()
    print(f"Created {len(user_challenges)} user challenges")
    return user_challenges


def main():
    """Main function to create all sample data"""
    print("Creating gamification sample data...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get existing users and flashcard sets
        users = db.query(User).limit(5).all()
        flashcard_sets = db.query(FlashcardSet).limit(3).all()
        
        if not users:
            print("No users found. Please create users first.")
            return
        
        if not flashcard_sets:
            print("No flashcard sets found. Please create flashcard sets first.")
            return
        
        print(f"Found {len(users)} users and {len(flashcard_sets)} flashcard sets")
        
        # Create sample data
        badges = create_sample_badges(db)
        challenges = create_sample_challenges(db)
        sessions = create_sample_game_sessions(db, users, flashcard_sets)
        transactions = create_sample_points_transactions(db, users, sessions)
        user_badges = create_sample_user_badges(db, users, badges)
        leaderboard_entries = create_sample_leaderboard_entries(db, users)
        user_challenges = create_sample_user_challenges(db, users, challenges)
        
        print("\n✅ Gamification sample data created successfully!")
        print(f"📊 Summary:")
        print(f"   - {len(badges)} badges")
        print(f"   - {len(challenges)} challenges")
        print(f"   - {len(sessions)} game sessions")
        print(f"   - {len(transactions)} points transactions")
        print(f"   - {len(user_badges)} user badges")
        print(f"   - {len(leaderboard_entries)} leaderboard entries")
        print(f"   - {len(user_challenges)} user challenges")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
