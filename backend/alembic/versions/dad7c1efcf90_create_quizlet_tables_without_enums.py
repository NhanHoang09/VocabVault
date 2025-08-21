"""Create Quizlet tables without enums

Revision ID: dad7c1efcf90
Revises: efef4a500809
Create Date: 2025-08-17 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dad7c1efcf90'
down_revision = 'efef4a500809'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create flashcard_sets table
    op.create_table('flashcard_sets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_featured', sa.Boolean(), nullable=True, default=False),
        sa.Column('total_cards', sa.Integer(), nullable=True, default=0),
        sa.Column('study_count', sa.Integer(), nullable=True, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flashcard_sets_id'), 'flashcard_sets', ['id'], unique=False)

    # Create flashcards table
    op.create_table('flashcards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=False),
        sa.Column('front_content', sa.Text(), nullable=False),
        sa.Column('back_content', sa.Text(), nullable=False),
        sa.Column('card_type', sa.String(), nullable=True),
        sa.Column('media_url', sa.String(), nullable=True),
        sa.Column('difficulty', sa.String(), nullable=True),
        sa.Column('mastery_level', sa.String(), nullable=True),
        sa.Column('mastery_score', sa.Float(), nullable=True, default=0.0),
        sa.Column('review_count', sa.Integer(), nullable=True, default=0),
        sa.Column('correct_count', sa.Integer(), nullable=True, default=0),
        sa.Column('incorrect_count', sa.Integer(), nullable=True, default=0),
        sa.Column('last_reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('next_review_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('card_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flashcards_id'), 'flashcards', ['id'], unique=False)

    # Create study_sessions table
    op.create_table('study_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=False),
        sa.Column('study_mode', sa.String(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('cards_studied', sa.Integer(), nullable=True, default=0),
        sa.Column('correct_answers', sa.Integer(), nullable=True, default=0),
        sa.Column('incorrect_answers', sa.Integer(), nullable=True, default=0),
        sa.Column('accuracy_rate', sa.Float(), nullable=True),
        sa.Column('session_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_sessions_id'), 'study_sessions', ['id'], unique=False)

    # Create study_attempts table
    op.create_table('study_attempts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('card_id', sa.Integer(), nullable=False),
        sa.Column('user_answer', sa.Text(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('response_time_seconds', sa.Float(), nullable=True),
        sa.Column('confidence_level', sa.Integer(), nullable=True),
        sa.Column('attempt_number', sa.Integer(), nullable=True, default=1),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['card_id'], ['flashcards.id'], ),
        sa.ForeignKeyConstraint(['session_id'], ['study_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_attempts_id'), 'study_attempts', ['id'], unique=False)

    # Create badges table
    op.create_table('badges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon_url', sa.String(), nullable=True),
        sa.Column('achievement_type', sa.String(), nullable=False),
        sa.Column('criteria', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('rarity', sa.String(), nullable=True, default='common'),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_badges_id'), 'badges', ['id'], unique=False)

    # Create user_badges table
    op.create_table('user_badges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('badge_id', sa.Integer(), nullable=False),
        sa.Column('earned_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('progress', sa.Float(), nullable=True, default=0.0),
        sa.ForeignKeyConstraint(['badge_id'], ['badges.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_badges_id'), 'user_badges', ['id'], unique=False)

    # Create game_sessions table
    op.create_table('game_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=False),
        sa.Column('game_type', sa.String(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True, default=0),
        sa.Column('max_score', sa.Integer(), nullable=True, default=0),
        sa.Column('accuracy_rate', sa.Float(), nullable=True),
        sa.Column('game_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_sessions_id'), 'game_sessions', ['id'], unique=False)

    # Create leaderboard table
    op.create_table('leaderboard',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('game_type', sa.String(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('time_taken', sa.Integer(), nullable=True),
        sa.Column('accuracy_rate', sa.Float(), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leaderboard_id'), 'leaderboard', ['id'], unique=False)

    # Create challenges table
    op.create_table('challenges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('challenge_type', sa.String(), nullable=False),
        sa.Column('criteria', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('reward_points', sa.Integer(), nullable=True, default=0),
        sa.Column('reward_badge_id', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['reward_badge_id'], ['badges.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_challenges_id'), 'challenges', ['id'], unique=False)

    # Create user_challenges table
    op.create_table('user_challenges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('challenge_id', sa.Integer(), nullable=False),
        sa.Column('progress', sa.Float(), nullable=True, default=0.0),
        sa.Column('is_completed', sa.Boolean(), nullable=True, default=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['challenge_id'], ['challenges.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_challenges_id'), 'user_challenges', ['id'], unique=False)

    # Create learning_streaks table
    op.create_table('learning_streaks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('current_streak', sa.Integer(), nullable=True, default=0),
        sa.Column('longest_streak', sa.Integer(), nullable=True, default=0),
        sa.Column('last_study_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('streak_start_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_streaks_id'), 'learning_streaks', ['id'], unique=False)

    # Create set_sharings table
    op.create_table('set_sharings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=False),
        sa.Column('shared_by', sa.Integer(), nullable=False),
        sa.Column('shared_with', sa.Integer(), nullable=False),
        sa.Column('permission_level', sa.String(), nullable=True, default='view'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ),
        sa.ForeignKeyConstraint(['shared_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['shared_with'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_set_sharings_id'), 'set_sharings', ['id'], unique=False)

    # Create ai_conversations table
    op.create_table('ai_conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('conversation_type', sa.String(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('context', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('message_count', sa.Integer(), nullable=True, default=0),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_conversations_id'), 'ai_conversations', ['id'], unique=False)

    # Create ai_messages table
    op.create_table('ai_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('sender', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(), nullable=True, default='text'),
        sa.Column('message_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['ai_conversations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_messages_id'), 'ai_messages', ['id'], unique=False)

    # Create content_generation table
    op.create_table('content_generation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('ai_type', sa.String(), nullable=False),
        sa.Column('input_text', sa.Text(), nullable=True),
        sa.Column('generated_content', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('user_feedback', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_generation_id'), 'content_generation', ['id'], unique=False)

    # Create learning_recommendations table
    op.create_table('learning_recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recommendation_type', sa.String(), nullable=False),
        sa.Column('target_set_id', sa.Integer(), nullable=True),
        sa.Column('priority_score', sa.Float(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('is_implemented', sa.Boolean(), nullable=True, default=False),
        sa.Column('implemented_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['target_set_id'], ['flashcard_sets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_recommendations_id'), 'learning_recommendations', ['id'], unique=False)

    # Create adaptive_learning_profiles table
    op.create_table('adaptive_learning_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('learning_style', sa.String(), nullable=True),
        sa.Column('preferred_difficulty', sa.Float(), nullable=True, default=0.5),
        sa.Column('study_preferences', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('knowledge_gaps', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('strength_areas', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('adaptive_algorithm_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_adaptive_learning_profiles_id'), 'adaptive_learning_profiles', ['id'], unique=False)

    # Create pronunciation_analysis table
    op.create_table('pronunciation_analysis',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('audio_url', sa.String(), nullable=True),
        sa.Column('accuracy_score', sa.Float(), nullable=True),
        sa.Column('fluency_score', sa.Float(), nullable=True),
        sa.Column('feedback', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pronunciation_analysis_id'), 'pronunciation_analysis', ['id'], unique=False)

    # Create user_analytics table
    op.create_table('user_analytics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('analytics_type', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_analytics_id'), 'user_analytics', ['id'], unique=False)

    # Create study_progress table
    op.create_table('study_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('set_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('study_time_minutes', sa.Integer(), nullable=True, default=0),
        sa.Column('cards_studied', sa.Integer(), nullable=True, default=0),
        sa.Column('correct_answers', sa.Integer(), nullable=True, default=0),
        sa.Column('incorrect_answers', sa.Integer(), nullable=True, default=0),
        sa.Column('accuracy_rate', sa.Float(), nullable=True, default=0.0),
        sa.Column('mastery_gained', sa.Float(), nullable=True, default=0.0),
        sa.Column('study_sessions', sa.Integer(), nullable=True, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['set_id'], ['flashcard_sets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_progress_id'), 'study_progress', ['id'], unique=False)

    # Create learning_insights table
    op.create_table('learning_insights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('insight_type', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True, default=1),
        sa.Column('is_read', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_insights_id'), 'learning_insights', ['id'], unique=False)

    # Create performance_metrics table
    op.create_table('performance_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('metric_name', sa.String(), nullable=False),
        sa.Column('metric_value', sa.Float(), nullable=False),
        sa.Column('metric_unit', sa.String(), nullable=True),
        sa.Column('context', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_performance_metrics_id'), 'performance_metrics', ['id'], unique=False)

    # Create study_goals table
    op.create_table('study_goals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('goal_type', sa.String(), nullable=False),
        sa.Column('target_value', sa.Float(), nullable=False),
        sa.Column('current_value', sa.Float(), nullable=True, default=0.0),
        sa.Column('unit', sa.String(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_goals_id'), 'study_goals', ['id'], unique=False)

    # Create learning_paths table
    op.create_table('learning_paths',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('path_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('current_step', sa.Integer(), nullable=True, default=0),
        sa.Column('total_steps', sa.Integer(), nullable=True, default=0),
        sa.Column('progress_percentage', sa.Float(), nullable=True, default=0.0),
        sa.Column('is_completed', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_learning_paths_id'), 'learning_paths', ['id'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index(op.f('ix_learning_paths_id'), table_name='learning_paths')
    op.drop_table('learning_paths')
    
    op.drop_index(op.f('ix_study_goals_id'), table_name='study_goals')
    op.drop_table('study_goals')
    
    op.drop_index(op.f('ix_performance_metrics_id'), table_name='performance_metrics')
    op.drop_table('performance_metrics')
    
    op.drop_index(op.f('ix_learning_insights_id'), table_name='learning_insights')
    op.drop_table('learning_insights')
    
    op.drop_index(op.f('ix_study_progress_id'), table_name='study_progress')
    op.drop_table('study_progress')
    
    op.drop_index(op.f('ix_user_analytics_id'), table_name='user_analytics')
    op.drop_table('user_analytics')
    
    op.drop_index(op.f('ix_pronunciation_analysis_id'), table_name='pronunciation_analysis')
    op.drop_table('pronunciation_analysis')
    
    op.drop_index(op.f('ix_adaptive_learning_profiles_id'), table_name='adaptive_learning_profiles')
    op.drop_table('adaptive_learning_profiles')
    
    op.drop_index(op.f('ix_learning_recommendations_id'), table_name='learning_recommendations')
    op.drop_table('learning_recommendations')
    
    op.drop_index(op.f('ix_content_generation_id'), table_name='content_generation')
    op.drop_table('content_generation')
    
    op.drop_index(op.f('ix_ai_messages_id'), table_name='ai_messages')
    op.drop_table('ai_messages')
    
    op.drop_index(op.f('ix_ai_conversations_id'), table_name='ai_conversations')
    op.drop_table('ai_conversations')
    
    op.drop_index(op.f('ix_set_sharings_id'), table_name='set_sharings')
    op.drop_table('set_sharings')
    
    op.drop_index(op.f('ix_learning_streaks_id'), table_name='learning_streaks')
    op.drop_table('learning_streaks')
    
    op.drop_index(op.f('ix_user_challenges_id'), table_name='user_challenges')
    op.drop_table('user_challenges')
    
    op.drop_index(op.f('ix_challenges_id'), table_name='challenges')
    op.drop_table('challenges')
    
    op.drop_index(op.f('ix_leaderboard_id'), table_name='leaderboard')
    op.drop_table('leaderboard')
    
    op.drop_index(op.f('ix_game_sessions_id'), table_name='game_sessions')
    op.drop_table('game_sessions')
    
    op.drop_index(op.f('ix_user_badges_id'), table_name='user_badges')
    op.drop_table('user_badges')
    
    op.drop_index(op.f('ix_badges_id'), table_name='badges')
    op.drop_table('badges')
    
    op.drop_index(op.f('ix_study_attempts_id'), table_name='study_attempts')
    op.drop_table('study_attempts')
    
    op.drop_index(op.f('ix_study_sessions_id'), table_name='study_sessions')
    op.drop_table('study_sessions')
    
    op.drop_index(op.f('ix_flashcards_id'), table_name='flashcards')
    op.drop_table('flashcards')
    
    op.drop_index(op.f('ix_flashcard_sets_id'), table_name='flashcard_sets')
    op.drop_table('flashcard_sets')
