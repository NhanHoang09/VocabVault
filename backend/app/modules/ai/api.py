"""
AI Module API
API endpoints for AI conversation, content generation, and adaptive learning
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.modules.auth.models import User
from app.modules.ai import schemas
from app.modules.ai.services import AIConversationService, AIChatService
from app.modules.ai.content_generation import ContentGenerationService
from app.modules.ai.adaptive_learning import AdaptiveLearningService
from app.modules.ai.tutor_sessions import AITutorSessionService

router = APIRouter()


# AI Conversation Endpoints
@router.post(
    "/ai/conversations",
    response_model=schemas.AIConversationResponse,
    summary="Create AI conversation",
    description="Create a new AI conversation session"
)
async def create_conversation(
    conversation: schemas.AIConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new AI conversation"""
    return AIConversationService.create_conversation(
        db=db,
        user_id=current_user.id,
        title=conversation.title,
        context_type=conversation.context_type,
        context_data=conversation.context_data
    )


@router.get(
    "/ai/conversations",
    response_model=schemas.AIConversationListResponse,
    summary="Get user conversations",
    description="Get all AI conversations for the current user"
)
async def get_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all AI conversations for the user"""
    conversations = AIConversationService.get_user_conversations(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    total = len(conversations)  # In a real app, you'd get total count separately
    
    return schemas.AIConversationListResponse(
        conversations=conversations,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get(
    "/ai/conversations/{conversation_id}",
    response_model=schemas.AIConversationResponse,
    summary="Get conversation",
    description="Get a specific AI conversation by ID"
)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific AI conversation"""
    conversation = AIConversationService.get_conversation(
        db=db, conversation_id=conversation_id, user_id=current_user.id
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.get(
    "/ai/conversations/{conversation_id}/messages",
    response_model=List[schemas.AIMessageResponse],
    summary="Get conversation messages",
    description="Get all messages in a conversation"
)
async def get_conversation_messages(
    conversation_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get messages in a conversation"""
    # Verify conversation belongs to user
    conversation = AIConversationService.get_conversation(
        db=db, conversation_id=conversation_id, user_id=current_user.id
    )
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return AIConversationService.get_conversation_messages(
        db=db, conversation_id=conversation_id, skip=skip, limit=limit
    )


@router.post(
    "/ai/chat",
    response_model=schemas.AIChatResponse,
    summary="Chat with AI",
    description="Send a message to AI and get a response"
)
async def chat_with_ai(
    chat_request: schemas.AIChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Chat with AI tutor"""
    return AIChatService.chat_with_ai(
        db=db,
        user_id=current_user.id,
        message=chat_request.message,
        conversation_id=chat_request.conversation_id,
        context_type=chat_request.context_type,
        context_data=chat_request.context_data
    )


# Content Generation Endpoints
@router.post(
    "/ai/generate/flashcards",
    response_model=schemas.ContentGenerationResponse,
    summary="Generate flashcards from text",
    description="Use AI to generate flashcards from provided text"
)
async def generate_flashcards(
    request: schemas.FlashcardGenerationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate flashcards from text using AI"""
    return ContentGenerationService.generate_flashcards_from_text(
        db=db,
        user_id=current_user.id,
        source_text=request.source_text,
        title=request.title,
        description=request.description,
        category=request.category,
        tags=request.tags,
        difficulty=request.difficulty,
        num_cards=request.num_cards
    )


@router.post(
    "/ai/generate/study-plan",
    response_model=schemas.ContentGenerationResponse,
    summary="Generate study plan",
    description="Generate a personalized study plan for a flashcard set"
)
async def generate_study_plan(
    request: schemas.StudyPlanGenerationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate a personalized study plan"""
    return ContentGenerationService.generate_study_plan(
        db=db,
        user_id=current_user.id,
        set_id=request.set_id,
        study_duration_minutes=request.study_duration_minutes,
        target_accuracy=request.target_accuracy,
        preferred_mode=request.preferred_mode
    )


@router.post(
    "/ai/generate/explanation",
    response_model=schemas.ContentGenerationResponse,
    summary="Generate explanation",
    description="Generate an AI explanation for a concept"
)
async def generate_explanation(
    concept: str,
    context: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate an AI explanation for a concept"""
    return ContentGenerationService.generate_explanation(
        db=db,
        user_id=current_user.id,
        concept=concept,
        context=context
    )


@router.post(
    "/ai/content/{content_id}/import",
    summary="Import generated content",
    description="Import AI-generated flashcards into a new flashcard set"
)
async def import_generated_content(
    content_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Import AI-generated flashcards"""
    flashcard_set = ContentGenerationService.import_generated_flashcards(
        db=db,
        user_id=current_user.id,
        generated_content_id=content_id
    )
    return {"message": "Content imported successfully", "flashcard_set_id": flashcard_set.id}


@router.get(
    "/ai/generated-content",
    response_model=schemas.GeneratedContentListResponse,
    summary="Get generated content",
    description="Get all AI-generated content for the user"
)
async def get_generated_content(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all generated content for the user"""
    from app.modules.ai.models import GeneratedContent
    from sqlalchemy import desc
    
    content = db.query(GeneratedContent).filter(
        GeneratedContent.user_id == current_user.id
    ).order_by(desc(GeneratedContent.created_at)).offset(skip).limit(limit).all()
    
    total = db.query(GeneratedContent).filter(
        GeneratedContent.user_id == current_user.id
    ).count()
    
    return schemas.GeneratedContentListResponse(
        content=content,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


# Learning Profile Endpoints
@router.post(
    "/ai/adaptive/profile",
    response_model=schemas.LearningProfileResponse,
    summary="Create learning profile",
    description="Create or update user's learning profile"
)
async def create_learning_profile(
    profile: schemas.LearningProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create or update learning profile"""
    return AdaptiveLearningService.create_or_update_learning_profile(
        db=db,
        user_id=current_user.id,
        preferred_study_mode=profile.preferred_study_mode,
        preferred_difficulty=profile.preferred_difficulty,
        study_session_duration=profile.study_session_duration,
        daily_study_goal=profile.daily_study_goal
    )


@router.get(
    "/ai/adaptive/profile",
    response_model=schemas.LearningProfileResponse,
    summary="Get learning profile",
    description="Get user's learning profile"
)
async def get_learning_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get learning profile"""
    profile = AdaptiveLearningService.get_learning_profile(db=db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Learning profile not found")
    return profile


@router.put(
    "/ai/adaptive/profile",
    response_model=schemas.LearningProfileResponse,
    summary="Update learning profile",
    description="Update user's learning profile"
)
async def update_learning_profile(
    profile_update: schemas.LearningProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update learning profile"""
    profile = AdaptiveLearningService.get_learning_profile(db=db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Learning profile not found")
    
    # Update fields
    if profile_update.preferred_study_mode is not None:
        profile.preferred_study_mode = profile_update.preferred_study_mode
    if profile_update.preferred_difficulty is not None:
        profile.preferred_difficulty = profile_update.preferred_difficulty
    if profile_update.study_session_duration is not None:
        profile.study_session_duration = profile_update.study_session_duration
    if profile_update.daily_study_goal is not None:
        profile.daily_study_goal = profile_update.daily_study_goal
    
    db.commit()
    db.refresh(profile)
    return profile


@router.post(
    "/ai/adaptive/analyze",
    summary="Analyze learning patterns",
    description="Analyze user's learning patterns and update profile"
)
async def analyze_learning_patterns(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Analyze learning patterns"""
    return AdaptiveLearningService.analyze_learning_patterns(db=db, user_id=current_user.id)


@router.post(
    "/ai/adaptive/recommendations/generate",
    response_model=List[schemas.AdaptiveRecommendationResponse],
    summary="Generate recommendations",
    description="Generate personalized learning recommendations"
)
async def generate_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate personalized recommendations"""
    return AdaptiveLearningService.generate_recommendations(db=db, user_id=current_user.id)


@router.get(
    "/ai/adaptive/recommendations",
    response_model=schemas.AdaptiveRecommendationListResponse,
    summary="Get recommendations",
    description="Get user's learning recommendations"
)
async def get_recommendations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's recommendations"""
    recommendations = AdaptiveLearningService.get_user_recommendations(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    
    return schemas.AdaptiveRecommendationListResponse(
        recommendations=recommendations,
        total=len(recommendations),
        page=skip // limit + 1,
        size=limit
    )


@router.put(
    "/ai/adaptive/recommendations/{recommendation_id}/apply",
    response_model=schemas.AdaptiveRecommendationResponse,
    summary="Apply recommendation",
    description="Mark a recommendation as applied"
)
async def apply_recommendation(
    recommendation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Apply a recommendation"""
    return AdaptiveLearningService.mark_recommendation_applied(
        db=db, user_id=current_user.id, recommendation_id=recommendation_id
    )


@router.get(
    "/ai/adaptive/insights",
    summary="Get learning insights",
    description="Get comprehensive learning insights for the user"
)
async def get_learning_insights(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get learning insights"""
    return AdaptiveLearningService.get_learning_insights(db=db, user_id=current_user.id)


# AI Tutor Session Endpoints
@router.post(
    "/ai/tutor/sessions",
    response_model=schemas.AITutorSessionResponse,
    summary="Create tutor session",
    description="Create a new AI tutor session"
)
async def create_tutor_session(
    session: schemas.AITutorSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new AI tutor session"""
    return AITutorSessionService.create_tutor_session(
        db=db,
        user_id=current_user.id,
        session_type=session.session_type,
        set_id=session.set_id,
        difficulty_level=session.difficulty_level,
        target_accuracy=session.target_accuracy
    )


@router.get(
    "/ai/tutor/sessions",
    response_model=schemas.AITutorSessionListResponse,
    summary="Get tutor sessions",
    description="Get all AI tutor sessions for the user"
)
async def get_tutor_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all tutor sessions for the user"""
    sessions = AITutorSessionService.get_user_tutor_sessions(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    
    return schemas.AITutorSessionListResponse(
        sessions=sessions,
        total=len(sessions),
        page=skip // limit + 1,
        size=limit
    )


@router.get(
    "/ai/tutor/sessions/{session_id}",
    response_model=schemas.AITutorSessionResponse,
    summary="Get tutor session",
    description="Get a specific AI tutor session"
)
async def get_tutor_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific tutor session"""
    session = AITutorSessionService.get_tutor_session(
        db=db, session_id=session_id, user_id=current_user.id
    )
    if not session:
        raise HTTPException(status_code=404, detail="Tutor session not found")
    return session


@router.get(
    "/ai/tutor/sessions/{session_id}/plan",
    summary="Get study plan",
    description="Get the guided study plan for a tutor session"
)
async def get_study_plan(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get guided study plan for a tutor session"""
    return AITutorSessionService.get_guided_study_plan(
        db=db, session_id=session_id, user_id=current_user.id
    )


@router.put(
    "/ai/tutor/sessions/{session_id}/progress",
    response_model=schemas.AITutorSessionResponse,
    summary="Update session progress",
    description="Update the progress of an AI tutor session"
)
async def update_session_progress(
    session_id: int,
    progress_update: schemas.AITutorSessionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update session progress"""
    return AITutorSessionService.update_session_progress(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        current_accuracy=progress_update.current_accuracy,
        cards_studied=progress_update.cards_studied,
        is_completed=progress_update.is_completed
    )


@router.post(
    "/ai/tutor/sessions/{session_id}/complete",
    response_model=schemas.AITutorSessionResponse,
    summary="Complete session",
    description="Complete an AI tutor session"
)
async def complete_session(
    session_id: int,
    final_accuracy: float,
    total_cards_studied: int,
    session_data: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Complete a tutor session"""
    return AITutorSessionService.complete_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        final_accuracy=final_accuracy,
        total_cards_studied=total_cards_studied,
        session_data=session_data
    )


@router.get(
    "/ai/tutor/recommendations",
    summary="Get session recommendations",
    description="Get personalized session recommendations"
)
async def get_session_recommendations(
    set_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get session recommendations"""
    return AITutorSessionService.get_session_recommendations(
        db=db, user_id=current_user.id, set_id=set_id
    )


@router.get(
    "/ai/tutor/analytics",
    summary="Get session analytics",
    description="Get analytics for AI tutor sessions"
)
async def get_session_analytics(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get session analytics"""
    return AITutorSessionService.get_session_analytics(
        db=db, user_id=current_user.id, days=days
    )
