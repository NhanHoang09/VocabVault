# 🎮 Gamification API Documentation

## 🎯 Tổng quan

Gamification module cung cấp **25+ endpoints** để quản lý hệ thống gamification hoàn chỉnh bao gồm badges, points, leaderboard, games và challenges. Module này tạo ra trải nghiệm học tập thú vị và có tính cạnh tranh.

**Base URL**: `/api/v1/gamification`

---

## 🏗️ Kiến trúc hệ thống

### 6 NHÓM CHÍNH

#### 1. **Badges (Huy hiệu) 🏆**

- **Mục đích**: Hệ thống thành tích và phần thưởng
- **Chức năng**:
  - Award badges cho user khi đạt thành tích
  - Track progress và achievements
  - Tạo motivation và sense of accomplishment
- **Endpoints**: 5 endpoints để quản lý badges
- **Ví dụ**: "First Steps", "Streak Master", "Speed Demon"

#### 2. **Points (Điểm số) 💰**

- **Mục đích**: Hệ thống điểm và level progression
- **Chức năng**:
  - Tính điểm dựa trên performance
  - Level up system (1 level per 1000 points)
  - Track transaction history
- **Endpoints**: 2 endpoints để xem stats và history
- **Ví dụ**: Study session = 10-50 points, Correct answer = 5-20 points

#### 3. **Leaderboard (Bảng xếp hạng) 🏅**

- **Mục đích**: Tạo tính cạnh tranh và social interaction
- **Chức năng**:
  - Hiển thị ranking của users
  - Multiple time periods (daily, weekly, monthly, all-time)
  - Track user position và score
- **Endpoints**: 1 endpoint với category filtering
- **Ví dụ**: Top 50 users theo points, streaks, badges

#### 4. **Game Sessions (Phiên chơi) 🎮**

- **Mục đích**: Quản lý phiên chơi game
- **Chức năng**:
  - Start/end game sessions
  - Track session duration và performance
  - Link games với flashcard sets
- **Endpoints**: 4 endpoints để CRUD sessions
- **Ví dụ**: 10-minute match game session với set "Basic English"

#### 5. **Games (Các trò chơi) 🎯**

- **Mục đích**: Educational games để học vocabulary
- **Chức năng**:
  - 4 loại game khác nhau
  - Real-time scoring và progress tracking
  - Performance analytics
- **Endpoints**: 12 endpoints cho 4 game types
- **Ví dụ**: Match cards, Type words, Speed Q&A, Memory game

#### 6. **Challenges (Thử thách) 🏁**

- **Mục đích**: Long-term goals và achievements
- **Chức năng**:
  - Weekly/monthly challenges
  - Progress tracking
  - Reward system
- **Endpoints**: 5 endpoints để manage challenges
- **Ví dụ**: "Study 7 consecutive days", "Earn 1000 points"

---

## 🎮 4 LOẠI GAME CHI TIẾT

### 1. **Match Game (Trò chơi ghép cặp) 🎯**

```
🎯 Concept: Ghép cặp thẻ từ vựng với nghĩa
📱 Gameplay:
- Hiển thị grid các thẻ (word + meaning)
- User click 2 thẻ để ghép cặp
- Nếu đúng → thẻ biến mất, + điểm
- Nếu sai → thẻ lật lại, - thời gian

🎮 Mechanics:
- Card pairs: 8-16 cặp thẻ
- Time limit: 300-600 seconds
- Scoring: Base points + time bonus + efficiency bonus
- Moves tracking: Số lần click để hoàn thành

📊 Example:
- 8 cặp thẻ, 5 phút
- Perfect score: 800 points
- Efficiency bonus: -10 points per extra move
```

### 2. **Gravity Game (Trò chơi rơi từ) 🌟**

```
🎯 Concept: Gõ từ vựng trước khi chúng rơi xuống
📱 Gameplay:
- Từ vựng rơi từ trên xuống
- User phải gõ đúng từ trước khi chạm đáy
- Tốc độ rơi tăng dần
- Combo multiplier cho chuỗi đúng liên tiếp

🎮 Mechanics:
- Word count: 50-100 từ
- Speed multiplier: 1.0x → 3.0x
- Combo system: 2x, 3x, 5x multiplier
- Scoring: Base points × combo × speed

📊 Example:
- 50 từ, 5 phút
- Combo 5x: 250 points per word
- Perfect run: 12,500 points
```

### 3. **Speed Challenge (Thử thách tốc độ) ⚡**

```
🎯 Concept: Trả lời câu hỏi nhanh nhất có thể
📱 Gameplay:
- Hiển thị câu hỏi (word → meaning hoặc ngược lại)
- Multiple choice hoặc typing
- Timer countdown
- Streak bonus cho chuỗi đúng

🎮 Mechanics:
- Question count: 20-50 câu
- Time limit: 60-300 seconds
- Difficulty levels: Easy, Medium, Hard
- Streak system: +10 points per consecutive correct

📊 Example:
- 30 câu, 2 phút
- Streak 10: +100 bonus points
- Perfect accuracy: 1500 points
```

### 4. **Memory Game (Trò chơi trí nhớ) 🧠**

```
🎯 Concept: Concentration game với thẻ từ vựng
📱 Gameplay:
- Grid các thẻ úp
- User lật 2 thẻ mỗi lượt
- Nếu match → thẻ mở, + điểm
- Nếu không match → thẻ úp lại
- Tìm tất cả cặp để hoàn thành

🎮 Mechanics:
- Card pairs: 12-24 cặp
- Time limit: 600-1200 seconds
- Reveal tracking: Số lần lật thẻ
- Scoring: Base points - penalty for extra reveals

📊 Example:
- 16 cặp thẻ, 10 phút
- Perfect memory: 1600 points
- Extra reveals: -10 points each
```

---

## 🔄 TÍCH HỢP HỆ THỐNG

### Flow hoàn chỉnh:

```
1. User start game session → 2. Choose game type → 3. Play game → 4. End session → 5. Award points → 6. Check badges → 7. Update leaderboard → 8. Check challenges
```

### Cross-system benefits:

- **Games** → **Points** → **Levels** → **Badges**
- **Performance** → **Leaderboard ranking**
- **Consistency** → **Study streaks** → **Challenges**
- **All activities** → **Analytics** → **Progress tracking**

### Educational value:

- **Match**: Visual learning, word-meaning association
- **Gravity**: Typing practice, speed reading
- **Speed Challenge**: Quick recall, decision making
- **Memory**: Concentration, pattern recognition

---

## 📋 Danh sách Endpoints

### 🏆 Badge Management

| Method | Endpoint                   | Auth | Description                  |
| ------ | -------------------------- | ---- | ---------------------------- |
| `GET`  | `/badges`                  | ✅   | Lấy danh sách tất cả badges  |
| `GET`  | `/badges/{badge_id}`       | ✅   | Lấy thông tin chi tiết badge |
| `GET`  | `/users/{user_id}/badges`  | ✅   | Lấy badges của user          |
| `POST` | `/badges/{badge_id}/award` | ✅   | Award badge cho user         |
| `POST` | `/badges/earn`             | ✅   | Earn badge (alias)           |

### 💰 Points System

| Method | Endpoint               | Auth | Description                        |
| ------ | ---------------------- | ---- | ---------------------------------- |
| `GET`  | `/points`              | ✅   | Lấy thống kê gamification của user |
| `GET`  | `/points/transactions` | ✅   | Lấy lịch sử giao dịch points       |

### 🏅 Leaderboard

| Method | Endpoint       | Auth | Description                   |
| ------ | -------------- | ---- | ----------------------------- |
| `GET`  | `/leaderboard` | ✅   | Lấy leaderboard theo category |

### 🎮 Game Sessions

| Method | Endpoint                       | Auth | Description                 |
| ------ | ------------------------------ | ---- | --------------------------- |
| `POST` | `/games/sessions`              | ✅   | Tạo game session mới        |
| `GET`  | `/games/sessions`              | ✅   | Lấy danh sách game sessions |
| `GET`  | `/games/sessions/{session_id}` | ✅   | Lấy thông tin game session  |
| `PUT`  | `/games/sessions/{session_id}` | ✅   | Cập nhật game session       |

### 🎯 Match Game

| Method | Endpoint                         | Auth | Description                    |
| ------ | -------------------------------- | ---- | ------------------------------ |
| `POST` | `/games/match/{session_id}`      | ✅   | Tạo Match game                 |
| `PUT`  | `/games/match/{session_id}`      | ✅   | Cập nhật Match game            |
| `POST` | `/games/match/{session_id}/move` | ✅   | Ghi nhận move trong Match game |

### 🌟 Gravity Game

| Method | Endpoint                             | Auth | Description                      |
| ------ | ------------------------------------ | ---- | -------------------------------- |
| `POST` | `/games/gravity/{session_id}`        | ✅   | Tạo Gravity game                 |
| `PUT`  | `/games/gravity/{session_id}`        | ✅   | Cập nhật Gravity game            |
| `POST` | `/games/gravity/{session_id}/answer` | ✅   | Submit answer trong Gravity game |

### ⚡ Speed Challenge

| Method | Endpoint                                     | Auth | Description                         |
| ------ | -------------------------------------------- | ---- | ----------------------------------- |
| `POST` | `/games/speed-challenge/{session_id}`        | ✅   | Tạo Speed Challenge                 |
| `PUT`  | `/games/speed-challenge/{session_id}`        | ✅   | Cập nhật Speed Challenge            |
| `POST` | `/games/speed-challenge/{session_id}/answer` | ✅   | Submit answer trong Speed Challenge |

### 🧠 Memory Game

| Method | Endpoint                            | Auth | Description                   |
| ------ | ----------------------------------- | ---- | ----------------------------- |
| `POST` | `/games/memory/{session_id}`        | ✅   | Tạo Memory game               |
| `PUT`  | `/games/memory/{session_id}`        | ✅   | Cập nhật Memory game          |
| `POST` | `/games/memory/{session_id}/reveal` | ✅   | Reveal card trong Memory game |

### 🏁 Challenges

| Method | Endpoint                              | Auth | Description              |
| ------ | ------------------------------------- | ---- | ------------------------ |
| `GET`  | `/challenges`                         | ✅   | Lấy danh sách challenges |
| `GET`  | `/challenges/{challenge_id}`          | ✅   | Lấy thông tin challenge  |
| `GET`  | `/users/{user_id}/challenges`         | ✅   | Lấy challenges của user  |
| `POST` | `/challenges/{challenge_id}/start`    | ✅   | Bắt đầu challenge        |
| `POST` | `/challenges/{challenge_id}/complete` | ✅   | Hoàn thành challenge     |

---

## 🏆 BADGE ENDPOINTS

### 1. GET `/api/v1/gamification/badges` - Lấy danh sách badges

**🎯 Mục đích**: Lấy tất cả badges có sẵn trong hệ thống

**🔑 Authentication**: Required

**📝 Query Parameters**:

- `skip` (optional): Số records bỏ qua (default: 0)
- `limit` (optional): Số records tối đa (default: 100, max: 1000)

**✅ Response (200 OK)**:

```json
{
  "items": [
    {
      "id": 1,
      "name": "First Steps",
      "description": "Complete your first study session",
      "icon_url": "https://example.com/badges/first-steps.png",
      "points_reward": 50,
      "requirements": {
        "study_sessions": 1
      },
      "rarity": "common",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "pages": 1
}
```

---

### 2. GET `/api/v1/gamification/badges/{badge_id}` - Lấy thông tin badge

**🎯 Mục đích**: Lấy thông tin chi tiết của một badge cụ thể

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `badge_id` (required): ID của badge

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "name": "First Steps",
  "description": "Complete your first study session",
  "icon_url": "https://example.com/badges/first-steps.png",
  "points_reward": 50,
  "requirements": {
    "study_sessions": 1
  },
  "rarity": "common",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### 3. GET `/api/v1/gamification/users/{user_id}/badges` - Lấy badges của user

**🎯 Mục đích**: Lấy tất cả badges mà user đã đạt được

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `user_id` (required): ID của user

**📝 Query Parameters**:

- `skip` (optional): Số records bỏ qua (default: 0)
- `limit` (optional): Số records tối đa (default: 100, max: 1000)

**✅ Response (200 OK)**:

```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "badge_id": 1,
      "badge": {
        "id": 1,
        "name": "First Steps",
        "description": "Complete your first study session",
        "icon_url": "https://example.com/badges/first-steps.png",
        "points_reward": 50,
        "requirements": {
          "study_sessions": 1
        },
        "rarity": "common"
      },
      "earned_at": "2024-01-15T10:30:00Z",
      "points_awarded": 50
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "pages": 1
}
```

---

### 4. POST `/api/v1/gamification/badges/{badge_id}/award` - Award badge

**🎯 Mục đích**: Award badge cho user hiện tại

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `badge_id` (required): ID của badge cần award

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "user_id": 1,
  "badge_id": 1,
  "badge": {
    "id": 1,
    "name": "First Steps",
    "description": "Complete your first study session",
    "icon_url": "https://example.com/badges/first-steps.png",
    "points_reward": 50,
    "requirements": {
      "study_sessions": 1
    },
    "rarity": "common"
  },
  "earned_at": "2024-01-15T10:30:00Z",
  "points_awarded": 50
}
```

---

### 5. POST `/api/v1/gamification/badges/earn` - Earn badge

**🎯 Mục đích**: Earn badge (alias cho award_badge)

**🔑 Authentication**: Required

**📝 Query Parameters**:

- `badge_id` (required): ID của badge cần earn

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "user_id": 1,
  "badge_id": 1,
  "badge": {
    "id": 1,
    "name": "First Steps",
    "description": "Complete your first study session",
    "icon_url": "https://example.com/badges/first-steps.png",
    "points_reward": 50,
    "requirements": {
      "study_sessions": 1
    },
    "rarity": "common"
  },
  "earned_at": "2024-01-15T10:30:00Z",
  "points_awarded": 50
}
```

---

## 💰 POINTS ENDPOINTS

### 6. GET `/api/v1/gamification/points` - Lấy thống kê gamification

**🎯 Mục đích**: Lấy thống kê gamification tổng quan của user

**🔑 Authentication**: Required

**✅ Response (200 OK)**:

```json
{
  "total_points": 1250,
  "level": 2,
  "experience_points": 250,
  "study_streak_days": 7,
  "longest_streak": 15,
  "total_badges": 5,
  "total_games_played": 12,
  "total_study_time_minutes": 1800,
  "average_accuracy": 0.85,
  "rank": 15
}
```

---

### 7. GET `/api/v1/gamification/points/transactions` - Lấy lịch sử giao dịch

**🎯 Mục đích**: Lấy lịch sử giao dịch points của user

**🔑 Authentication**: Required

**📝 Query Parameters**:

- `skip` (optional): Số records bỏ qua (default: 0)
- `limit` (optional): Số records tối đa (default: 100, max: 1000)

**✅ Response (200 OK)**:

```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "points": 50,
      "transaction_type": "badge_earned",
      "description": "Earned First Steps badge",
      "reference_id": 1,
      "reference_type": "badge",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "pages": 1
}
```

---

## 🏅 LEADERBOARD ENDPOINTS

### 8. GET `/api/v1/gamification/leaderboard` - Lấy leaderboard

**🎯 Mục đích**: Lấy leaderboard theo category

**🔑 Authentication**: Required

**📝 Query Parameters**:

- `category` (optional): Category của leaderboard (daily, weekly, monthly, all_time) (default: all_time)
- `limit` (optional): Số entries tối đa (default: 50, max: 100)

**✅ Response (200 OK)**:

```json
{
  "category": "all_time",
  "period_start": "2024-01-01T00:00:00Z",
  "period_end": "2024-12-31T23:59:59Z",
  "entries": [
    {
      "rank": 1,
      "user_id": 1,
      "username": "top_learner",
      "score": 5000,
      "total_points": 5000,
      "study_streak_days": 30,
      "total_badges": 15,
      "total_games_played": 50
    }
  ],
  "total_entries": 1,
  "user_rank": 15,
  "user_score": 1250
}
```

---

## 🎮 GAME SESSION ENDPOINTS

### 9. POST `/api/v1/gamification/games/sessions` - Tạo game session

**🎯 Mục đích**: Tạo game session mới

**🔑 Authentication**: Required

**📝 Request Body**:

```json
{
  "game_type": "match",
  "set_id": 1,
  "difficulty": "medium",
  "time_limit_minutes": 10
}
```

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "user_id": 1,
  "game_type": "match",
  "set_id": 1,
  "difficulty": "medium",
  "time_limit_minutes": 10,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": null,
  "duration_minutes": null,
  "score": null,
  "accuracy": null,
  "status": "active"
}
```

---

### 10. GET `/api/v1/gamification/games/sessions` - Lấy danh sách game sessions

**🎯 Mục đích**: Lấy danh sách game sessions của user

**🔑 Authentication**: Required

**📝 Query Parameters**:

- `skip` (optional): Số records bỏ qua (default: 0)
- `limit` (optional): Số records tối đa (default: 100, max: 1000)
- `game_type` (optional): Filter theo game type

**✅ Response (200 OK)**:

```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "game_type": "match",
      "set_id": 1,
      "difficulty": "medium",
      "time_limit_minutes": 10,
      "started_at": "2024-01-15T10:30:00Z",
      "ended_at": "2024-01-15T10:40:00Z",
      "duration_minutes": 10,
      "score": 850,
      "accuracy": 0.85,
      "status": "completed"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "pages": 1
}
```

---

### 11. GET `/api/v1/gamification/games/sessions/{session_id}` - Lấy thông tin game session

**🎯 Mục đích**: Lấy thông tin chi tiết của game session

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "user_id": 1,
  "game_type": "match",
  "set_id": 1,
  "difficulty": "medium",
  "time_limit_minutes": 10,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": "2024-01-15T10:40:00Z",
  "duration_minutes": 10,
  "score": 850,
  "accuracy": 0.85,
  "status": "completed"
}
```

---

### 12. PUT `/api/v1/gamification/games/sessions/{session_id}` - Cập nhật game session

**🎯 Mục đích**: Cập nhật game session (kết thúc session)

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "ended_at": "2024-01-15T10:40:00Z",
  "score": 850,
  "accuracy": 0.85,
  "status": "completed"
}
```

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "user_id": 1,
  "game_type": "match",
  "set_id": 1,
  "difficulty": "medium",
  "time_limit_minutes": 10,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": "2024-01-15T10:40:00Z",
  "duration_minutes": 10,
  "score": 850,
  "accuracy": 0.85,
  "status": "completed"
}
```

---

## 🎯 MATCH GAME ENDPOINTS

### 13. POST `/api/v1/gamification/games/match/{session_id}` - Tạo Match game

**🎯 Mục đích**: Tạo Match game trong session

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "card_pairs": 8,
  "time_limit_seconds": 300
}
```

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "session_id": 1,
  "card_pairs": 8,
  "time_limit_seconds": 300,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": null,
  "duration_seconds": null,
  "moves_count": 0,
  "matches_found": 0,
  "score": null,
  "status": "active"
}
```

---

### 14. PUT `/api/v1/gamification/games/match/{session_id}` - Cập nhật Match game

**🎯 Mục đích**: Cập nhật tiến độ Match game

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "ended_at": "2024-01-15T10:35:00Z",
  "moves_count": 24,
  "matches_found": 8,
  "score": 850,
  "status": "completed"
}
```

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "session_id": 1,
  "card_pairs": 8,
  "time_limit_seconds": 300,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": "2024-01-15T10:35:00Z",
  "duration_seconds": 300,
  "moves_count": 24,
  "matches_found": 8,
  "score": 850,
  "status": "completed"
}
```

---

### 15. POST `/api/v1/gamification/games/match/{session_id}/move` - Ghi nhận move

**🎯 Mục đích**: Ghi nhận một move trong Match game

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "is_match": true
}
```

**✅ Response (200 OK)**:

```json
{
  "move_result": "match_found",
  "moves_count": 2,
  "matches_found": 1,
  "score_increment": 100,
  "current_score": 100
}
```

---

## 🌟 GRAVITY GAME ENDPOINTS

### 16. POST `/api/v1/gamification/games/gravity/{session_id}` - Tạo Gravity game

**🎯 Mục đích**: Tạo Gravity game trong session

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "word_count": 50,
  "time_limit_seconds": 300,
  "speed_multiplier": 1.0
}
```

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "session_id": 1,
  "word_count": 50,
  "time_limit_seconds": 300,
  "speed_multiplier": 1.0,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": null,
  "duration_seconds": null,
  "words_typed": 0,
  "correct_answers": 0,
  "combo_multiplier": 1,
  "score": null,
  "status": "active"
}
```

---

### 17. PUT `/api/v1/gamification/games/gravity/{session_id}` - Cập nhật Gravity game

**🎯 Mục đích**: Cập nhật tiến độ Gravity game

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "ended_at": "2024-01-15T10:35:00Z",
  "words_typed": 45,
  "correct_answers": 40,
  "combo_multiplier": 3,
  "score": 1200,
  "status": "completed"
}
```

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "session_id": 1,
  "word_count": 50,
  "time_limit_seconds": 300,
  "speed_multiplier": 1.0,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": "2024-01-15T10:35:00Z",
  "duration_seconds": 300,
  "words_typed": 45,
  "correct_answers": 40,
  "combo_multiplier": 3,
  "score": 1200,
  "status": "completed"
}
```

---

### 18. POST `/api/v1/gamification/games/gravity/{session_id}/answer` - Submit answer

**🎯 Mục đích**: Submit answer trong Gravity game

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "is_correct": true,
  "response_time_seconds": 2.5
}
```

**✅ Response (200 OK)**:

```json
{
  "answer_result": "correct",
  "words_typed": 1,
  "correct_answers": 1,
  "combo_multiplier": 2,
  "score_increment": 50,
  "current_score": 50
}
```

---

## ⚡ SPEED CHALLENGE ENDPOINTS

### 19. POST `/api/v1/gamification/games/speed-challenge/{session_id}` - Tạo Speed Challenge

**🎯 Mục đích**: Tạo Speed Challenge trong session

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "question_count": 20,
  "time_limit_seconds": 120,
  "difficulty": "medium"
}
```

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "session_id": 1,
  "question_count": 20,
  "time_limit_seconds": 120,
  "difficulty": "medium",
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": null,
  "duration_seconds": null,
  "questions_answered": 0,
  "correct_answers": 0,
  "current_streak": 0,
  "score": null,
  "status": "active"
}
```

---

### 20. PUT `/api/v1/gamification/games/speed-challenge/{session_id}` - Cập nhật Speed Challenge

**🎯 Mục đích**: Cập nhật tiến độ Speed Challenge

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "ended_at": "2024-01-15T10:32:00Z",
  "questions_answered": 18,
  "correct_answers": 15,
  "current_streak": 5,
  "score": 750,
  "status": "completed"
}
```

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "session_id": 1,
  "question_count": 20,
  "time_limit_seconds": 120,
  "difficulty": "medium",
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": "2024-01-15T10:32:00Z",
  "duration_seconds": 120,
  "questions_answered": 18,
  "correct_answers": 15,
  "current_streak": 5,
  "score": 750,
  "status": "completed"
}
```

---

### 21. POST `/api/v1/gamification/games/speed-challenge/{session_id}/answer` - Submit answer

**🎯 Mục đích**: Submit answer trong Speed Challenge

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "is_correct": true,
  "response_time_seconds": 3.2
}
```

**✅ Response (200 OK)**:

```json
{
  "answer_result": "correct",
  "questions_answered": 1,
  "correct_answers": 1,
  "current_streak": 1,
  "score_increment": 50,
  "current_score": 50
}
```

---

## 🧠 MEMORY GAME ENDPOINTS

### 22. POST `/api/v1/gamification/games/memory/{session_id}` - Tạo Memory game

**🎯 Mục đích**: Tạo Memory game trong session

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "card_pairs": 12,
  "time_limit_seconds": 600
}
```

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "session_id": 1,
  "card_pairs": 12,
  "time_limit_seconds": 600,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": null,
  "duration_seconds": null,
  "cards_revealed": 0,
  "matches_found": 0,
  "score": null,
  "status": "active"
}
```

---

### 23. PUT `/api/v1/gamification/games/memory/{session_id}` - Cập nhật Memory game

**🎯 Mục đích**: Cập nhật tiến độ Memory game

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "ended_at": "2024-01-15T10:40:00Z",
  "cards_revealed": 48,
  "matches_found": 12,
  "score": 1200,
  "status": "completed"
}
```

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "session_id": 1,
  "card_pairs": 12,
  "time_limit_seconds": 600,
  "started_at": "2024-01-15T10:30:00Z",
  "ended_at": "2024-01-15T10:40:00Z",
  "duration_seconds": 600,
  "cards_revealed": 48,
  "matches_found": 12,
  "score": 1200,
  "status": "completed"
}
```

---

### 24. POST `/api/v1/gamification/games/memory/{session_id}/reveal` - Reveal card

**🎯 Mục đích**: Reveal card trong Memory game

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `session_id` (required): ID của game session

**📝 Request Body**:

```json
{
  "card_id": 1,
  "is_match": true
}
```

**✅ Response (200 OK)**:

```json
{
  "reveal_result": "match_found",
  "cards_revealed": 2,
  "matches_found": 1,
  "score_increment": 100,
  "current_score": 100
}
```

---

## 🏁 CHALLENGE ENDPOINTS

### 25. GET `/api/v1/gamification/challenges` - Lấy danh sách challenges

**🎯 Mục đích**: Lấy tất cả challenges có sẵn

**🔑 Authentication**: Required

**📝 Query Parameters**:

- `skip` (optional): Số records bỏ qua (default: 0)
- `limit` (optional): Số records tối đa (default: 100, max: 1000)
- `challenge_type` (optional): Filter theo challenge type

**✅ Response (200 OK)**:

```json
{
  "items": [
    {
      "id": 1,
      "name": "Weekly Study Challenge",
      "description": "Study for 7 consecutive days",
      "challenge_type": "streak",
      "requirements": {
        "study_days": 7
      },
      "points_reward": 200,
      "badge_reward_id": 2,
      "start_date": "2024-01-01T00:00:00Z",
      "end_date": "2024-01-31T23:59:59Z",
      "status": "active"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "pages": 1
}
```

---

### 26. GET `/api/v1/gamification/challenges/{challenge_id}` - Lấy thông tin challenge

**🎯 Mục đích**: Lấy thông tin chi tiết của challenge

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `challenge_id` (required): ID của challenge

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "name": "Weekly Study Challenge",
  "description": "Study for 7 consecutive days",
  "challenge_type": "streak",
  "requirements": {
    "study_days": 7
  },
  "points_reward": 200,
  "badge_reward_id": 2,
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-31T23:59:59Z",
  "status": "active"
}
```

---

### 27. GET `/api/v1/gamification/users/{user_id}/challenges` - Lấy challenges của user

**🎯 Mục đích**: Lấy challenges mà user đang tham gia

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `user_id` (required): ID của user

**📝 Query Parameters**:

- `skip` (optional): Số records bỏ qua (default: 0)
- `limit` (optional): Số records tối đa (default: 100, max: 1000)

**✅ Response (200 OK)**:

```json
{
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "challenge_id": 1,
      "challenge": {
        "id": 1,
        "name": "Weekly Study Challenge",
        "description": "Study for 7 consecutive days",
        "challenge_type": "streak",
        "requirements": {
          "study_days": 7
        },
        "points_reward": 200,
        "badge_reward_id": 2
      },
      "started_at": "2024-01-15T10:30:00Z",
      "completed_at": null,
      "progress": {
        "study_days": 5
      },
      "status": "in_progress"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100,
  "pages": 1
}
```

---

### 28. POST `/api/v1/gamification/challenges/{challenge_id}/start` - Bắt đầu challenge

**🎯 Mục đích**: Bắt đầu tham gia challenge

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `challenge_id` (required): ID của challenge

**✅ Response (201 Created)**:

```json
{
  "id": 1,
  "user_id": 1,
  "challenge_id": 1,
  "challenge": {
    "id": 1,
    "name": "Weekly Study Challenge",
    "description": "Study for 7 consecutive days",
    "challenge_type": "streak",
    "requirements": {
      "study_days": 7
    },
    "points_reward": 200,
    "badge_reward_id": 2
  },
  "started_at": "2024-01-15T10:30:00Z",
  "completed_at": null,
  "progress": {
    "study_days": 0
  },
  "status": "in_progress"
}
```

---

### 29. POST `/api/v1/gamification/challenges/{challenge_id}/complete` - Hoàn thành challenge

**🎯 Mục đích**: Submit progress và hoàn thành challenge

**🔑 Authentication**: Required

**📝 Path Parameters**:

- `challenge_id` (required): ID của challenge

**📝 Request Body**:

```json
{
  "progress": {
    "study_days": 7
  }
}
```

**✅ Response (200 OK)**:

```json
{
  "id": 1,
  "user_id": 1,
  "challenge_id": 1,
  "challenge": {
    "id": 1,
    "name": "Weekly Study Challenge",
    "description": "Study for 7 consecutive days",
    "challenge_type": "streak",
    "requirements": {
      "study_days": 7
    },
    "points_reward": 200,
    "badge_reward_id": 2
  },
  "started_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-22T10:30:00Z",
  "progress": {
    "study_days": 7
  },
  "status": "completed",
  "points_awarded": 200,
  "badge_awarded": true
}
```

---

## 📊 Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication required"
}
```

### 403 Forbidden

```json
{
  "detail": "Access denied"
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
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🔧 Game Types

| Type              | Description                 |
| ----------------- | --------------------------- |
| `match`           | Match card pairs game       |
| `gravity`         | Type words before they fall |
| `speed_challenge` | Answer questions quickly    |
| `memory`          | Memory/Concentration game   |

## 🏆 Challenge Types

| Type       | Description                     |
| ---------- | ------------------------------- |
| `streak`   | Study streak challenges         |
| `points`   | Points earning challenges       |
| `games`    | Game completion challenges      |
| `accuracy` | Accuracy improvement challenges |

## 🎯 Badge Rarities

| Rarity      | Description          |
| ----------- | -------------------- |
| `common`    | Easy to earn         |
| `uncommon`  | Moderately difficult |
| `rare`      | Hard to earn         |
| `epic`      | Very difficult       |
| `legendary` | Extremely difficult  |

---

## 📝 Notes

- Tất cả endpoints yêu cầu authentication
- Points được tự động tính toán dựa trên performance
- Badges được award tự động khi đạt requirements
- Leaderboard được cập nhật real-time
- Game sessions có thể được pause/resume
- Challenges có thể có multiple requirements
