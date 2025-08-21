"""Fix user_badges table

Revision ID: fix_user_badges
Revises: create_challenges_table
Create Date: 2025-08-21 04:15:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_user_badges'
down_revision = 'create_challenges_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Fix user_badges table - ensure context_data column exists
    op.execute("""
        DO $$
        BEGIN
            -- Check if context_data column exists
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'user_badges' AND column_name = 'context_data'
            ) THEN
                -- Add context_data column if it doesn't exist
                ALTER TABLE user_badges ADD COLUMN context_data JSONB;
            END IF;
        END $$;
    """)
    
    # Create indexes for better performance
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_badges_user_id ON user_badges (user_id);
        CREATE INDEX IF NOT EXISTS idx_user_badges_badge_id ON user_badges (badge_id);
    """)


def downgrade() -> None:
    # Remove indexes
    op.execute("""
        DROP INDEX IF EXISTS idx_user_badges_user_id;
        DROP INDEX IF EXISTS idx_user_badges_badge_id;
    """)
    
    # Note: We don't remove the context_data column as it might be needed by other parts of the system
