"""
Content Generation Service
AI-powered content generation for flashcards, study plans, and educational materials
"""
import openai
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.core.config import settings
from app.modules.ai.models import GeneratedContent
from app.modules.flashcards.models import FlashcardSet, Flashcard, StudySession
from app.modules.ai.models import LearningProfile
from app.core.exceptions import VocabularyVaultException

logger = logging.getLogger(__name__)


class ContentGenerationService:
    """Service for AI content generation"""
    
    @staticmethod
    def generate_flashcards_from_text(
        db: Session, 
        user_id: int, 
        source_text: str, 
        title: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        difficulty: str = "medium",
        num_cards: int = 10
    ) -> GeneratedContent:
        """Generate flashcards from text using AI"""
        if not settings.OPENAI_API_KEY:
            raise VocabularyVaultException(
                status_code=503,
                detail="AI service is not available. Please configure OpenAI API key."
            )
        
        try:
            # Create prompt for flashcard generation
            prompt = f"""
            Generate {num_cards} vocabulary flashcards from the following text:
            
            Text: {source_text}
            
            Requirements:
            - Create {num_cards} flashcards
            - Each flashcard should have a term/concept and its definition/explanation
            - Difficulty level: {difficulty}
            - Make the content educational and clear
            - Focus on key vocabulary and important concepts
            
            Return the result as a JSON array with this format:
            [
                {{
                    "front": "term or concept",
                    "back": "definition or explanation"
                }}
            ]
            """
            
            # Generate content using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            try:
                flashcards_data = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: try to extract JSON from response
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    flashcards_data = json.loads(json_match.group())
                else:
                    raise ValueError("Failed to parse AI response as JSON")
            
            # Create generated content record
            generated_content = GeneratedContent(
                user_id=user_id,
                content_type="flashcard_set",
                source_text=source_text,
                generated_data={
                    "title": title,
                    "description": description,
                    "category": category,
                    "tags": tags or [],
                    "difficulty": difficulty,
                    "flashcards": flashcards_data
                },
                generation_metadata={
                    "model": "gpt-3.5-turbo",
                    "num_cards": num_cards,
                    "generation_time": datetime.now().isoformat()
                }
            )
            
            db.add(generated_content)
            db.commit()
            db.refresh(generated_content)
            
            return generated_content
            
        except Exception as e:
            logger.error(f"Error generating flashcards: {str(e)}")
            raise VocabularyVaultException(
                status_code=500,
                detail="Failed to generate flashcards. Please try again."
            )
    
    @staticmethod
    def generate_study_plan(
        db: Session, 
        user_id: int, 
        set_id: int,
        study_duration_minutes: int = 30,
        target_accuracy: float = 0.8,
        preferred_mode: Optional[str] = None
    ) -> GeneratedContent:
        """Generate a personalized study plan"""
        # Get flashcard set
        flashcard_set = db.query(FlashcardSet).filter(
            and_(
                FlashcardSet.id == set_id,
                FlashcardSet.user_id == user_id
            )
        ).first()
        
        if not flashcard_set:
            raise VocabularyVaultException(
                status_code=404,
                detail="Flashcard set not found"
            )
        
        # Get user's learning profile
        learning_profile = db.query(LearningProfile).filter(
            LearningProfile.user_id == user_id
        ).first()
        
        # Get recent study data
        recent_sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.set_id == set_id,
                StudySession.start_time >= datetime.now() - timedelta(days=7)
            )
        ).all()
        
        # Generate study plan using AI
        if settings.OPENAI_API_KEY:
            try:
                prompt = f"""
                Create a personalized study plan for a vocabulary learning session.
                
                Set Information:
                - Title: {flashcard_set.title}
                - Total cards: {flashcard_set.total_cards}
                - Category: {flashcard_set.category or 'General'}
                
                User Preferences:
                - Study duration: {study_duration_minutes} minutes
                - Target accuracy: {target_accuracy * 100}%
                - Preferred mode: {preferred_mode or 'adaptive'}
                - Learning profile: {learning_profile.preferred_study_mode if learning_profile else 'flashcards'}
                
                Recent Performance:
                - Recent sessions: {len(recent_sessions)}
                - Average accuracy: {sum(s.accuracy_rate or 0 for s in recent_sessions) / len(recent_sessions) if recent_sessions else 0:.2f}
                
                Create a detailed study plan with:
                1. Recommended study modes and their duration
                2. Card selection strategy
                3. Break intervals
                4. Success criteria
                5. Tips for improvement
                
                Return as JSON:
                {{
                    "plan": {{
                        "duration_minutes": {study_duration_minutes},
                        "target_accuracy": {target_accuracy},
                        "phases": [
                            {{
                                "phase": "warmup",
                                "duration_minutes": 5,
                                "mode": "flashcards",
                                "description": "..."
                            }}
                        ],
                        "tips": ["..."],
                        "success_criteria": "..."
                    }}
                }}
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800,
                    temperature=0.7
                )
                
                content = response.choices[0].message.content.strip()
                study_plan_data = json.loads(content)
                
            except Exception as e:
                logger.error(f"Error generating study plan: {str(e)}")
                # Fallback to basic study plan
                study_plan_data = ContentGenerationService._create_basic_study_plan(
                    study_duration_minutes, target_accuracy, preferred_mode
                )
        else:
            # Basic study plan without AI
            study_plan_data = ContentGenerationService._create_basic_study_plan(
                study_duration_minutes, target_accuracy, preferred_mode
            )
        
        # Create generated content record
        generated_content = GeneratedContent(
            user_id=user_id,
            content_type="study_plan",
            source_text=f"Study plan for set: {flashcard_set.title}",
            generated_data=study_plan_data,
                            generation_metadata={
                    "set_id": set_id,
                    "generation_time": datetime.now().isoformat()
                }
        )
        
        db.add(generated_content)
        db.commit()
        db.refresh(generated_content)
        
        return generated_content
    
    @staticmethod
    def _create_basic_study_plan(
        duration_minutes: int, 
        target_accuracy: float, 
        preferred_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a basic study plan without AI"""
        mode = preferred_mode or "flashcards"
        
        return {
            "plan": {
                "duration_minutes": duration_minutes,
                "target_accuracy": target_accuracy,
                "phases": [
                    {
                        "phase": "warmup",
                        "duration_minutes": min(5, duration_minutes // 4),
                        "mode": mode,
                        "description": "Start with familiar cards to build confidence"
                    },
                    {
                        "phase": "main_study",
                        "duration_minutes": duration_minutes - min(10, duration_minutes // 2),
                        "mode": mode,
                        "description": "Focus on learning new and challenging cards"
                    },
                    {
                        "phase": "review",
                        "duration_minutes": min(5, duration_minutes // 4),
                        "mode": mode,
                        "description": "Review difficult cards and reinforce learning"
                    }
                ],
                "tips": [
                    "Take short breaks between phases",
                    "Focus on understanding, not just memorization",
                    "Review incorrect answers carefully"
                ],
                "success_criteria": f"Achieve {target_accuracy * 100}% accuracy and complete all phases"
            }
        }
    
    @staticmethod
    def generate_explanation(
        db: Session,
        user_id: int,
        concept: str,
        context: Optional[str] = None
    ) -> GeneratedContent:
        """Generate an AI explanation for a concept"""
        if not settings.OPENAI_API_KEY:
            raise VocabularyVaultException(
                status_code=503,
                detail="AI service is not available. Please configure OpenAI API key."
            )
        
        try:
            prompt = f"""
            Provide a clear and educational explanation for the concept: "{concept}"
            
            {f"Context: {context}" if context else ""}
            
            Requirements:
            - Make it easy to understand
            - Include examples if helpful
            - Keep it concise but comprehensive
            - Focus on vocabulary learning context
            
            Return as JSON:
            {{
                "concept": "{concept}",
                "explanation": "detailed explanation here",
                "examples": ["example 1", "example 2"],
                "related_terms": ["term1", "term2"],
                "difficulty_level": "medium"
            }}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            explanation_data = json.loads(content)
            
            # Create generated content record
            generated_content = GeneratedContent(
                user_id=user_id,
                content_type="explanation",
                source_text=concept,
                generated_data=explanation_data,
                generation_metadata={
                    "model": "gpt-3.5-turbo",
                    "generation_time": datetime.now().isoformat()
                }
            )
            
            db.add(generated_content)
            db.commit()
            db.refresh(generated_content)
            
            return generated_content
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            raise VocabularyVaultException(
                status_code=500,
                detail="Failed to generate explanation. Please try again."
            )
    
    @staticmethod
    def import_generated_flashcards(
        db: Session,
        user_id: int,
        generated_content_id: int
    ) -> FlashcardSet:
        """Import AI-generated flashcards into a new flashcard set"""
        # Get generated content
        generated_content = db.query(GeneratedContent).filter(
            and_(
                GeneratedContent.id == generated_content_id,
                GeneratedContent.user_id == user_id,
                GeneratedContent.content_type == "flashcard_set"
            )
        ).first()
        
        if not generated_content:
            raise VocabularyVaultException(
                status_code=404,
                detail="Generated content not found"
            )
        
        if generated_content.is_imported:
            raise VocabularyVaultException(
                status_code=400,
                detail="Content has already been imported"
            )
        
        # Create new flashcard set
        data = generated_content.generated_data
        flashcard_set = FlashcardSet(
            user_id=user_id,
            title=data["title"],
            description=data.get("description"),
            category=data.get("category"),
            tags=data.get("tags", []),
            total_cards=len(data["flashcards"])
        )
        
        db.add(flashcard_set)
        db.flush()  # Get the ID
        
        # Create flashcards
        for card_data in data["flashcards"]:
            flashcard = Flashcard(
                set_id=flashcard_set.id,
                front_content=card_data["front"],
                back_content=card_data["back"],
                difficulty=data.get("difficulty", "medium")
            )
            db.add(flashcard)
        
        # Mark as imported
        generated_content.is_imported = True
        
        db.commit()
        db.refresh(flashcard_set)
        
        return flashcard_set
