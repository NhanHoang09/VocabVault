# Social Features API Documentation

## Overview

The Social Features API provides comprehensive social and community functionality for the My Vocabulary Vault application. This module enables users to share flashcard sets, participate in study groups, interact with the community, and receive personalized notifications.

## Features

### 🏘️ Community Sets
- Share flashcard sets with the community
- Browse and discover sets created by other users
- Rate and review community sets
- Filter sets by category, difficulty, and language

### 👥 Study Groups
- Create collaborative study groups
- Join existing groups for group learning
- Participate in group study sessions
- Track group progress and performance

### 📊 Social Analytics
- Track social interactions and engagement
- Monitor community participation
- Analyze learning effectiveness in social contexts
- Generate personalized recommendations

### 🔔 Notifications
- Receive real-time notifications
- Track unread notifications
- Manage notification preferences
- Get activity updates

## Authentication

All endpoints require authentication. Include your JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## API Endpoints

### Community Sets

#### Create Community Set
```http
POST /api/v1/social/community-sets
```

Share a flashcard set with the community.

**Request Body:**
```json
{
  "original_set_id": 123,
  "title": "Advanced English Vocabulary",
  "description": "A comprehensive set of advanced English words",
  "category": "language",
  "tags": ["english", "advanced", "vocabulary"],
  "difficulty_level": "hard",
  "language": "en",
  "is_public": true
}
```

**Response:**
```json
{
  "id": 1,
  "original_set_id": 123,
  "creator_id": 456,
  "title": "Advanced English Vocabulary",
  "description": "A comprehensive set of advanced English words",
  "category": "language",
  "tags": ["english", "advanced", "vocabulary"],
  "difficulty_level": "hard",
  "language": "en",
  "is_public": true,
  "is_featured": false,
  "view_count": 0,
  "import_count": 0,
  "rating": 0.0,
  "rating_count": 0,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### Get Community Sets
```http
GET /api/v1/social/community-sets
```

Browse community-shared flashcard sets with filters.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 20, max: 100)
- `category` (string, optional): Filter by category
- `difficulty` (string, optional): Filter by difficulty level
- `language` (string, optional): Filter by language
- `featured_only` (boolean, optional): Show only featured sets (default: false)

**Response:**
```json
{
  "sets": [
    {
      "id": 1,
      "original_set_id": 123,
      "creator_id": 456,
      "title": "Advanced English Vocabulary",
      "description": "A comprehensive set of advanced English words",
      "category": "language",
      "tags": ["english", "advanced", "vocabulary"],
      "difficulty_level": "hard",
      "language": "en",
      "is_public": true,
      "is_featured": false,
      "view_count": 15,
      "import_count": 3,
      "rating": 4.5,
      "rating_count": 2,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

#### Rate Community Set
```http
POST /api/v1/social/community-sets/{set_id}/rate
```

Rate and review a community set.

**Request Body:**
```json
{
  "rating": 5,
  "review": "Excellent vocabulary set! Very helpful for advanced learners."
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 456,
  "community_set_id": 1,
  "rating": 5,
  "review": "Excellent vocabulary set! Very helpful for advanced learners.",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

### Study Groups

#### Create Study Group
```http
POST /api/v1/social/study-groups
```

Create a new study group for collaborative learning.

**Request Body:**
```json
{
  "name": "Advanced English Learners",
  "description": "A group for advanced English vocabulary study",
  "is_public": true,
  "max_members": 20
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Advanced English Learners",
  "description": "A group for advanced English vocabulary study",
  "creator_id": 456,
  "is_public": true,
  "max_members": 20,
  "current_members": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### Join Study Group
```http
POST /api/v1/social/study-groups/{group_id}/join
```

Join an existing study group.

**Response:**
```json
{
  "id": 1,
  "group_id": 1,
  "user_id": 789,
  "role": "member",
  "joined_at": "2024-01-01T00:00:00Z"
}
```

#### Get User Study Groups
```http
GET /api/v1/social/study-groups
```

Get study groups for the current user.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 20, max: 100)

**Response:**
```json
{
  "groups": [
    {
      "id": 1,
      "name": "Advanced English Learners",
      "description": "A group for advanced English vocabulary study",
      "creator_id": 456,
      "is_public": true,
      "max_members": 20,
      "current_members": 3,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

### Notifications

#### Get User Notifications
```http
GET /api/v1/social/notifications
```

Get notifications for the current user.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 20, max: 100)
- `unread_only` (boolean, optional): Show only unread notifications (default: false)

**Response:**
```json
{
  "notifications": [
    {
      "id": 1,
      "user_id": 456,
      "notification_type": "follow",
      "title": "New Follower",
      "message": "John Doe started following you",
      "data": {"follower_id": 789, "follower_name": "John Doe"},
      "is_read": false,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "unread_count": 1
}
```

#### Mark Notification as Read
```http
PUT /api/v1/social/notifications/{notification_id}/read
```

Mark a notification as read.

**Response:**
```json
{
  "id": 1,
  "user_id": 456,
  "notification_type": "follow",
  "title": "New Follower",
  "message": "John Doe started following you",
  "data": {"follower_id": 789, "follower_name": "John Doe"},
  "is_read": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Social Analytics

#### Get Social Insights
```http
GET /api/v1/social/analytics
```

Get social interaction analytics for the user.

**Query Parameters:**
- `days` (int, optional): Number of days to analyze (default: 30, max: 365)

**Response:**
```json
{
  "total_followers": 15,
  "total_following": 8,
  "sets_shared": 5,
  "sets_imported": 12,
  "community_rating": 4.2,
  "group_participation": 3,
  "recent_activity": [
    {
      "type": "share",
      "description": "Shared 'Advanced English Vocabulary' set",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Advanced Analytics
```http
GET /api/v1/social/advanced-analytics
```

Get comprehensive analytics including social and community data.

**Query Parameters:**
- `days` (int, optional): Number of days to analyze (default: 30, max: 365)

**Response:**
```json
{
  "study_trends": {
    "total_study_time": 450,
    "average_accuracy": 0.85,
    "cards_studied": 150,
    "study_sessions": 12
  },
  "social_interactions": {
    "total_interactions": 25,
    "interaction_breakdown": {
      "share": 5,
      "import": 12,
      "rate": 8
    }
  },
  "community_engagement": {
    "sets_shared": 5,
    "sets_imported": 12,
    "average_rating": 4.2,
    "group_participation": 3
  },
  "learning_effectiveness": {
    "retention_rate": 0.78,
    "improvement_rate": 0.15,
    "consistency_score": 0.92
  },
  "recommendations": [
    {
      "type": "study_time",
      "title": "Increase Study Time",
      "description": "Try to study for at least 30 minutes daily for better retention",
      "priority": "medium"
    }
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limits

- **Community Sets**: 10 requests per minute
- **Study Groups**: 5 requests per minute
- **Notifications**: 20 requests per minute
- **Analytics**: 5 requests per minute

## Best Practices

### Community Sets
1. **Descriptive Titles**: Use clear, descriptive titles for your sets
2. **Proper Categorization**: Choose appropriate categories and tags
3. **Quality Content**: Ensure your sets contain high-quality, accurate content
4. **Regular Updates**: Keep your sets updated and relevant

### Study Groups
1. **Clear Purpose**: Define the group's purpose and goals clearly
2. **Active Participation**: Encourage regular participation from members
3. **Respectful Environment**: Maintain a supportive and respectful learning environment
4. **Progress Tracking**: Monitor group progress and celebrate achievements

### Notifications
1. **Timely Responses**: Respond to notifications promptly
2. **Manage Preferences**: Configure notification settings according to your preferences
3. **Regular Cleanup**: Mark notifications as read to keep your inbox organized

## Examples

### Complete Workflow: Sharing a Set

1. **Create a Community Set**
```bash
curl -X POST "http://localhost:8000/api/v1/social/community-sets" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "original_set_id": 123,
    "title": "Business English Vocabulary",
    "description": "Essential business terms for professionals",
    "category": "business",
    "tags": ["business", "english", "professional"],
    "difficulty_level": "medium",
    "language": "en",
    "is_public": true
  }'
```

2. **Browse Community Sets**
```bash
curl -X GET "http://localhost:8000/api/v1/social/community-sets?category=business&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

3. **Rate a Set**
```bash
curl -X POST "http://localhost:8000/api/v1/social/community-sets/1/rate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "review": "Excellent business vocabulary set!"
  }'
```

### Study Group Management

1. **Create a Study Group**
```bash
curl -X POST "http://localhost:8000/api/v1/social/study-groups" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Business English Study Group",
    "description": "Group for studying business English vocabulary",
    "is_public": true,
    "max_members": 15
  }'
```

2. **Join a Study Group**
```bash
curl -X POST "http://localhost:8000/api/v1/social/study-groups/1/join" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Support

For questions or issues with the Social Features API, please refer to:
- [API Documentation](https://your-api-docs.com)
- [Community Guidelines](https://your-community-guidelines.com)
- [Support Forum](https://your-support-forum.com)
