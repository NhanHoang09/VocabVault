# 🎮 Gamification API - Quick Reference

## 📋 Overview

Gamification module provides a complete gaming system for vocabulary learning with badges, points, leaderboards, and educational games.

**Base URL**: `/api/v1/gamification`

---

## 🏗️ System Architecture

### 6 MAIN COMPONENTS

#### 1. **Badges (Huy hiệu) 🏆**

- **Purpose**: Achievement and reward system
- **Features**:
  - Award badges for accomplishments
  - Track progress and achievements
  - Create motivation and sense of accomplishment
- **Endpoints**: 5 endpoints for badge management
- **Examples**: "First Steps", "Streak Master", "Speed Demon"

#### 2. **Points (Điểm số) 💰**

- **Purpose**: Point and level progression system
- **Features**:
  - Calculate points based on performance
  - Level up system (1 level per 1000 points)
  - Track transaction history
- **Endpoints**: 2 endpoints for stats and history
- **Examples**: Study session = 10-50 points, Correct answer = 5-20 points

#### 3. **Leaderboard (Bảng xếp hạng) 🏅**

- **Purpose**: Competition and social interaction
- **Features**:
  - Display user rankings
  - Multiple time periods (daily, weekly, monthly, all-time)
  - Track user position and score
- **Endpoints**: 1 endpoint with category filtering
- **Examples**: Top 50 users by points, streaks, badges

#### 4. **Game Sessions (Phiên chơi) 🎮**

- **Purpose**: Game session management
- **Features**:
  - Start/end game sessions
  - Track session duration and performance
  - Link games with flashcard sets
- **Endpoints**: 4 endpoints for CRUD sessions
- **Examples**: 10-minute match game session with "Basic English" set

#### 5. **Games (Các trò chơi) 🎯**

- **Purpose**: Educational games for vocabulary learning
- **Features**:
  - 4 different game types
  - Real-time scoring and progress tracking
  - Performance analytics
- **Endpoints**: 12 endpoints for 4 game types
- **Examples**: Match cards, Type words, Speed Q&A, Memory game

#### 6. **Challenges (Thử thách) 🏁**

- **Purpose**: Long-term goals and achievements
- **Features**:
  - Weekly/monthly challenges
  - Progress tracking
  - Reward system
- **Endpoints**: 5 endpoints for challenge management
- **Examples**: "Study 7 consecutive days", "Earn 1000 points"

---

## 🎮 4 GAME TYPES DETAILED

### 1. **Match Game (Trò chơi ghép cặp) 🎯**

```
🎯 Concept: Match vocabulary cards with meanings
📱 Gameplay:
- Display grid of cards (word + meaning)
- User clicks 2 cards to match
- If correct → cards disappear, + points
- If wrong → cards flip back, - time

🎮 Mechanics:
- Card pairs: 8-16 pairs
- Time limit: 300-600 seconds
- Scoring: Base points + time bonus + efficiency bonus
- Moves tracking: Number of clicks to complete

📊 Example:
- 8 card pairs, 5 minutes
- Perfect score: 800 points
- Efficiency bonus: -10 points per extra move
```

### 2. **Gravity Game (Trò chơi rơi từ) 🌟**

```
🎯 Concept: Type words before they fall to bottom
📱 Gameplay:
- Words fall from top to bottom
- User must type correct word before it hits bottom
- Falling speed increases gradually
- Combo multiplier for consecutive correct answers

🎮 Mechanics:
- Word count: 50-100 words
- Speed multiplier: 1.0x → 3.0x
- Combo system: 2x, 3x, 5x multiplier
- Scoring: Base points × combo × speed

📊 Example:
- 50 words, 5 minutes
- Combo 5x: 250 points per word
- Perfect run: 12,500 points
```

### 3. **Speed Challenge (Thử thách tốc độ) ⚡**

```
🎯 Concept: Answer questions as fast as possible
📱 Gameplay:
- Display questions (word → meaning or vice versa)
- Multiple choice or typing
- Timer countdown
- Streak bonus for consecutive correct

🎮 Mechanics:
- Question count: 20-50 questions
- Time limit: 60-300 seconds
- Difficulty levels: Easy, Medium, Hard
- Streak system: +10 points per consecutive correct

📊 Example:
- 30 questions, 2 minutes
- Streak 10: +100 bonus points
- Perfect accuracy: 1500 points
```

### 4. **Memory Game (Trò chơi trí nhớ) 🧠**

```
🎯 Concept: Concentration game with vocabulary cards
📱 Gameplay:
- Grid of face-down cards
- User flips 2 cards per turn
- If match → cards stay open, + points
- If no match → cards flip back
- Find all pairs to complete

🎮 Mechanics:
- Card pairs: 12-24 pairs
- Time limit: 600-1200 seconds
- Reveal tracking: Number of card flips
- Scoring: Base points - penalty for extra reveals

📊 Example:
- 16 card pairs, 10 minutes
- Perfect memory: 1600 points
- Extra reveals: -10 points each
```

---

## 🔄 SYSTEM INTEGRATION

### Complete Flow:

```
1. User start game session → 2. Choose game type → 3. Play game → 4. End session → 5. Award points → 6. Check badges → 7. Update leaderboard → 8. Check challenges
```

### Cross-system Benefits:

- **Games** → **Points** → **Levels** → **Badges**
- **Performance** → **Leaderboard ranking**
- **Consistency** → **Study streaks** → **Challenges**
- **All activities** → **Analytics** → **Progress tracking**

### Educational Value:

- **Match**: Visual learning, word-meaning association
- **Gravity**: Typing practice, speed reading
- **Speed Challenge**: Quick recall, decision making
- **Memory**: Concentration, pattern recognition

---

## 🚀 Quick Start

### Authentication

All endpoints require authentication via Bearer token:

```bash
Authorization: Bearer <your_jwt_token>
```

### Common Headers

```bash
Content-Type: application/json
Accept: application/json
```

## 🏆 Core Features

### 1. Badge System

- **GET** `/badges` - List all badges
- **GET** `/badges/{id}` - Get badge details
- **GET** `/users/{id}/badges` - Get user badges
- **POST** `/badges/{id}/award` - Award badge

### 2. Points System

- **GET** `/points` - Get user stats
- **GET** `/points/transactions` - Get transaction history

### 3. Leaderboard

- **GET** `/leaderboard` - Get rankings

### 4. Game Sessions

- **POST** `/games/sessions` - Start game session
- **GET** `/games/sessions` - List sessions
- **PUT** `/games/sessions/{id}` - End session

### 5. Educational Games

- **Match Game**: `/games/match/{session_id}`
- **Gravity Game**: `/games/gravity/{session_id}`
- **Speed Challenge**: `/games/speed-challenge/{session_id}`
- **Memory Game**: `/games/memory/{session_id}`

### 6. Challenges

- **GET** `/challenges` - List challenges
- **POST** `/challenges/{id}/start` - Start challenge
- **POST** `/challenges/{id}/complete` - Complete challenge

## 🎯 Game Types

| Game            | Description        | Endpoints                     |
| --------------- | ------------------ | ----------------------------- |
| Match           | Match card pairs   | `POST`, `PUT`, `POST /move`   |
| Gravity         | Type falling words | `POST`, `PUT`, `POST /answer` |
| Speed Challenge | Quick Q&A          | `POST`, `PUT`, `POST /answer` |
| Memory          | Concentration game | `POST`, `PUT`, `POST /reveal` |

## 🏅 Challenge Types

| Type     | Description                     |
| -------- | ------------------------------- |
| streak   | Study streak challenges         |
| points   | Points earning challenges       |
| games    | Game completion challenges      |
| accuracy | Accuracy improvement challenges |

## 💰 Points System

### Earning Points

- Study sessions: 10-50 points
- Correct answers: 5-20 points
- Game completion: 50-200 points
- Badge earning: 25-500 points
- Challenge completion: 100-1000 points

### Levels

- Level 1: 0-999 points
- Level 2: 1000-1999 points
- Level 3: 2000-2999 points
- And so on...

## 🏆 Badge System

### Rarities

- **Common**: Easy to earn
- **Uncommon**: Moderately difficult
- **Rare**: Hard to earn
- **Epic**: Very difficult
- **Legendary**: Extremely difficult

### Example Badges

- First Steps (Common): Complete first study session
- Streak Master (Rare): 30-day study streak
- Speed Demon (Epic): Complete speed challenge in record time
- Perfect Memory (Legendary): Complete memory game with 100% accuracy

## 📊 Response Formats

### Success Response

```json
{
  "id": 1,
  "name": "Example",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### List Response

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

### Error Response

```json
{
  "detail": "Error message"
}
```

## 🔧 Common Parameters

### Pagination

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

### Filtering

- `game_type`: Filter by game type
- `challenge_type`: Filter by challenge type
- `category`: Leaderboard category (daily, weekly, monthly, all_time)

## 🚨 Error Codes

| Code | Description                            |
| ---- | -------------------------------------- |
| 400  | Bad Request - Invalid data             |
| 401  | Unauthorized - Authentication required |
| 403  | Forbidden - Access denied              |
| 404  | Not Found - Resource not found         |
| 422  | Validation Error - Invalid input       |

## 📝 Best Practices

1. **Session Management**: Always start a game session before playing games
2. **Progress Tracking**: Update game progress regularly
3. **Error Handling**: Check response status codes
4. **Rate Limiting**: Respect API rate limits
5. **Data Validation**: Validate input data before sending

## 🔗 Related Documentation

- [Full API Documentation](README.md)
- [Authentication Guide](../auth/README.md)
- [Flashcards API](../flashcards/README.md)
- [Analytics API](../analytics/README.md)
