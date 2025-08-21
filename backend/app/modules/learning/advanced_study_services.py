"""
Advanced Study Modes Services
Services for Spell Mode and Test Mode
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import random
import re

from app.modules.flashcards.models import Flashcard
from app.modules.flashcards.schemas import (
    SpellModeAnswer, SpellModeAnswerResponse, SpellModeProgress,
    TestSessionCreate, TestSessionResponse, TestResult, TestQuestion,
    TestQuestionResponse, QuestionType
)
from app.modules.learning.services import StudySessionService, StudyAttemptService, StudyAttemptCreate


class SpellModeService:
    """Service for Spell Mode study sessions"""
    
    @staticmethod
    def submit_spell_answer(
        db: Session,
        user_id: int,
        answer_data: SpellModeAnswer
    ) -> SpellModeAnswerResponse:
        """Submit a spell mode answer and get feedback"""
        # Get the flashcard
        flashcard = db.query(Flashcard).filter(Flashcard.id == answer_data.card_id).first()
        if not flashcard:
            raise ValueError("Flashcard not found")
        
        # Check spelling accuracy
        is_correct = answer_data.user_spelling.lower().strip() == flashcard.back_content.lower().strip()
        
        # Generate phonetic feedback
        phonetic_feedback = SpellModeService._generate_phonetic_feedback(
            answer_data.user_spelling,
            flashcard.back_content
        )
        
        # Generate pronunciation tips
        pronunciation_tips = SpellModeService._generate_pronunciation_tips(
            flashcard.back_content
        )
        
        # Create study attempt
        study_attempt = StudyAttemptService.create_study_attempt(
            db=db,
            user_id=user_id,
            attempt_data=StudyAttemptCreate(
                card_id=answer_data.card_id,
                session_id=answer_data.session_id,
                user_answer=answer_data.user_spelling,
                is_correct=is_correct,
                response_time_seconds=answer_data.response_time_seconds
            )
        )
        
        return SpellModeAnswerResponse(
            card_id=answer_data.card_id,
            user_spelling=answer_data.user_spelling,
            correct_spelling=flashcard.back_content,
            is_correct=is_correct,
            phonetic_feedback=phonetic_feedback,
            pronunciation_tips=pronunciation_tips,
            response_time_seconds=answer_data.response_time_seconds or 0.0,
            created_at=study_attempt.created_at
        )
    
    @staticmethod
    def get_spell_progress(
        db: Session,
        session_id: int,
        user_id: int
    ) -> SpellModeProgress:
        """Get spell mode progress for a session"""
        # Get session
        session = StudySessionService.get_study_session_by_id(db, session_id, user_id)
        if not session:
            raise ValueError("Study session not found")
        
        # Get total cards in set
        total_cards = db.query(Flashcard).filter(Flashcard.set_id == session.set_id).count()
        
        # Get attempts for this session
        attempts = StudyAttemptService.get_session_attempts(db, session_id, user_id, limit=1000)
        
        cards_answered = len(attempts)
        correct_spellings = sum(1 for attempt in attempts if attempt.is_correct)
        accuracy_percentage = (correct_spellings / cards_answered * 100) if cards_answered > 0 else 0
        
        # Calculate average response time
        response_times = [attempt.response_time_seconds for attempt in attempts if attempt.response_time_seconds]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Count audio plays (this would need to be tracked separately)
        audio_plays_count = 0  # TODO: Implement audio play tracking
        
        return SpellModeProgress(
            session_id=session_id,
            total_cards=total_cards,
            cards_answered=cards_answered,
            correct_spellings=correct_spellings,
            accuracy_percentage=accuracy_percentage,
            average_response_time=average_response_time,
            audio_plays_count=audio_plays_count
        )
    
    @staticmethod
    def _generate_phonetic_feedback(user_spelling: str, correct_spelling: str) -> str:
        """Generate phonetic feedback for spelling"""
        if user_spelling.lower().strip() == correct_spelling.lower().strip():
            return "Perfect spelling!"
        
        # Simple phonetic feedback based on common mistakes
        user_words = user_spelling.lower().split()
        correct_words = correct_spelling.lower().split()
        
        if len(user_words) != len(correct_words):
            return f"Check the number of words. You wrote {len(user_words)}, but there should be {len(correct_words)}."
        
        feedback_parts = []
        for i, (user_word, correct_word) in enumerate(zip(user_words, correct_words)):
            if user_word != correct_word:
                feedback_parts.append(f"Word {i+1}: '{user_word}' should be '{correct_word}'")
        
        return " ".join(feedback_parts) if feedback_parts else "Check your spelling carefully."
    
    @staticmethod
    def _generate_pronunciation_tips(word: str) -> List[str]:
        """Generate pronunciation tips for a word"""
        tips = []
        
        # Simple pronunciation tips based on word patterns
        if any(char in word.lower() for char in ['th', 'ch', 'sh', 'ph']):
            tips.append("Pay attention to consonant combinations")
        
        if word.lower().endswith('e'):
            tips.append("The final 'e' is often silent")
        
        if len(word) > 8:
            tips.append("Break the word into syllables")
        
        if any(char in word.lower() for char in ['a', 'e', 'i', 'o', 'u']):
            tips.append("Focus on vowel sounds")
        
        return tips


class TestModeService:
    """Service for Test Mode study sessions"""
    
    @staticmethod
    def create_test_session(
        db: Session,
        user_id: int,
        test_data: TestSessionCreate
    ) -> TestSessionResponse:
        """Create a new test session"""
        # Verify flashcard set exists
        flashcard_set = db.query(Flashcard).filter(Flashcard.set_id == test_data.set_id).first()
        if not flashcard_set:
            raise ValueError("Flashcard set not found")
        
        # Create test session
        test_session = TestSessionResponse(
            id=0,  # Will be set by database
            user_id=user_id,
            set_id=test_data.set_id,
            question_count=test_data.question_count,
            time_limit_minutes=test_data.time_limit_minutes,
            include_explanations=test_data.include_explanations,
            started_at=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        
        # TODO: Store test session in database
        # For now, return the response object
        return test_session
    
    @staticmethod
    def generate_test_questions(
        db: Session,
        set_id: int,
        question_count: int,
        question_types: Optional[List[QuestionType]] = None
    ) -> List[TestQuestion]:
        """Generate test questions from flashcard set"""
        # Get flashcards from the set
        flashcards = db.query(Flashcard).filter(Flashcard.set_id == set_id).all()
        
        if not flashcards:
            raise ValueError("No flashcards found in set")
        
        # Use all question types if none specified
        if not question_types:
            question_types = [QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE, QuestionType.FILL_IN_BLANK]
        
        questions = []
        used_cards = set()
        
        for i in range(min(question_count, len(flashcards))):
            # Select a random card that hasn't been used
            available_cards = [card for card in flashcards if card.id not in used_cards]
            if not available_cards:
                break
            
            card = random.choice(available_cards)
            used_cards.add(card.id)
            
            # Generate question based on type
            question_type = random.choice(question_types)
            question = TestModeService._generate_question(card, question_type, flashcards)
            questions.append(question)
        
        return questions
    
    @staticmethod
    def _generate_question(card: Flashcard, question_type: QuestionType, all_cards: List[Flashcard]) -> TestQuestion:
        """Generate a specific type of question from a flashcard"""
        if question_type == QuestionType.MULTIPLE_CHOICE:
            return TestModeService._generate_multiple_choice(card, all_cards)
        elif question_type == QuestionType.TRUE_FALSE:
            return TestModeService._generate_true_false(card)
        elif question_type == QuestionType.FILL_IN_BLANK:
            return TestModeService._generate_fill_in_blank(card)
        else:
            return TestModeService._generate_multiple_choice(card, all_cards)  # Default
    
    @staticmethod
    def _generate_multiple_choice(card: Flashcard, all_cards: List[Flashcard]) -> TestQuestion:
        """Generate a multiple choice question"""
        # Get 3 wrong answers from other cards
        other_cards = [c for c in all_cards if c.id != card.id]
        wrong_answers = random.sample([c.back_content for c in other_cards], min(3, len(other_cards)))
        
        # Add correct answer and shuffle
        options = wrong_answers + [card.back_content]
        random.shuffle(options)
        
        return TestQuestion(
            id=card.id,
            question_type=QuestionType.MULTIPLE_CHOICE,
            question_text=f"What is the meaning of: {card.front_content}?",
            options=options,
            correct_answer=card.back_content,
            explanation=f"The correct answer is '{card.back_content}'",
            difficulty=card.difficulty or "medium",
            points=1
        )
    
    @staticmethod
    def _generate_true_false(card: Flashcard) -> TestQuestion:
        """Generate a true/false question"""
        # Randomly decide if the statement will be true or false
        is_true = random.choice([True, False])
        
        if is_true:
            question_text = f"'{card.front_content}' means '{card.back_content}'"
            correct_answer = "True"
        else:
            # Generate a wrong meaning
            wrong_meanings = ["something else", "the opposite", "a different concept"]
            wrong_meaning = random.choice(wrong_meanings)
            question_text = f"'{card.front_content}' means '{wrong_meaning}'"
            correct_answer = "False"
        
        return TestQuestion(
            id=card.id,
            question_type=QuestionType.TRUE_FALSE,
            question_text=question_text,
            options=["True", "False"],
            correct_answer=correct_answer,
            explanation=f"The correct meaning is '{card.back_content}'",
            difficulty=card.difficulty or "medium",
            points=1
        )
    
    @staticmethod
    def _generate_fill_in_blank(card: Flashcard) -> TestQuestion:
        """Generate a fill-in-the-blank question"""
        return TestQuestion(
            id=card.id,
            question_type=QuestionType.FILL_IN_BLANK,
            question_text=f"Complete: {card.front_content} = _____",
            correct_answer=card.back_content,
            explanation=f"The answer is '{card.back_content}'",
            difficulty=card.difficulty or "medium",
            points=1
        )
    
    @staticmethod
    def calculate_test_result(
        question_results: List[TestQuestionResponse],
        time_taken_seconds: int
    ) -> TestResult:
        """Calculate test results and generate analysis"""
        total_score = sum(result.points_earned for result in question_results)
        max_score = len(question_results)
        correct_answers = sum(1 for result in question_results if result.is_correct)
        accuracy_percentage = (correct_answers / len(question_results) * 100) if question_results else 0
        
        # Generate performance analysis
        performance_analysis = TestModeService._analyze_performance(question_results, time_taken_seconds)
        
        # Generate recommendations
        recommendations = TestModeService._generate_recommendations(accuracy_percentage, performance_analysis)
        
        return TestResult(
            test_session_id=0,  # Would be set from actual session
            total_score=total_score,
            max_score=max_score,
            accuracy_percentage=accuracy_percentage,
            time_taken_seconds=time_taken_seconds,
            questions_answered=len(question_results),
            correct_answers=correct_answers,
            question_results=question_results,
            performance_analysis=performance_analysis,
            recommendations=recommendations
        )
    
    @staticmethod
    def _analyze_performance(question_results: List[TestQuestionResponse], time_taken: int) -> Dict[str, Any]:
        """Analyze test performance"""
        response_times = [result.response_time_seconds for result in question_results]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Analyze by question type
        type_performance = {}
        for result in question_results:
            # This would need question type information
            pass
        
        return {
            "average_response_time": avg_response_time,
            "total_time_taken": time_taken,
            "questions_per_minute": len(question_results) / (time_taken / 60) if time_taken > 0 else 0,
            "type_performance": type_performance
        }
    
    @staticmethod
    def _generate_recommendations(accuracy: float, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on performance"""
        recommendations = []
        
        if accuracy < 60:
            recommendations.append("Focus on reviewing difficult concepts")
            recommendations.append("Consider using flashcards mode for practice")
        elif accuracy < 80:
            recommendations.append("Good progress! Review areas of weakness")
            recommendations.append("Try write mode to improve recall")
        else:
            recommendations.append("Excellent performance! Keep up the good work")
            recommendations.append("Consider challenging yourself with harder questions")
        
        if analysis.get("average_response_time", 0) > 10:
            recommendations.append("Work on improving response speed")
        
        return recommendations
