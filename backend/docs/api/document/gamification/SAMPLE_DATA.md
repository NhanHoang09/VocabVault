# 🎮 Gamification Sample Data

## 📋 Overview

This document describes the sample data created for the gamification system to help with testing and development.

## 🚀 Quick Start

### Using Python Script

```bash
cd backend
./scripts/run_gamification_sample_data.sh
```

### Using SQL Script

```bash
# Connect to your database and run:
psql -d your_database -f scripts/create_gamification_sample_data.sql
```

### Manual Python Execution

```bash
cd backend
source venv/bin/activate
python scripts/create_gamification_sample_data.py
```

## 📊 Sample Data Summary

| Table                   | Records | Description                      |
| ----------------------- | ------- | -------------------------------- |
| **Badges**              | 8       | Available badges in the system   |
| **Challenges**          | 5       | Available challenges             |
| **Game Sessions**       | 10-25   | Game sessions per user           |
| **Points Transactions** | 25-75   | Transaction history per user     |
| **User Badges**         | 8-16    | Awarded badges per user          |
| **Leaderboard Entries** | 16-20   | Rankings per user                |
| **User Challenges**     | 10-20   | Challenge participation per user |

## 🏆 Sample Badges

### Common Badges

- **First Steps** (50 points): Complete your first study session
- **Match Maker** (150 points): Complete 10 match games

### Uncommon Badges

- **Gravity Master** (250 points): Type 50 words correctly in gravity game
- **Fast Learner** (100 points): Complete 5 study sessions in one day

### Rare Badges

- **Streak Master** (200 points): Maintain a 7-day study streak

### Epic Badges

- **Speed Demon** (300 points): Complete a speed challenge in under 30 seconds

### Legendary Badges

- **Perfect Memory** (400 points): Complete a memory game with 100% accuracy
- **Consistent Studier** (500 points): Study for 30 consecutive days

## 🏁 Sample Challenges

### Recurring Challenges

- **Weekly Study Streak** (200 points): Study for 7 consecutive days
- **Daily Goal** (50 points): Study for at least 30 minutes today

### One-time Challenges

- **Speed Runner** (150 points): Complete 5 speed challenges
- **Game Master** (300 points): Play all 4 types of games
- **Perfect Score** (250 points): Achieve 100% accuracy in any game

## 🎮 Sample Game Sessions

### Match Game Sessions

```json
{
  "game_type": "match",
  "duration_seconds": 900,
  "score": 750,
  "accuracy_rate": 0.94,
  "cards_played": 40,
  "correct_answers": 38,
  "incorrect_answers": 2
}
```

### Gravity Game Sessions

```json
{
  "game_type": "gravity",
  "duration_seconds": 1800,
  "score": 1200,
  "accuracy_rate": 0.8,
  "cards_played": 50,
  "correct_answers": 40,
  "incorrect_answers": 10
}
```

### Speed Challenge Sessions

```json
{
  "game_type": "speed_challenge",
  "duration_seconds": 2700,
  "score": 900,
  "accuracy_rate": 0.9,
  "cards_played": 30,
  "correct_answers": 27,
  "incorrect_answers": 3
}
```

### Memory Game Sessions

```json
{
  "game_type": "memory",
  "duration_seconds": 720,
  "score": 1600,
  "accuracy_rate": 1.0,
  "cards_played": 32,
  "correct_answers": 32,
  "incorrect_answers": 0
}
```

## 💰 Sample Points Transactions

### Transaction Types

- **Study** (10-100 points): Study session completed
- **Game** (50-200 points): Game session completed
- **Badge** (25-500 points): Badge earned
- **Bonus** (10-100 points): Bonus points awarded
- **Challenge** (50-300 points): Challenge completed

### Example Transactions

```json
[
  {
    "points": 50,
    "transaction_type": "study",
    "description": "Study session completed"
  },
  {
    "points": 200,
    "transaction_type": "badge",
    "description": "Badge earned: First Steps"
  },
  {
    "points": 100,
    "transaction_type": "challenge",
    "description": "Challenge completed: Daily Goal"
  }
]
```

## 🏅 Sample Leaderboard Entries

### Categories

- **Daily**: Today's rankings
- **Weekly**: This week's rankings
- **Monthly**: This month's rankings
- **All-time**: Overall rankings

### Example Entry

```json
{
  "category": "weekly",
  "score": 3500,
  "rank": 8,
  "study_time_minutes": 480,
  "cards_studied": 150,
  "games_played": 12,
  "badges_earned": 4
}
```

## 🎯 Sample User Challenges

### Challenge States

- **Completed**: Challenge finished successfully
- **In Progress**: Challenge started but not completed
- **Not Started**: Challenge available but not started

### Example Progress Data

```json
{
  "current_progress": 60,
  "target": 100,
  "speed_challenges_completed": 3,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

## 🔧 Game-Specific Data

### Match Game Data

```json
{
  "moves_count": 45,
  "matches_found": 19,
  "total_pairs": 20,
  "time_bonus": 150,
  "perfect_match_bonus": 0
}
```

### Gravity Game Data

```json
{
  "words_typed": 50,
  "words_correct": 40,
  "words_incorrect": 10,
  "combo_multiplier": 3.5,
  "max_combo": 15,
  "time_bonus": 300
}
```

### Speed Challenge Data

```json
{
  "total_questions": 30,
  "questions_answered": 30,
  "correct_answers": 27,
  "incorrect_answers": 3,
  "time_limit_seconds": 300,
  "time_remaining_seconds": 45,
  "average_response_time": 4.2,
  "fastest_response_time": 1.5,
  "slowest_response_time": 12.0,
  "streak_count": 8,
  "max_streak": 12
}
```

### Memory Game Data

```json
{
  "total_cards": 32,
  "cards_revealed": 32,
  "matches_found": 16,
  "moves_count": 48,
  "time_limit_seconds": 600,
  "time_remaining_seconds": 120
}
```

## 📈 Data Distribution

### User Performance Ranges

- **Total Points**: 1,000 - 25,000
- **Study Time**: 30 - 480 minutes per period
- **Cards Studied**: 20 - 800 per period
- **Games Played**: 1 - 75 per period
- **Badges Earned**: 1 - 12 per user

### Game Performance Ranges

- **Accuracy**: 60% - 100%
- **Duration**: 5 - 45 minutes
- **Score**: 400 - 1,600 points
- **Cards/Questions**: 10 - 50 per session

## 🧪 Testing Scenarios

### Badge Testing

- Test badge earning with different criteria
- Verify points rewards are awarded correctly
- Check badge rarity distribution

### Challenge Testing

- Test challenge progress tracking
- Verify completion detection
- Test recurring vs one-time challenges

### Game Testing

- Test all 4 game types
- Verify scoring calculations
- Test performance tracking

### Leaderboard Testing

- Test different time periods
- Verify ranking calculations
- Test score aggregation

### Points Testing

- Test transaction history
- Verify point calculations
- Test level progression

## 🔍 Verification Queries

### Check Badge Distribution

```sql
SELECT rarity, COUNT(*) as count
FROM badges
GROUP BY rarity
ORDER BY count DESC;
```

### Check User Progress

```sql
SELECT
    u.username,
    COUNT(ub.id) as badges_earned,
    SUM(pt.points) as total_points,
    COUNT(gs.id) as games_played
FROM users u
LEFT JOIN user_badges ub ON u.id = ub.user_id
LEFT JOIN points_transactions pt ON u.id = pt.user_id
LEFT JOIN game_sessions gs ON u.id = gs.user_id
GROUP BY u.id, u.username;
```

### Check Game Performance

```sql
SELECT
    game_type,
    AVG(accuracy_rate) as avg_accuracy,
    AVG(score) as avg_score,
    AVG(duration_seconds) as avg_duration
FROM game_sessions
GROUP BY game_type;
```

## 🚨 Troubleshooting

### Common Issues

1. **No users found**: Create users first using auth module
2. **No flashcard sets**: Create flashcard sets first
3. **Database connection failed**: Check database is running
4. **Permission denied**: Check file permissions on scripts

### Reset Sample Data

```sql
-- Clear all gamification data (use with caution!)
DELETE FROM user_challenges;
DELETE FROM leaderboard_entries;
DELETE FROM user_badges;
DELETE FROM points_transactions;
DELETE FROM memory_games;
DELETE FROM speed_challenges;
DELETE FROM gravity_games;
DELETE FROM match_games;
DELETE FROM game_sessions;
DELETE FROM challenges;
DELETE FROM badges;
```

## 📝 Notes

- Sample data is created for the first 5 users in the system
- Data spans the last 30 days for realistic testing
- All game types are represented with various performance levels
- Leaderboard data includes all time periods
- Challenge data includes various completion states
