from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_pagination_params
from app.modules.auth.models import User
from app.modules.flashcards.schemas import (
    StudySessionCreate, StudySessionUpdate, StudySessionResponse,
    StudyAttemptCreate, StudyAttemptResponse,
    WriteModeAnswer, WriteModeAnswerResponse, WriteModeProgress,
    SpellModeAnswer, SpellModeAnswerResponse, SpellModeProgress,
    TestSessionCreate, TestSessionResponse, TestResult, TestQuestion,
    QuestionType
)
from app.modules.learning.services import StudySessionService, StudyAttemptService, WriteModeService
from app.modules.learning.advanced_study_services import SpellModeService, TestModeService

router = APIRouter(
    prefix="/study", 
    tags=["study"],
    responses={
        404: {"description": "Resource not found"},
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient permissions"},
        422: {"description": "Validation error"}
    }
)


# Study Session Endpoints
@router.post("/sessions", response_model=StudySessionResponse, status_code=201)
def create_study_session(
    session_data: StudySessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start a new study session
    
    This endpoint allows users to start a new study session for a flashcard set.
    
    **Features:**
    - Create study sessions for any study mode
    - Track session start time and duration
    - Initialize session statistics
    
    **Required fields:**
    - `set_id`: ID of the flashcard set to study
    - `study_mode`: Study mode (flashcards, learn, write, spell, test)
    
    **Optional fields:**
    - `duration_minutes`: Expected session duration
    
    **Returns:** The created study session with initial statistics
    """
    try:
        study_session = StudySessionService.create_study_session(
            db=db,
            user_id=current_user.id,
            session_data=session_data
        )
        return study_session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions", response_model=List[StudySessionResponse])
def get_user_study_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    set_id: Optional[int] = Query(None, description="Filter by flashcard set ID"),
    study_mode: Optional[str] = Query(None, description="Filter by study mode")
):
    """
    Get user's study sessions
    
    This endpoint retrieves all study sessions for the authenticated user.
    
    **Features:**
    - Pagination support
    - Filter by flashcard set
    - Filter by study mode
    - Session statistics and performance data
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum records to return (default: 100, max: 1000)
    - `set_id`: Filter by specific flashcard set
    - `study_mode`: Filter by study mode
    
    **Returns:** List of study sessions with performance data
    """
    try:
        study_sessions = StudySessionService.get_user_study_sessions(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            set_id=set_id,
            study_mode=study_mode
        )
        return study_sessions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions/{session_id}", response_model=StudySessionResponse)
def get_study_session(
    session_id: int = Path(..., gt=0, description="Study session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific study session
    
    This endpoint retrieves detailed information about a specific study session.
    
    **Features:**
    - Complete session statistics
    - Performance metrics
    - Session duration and timing data
    
    **Access Control:**
    - Users can only access their own study sessions
    
    **Path Parameters:**
    - `session_id`: The unique identifier of the study session
    
    **Returns:** Detailed study session information
    """
    try:
        study_session = StudySessionService.get_study_session_by_id(
            db=db,
            session_id=session_id,
            user_id=current_user.id
        )
        return study_session
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/sessions/{session_id}", response_model=StudySessionResponse)
def update_study_session(
    session_data: StudySessionUpdate,
    session_id: int = Path(..., gt=0, description="Study session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a study session (end session)
    
    This endpoint allows users to end a study session and update final statistics.
    
    **Features:**
    - End session and calculate final duration
    - Update accuracy and performance metrics
    - Calculate session statistics
    
    **Access Control:**
    - Users can only update their own study sessions
    
    **Path Parameters:**
    - `session_id`: The unique identifier of the study session
    
    **Returns:** Updated study session with final statistics
    """
    try:
        study_session = StudySessionService.update_study_session(
            db=db,
            session_id=session_id,
            user_id=current_user.id,
            update_data=session_data
        )
        return study_session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Study Attempt Endpoints
@router.post("/attempts", response_model=StudyAttemptResponse, status_code=201)
def create_study_attempt(
    attempt_data: StudyAttemptCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Record a study attempt
    
    This endpoint records an individual study attempt for a flashcard.
    
    **Features:**
    - Track user answers and correctness
    - Record response times
    - Update card mastery levels
    - Calculate performance metrics
    
    **Required fields:**
    - `card_id`: ID of the flashcard being studied
    - `session_id`: ID of the study session
    - `user_answer`: User's answer
    - `is_correct`: Whether the answer is correct
    
    **Optional fields:**
    - `response_time_seconds`: Time taken to answer
    - `confidence_level`: User's confidence (1-5)
    
    **Returns:** The recorded study attempt
    """
    try:
        study_attempt = StudyAttemptService.create_study_attempt(
            db=db,
            user_id=current_user.id,
            attempt_data=attempt_data
        )
        return study_attempt
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions/{session_id}/attempts", response_model=List[StudyAttemptResponse])
def get_session_attempts(
    session_id: int = Path(..., gt=0, description="Study session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get all attempts for a study session
    
    This endpoint retrieves all study attempts within a specific session.
    
    **Features:**
    - Pagination support for large sessions
    - Detailed attempt information
    - Performance analysis data
    
    **Access Control:**
    - Users can only access attempts from their own sessions
    
    **Path Parameters:**
    - `session_id`: The unique identifier of the study session
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum records to return (default: 100, max: 1000)
    
    **Returns:** List of study attempts with detailed information
    """
    try:
        attempts = StudyAttemptService.get_session_attempts(
            db=db,
            session_id=session_id,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        return attempts
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/attempts/{attempt_id}", response_model=StudyAttemptResponse)
def get_study_attempt(
    attempt_id: int = Path(..., gt=0, description="Study attempt ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific study attempt
    
    This endpoint retrieves detailed information about a specific study attempt.
    
    **Features:**
    - Complete attempt data
    - Performance metrics
    - Response time and confidence data
    
    **Access Control:**
    - Users can only access their own study attempts
    
    **Path Parameters:**
    - `attempt_id`: The unique identifier of the study attempt
    
    **Returns:** Detailed study attempt information
    """
    try:
        attempt = StudyAttemptService.get_study_attempt_by_id(
            db=db,
            attempt_id=attempt_id,
            user_id=current_user.id
        )
        return attempt
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Advanced Study Modes Endpoints

# Write Mode Endpoints
@router.post("/write/answer", response_model=WriteModeAnswerResponse, status_code=201)
def submit_write_answer(
    answer_data: WriteModeAnswer,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit a write mode answer
    
    This endpoint processes a written answer and provides feedback.
    
    **Features:**
    - Fuzzy matching for answer accuracy
    - Detailed feedback and suggestions
    - Progress tracking
    - Response time analysis
    
    **Required fields:**
    - `card_id`: ID of the flashcard
    - `session_id`: ID of the study session
    - `user_answer`: User's written answer
    
    **Optional fields:**
    - `response_time_seconds`: Time taken to answer
    - `confidence_level`: User's confidence (1-5)
    
    **Returns:** Answer feedback with accuracy score and suggestions
    """
    try:
        response = WriteModeService.submit_write_answer(
            db=db,
            user_id=current_user.id,
            answer_data=answer_data
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/write/progress/{session_id}", response_model=WriteModeProgress)
def get_write_progress(
    session_id: int = Path(..., gt=0, description="Study session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get write mode progress
    
    This endpoint retrieves progress information for a write mode session.
    
    **Features:**
    - Real-time progress tracking
    - Accuracy statistics
    - Response time analysis
    - Session completion status
    
    **Access Control:**
    - Users can only access their own session progress
    
    **Path Parameters:**
    - `session_id`: The unique identifier of the study session
    
    **Returns:** Write mode progress with detailed statistics
    """
    try:
        progress = WriteModeService.get_write_progress(
            db=db,
            session_id=session_id,
            user_id=current_user.id
        )
        return progress
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Spell Mode Endpoints
@router.post("/spell/answer", response_model=SpellModeAnswerResponse, status_code=201)
def submit_spell_answer(
    answer_data: SpellModeAnswer,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit a spell mode answer
    
    This endpoint processes a spelling attempt and provides feedback.
    
    **Features:**
    - Exact spelling validation
    - Phonetic feedback
    - Pronunciation tips
    - Audio play tracking
    
    **Required fields:**
    - `card_id`: ID of the flashcard
    - `session_id`: ID of the study session
    - `user_spelling`: User's spelling attempt
    
    **Optional fields:**
    - `response_time_seconds`: Time taken to answer
    - `audio_played`: Whether audio was played
    
    **Returns:** Spelling feedback with phonetic guidance
    """
    try:
        response = SpellModeService.submit_spell_answer(
            db=db,
            user_id=current_user.id,
            answer_data=answer_data
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/spell/progress/{session_id}", response_model=SpellModeProgress)
def get_spell_progress(
    session_id: int = Path(..., gt=0, description="Study session ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get spell mode progress
    
    This endpoint retrieves progress information for a spell mode session.
    
    **Features:**
    - Spelling accuracy tracking
    - Audio play statistics
    - Response time analysis
    - Session completion status
    
    **Access Control:**
    - Users can only access their own session progress
    
    **Path Parameters:**
    - `session_id`: The unique identifier of the study session
    
    **Returns:** Spell mode progress with detailed statistics
    """
    try:
        progress = SpellModeService.get_spell_progress(
            db=db,
            session_id=session_id,
            user_id=current_user.id
        )
        return progress
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Test Mode Endpoints
@router.post("/test/sessions", response_model=TestSessionResponse, status_code=201)
def create_test_session(
    test_data: TestSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new test session
    
    This endpoint creates a new test session with customizable parameters.
    
    **Features:**
    - Customizable question count
    - Time limit settings
    - Question type selection
    - Explanation options
    
    **Required fields:**
    - `set_id`: ID of the flashcard set
    
    **Optional fields:**
    - `question_count`: Number of questions (default: 10, range: 5-50)
    - `time_limit_minutes`: Time limit in minutes (range: 5-120)
    - `include_explanations`: Include explanations in results (default: true)
    - `question_types`: Types of questions to include
    
    **Returns:** Test session with configuration details
    """
    try:
        test_session = TestModeService.create_test_session(
            db=db,
            user_id=current_user.id,
            test_data=test_data
        )
        return test_session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test/generate", response_model=List[TestQuestion])
def generate_test_questions(
    set_id: int = Query(..., gt=0, description="Flashcard set ID"),
    question_count: int = Query(10, ge=5, le=50, description="Number of questions to generate"),
    question_types: Optional[List[QuestionType]] = Query(None, description="Types of questions to include"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate test questions
    
    This endpoint generates test questions from a flashcard set.
    
    **Features:**
    - Multiple question types (MCQ, True/False, Fill-in-blank)
    - Random question selection
    - Difficulty-based generation
    - Balanced question distribution
    
    **Query Parameters:**
    - `set_id`: ID of the flashcard set
    - `question_count`: Number of questions (default: 10, range: 5-50)
    - `question_types`: Types of questions to include
    
    **Returns:** List of generated test questions
    """
    try:
        questions = TestModeService.generate_test_questions(
            db=db,
            set_id=set_id,
            question_count=question_count,
            question_types=question_types
        )
        return questions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test/calculate-result", response_model=TestResult)
def calculate_test_result(
    question_results: List[dict],
    time_taken_seconds: int = Query(..., ge=0, description="Total time taken in seconds"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Calculate test results
    
    This endpoint calculates comprehensive test results and analysis.
    
    **Features:**
    - Score calculation
    - Performance analysis
    - Personalized recommendations
    - Detailed statistics
    
    **Required fields:**
    - `question_results`: List of question responses
    - `time_taken_seconds`: Total time taken
    
    **Returns:** Comprehensive test results with analysis and recommendations
    """
    try:
        # Convert dict to TestQuestionResponse objects
        from app.modules.flashcards.schemas import TestQuestionResponse
        results = [TestQuestionResponse(**result) for result in question_results]
        
        test_result = TestModeService.calculate_test_result(
            question_results=results,
            time_taken_seconds=time_taken_seconds
        )
        return test_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
