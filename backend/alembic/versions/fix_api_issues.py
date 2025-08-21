"""Fix API issues - badges and study sessions

Revision ID: fix_api_issues
Revises: add_phase_4_tables
Create Date: 2025-08-21 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_api_issues'
down_revision = 'add_phase_4_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Fix badges table - ensure all required columns exist
    op.execute("""
        DO $$
        BEGIN
            -- Check if achievement_type column exists (this is the actual column name)
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'badges' AND column_name = 'achievement_type'
            ) THEN
                -- Add achievement_type column if it doesn't exist
                ALTER TABLE badges ADD COLUMN achievement_type VARCHAR(50);
            END IF;
            
            -- Check if points_reward column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'badges' AND column_name = 'points_reward'
            ) THEN
                -- Add points_reward column if it doesn't exist
                ALTER TABLE badges ADD COLUMN points_reward INTEGER DEFAULT 0;
            END IF;
            
            -- Check if criteria column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'badges' AND column_name = 'criteria'
            ) THEN
                -- Add criteria column if it doesn't exist
                ALTER TABLE badges ADD COLUMN criteria JSONB;
            END IF;
            
            -- Check if rarity column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'badges' AND column_name = 'rarity'
            ) THEN
                -- Add rarity column if it doesn't exist
                ALTER TABLE badges ADD COLUMN rarity VARCHAR DEFAULT 'common';
            END IF;
            
            -- Check if is_active column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'badges' AND column_name = 'is_active'
            ) THEN
                -- Add is_active column if it doesn't exist
                ALTER TABLE badges ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
            END IF;
        END $$;
    """)
    
    # Fix study_sessions table - ensure start_time column exists and is properly named
    op.execute("""
        DO $$
        BEGIN
            -- Check if start_time column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'study_sessions' AND column_name = 'start_time'
            ) THEN
                -- Add start_time column if it doesn't exist
                ALTER TABLE study_sessions ADD COLUMN start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            END IF;
            
            -- Check if started_at column exists and rename it to start_time if needed
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'study_sessions' AND column_name = 'started_at'
            ) THEN
                -- Rename started_at to start_time
                ALTER TABLE study_sessions RENAME COLUMN started_at TO start_time;
            END IF;
        END $$;
    """)
    
    # Add unique constraint to badges name if it doesn't exist
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint 
                WHERE conname = 'badges_name_key'
            ) THEN
                ALTER TABLE badges ADD CONSTRAINT badges_name_key UNIQUE (name);
            END IF;
        END $$;
    """)
    
    # Add some sample badges if table is empty
    op.execute("""
        INSERT INTO badges (name, description, achievement_type, icon_url, points_reward, criteria, rarity, is_active)
        VALUES 
        ('First Steps', 'Complete your first study session', 'STUDY_STREAK', '/icons/first-steps.png', 10, '{"study_sessions": 1}', 'common', true),
        ('Week Warrior', 'Study for 7 consecutive days', 'STUDY_STREAK', '/icons/week-warrior.png', 50, '{"study_streak": 7}', 'rare', true),
        ('Perfect Score', 'Get 100% accuracy in a study session', 'PERFECT_SCORE', '/icons/perfect-score.png', 25, '{"accuracy": 100}', 'rare', true),
        ('Speed Demon', 'Complete a study session in under 5 minutes', 'SPEED_DEMON', '/icons/speed-demon.png', 30, '{"duration_seconds": 300}', 'epic', true),
        ('Master Learner', 'Study 100 cards', 'MASTER_LEARNER', '/icons/master-learner.png', 100, '{"cards_studied": 100}', 'epic', true)
        ON CONFLICT (name) DO NOTHING;
    """)
    
    # Create indexes for better performance
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_badges_achievement_type ON badges (achievement_type);
        CREATE INDEX IF NOT EXISTS idx_badges_is_active ON badges (is_active);
        CREATE INDEX IF NOT EXISTS idx_study_sessions_start_time ON study_sessions (start_time);
        CREATE INDEX IF NOT EXISTS idx_study_sessions_user_id ON study_sessions (user_id);
    """)


def downgrade() -> None:
    # Remove indexes
    op.execute("""
        DROP INDEX IF EXISTS idx_badges_achievement_type;
        DROP INDEX IF EXISTS idx_badges_is_active;
        DROP INDEX IF EXISTS idx_study_sessions_start_time;
        DROP INDEX IF EXISTS idx_study_sessions_user_id;
    """)
    
    # Remove sample badges
    op.execute("""
        DELETE FROM badges WHERE name IN (
            'First Steps', 'Week Warrior', 'Perfect Score', 'Speed Demon', 'Master Learner'
        );
    """)
    
    # Note: We don't remove the columns as they might be needed by other parts of the system
