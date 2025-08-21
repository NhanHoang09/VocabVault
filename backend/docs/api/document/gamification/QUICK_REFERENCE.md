# 🎮 Gamification API - Quick Reference

## 🏗️ System Overview

### 6 MAIN COMPONENTS

#### 1. **Badges (Huy hiệu) 🏆**

- Achievement and reward system
- 5 endpoints for badge management
- Examples: "First Steps", "Streak Master", "Speed Demon"

#### 2. **Points (Điểm số) 💰**

- Point and level progression system
- 2 endpoints for stats and history
- Level up: 1 level per 1000 points

#### 3. **Leaderboard (Bảng xếp hạng) 🏅**

- Competition and social interaction
- 1 endpoint with category filtering
- Time periods: daily, weekly, monthly, all-time

#### 4. **Game Sessions (Phiên chơi) 🎮**

- Game session management
- 4 endpoints for CRUD sessions
- Link games with flashcard sets

#### 5. **Games (Các trò chơi) 🎯**

- Educational games for vocabulary learning
- 12 endpoints for 4 game types
- Real-time scoring and progress tracking

#### 6. **Challenges (Thử thách) 🏁**

- Long-term goals and achievements
- 5 endpoints for challenge management
- Weekly/monthly challenges with rewards

---

## 🎮 4 GAME TYPES

### 1. **Match Game (Trò chơi ghép cặp) 🎯**

- **Concept**: Match vocabulary cards with meanings
- **Mechanics**: 8-16 card pairs, 300-600s time limit
- **Scoring**: Base points + time bonus + efficiency bonus
- **Example**: 8 pairs, 5 min → Perfect score: 800 points

### 2. **Gravity Game (Trò chơi rơi từ) 🌟**

- **Concept**: Type words before they fall to bottom
- **Mechanics**: 50-100 words, speed multiplier 1.0x→3.0x
- **Scoring**: Base points × combo × speed
- **Example**: 50 words, combo 5x → 12,500 points

### 3. **Speed Challenge (Thử thách tốc độ) ⚡**

- **Concept**: Answer questions as fast as possible
- **Mechanics**: 20-50 questions, 60-300s time limit
- **Scoring**: Base points + streak bonus
- **Example**: 30 questions, streak 10 → 1500 points

### 4. **Memory Game (Trò chơi trí nhớ) 🧠**

- **Concept**: Concentration game with vocabulary cards
- **Mechanics**: 12-24 card pairs, 600-1200s time limit
- **Scoring**: Base points - penalty for extra reveals
- **Example**: 16 pairs, perfect memory → 1600 points

---

## 🚀 Essential Endpoints

### Badges

```bash
GET    /api/v1/gamification/badges                    # List all badges
GET    /api/v1/gamification/badges/{id}               # Get badge details
GET    /api/v1/gamification/users/{id}/badges         # Get user badges
POST   /api/v1/gamification/badges/{id}/award         # Award badge
```

### Points & Stats

```bash
GET    /api/v1/gamification/points                    # Get user stats
GET    /api/v1/gamification/points/transactions       # Get transaction history
```

### Leaderboard

```bash
GET    /api/v1/gamification/leaderboard               # Get rankings
```

### Game Sessions

```bash
POST   /api/v1/gamification/games/sessions            # Start session
GET    /api/v1/gamification/games/sessions            # List sessions
PUT    /api/v1/gamification/games/sessions/{id}       # End session
```

### Games

```bash
# Match Game
POST   /api/v1/gamification/games/match/{session_id}  # Create match game
PUT    /api/v1/gamification/games/match/{session_id}  # Update match game
POST   /api/v1/gamification/games/match/{session_id}/move  # Record move

# Gravity Game
POST   /api/v1/gamification/games/gravity/{session_id}     # Create gravity game
PUT    /api/v1/gamification/games/gravity/{session_id}     # Update gravity game
POST   /api/v1/gamification/games/gravity/{session_id}/answer  # Submit answer

# Speed Challenge
POST   /api/v1/gamification/games/speed-challenge/{session_id}  # Create speed challenge
PUT    /api/v1/gamification/games/speed-challenge/{session_id}  # Update speed challenge
POST   /api/v1/gamification/games/speed-challenge/{session_id}/answer  # Submit answer

# Memory Game
POST   /api/v1/gamification/games/memory/{session_id}      # Create memory game
PUT    /api/v1/gamification/games/memory/{session_id}      # Update memory game
POST   /api/v1/gamification/games/memory/{session_id}/reveal  # Reveal card
```

### Challenges

```bash
GET    /api/v1/gamification/challenges                # List challenges
GET    /api/v1/gamification/challenges/{id}           # Get challenge details
POST   /api/v1/gamification/challenges/{id}/start     # Start challenge
POST   /api/v1/gamification/challenges/{id}/complete  # Complete challenge
```

## 📊 Common Request/Response Examples

### Start Game Session

```bash
POST /api/v1/gamification/games/sessions
Content-Type: application/json
Authorization: Bearer <token>

{
  "game_type": "match",
  "set_id": 1,
  "difficulty": "medium",
  "time_limit_minutes": 10
}
```

### Get User Stats

```bash
GET /api/v1/gamification/points
Authorization: Bearer <token>

# Response
{
  "total_points": 1250,
  "level": 2,
  "experience_points": 250,
  "study_streak_days": 7,
  "longest_streak": 15,
  "total_badges": 5,
  "total_games_played": 12
}
```

### Submit Game Answer

```bash
POST /api/v1/gamification/games/gravity/{session_id}/answer
Content-Type: application/json
Authorization: Bearer <token>

{
  "is_correct": true,
  "response_time_seconds": 2.5
}
```

## 🎯 Game Types & Parameters

| Game Type         | Description        | Key Parameters                     |
| ----------------- | ------------------ | ---------------------------------- |
| `match`           | Match card pairs   | `card_pairs`, `time_limit_seconds` |
| `gravity`         | Type falling words | `word_count`, `speed_multiplier`   |
| `speed_challenge` | Quick Q&A          | `question_count`, `difficulty`     |
| `memory`          | Concentration      | `card_pairs`, `time_limit_seconds` |

## 🏅 Challenge Types

| Type       | Description     | Example Requirements          |
| ---------- | --------------- | ----------------------------- |
| `streak`   | Study streaks   | `{"study_days": 7}`           |
| `points`   | Points earning  | `{"points_required": 1000}`   |
| `games`    | Game completion | `{"games_played": 10}`        |
| `accuracy` | Accuracy goals  | `{"accuracy_threshold": 0.9}` |

## 💰 Points System

### Earning Points

- Study session: 10-50 points
- Correct answer: 5-20 points
- Game completion: 50-200 points
- Badge earned: 25-500 points
- Challenge completed: 100-1000 points

### Levels

- Level = (total_points // 1000) + 1
- Experience = total_points % 1000

## 🏆 Badge Rarities

| Rarity    | Points Reward | Difficulty |
| --------- | ------------- | ---------- |
| Common    | 25-50         | Easy       |
| Uncommon  | 75-150        | Medium     |
| Rare      | 200-350       | Hard       |
| Epic      | 400-750       | Very Hard  |
| Legendary | 800-1500      | Extreme    |

## 🔧 Query Parameters

### Pagination

```bash
?skip=0&limit=20
```

### Filtering

```bash
?game_type=match
?challenge_type=streak
?category=weekly
```

## 🚨 Common Error Codes

| Code | Meaning          | Solution               |
| ---- | ---------------- | ---------------------- |
| 400  | Bad Request      | Check request data     |
| 401  | Unauthorized     | Add valid token        |
| 403  | Forbidden        | Check permissions      |
| 404  | Not Found        | Verify resource exists |
| 422  | Validation Error | Fix input format       |

## 📝 Best Practices

1. **Always authenticate** with Bearer token
2. **Start game sessions** before playing games
3. **Update progress** regularly during games
4. **Handle errors** gracefully
5. **Use pagination** for large lists
6. **Validate input** before sending

## 🔄 System Integration Flow

```
1. Start game session → 2. Choose game type → 3. Play game → 4. End session → 5. Award points → 6. Check badges → 7. Update leaderboard → 8. Check challenges
```

## 🎓 Educational Value

- **Match**: Visual learning, word-meaning association
- **Gravity**: Typing practice, speed reading
- **Speed Challenge**: Quick recall, decision making
- **Memory**: Concentration, pattern recognition

## 🔗 Related APIs

- **Auth**: `/api/v1/auth/*` - Authentication
- **Flashcards**: `/api/v1/flashcards/*` - Flashcard management
- **Analytics**: `/api/v1/analytics/*` - Learning analytics
- **Learning**: `/api/v1/learning/*` - Study sessions
