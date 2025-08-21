"""Add new user fields for gamification and analytics

Revision ID: efef4a500809
Revises: 50106b17454e
Create Date: 2025-08-17 19:27:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'efef4a500809'
down_revision = '50106b17454e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to users table
    op.add_column('users', sa.Column('total_points', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('level', sa.Integer(), nullable=True, default=1))
    op.add_column('users', sa.Column('experience_points', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('study_streak_days', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('longest_streak', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('last_study_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('total_study_time_minutes', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('total_cards_studied', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('total_correct_answers', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('total_incorrect_answers', sa.Integer(), nullable=True, default=0))
    op.add_column('users', sa.Column('average_accuracy', sa.Float(), nullable=True, default=0.0))
    op.add_column('users', sa.Column('study_preferences', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('users', sa.Column('notification_settings', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('users', sa.Column('privacy_settings', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    # Drop columns from users table
    op.drop_column('users', 'privacy_settings')
    op.drop_column('users', 'notification_settings')
    op.drop_column('users', 'study_preferences')
    op.drop_column('users', 'average_accuracy')
    op.drop_column('users', 'total_incorrect_answers')
    op.drop_column('users', 'total_correct_answers')
    op.drop_column('users', 'total_cards_studied')
    op.drop_column('users', 'total_study_time_minutes')
    op.drop_column('users', 'last_study_date')
    op.drop_column('users', 'longest_streak')
    op.drop_column('users', 'study_streak_days')
    op.drop_column('users', 'experience_points')
    op.drop_column('users', 'level')
    op.drop_column('users', 'total_points')
