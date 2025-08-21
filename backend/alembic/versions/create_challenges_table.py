"""Create challenges table

Revision ID: create_challenges_table
Revises: fix_api_issues
Create Date: 2025-08-21 04:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_challenges_table'
down_revision = 'fix_api_issues'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create challenges table if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'challenges') THEN
                CREATE TABLE challenges (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL UNIQUE,
                    description TEXT NOT NULL,
                    challenge_type VARCHAR NOT NULL,
                    criteria JSONB,
                    reward_points INTEGER DEFAULT 0,
                    reward_badge_id INTEGER REFERENCES badges(id),
                    duration_days INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_recurring BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            END IF;
        END $$;
    """)
    
    # Add missing columns if table exists but columns are missing
    op.execute("""
        DO $$
        BEGIN
            -- Check if table has title column instead of name
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'title'
            ) AND NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'name'
            ) THEN
                -- Rename title to name
                ALTER TABLE challenges RENAME COLUMN title TO name;
            END IF;
            
            -- Add name column if it doesn't exist
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'name'
            ) THEN
                ALTER TABLE challenges ADD COLUMN name VARCHAR NOT NULL UNIQUE;
            END IF;
            
            -- Add description column if it doesn't exist
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'description'
            ) THEN
                ALTER TABLE challenges ADD COLUMN description TEXT NOT NULL;
            END IF;
            
            -- Add challenge_type column if it doesn't exist
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'challenge_type'
            ) THEN
                ALTER TABLE challenges ADD COLUMN challenge_type VARCHAR NOT NULL;
            END IF;
            
            -- Add other columns if they don't exist
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'criteria'
            ) THEN
                ALTER TABLE challenges ADD COLUMN criteria JSONB;
            END IF;
            
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'reward_points'
            ) THEN
                ALTER TABLE challenges ADD COLUMN reward_points INTEGER DEFAULT 0;
            END IF;
            
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'duration_days'
            ) THEN
                ALTER TABLE challenges ADD COLUMN duration_days INTEGER DEFAULT 1;
            END IF;
            
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'is_active'
            ) THEN
                ALTER TABLE challenges ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
            END IF;
            
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'challenges' AND column_name = 'is_recurring'
            ) THEN
                ALTER TABLE challenges ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE;
            END IF;
        END $$;
    """)
    
    # Create user_challenges table
    op.execute("""
        CREATE TABLE IF NOT EXISTS user_challenges (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            challenge_id INTEGER NOT NULL REFERENCES challenges(id),
            started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            completed_at TIMESTAMP WITH TIME ZONE,
            progress_data JSONB,
            is_completed BOOLEAN DEFAULT FALSE,
            is_failed BOOLEAN DEFAULT FALSE,
            UNIQUE(user_id, challenge_id)
        )
    """)
    
    # Add unique constraint to challenges name if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint 
                WHERE conname = 'challenges_name_key'
            ) THEN
                ALTER TABLE challenges ADD CONSTRAINT challenges_name_key UNIQUE (name);
            END IF;
        END $$;
    """)
    
    # Add some sample challenges
    op.execute("""
        INSERT INTO challenges (name, description, challenge_type, criteria, reward_points, duration_days, is_active, is_recurring)
        VALUES 
        ('Daily Study Goal', 'Study for at least 30 minutes today', 'DAILY_GOAL', '{"study_time_minutes": 30}', 50, 1, true, true),
        ('Weekly Streak', 'Study for 7 consecutive days', 'WEEKLY_GOAL', '{"study_streak": 7}', 200, 7, true, true),
        ('Perfect Score', 'Get 100% accuracy in a study session', 'PERFECT_SCORE', '{"accuracy": 100}', 100, 1, true, false),
        ('Speed Runner', 'Complete a study session in under 10 minutes', 'SPEED_RUN', '{"duration_seconds": 600}', 75, 1, true, false),
        ('Card Master', 'Study 50 cards in one session', 'GAME_MASTER', '{"cards_studied": 50}', 150, 1, true, false)
        ON CONFLICT (name) DO NOTHING;
    """)
    
    # Create indexes
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_challenges_type ON challenges (challenge_type);
        CREATE INDEX IF NOT EXISTS idx_challenges_active ON challenges (is_active);
        CREATE INDEX IF NOT EXISTS idx_user_challenges_user_id ON user_challenges (user_id);
        CREATE INDEX IF NOT EXISTS idx_user_challenges_challenge_id ON user_challenges (challenge_id);
    """)


def downgrade() -> None:
    # Remove indexes
    op.execute("""
        DROP INDEX IF EXISTS idx_challenges_type;
        DROP INDEX IF EXISTS idx_challenges_active;
        DROP INDEX IF EXISTS idx_user_challenges_user_id;
        DROP INDEX IF EXISTS idx_user_challenges_challenge_id;
    """)
    
    # Remove sample challenges
    op.execute("""
        DELETE FROM challenges WHERE name IN (
            'Daily Study Goal', 'Weekly Streak', 'Perfect Score', 'Speed Runner', 'Card Master'
        );
    """)
    
    # Drop tables
    op.execute("DROP TABLE IF EXISTS user_challenges CASCADE;")
    op.execute("DROP TABLE IF EXISTS challenges CASCADE;")
