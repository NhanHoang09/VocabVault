# 🤖 AI Module - Quick Reference

## Endpoint Overview

### AI Conversations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/conversations` | Create new AI conversation |
| GET | `/ai/conversations` | Get user conversations |
| GET | `/ai/conversations/{id}` | Get specific conversation |
| GET | `/ai/conversations/{id}/messages` | Get conversation messages |
| POST | `/ai/chat` | Chat with AI tutor |

### Content Generation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/generate/flashcards` | Generate flashcards from text |
| POST | `/ai/generate/study-plan` | Generate personalized study plan |
| POST | `/ai/generate/explanation` | Generate concept explanation |
| POST | `/ai/content/{id}/import` | Import generated content |
| GET | `/ai/generated-content` | Get generated content |

### Learning Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/adaptive/profile` | Create/update learning profile |
| GET | `/ai/adaptive/profile` | Get learning profile |
| PUT | `/ai/adaptive/profile` | Update learning profile |
| POST | `/ai/adaptive/analyze` | Analyze learning patterns |

### Adaptive Recommendations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/adaptive/recommendations/generate` | Generate recommendations |
| GET | `/ai/adaptive/recommendations` | Get recommendations |
| PUT | `/ai/adaptive/recommendations/{id}/apply` | Apply recommendation |
| GET | `/ai/adaptive/insights` | Get learning insights |

### AI Tutor Sessions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/tutor/sessions` | Create tutor session |
| GET | `/ai/tutor/sessions` | Get tutor sessions |
| GET | `/ai/tutor/sessions/{id}` | Get specific session |
| GET | `/ai/tutor/sessions/{id}/plan` | Get study plan |
| PUT | `/ai/tutor/sessions/{id}/progress` | Update progress |
| POST | `/ai/tutor/sessions/{id}/complete` | Complete session |
| GET | `/ai/tutor/recommendations` | Get session recommendations |
| GET | `/ai/tutor/analytics` | Get session analytics |

## Common Request Bodies

### Create AI Conversation
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

### Chat with AI
```json
{
  "message": "Can you help me understand this concept?",
  "conversation_id": 1,
  "context_type": "study_help",
  "context_data": {
    "flashcard_id": 456
  }
}
```

### Generate Flashcards
```json
{
  "source_text": "Your text content here...",
  "title": "Flashcard Set Title",
  "description": "Optional description",
  "category": "Subject",
  "tags": ["tag1", "tag2"],
  "difficulty": "medium",
  "num_cards": 10
}
```

### Create Learning Profile
```json
{
  "preferred_study_mode": "flashcards",
  "preferred_difficulty": "adaptive",
  "study_session_duration": 15,
  "daily_study_goal": 50
}
```

### Create Tutor Session
```json
{
  "session_type": "guided_study",
  "set_id": 123,
  "difficulty_level": "medium",
  "target_accuracy": 0.8
}
```

## Common Response Formats

### AI Conversation Response
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Study Help Session",
  "context_type": "study_help",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z"
}
```

### AI Chat Response
```json
{
  "conversation_id": 1,
  "message": {
    "id": 10,
    "role": "user",
    "content": "User message",
    "created_at": "2024-01-15T10:05:00Z"
  },
  "response": {
    "id": 11,
    "role": "assistant",
    "content": "AI response",
    "created_at": "2024-01-15T10:05:05Z"
  }
}
```

### Learning Profile Response
```json
{
  "id": 1,
  "user_id": 1,
  "preferred_study_mode": "flashcards",
  "preferred_difficulty": "adaptive",
  "study_session_duration": 15,
  "daily_study_goal": 50,
  "accuracy_rate": 0.85,
  "learning_speed": 4.5,
  "recommended_difficulty": "medium",
  "recommended_study_mode": "write"
}
```

### Tutor Session Response
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
  "started_at": "2024-01-15T10:20:00Z"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |
| 503 | Service Unavailable - AI service down |

## Context Types

| Type | Description |
|------|-------------|
| `general` | General conversation |
| `study_help` | Study assistance |
| `flashcard_explanation` | Flashcard explanations |
| `content_generation` | Content generation help |

## Session Types

| Type | Description |
|------|-------------|
| `guided_study` | Guided learning session |
| `review` | Review session |
| `practice` | Practice session |
| `assessment` | Assessment session |

## Content Types

| Type | Description |
|------|-------------|
| `flashcard_set` | Generated flashcard set |
| `explanation` | Concept explanation |
| `quiz` | Generated quiz |
| `study_plan` | Study plan |
| `recommendation` | Learning recommendation |

## Recommendation Types

| Type | Description |
|------|-------------|
| `study_mode` | Study mode recommendations |
| `difficulty` | Difficulty adjustments |
| `content` | Content recommendations |
| `timing` | Study timing suggestions |

## Query Parameters

### Pagination
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 20, max: 100)

### Analytics
- `days`: Number of days for analytics (default: 30, max: 365)

### Content Generation
- `concept`: Concept to explain
- `context`: Additional context for explanation

### Session Completion
- `final_accuracy`: Final accuracy achieved
- `total_cards_studied`: Total cards studied
- `session_data`: Additional session data (optional)

## Authentication

All endpoints require Bearer token authentication:

```bash
Authorization: Bearer <your_jwt_token>
```

## Rate Limits

- AI Chat: 10 requests/minute
- Content Generation: 5 requests/minute
- Analysis: 20 requests/minute

## Environment Variables

```bash
OPENAI_API_KEY=your_openai_api_key
```

## Quick Examples

### Start AI Chat
```bash
curl -X POST "http://localhost:8000/api/v1/ai/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me study vocabulary"}'
```

### Generate Flashcards
```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate/flashcards" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"source_text": "Your text here", "title": "My Set", "num_cards": 5}'
```

### Get Learning Insights
```bash
curl -X GET "http://localhost:8000/api/v1/ai/adaptive/insights" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Tutor Session
```bash
curl -X POST "http://localhost:8000/api/v1/ai/tutor/sessions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"session_type": "guided_study", "set_id": 123}'
```
