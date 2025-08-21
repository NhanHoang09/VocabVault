"""Add AI module tables

Revision ID: add_ai_tables
Revises: add_gamification_tables
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_ai_tables'
down_revision = 'add_new_games'
branch_labels = None
depends_on = None


def upgrade():
    # Create ai_conversations table
    op.create_table('ai_conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('context_type', sa.String(length=50), nullable=False),
        sa.Column('context_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_conversations_id'), 'ai_conversations', ['id'], unique=False)

    # Create ai_messages table
    op.create_table('ai_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('message_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['ai_conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_messages_id'), 'ai_messages', ['id'], unique=False)

    # Create generated_content table
    op.create_table('generated_content',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=False),
        sa.Column('source_text', sa.Text(), nullable=True),
        sa.Column('generated_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('generation_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_imported', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_content_id'), 'generated_content', ['id'], unique=False)

    # Create learning_profiles table
    op.create_table('learning_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('preferred_study_mode', sa.String(length=50), nullable=True),
        sa.Column('preferred_difficulty', sa.String(length=20), nullable=True),
        sa.Column('study_session_duration', sa.Integer(), nullable=True),
        sa.Column('daily_study_goal', sa.Integer(), nullable=True),
        sa.Column('average_response_time', sa.Float(), nullable=True),
        sa.Column('accuracy_rate', sa.Float(), nullable=True),
        sa.Column('retention_rate', sa.Float(), nullable=True),
        sa.Column('learning_speed', sa.Float(), nullable=True),
        sa.Column('recommended_difficulty', sa.String(length=20), nullable=True),
        sa.Column('recommended_study_mode', sa.String(length=50), nullable=True),
        sa.Column('next_review_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_learning_profiles_id'), 'learning_profiles', ['id'], unique=False)

    # Create adaptive_recommendations table
    op.create_table('adaptive_recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recommendation_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_applied', sa.Boolean(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_adaptive_recommendations_id'), 'adaptive_recommendations', ['id'], unique=False)

    # Create ai_tutor_sessions table
    op.create_table('ai_tutor_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=True),
        sa.Column('session_type', sa.String(length=50), nullable=False),
        sa.Column('difficulty_level', sa.String(length=20), nullable=False),
        sa.Column('target_accuracy', sa.Float(), nullable=True),
        sa.Column('current_accuracy', sa.Float(), nullable=True),
        sa.Column('cards_studied', sa.Integer(), nullable=True),
        sa.Column('total_cards', sa.Integer(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=True),
        sa.Column('session_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_tutor_sessions_id'), 'ai_tutor_sessions', ['id'], unique=False)


def downgrade():
    # Drop ai_tutor_sessions table
    op.drop_index(op.f('ix_ai_tutor_sessions_id'), table_name='ai_tutor_sessions')
    op.drop_table('ai_tutor_sessions')

    # Drop adaptive_recommendations table
    op.drop_index(op.f('ix_adaptive_recommendations_id'), table_name='adaptive_recommendations')
    op.drop_table('adaptive_recommendations')

    # Drop learning_profiles table
    op.drop_index(op.f('ix_learning_profiles_id'), table_name='learning_profiles')
    op.drop_table('learning_profiles')

    # Drop generated_content table
    op.drop_index(op.f('ix_generated_content_id'), table_name='generated_content')
    op.drop_table('generated_content')

    # Drop ai_messages table
    op.drop_index(op.f('ix_ai_messages_id'), table_name='ai_messages')
    op.drop_table('ai_messages')

    # Drop ai_conversations table
    op.drop_index(op.f('ix_ai_conversations_id'), table_name='ai_conversations')
    op.drop_table('ai_conversations')
