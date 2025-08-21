# 🤖 AI Module API Documentation

## Overview

The AI Module provides intelligent features for vocabulary learning, including AI conversations, content generation, adaptive learning, and guided study sessions. This module leverages OpenAI's GPT models to enhance the learning experience.

## Features

### 🗣️ AI Conversations
- **AI Tutor Chat**: Interactive conversations with an AI tutor for study help
- **Context-Aware Responses**: AI responses tailored to study context and user needs
- **Conversation History**: Persistent chat history for continuous learning

### 🎯 Content Generation
- **Flashcard Generation**: Create flashcards from text using AI
- **Study Plan Generation**: Personalized study plans based on user performance
- **Concept Explanations**: AI-generated explanations for difficult concepts

### 🧠 Adaptive Learning
- **Learning Profiles**: Personalized learning preferences and analytics
- **Smart Recommendations**: AI-powered recommendations for study improvement
- **Performance Analysis**: Deep insights into learning patterns and progress

### 👨‍🏫 AI Tutor Sessions
- **Guided Study**: Structured learning sessions with AI guidance
- **Multiple Session Types**: Review, practice, assessment, and guided study modes
- **Progress Tracking**: Real-time progress monitoring and adjustment

## Authentication

All AI endpoints require authentication. Include your JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## API Endpoints

### AI Conversations

#### Create AI Conversation
```http
POST /api/v1/ai/conversations
```

**Request Body:**
```json
{
  "title": "Study Help Session",
  "context_type": "study_help",
  "context_data": {
    "set_id": 123,
    "difficulty": "medium"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Study Help Session",
  "context_type": "study_help",
  "context_data": {
    "set_id": 123,
    "difficulty": "medium"
  },
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": null
}
```

#### Get User Conversations
```http
GET /api/v1/ai/conversations?skip=0&limit=20
```

#### Get Conversation Messages
```http
GET /api/v1/ai/conversations/{conversation_id}/messages?skip=0&limit=50
```

#### Chat with AI
```http
POST /api/v1/ai/chat
```

**Request Body:**
```json
{
  "message": "Can you help me understand the difference between 'affect' and 'effect'?",
  "conversation_id": 1,
  "context_type": "study_help",
  "context_data": {
    "flashcard_id": 456
  }
}
```

**Response:**
```json
{
  "conversation_id": 1,
  "message": {
    "id": 10,
    "conversation_id": 1,
    "role": "user",
    "content": "Can you help me understand the difference between 'affect' and 'effect'?",
    "created_at": "2024-01-15T10:05:00Z"
  },
  "response": {
    "id": 11,
    "conversation_id": 1,
    "role": "assistant",
    "content": "Great question! Here's the key difference:\n\n- **Affect** (verb): to influence or change something\n- **Effect** (noun): the result or outcome of something\n\nExample: The rain will affect the game, and the effect will be a cancellation.\n\nThink of it this way: 'A' for action (affect), 'E' for end result (effect).",
    "created_at": "2024-01-15T10:05:05Z"
  }
}
```

### Content Generation

#### Generate Flashcards from Text
```http
POST /api/v1/ai/generate/flashcards
```

**Request Body:**
```json
{
  "source_text": "Photosynthesis is the process by which plants convert sunlight into energy. Chlorophyll is the green pigment that captures light. Carbon dioxide and water are converted into glucose and oxygen.",
  "title": "Photosynthesis Basics",
  "description": "Key concepts about photosynthesis",
  "category": "Biology",
  "tags": ["science", "biology", "plants"],
  "difficulty": "medium",
  "num_cards": 5
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "content_type": "flashcard_set",
  "source_text": "Photosynthesis is the process...",
  "generated_data": {
    "title": "Photosynthesis Basics",
    "description": "Key concepts about photosynthesis",
    "category": "Biology",
    "tags": ["science", "biology", "plants"],
    "difficulty": "medium",
    "flashcards": [
      {
        "front": "What is photosynthesis?",
        "back": "The process by which plants convert sunlight into energy"
      },
      {
        "front": "What is chlorophyll?",
        "back": "The green pigment that captures light in plants"
      }
    ]
  },
  "is_imported": false,
  "created_at": "2024-01-15T10:10:00Z"
}
```

#### Generate Study Plan
```http
POST /api/v1/ai/generate/study-plan
```

**Request Body:**
```json
{
  "set_id": 123,
  "study_duration_minutes": 30,
  "target_accuracy": 0.8,
  "preferred_mode": "flashcards"
}
```

#### Generate Explanation
```http
POST /api/v1/ai/generate/explanation?concept=photosynthesis&context=biology
```

#### Import Generated Content
```http
POST /api/v1/ai/content/{content_id}/import
```

#### Get Generated Content
```http
GET /api/v1/ai/generated-content?skip=0&limit=20
```

### Learning Profiles

#### Create/Update Learning Profile
```http
POST /api/v1/ai/adaptive/profile
```

**Request Body:**
```json
{
  "preferred_study_mode": "flashcards",
  "preferred_difficulty": "adaptive",
  "study_session_duration": 15,
  "daily_study_goal": 50
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "preferred_study_mode": "flashcards",
  "preferred_difficulty": "adaptive",
  "study_session_duration": 15,
  "daily_study_goal": 50,
  "average_response_time": 3.2,
  "accuracy_rate": 0.85,
  "retention_rate": 0.78,
  "learning_speed": 4.5,
  "recommended_difficulty": "medium",
  "recommended_study_mode": "write",
  "next_review_time": "2024-01-16T10:00:00Z",
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### Get Learning Profile
```http
GET /api/v1/ai/adaptive/profile
```

#### Update Learning Profile
```http
PUT /api/v1/ai/adaptive/profile
```

#### Analyze Learning Patterns
```http
POST /api/v1/ai/adaptive/analyze
```

**Response:**
```json
{
  "accuracy_rate": 0.85,
  "average_response_time": 3.2,
  "recommended_difficulty": "medium",
  "recommended_study_mode": "write",
  "learning_speed": 4.5,
  "retention_rate": 0.78,
  "mode_performance": {
    "flashcards": {
      "sessions": 15,
      "total_accuracy": 0.82
    },
    "write": {
      "sessions": 8,
      "total_accuracy": 0.88
    }
  },
  "study_consistency": "high"
}
```

### Adaptive Recommendations

#### Generate Recommendations
```http
POST /api/v1/ai/adaptive/recommendations/generate
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "recommendation_type": "study_mode",
    "title": "Try Write Mode",
    "description": "Based on your performance, you might benefit from using write mode instead of flashcards.",
    "priority": 3,
    "data": {
      "recommended_mode": "write"
    },
    "is_applied": false,
    "created_at": "2024-01-15T10:15:00Z"
  }
]
```

#### Get Recommendations
```http
GET /api/v1/ai/adaptive/recommendations?skip=0&limit=10
```

#### Apply Recommendation
```http
PUT /api/v1/ai/adaptive/recommendations/{recommendation_id}/apply
```

#### Get Learning Insights
```http
GET /api/v1/ai/adaptive/insights
```

**Response:**
```json
{
  "profile": {
    "preferred_study_mode": "flashcards",
    "preferred_difficulty": "adaptive",
    "study_session_duration": 15,
    "daily_study_goal": 50
  },
  "performance": {
    "accuracy_rate": 0.85,
    "average_response_time": 3.2,
    "learning_speed": 4.5,
    "retention_rate": 0.78,
    "accuracy_trend": "improving"
  },
  "recommendations": {
    "recommended_difficulty": "medium",
    "recommended_study_mode": "write"
  },
  "study_habits": {
    "study_streak": 7,
    "mode_performance": {
      "flashcards": {
        "sessions": 15,
        "total_accuracy": 0.82
      }
    },
    "study_consistency": "high"
  }
}
```

### AI Tutor Sessions

#### Create Tutor Session
```http
POST /api/v1/ai/tutor/sessions
```

**Request Body:**
```json
{
  "session_type": "guided_study",
  "set_id": 123,
  "difficulty_level": "medium",
  "target_accuracy": 0.8
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "set_id": 123,
  "session_type": "guided_study",
  "difficulty_level": "medium",
  "target_accuracy": 0.8,
  "current_accuracy": null,
  "cards_studied": 0,
  "total_cards": 25,
  "is_completed": false,
  "started_at": "2024-01-15T10:20:00Z",
  "completed_at": null
}
```

#### Get Tutor Sessions
```http
GET /api/v1/ai/tutor/sessions?skip=0&limit=20
```

#### Get Study Plan
```http
GET /api/v1/ai/tutor/sessions/{session_id}/plan
```

**Response:**
```json
{
  "session_type": "guided_study",
  "target_accuracy": 0.8,
  "difficulty_level": "medium",
  "phases": [
    {
      "phase": "introduction",
      "description": "Let's start with an overview of what we'll learn today",
      "duration_minutes": 2,
      "mode": "flashcards",
      "objectives": ["Familiarize with new concepts", "Set learning goals"]
    },
    {
      "phase": "learning",
      "description": "Focus on understanding new concepts",
      "duration_minutes": 10,
      "mode": "learn",
      "objectives": ["Learn new vocabulary", "Understand definitions"]
    }
  ],
  "tips": [
    "Take your time to understand each concept",
    "Don't worry about making mistakes - they help you learn"
  ],
  "success_criteria": "Achieve 80% accuracy and complete all phases"
}
```

#### Update Session Progress
```http
PUT /api/v1/ai/tutor/sessions/{session_id}/progress
```

**Request Body:**
```json
{
  "current_accuracy": 0.75,
  "cards_studied": 15,
  "is_completed": false
}
```

#### Complete Session
```http
POST /api/v1/ai/tutor/sessions/{session_id}/complete?final_accuracy=0.82&total_cards_studied=25
```

#### Get Session Recommendations
```http
GET /api/v1/ai/tutor/recommendations?set_id=123
```

**Response:**
```json
{
  "recommended_session_type": "practice",
  "recommended_difficulty": "medium",
  "reason": "Moderate accuracy - practice will help improve",
  "current_accuracy": 0.75,
  "recent_sessions_count": 5
}
```

#### Get Session Analytics
```http
GET /api/v1/ai/tutor/analytics?days=30
```

**Response:**
```json
{
  "total_sessions": 12,
  "completed_sessions": 10,
  "completion_rate": 0.83,
  "average_accuracy": 0.78,
  "session_types": {
    "guided_study": {
      "count": 5,
      "completed": 4,
      "avg_accuracy": 0.75
    },
    "practice": {
      "count": 7,
      "completed": 6,
      "avg_accuracy": 0.80
    }
  },
  "period_days": 30
}
```

## Error Responses

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: AI service not available (OpenAI API issues)

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

## Rate Limits

- **AI Chat**: 10 requests per minute per user
- **Content Generation**: 5 requests per minute per user
- **Analysis**: 20 requests per minute per user

## Configuration

### Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# AI Service Settings
AI_MODEL=gpt-3.5-turbo
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.7
```

### OpenAI API Key Setup

1. Get an API key from [OpenAI Platform](https://platform.openai.com/)
2. Add the key to your `.env` file:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
3. Restart the application

## Best Practices

### For AI Conversations
- Provide clear, specific questions
- Use context data to help AI understand your study situation
- Review conversation history for continuity

### For Content Generation
- Provide detailed source text for better flashcard generation
- Specify appropriate difficulty levels
- Review generated content before importing

### For Adaptive Learning
- Complete regular study sessions to improve recommendations
- Update your learning profile preferences
- Apply recommendations to see improved results

### For Tutor Sessions
- Choose session types based on your current needs
- Follow the guided study plans
- Track your progress regularly

## Examples

### Complete Study Session with AI

1. **Create a tutor session:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai/tutor/sessions" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "session_type": "guided_study",
       "set_id": 123,
       "difficulty_level": "medium",
       "target_accuracy": 0.8
     }'
   ```

2. **Get the study plan:**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/ai/tutor/sessions/1/plan" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **Update progress during session:**
   ```bash
   curl -X PUT "http://localhost:8000/api/v1/ai/tutor/sessions/1/progress" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "current_accuracy": 0.75,
       "cards_studied": 15
     }'
   ```

4. **Complete the session:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai/tutor/sessions/1/complete?final_accuracy=0.82&total_cards_studied=25" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Generate and Import Flashcards

1. **Generate flashcards from text:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai/generate/flashcards" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "source_text": "Photosynthesis is the process by which plants convert sunlight into energy...",
       "title": "Photosynthesis Basics",
       "category": "Biology",
       "num_cards": 5
     }'
   ```

2. **Import the generated content:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/ai/content/1/import" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

## Support

For issues with the AI module:

1. Check that your OpenAI API key is properly configured
2. Verify you have sufficient API credits
3. Review the error messages for specific issues
4. Check the application logs for detailed error information

## Future Enhancements

- **Multi-language Support**: AI conversations in multiple languages
- **Voice Integration**: Speech-to-text and text-to-speech capabilities
- **Advanced Analytics**: More detailed learning insights and predictions
- **Custom AI Models**: Support for fine-tuned models for specific subjects
- **Collaborative Learning**: AI-assisted group study sessions
