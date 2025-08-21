# 📚 Flashcards API - Quick Reference

## 🚀 Base URL
```
/api/v1/flashcards
```

## 📋 Endpoints Summary

### 🔐 FlashcardSet Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/sets` | ✅ | Create new flashcard set |
| `GET` | `/sets` | ✅ | Get user's flashcard sets |
| `GET` | `/sets/public` | ❌ | Get public flashcard sets |
| `GET` | `/sets/{id}` | ❌ | Get specific flashcard set |
| `GET` | `/sets/{id}/with-cards` | ❌ | Get set with all cards |
| `PUT` | `/sets/{id}` | ✅ | Update flashcard set |
| `DELETE` | `/sets/{id}` | ✅ | Delete flashcard set |

### 🃏 Flashcard Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/sets/{id}/cards` | ✅ | Create new flashcard |
| `GET` | `/sets/{id}/cards` | ❌ | Get all cards in set |
| `GET` | `/cards/{id}` | ❌ | Get specific flashcard |
| `PUT` | `/cards/{id}` | ✅ | Update flashcard |
| `DELETE` | `/cards/{id}` | ✅ | Delete flashcard |

## 🔑 Authentication

```bash
# Required endpoints
Authorization: Bearer <your_jwt_token>

# Optional endpoints (public sets)
No authentication needed
```

## 📝 Common Request Bodies

### Create Flashcard Set
```json
{
  "title": "Set Title",
  "description": "Set Description",
  "category": "Category",
  "tags": ["tag1", "tag2"],
  "is_public": true,
  "is_featured": false
}
```

### Create Flashcard
```json
{
  "front_content": "Question",
  "back_content": "Answer",
  "card_type": "text",
  "difficulty": "easy",
  "media_url": null,
  "card_metadata": {}
}
```

## 📊 Common Response Models

### FlashcardSet
```json
{
  "id": 1,
  "title": "Set Title",
  "description": "Set Description",
  "category": "Category",
  "tags": ["tag1", "tag2"],
  "is_public": true,
  "is_featured": false,
  "user_id": 1,
  "cards_count": 10,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Flashcard
```json
{
  "id": 1,
  "set_id": 1,
  "front_content": "Question",
  "back_content": "Answer",
  "card_type": "text",
  "media_url": null,
  "difficulty": "easy",
  "card_metadata": {},
  "mastery_level": "NOT_LEARNED",
  "mastery_score": 0.0,
  "review_count": 0,
  "correct_count": 0,
  "incorrect_count": 0,
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

## 🔍 Query Parameters

### Pagination
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

### Search & Filter
- `search`: Search term for title or description
- `category`: Filter by specific category

## 🎯 Status Codes

- `200 OK`: Success
- `201 Created`: Resource created
- `204 No Content`: Resource deleted
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Validation Error`: Validation failed

## 🚀 Quick Examples

### Create Set
```bash
curl -X POST "http://localhost:8000/api/v1/flashcards/sets" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Set", "is_public": true}'
```

### Add Card
```bash
curl -X POST "http://localhost:8000/api/v1/flashcards/sets/1/cards" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"front_content": "Hello", "back_content": "Xin chào"}'
```

### Get Public Sets
```bash
curl -X GET "http://localhost:8000/api/v1/flashcards/sets/public?limit=10"
```

## ⚠️ Important Notes

- **Owner Access**: Only set owners can create/update/delete
- **Public Access**: Everyone can view public sets
- **Private Access**: Private sets only visible to owners
- **Progress Tracking**: Automatically tracks learning progress
- **Media Support**: Supports text, image, audio, video
- **Pagination**: All list endpoints support pagination
- **Search**: Search in title and description fields
- **Validation**: All inputs are validated
- **Error Handling**: Comprehensive error responses

---

**Legend**: ✅ = Required Auth, ❌ = No Auth Required
