"""Add gamification tables

Revision ID: add_gamification_tables
Revises: dad7c1efcf90
Create Date: 2025-08-18 23:35:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_gamification_tables'
down_revision = 'dad7c1efcf90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create badges table
    op.execute("""
        CREATE TABLE IF NOT EXISTS badges (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            description TEXT NOT NULL,
            badge_type VARCHAR NOT NULL,
            icon_url VARCHAR,
            points_reward INTEGER DEFAULT 0,
            criteria JSONB,
            rarity VARCHAR DEFAULT 'common',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """)
    
    # Create user_badges table
    op.execute("""
        CREATE TABLE IF NOT EXISTS user_badges (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            badge_id INTEGER NOT NULL REFERENCES badges(id),
            earned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            context_data JSONB,
            UNIQUE(user_id, badge_id)
        )
    """)
    
    # Create points_transactions table
    op.execute("""
        CREATE TABLE IF NOT EXISTS points_transactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            points INTEGER NOT NULL,
            transaction_type VARCHAR NOT NULL,
            description TEXT NOT NULL,
            reference_id INTEGER,
            reference_type VARCHAR,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """)
    
    # Create leaderboard_entries table
    op.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard_entries (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            category VARCHAR NOT NULL,
            period_start TIMESTAMP WITH TIME ZONE NOT NULL,
            period_end TIMESTAMP WITH TIME ZONE NOT NULL,
            score INTEGER DEFAULT 0,
            rank INTEGER,
            study_time_minutes INTEGER DEFAULT 0,
            cards_studied INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            badges_earned INTEGER DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)
    
    # Create indexes for leaderboard_entries
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_leaderboard_category_period 
        ON leaderboard_entries (category, period_start, period_end)
    """)
    
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_leaderboard_user_category 
        ON leaderboard_entries (user_id, category)
    """)
    
    # Create game_sessions table
    op.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            game_type VARCHAR NOT NULL,
            set_id INTEGER NOT NULL REFERENCES flashcard_sets(id),
            start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            end_time TIMESTAMP WITH TIME ZONE,
            duration_seconds INTEGER,
            score INTEGER DEFAULT 0,
            max_score INTEGER DEFAULT 0,
            accuracy_rate FLOAT,
            cards_played INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            incorrect_answers INTEGER DEFAULT 0,
            game_data JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """)
    
    # Create match_games table
    op.execute("""
        CREATE TABLE IF NOT EXISTS match_games (
            id SERIAL PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES game_sessions(id),
            moves_count INTEGER DEFAULT 0,
            matches_found INTEGER DEFAULT 0,
            total_pairs INTEGER DEFAULT 0,
            time_bonus INTEGER DEFAULT 0,
            perfect_match_bonus INTEGER DEFAULT 0,
            game_state JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """)
    
    # Create gravity_games table
    op.execute("""
        CREATE TABLE IF NOT EXISTS gravity_games (
            id SERIAL PRIMARY KEY,
            session_id INTEGER NOT NULL REFERENCES game_sessions(id),
            words_typed INTEGER DEFAULT 0,
            words_correct INTEGER DEFAULT 0,
            words_incorrect INTEGER DEFAULT 0,
            combo_multiplier FLOAT DEFAULT 1.0,
            max_combo INTEGER DEFAULT 0,
            time_bonus INTEGER DEFAULT 0,
            game_state JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """)
    
    # Create indexes
    op.execute("CREATE INDEX IF NOT EXISTS ix_badges_id ON badges (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_user_badges_id ON user_badges (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_points_transactions_id ON points_transactions (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_leaderboard_entries_id ON leaderboard_entries (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_game_sessions_id ON game_sessions (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_match_games_id ON match_games (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_gravity_games_id ON gravity_games (id)")


def downgrade() -> None:
    # Drop tables in reverse order
    op.execute("DROP TABLE IF EXISTS gravity_games CASCADE")
    op.execute("DROP TABLE IF EXISTS match_games CASCADE")
    op.execute("DROP TABLE IF EXISTS game_sessions CASCADE")
    op.execute("DROP TABLE IF EXISTS leaderboard_entries CASCADE")
    op.execute("DROP TABLE IF EXISTS points_transactions CASCADE")
    op.execute("DROP TABLE IF EXISTS user_badges CASCADE")
    op.execute("DROP TABLE IF EXISTS badges CASCADE")
