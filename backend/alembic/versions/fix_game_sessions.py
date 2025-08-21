"""Fix game_sessions table

Revision ID: fix_game_sessions
Revises: fix_user_badges
Create Date: 2025-08-21 04:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_game_sessions'
down_revision = 'fix_user_badges'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Fix game_sessions table - ensure all required columns exist
    op.execute("""
        DO $$
        BEGIN
            -- Check if cards_played column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'game_sessions' AND column_name = 'cards_played'
            ) THEN
                -- Add cards_played column if it doesn't exist
                ALTER TABLE game_sessions ADD COLUMN cards_played INTEGER DEFAULT 0;
            END IF;
            
            -- Check if correct_answers column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'game_sessions' AND column_name = 'correct_answers'
            ) THEN
                -- Add correct_answers column if it doesn't exist
                ALTER TABLE game_sessions ADD COLUMN correct_answers INTEGER DEFAULT 0;
            END IF;
            
            -- Check if incorrect_answers column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'game_sessions' AND column_name = 'incorrect_answers'
            ) THEN
                -- Add incorrect_answers column if it doesn't exist
                ALTER TABLE game_sessions ADD COLUMN incorrect_answers INTEGER DEFAULT 0;
            END IF;
            
            -- Check if game_data column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'game_sessions' AND column_name = 'game_data'
            ) THEN
                -- Add game_data column if it doesn't exist
                ALTER TABLE game_sessions ADD COLUMN game_data JSONB;
            END IF;
        END $$;
    """)
    
    # Create indexes for better performance
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_game_sessions_user_id ON game_sessions (user_id);
        CREATE INDEX IF NOT EXISTS idx_game_sessions_game_type ON game_sessions (game_type);
        CREATE INDEX IF NOT EXISTS idx_game_sessions_set_id ON game_sessions (set_id);
    """)


def downgrade() -> None:
    # Remove indexes
    op.execute("""
        DROP INDEX IF EXISTS idx_game_sessions_user_id;
        DROP INDEX IF EXISTS idx_game_sessions_game_type;
        DROP INDEX IF EXISTS idx_game_sessions_set_id;
    """)
    
    # Note: We don't remove the columns as they might be needed by other parts of the system
