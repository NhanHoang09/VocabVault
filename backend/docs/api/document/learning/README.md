# 📚 Learning API - Advanced Study Modes

## 📋 Overview

The Learning API provides comprehensive study session management and advanced study modes for vocabulary learning. This includes traditional study sessions, write mode, spell mode, and test mode with detailed progress tracking and analytics.

## 🔐 Authentication

All endpoints require authentication using Bearer token:

```http
Authorization: Bearer <your_jwt_token>
```

## 📊 Study Session Management

### Create Study Session
```http
POST /api/v1/study/sessions
```

**Request Body:**
```json
{
  "set_id": 1,
  "study_mode": "write",
  "duration_minutes": 30
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "set_id": 1,
  "study_mode": "write",
  "duration_minutes": 30,
  "total_cards_studied": 0,
  "correct_answers": 0,
  "incorrect_answers": 0,
  "accuracy_percentage": 0.0,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Get User Study Sessions
```http
GET /api/v1/study/sessions?skip=0&limit=10&set_id=1&study_mode=write
```

### Get Study Session Details
```http
GET /api/v1/study/sessions/{session_id}
```

### Update Study Session
```http
PUT /api/v1/study/sessions/{session_id}
```

**Request Body:**
```json
{
  "ended_at": "2024-01-15T11:00:00Z",
  "total_cards_studied": 20,
  "correct_answers": 18,
  "incorrect_answers": 2,
  "accuracy_percentage": 90.0
}
```

## 📝 Study Attempts

### Record Study Attempt
```http
POST /api/v1/study/attempts
```

**Request Body:**
```json
{
  "card_id": 1,
  "session_id": 1,
  "user_answer": "apple",
  "is_correct": true,
  "response_time_seconds": 3.5
}
```

### Get Session Attempts
```http
GET /api/v1/study/sessions/{session_id}/attempts?skip=0&limit=20
```

### Get Study Attempt Details
```http
GET /api/v1/study/attempts/{attempt_id}
```

## ✍️ Write Mode

Write Mode allows users to practice vocabulary by typing answers, with intelligent fuzzy matching and detailed feedback.

### Submit Write Answer
```http
POST /api/v1/study/write/answer
```

**Request Body:**
```json
{
  "card_id": 1,
  "session_id": 1,
  "user_answer": "apple",
  "response_time_seconds": 4.2,
  "confidence_level": 4
}
```

**Response:**
```json
{
  "card_id": 1,
  "user_answer": "apple",
  "correct_answer": "apple",
  "is_correct": true,
  "accuracy_score": 1.0,
  "feedback": "Excellent! Your answer is very close to the correct answer.",
  "suggestions": [],
  "response_time_seconds": 4.2,
  "created_at": "2024-01-15T10:35:00Z"
}
```

### Get Write Progress
```http
GET /api/v1/study/write/progress/{session_id}
```

**Response:**
```json
{
  "session_id": 1,
  "total_cards": 50,
  "cards_answered": 20,
  "correct_answers": 18,
  "accuracy_percentage": 90.0,
  "average_response_time": 4.5,
  "time_remaining_seconds": 600
}
```

## 🎯 Spell Mode

Spell Mode focuses on spelling accuracy with phonetic feedback and pronunciation tips.

### Submit Spell Answer
```http
POST /api/v1/study/spell/answer
```

**Request Body:**
```json
{
  "card_id": 1,
  "session_id": 1,
  "user_spelling": "apple",
  "response_time_seconds": 3.8,
  "audio_played": true
}
```

**Response:**
```json
{
  "card_id": 1,
  "user_spelling": "apple",
  "correct_spelling": "apple",
  "is_correct": true,
  "phonetic_feedback": "Perfect spelling!",
  "pronunciation_tips": [
    "Focus on vowel sounds",
    "Break the word into syllables"
  ],
  "response_time_seconds": 3.8,
  "created_at": "2024-01-15T10:40:00Z"
}
```

### Get Spell Progress
```http
GET /api/v1/study/spell/progress/{session_id}
```

**Response:**
```json
{
  "session_id": 1,
  "total_cards": 50,
  "cards_answered": 15,
  "correct_spellings": 14,
  "accuracy_percentage": 93.3,
  "average_response_time": 4.2,
  "audio_plays_count": 8
}
```

## 📝 Test Mode

Test Mode provides comprehensive assessment with multiple question types and detailed analytics.

### Create Test Session
```http
POST /api/v1/study/test/sessions
```

**Request Body:**
```json
{
  "set_id": 1,
  "question_count": 20,
  "time_limit_minutes": 30,
  "include_explanations": true,
  "question_types": ["multiple_choice", "true_false", "fill_in_blank"]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "set_id": 1,
  "question_count": 20,
  "time_limit_minutes": 30,
  "include_explanations": true,
  "started_at": "2024-01-15T11:00:00Z",
  "ended_at": null,
  "total_score": 0,
  "max_score": 20,
  "accuracy_percentage": 0.0,
  "time_taken_seconds": null,
  "questions_answered": 0,
  "correct_answers": 0,
  "created_at": "2024-01-15T11:00:00Z"
}
```

### Generate Test Questions
```http
POST /api/v1/study/test/generate?set_id=1&question_count=20&question_types=multiple_choice&question_types=true_false
```

**Response:**
```json
[
  {
    "id": 1,
    "question_type": "multiple_choice",
    "question_text": "What is the meaning of: apple?",
    "options": [
      "A fruit",
      "A vegetable",
      "A color",
      "A number"
    ],
    "correct_answer": "A fruit",
    "explanation": "The correct answer is 'A fruit'",
    "difficulty": "medium",
    "points": 1
  },
  {
    "id": 2,
    "question_type": "true_false",
    "question_text": "'apple' means 'a fruit'",
    "options": ["True", "False"],
    "correct_answer": "True",
    "explanation": "The correct meaning is 'a fruit'",
    "difficulty": "easy",
    "points": 1
  }
]
```

### Calculate Test Results
```http
POST /api/v1/study/test/calculate-result?time_taken_seconds=1800
```

**Request Body:**
```json
[
  {
    "question_id": 1,
    "user_answer": "A fruit",
    "is_correct": true,
    "points_earned": 1,
    "response_time_seconds": 5.2,
    "explanation": "The correct answer is 'A fruit'"
  },
  {
    "question_id": 2,
    "user_answer": "True",
    "is_correct": true,
    "points_earned": 1,
    "response_time_seconds": 3.1,
    "explanation": "The correct meaning is 'a fruit'"
  }
]
```

**Response:**
```json
{
  "test_session_id": 1,
  "total_score": 18,
  "max_score": 20,
  "accuracy_percentage": 90.0,
  "time_taken_seconds": 1800,
  "questions_answered": 20,
  "correct_answers": 18,
  "question_results": [...],
  "performance_analysis": {
    "average_response_time": 4.5,
    "total_time_taken": 1800,
    "questions_per_minute": 0.67,
    "type_performance": {}
  },
  "recommendations": [
    "Good progress! Review areas of weakness",
    "Try write mode to improve recall"
  ]
}
```

## 📈 Study Modes Comparison

| Feature | Flashcards | Learn | Write | Spell | Test |
|---------|------------|-------|-------|-------|------|
| **Answer Type** | Multiple choice | Multiple choice | Free text | Free text | Mixed |
| **Feedback** | Immediate | Immediate | Detailed | Phonetic | Comprehensive |
| **Scoring** | Binary | Binary | Fuzzy matching | Exact | Points-based |
| **Progress Tracking** | Basic | Basic | Advanced | Advanced | Analytics |
| **Question Types** | Single | Single | Single | Single | Multiple |
| **Time Pressure** | Optional | Optional | Optional | Optional | Configurable |

## 🎯 Study Mode Features

### Write Mode Features
- **Fuzzy Matching**: Intelligent answer comparison using sequence matching
- **Detailed Feedback**: Specific suggestions for improvement
- **Confidence Tracking**: User confidence level recording
- **Response Time Analysis**: Performance timing metrics

### Spell Mode Features
- **Exact Spelling Validation**: Precise spelling accuracy checking
- **Phonetic Feedback**: Detailed spelling guidance
- **Pronunciation Tips**: Helpful pronunciation suggestions
- **Audio Integration**: Audio play tracking and support

### Test Mode Features
- **Multiple Question Types**: MCQ, True/False, Fill-in-blank
- **Customizable Parameters**: Question count, time limits, difficulty
- **Comprehensive Analytics**: Detailed performance analysis
- **Personalized Recommendations**: AI-generated study suggestions

## 🔧 Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "detail": "Invalid study mode. Must be one of: flashcards, learn, write, spell, test"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication required"
}
```

**404 Not Found:**
```json
{
  "detail": "Study session not found"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "set_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 📊 Performance Metrics

### Write Mode Metrics
- **Accuracy Score**: 0.0 to 1.0 (fuzzy matching)
- **Response Time**: Seconds per answer
- **Confidence Level**: 1-5 scale
- **Completion Rate**: Percentage of cards answered

### Spell Mode Metrics
- **Spelling Accuracy**: Percentage of correct spellings
- **Audio Usage**: Number of audio plays
- **Response Time**: Average time per spelling
- **Error Patterns**: Common spelling mistakes

### Test Mode Metrics
- **Total Score**: Points earned vs maximum
- **Accuracy Percentage**: Overall test accuracy
- **Time Efficiency**: Questions per minute
- **Question Type Performance**: Performance by question type

## 🚀 Best Practices

### For Write Mode
1. **Use Clear Prompts**: Provide context for expected answers
2. **Implement Fuzzy Matching**: Allow for minor spelling variations
3. **Provide Detailed Feedback**: Give specific improvement suggestions
4. **Track Confidence**: Use confidence levels for adaptive learning

### For Spell Mode
1. **Exact Validation**: Require precise spelling accuracy
2. **Phonetic Support**: Provide pronunciation guidance
3. **Audio Integration**: Include audio playback options
4. **Error Analysis**: Track common spelling mistakes

### For Test Mode
1. **Question Variety**: Mix different question types
2. **Time Management**: Set appropriate time limits
3. **Difficulty Progression**: Increase difficulty gradually
4. **Detailed Analytics**: Provide comprehensive performance insights

## 🔗 Related Endpoints

- **Flashcard Sets**: `/api/v1/flashcards/sets`
- **Flashcards**: `/api/v1/flashcards/cards`
- **Gamification**: `/api/v1/gamification/*`
- **Analytics**: `/api/v1/analytics/*`

## 📝 Notes

- All study sessions are automatically linked to user accounts
- Progress tracking is real-time and persistent
- Test results include detailed performance analytics
- Audio features require additional audio file management
- Fuzzy matching threshold is configurable (default: 80% accuracy)
