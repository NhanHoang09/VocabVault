"""
AI Module Services
Services for AI conversation, content generation, and adaptive learning
"""
import openai
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from app.core.config import settings
from app.modules.ai.models import (
    AIConversation, AIMessage, GeneratedContent, LearningProfile,
    AdaptiveRecommendation, AITutorSession
)
from app.modules.flashcards.models import FlashcardSet, Flashcard, StudySession, StudyAttempt
from app.modules.analytics.models import UserAnalytics, StudyProgress
from app.modules.auth.models import User
from app.core.exceptions import VocabularyVaultException

logger = logging.getLogger(__name__)

# Initialize OpenAI client
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
else:
    logger.warning("OpenAI API key not configured. AI features will be limited.")


class AIConversationService:
    """Service for managing AI conversations"""
    
    @staticmethod
    def create_conversation(
        db: Session, 
        user_id: int, 
        title: str, 
        context_type: str = "general",
        context_data: Optional[Dict[str, Any]] = None
    ) -> AIConversation:
        """Create a new AI conversation"""
        conversation = AIConversation(
            user_id=user_id,
            title=title,
            context_type=context_type,
            context_data=context_data
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    def get_conversation(db: Session, conversation_id: int, user_id: int) -> Optional[AIConversation]:
        """Get a conversation by ID for a specific user"""
        return db.query(AIConversation).filter(
            and_(
                AIConversation.id == conversation_id,
                AIConversation.user_id == user_id
            )
        ).first()
    
    @staticmethod
    def get_user_conversations(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[AIConversation]:
        """Get all conversations for a user"""
        return db.query(AIConversation).filter(
            AIConversation.user_id == user_id
        ).order_by(desc(AIConversation.updated_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def add_message(
        db: Session, 
        conversation_id: int, 
        role: str, 
        content: str,
        message_metadata: Optional[Dict[str, Any]] = None
    ) -> AIMessage:
        """Add a message to a conversation"""
        message = AIMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
            message_metadata=message_metadata
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    @staticmethod
    def get_conversation_messages(
        db: Session, 
        conversation_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[AIMessage]:
        """Get messages for a conversation"""
        return db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation_id
        ).order_by(AIMessage.created_at).offset(skip).limit(limit).all()


class AIChatService:
    """Service for AI chat functionality"""
    
    @staticmethod
    def generate_ai_response(
        messages: List[Dict[str, str]], 
        context_type: str = "general",
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate AI response using OpenAI"""
        if not settings.OPENAI_API_KEY:
            raise VocabularyVaultException(
                status_code=503,
                detail="AI service is not available. Please configure OpenAI API key."
            )
        
        try:
            # Build system prompt based on context
            system_prompt = AIChatService._build_system_prompt(context_type, context_data)
            
            # Prepare messages for OpenAI
            openai_messages = [{"role": "system", "content": system_prompt}]
            openai_messages.extend(messages)
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=openai_messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            raise VocabularyVaultException(
                status_code=500,
                detail="Failed to generate AI response. Please try again."
            )
    
    @staticmethod
    def _build_system_prompt(context_type: str, context_data: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt based on context type"""
        base_prompt = """You are an AI tutor for a vocabulary learning application called "My Vocabulary Vault". 
        You help users learn and understand vocabulary through various study methods. Be helpful, encouraging, and educational."""
        
        if context_type == "study_help":
            base_prompt += "\n\nYou are helping with study techniques and learning strategies. Provide practical advice and motivation."
        elif context_type == "flashcard_explanation":
            base_prompt += "\n\nYou are explaining vocabulary concepts and providing additional context for flashcards. Be clear and educational."
        elif context_type == "content_generation":
            base_prompt += "\n\nYou are helping to generate educational content like flashcards, quizzes, and study materials."
        
        return base_prompt
    
    @staticmethod
    def chat_with_ai(
        db: Session, 
        user_id: int, 
        message: str, 
        conversation_id: Optional[int] = None,
        context_type: str = "general",
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle a chat interaction with AI"""
        # Get or create conversation
        if conversation_id:
            conversation = AIConversationService.get_conversation(db, conversation_id, user_id)
            if not conversation:
                raise VocabularyVaultException(
                    status_code=404,
                    detail="Conversation not found"
                )
        else:
            # Create new conversation
            title = f"AI Chat - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            conversation = AIConversationService.create_conversation(
                db, user_id, title, context_type, context_data
            )
        
        # Add user message
        user_message = AIConversationService.add_message(
            db, conversation.id, "user", message
        )
        
        # Get conversation history
        messages = AIConversationService.get_conversation_messages(db, conversation.id)
        
        # Prepare messages for AI
        ai_messages = []
        for msg in messages[-10:]:  # Last 10 messages for context
            ai_messages.append({"role": msg.role, "content": msg.content})
        
        # Generate AI response
        ai_response_content = AIChatService.generate_ai_response(
            ai_messages, context_type, context_data
        )
        
        # Add AI response
        ai_message = AIConversationService.add_message(
            db, conversation.id, "assistant", ai_response_content
        )
        
        return {
            "conversation_id": conversation.id,
            "message": user_message,
            "response": ai_message
        }
