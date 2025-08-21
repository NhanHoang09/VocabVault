# 📊 Analytics API Documentation

## 🎯 Tổng quan

Analytics module cung cấp **7 endpoints** để phân tích tiến độ học tập và thống kê chi tiết. Module này cung cấp insights về performance, mastery levels, study streaks và các metrics quan trọng khác.

**Base URL**: `/api/v1/analytics`

---

## 📋 Danh sách Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/progress` | ✅ | Lấy tiến độ tổng quan của user |
| `GET` | `/sets/{id}/progress` | ✅ | Lấy tiến độ của flashcard set |
| `GET` | `/stats/daily` | ✅ | Thống kê hàng ngày |
| `GET` | `/stats/weekly` | ✅ | Thống kê hàng tuần |
| `GET` | `/stats/monthly` | ✅ | Thống kê hàng tháng |
| `GET` | `/mastery` | ✅ | Phân bố mastery levels |
| `GET` | `/streaks` | ✅ | Thông tin study streaks |

---

## 📊 ANALYTICS ENDPOINTS

### 1. GET `/api/v1/analytics/progress` - Lấy tiến độ tổng quan

**🎯 Mục đích**: Lấy thống kê tiến độ tổng quan của user

**🔑 Authentication**: Required

**✅ Response (200 OK)**:
```json
{
  "user_id": 1,
  "total_cards": 100,
  "cards_studied": 80,
  "correct_answers": 720,
  "incorrect_answers": 180,
  "accuracy_rate": 0.8,
  "total_study_time_minutes": 1200,
  "total_sets": 5,
  "active_sets": 3,
  "study_sessions_count": 25,
  "current_streak_days": 7,
  "longest_streak_days": 15,
  "mastery_distribution": {
    "not_learned": 20,
    "learning": 30,
    "well_learned": 25,
    "mastered": 25
  },
  "average_session_duration_minutes": 48.0,
  "last_study_date": "2024-01-15T10:30:00Z"
}
```

---

### 2. GET `/api/v1/analytics/sets/{set_id}/progress` - Lấy tiến độ flashcard set

**🎯 Mục đích**: Lấy thống kê tiến độ chi tiết cho một flashcard set

**🔑 Authentication**: Required

**📝 Path Parameters**:
- `set_id` (required): ID của flashcard set

**✅ Response (200 OK)**:
```json
{
  "set_id": 1,
  "set_title": "Từ vựng tiếng Anh cơ bản",
  "total_cards": 50,
  "cards_studied": 45,
  "correct_answers": 180,
  "incorrect_answers": 45,
  "accuracy_rate": 0.8,
  "total_study_time_minutes": 300,
  "cards_in_set": 50,
  "mastery_distribution": {
    "not_learned": 5,
    "learning": 15,
    "well_learned": 20,
    "mastered": 10
  },
  "study_sessions_count": 8,
  "last_studied": "2024-01-15T10:30:00Z",
  "average_session_duration_minutes": 37.5,
  "study_mode_breakdown": {
    "flashcards": 5,
    "learn": 2,
    "write": 1
  }
}
```

---

### 3. GET `/api/v1/analytics/stats/daily` - Thống kê hàng ngày

**🎯 Mục đích**: Lấy thống kê học tập cho một ngày cụ thể

**🔑 Authentication**: Required

**🔍 Query Parameters**:
- `date` (optional): Ngày cần thống kê (YYYY-MM-DD, default: hôm nay)

**✅ Response (200 OK)**:
```json
{
  "date": "2024-01-15",
  "study_time_minutes": 45,
  "sessions_count": 2,
  "cards_studied": 25,
  "correct_answers": 22,
  "incorrect_answers": 3,
  "accuracy_rate": 0.88,
  "study_mode_breakdown": {
    "flashcards": 1,
    "learn": 1
  },
  "sets_studied": [1, 2]
}
```

---

### 4. GET `/api/v1/analytics/stats/weekly` - Thống kê hàng tuần

**🎯 Mục đích**: Lấy thống kê học tập cho một tuần cụ thể

**🔑 Authentication**: Required

**🔍 Query Parameters**:
- `week_start` (optional): Ngày bắt đầu tuần (YYYY-MM-DD, default: tuần hiện tại)

**✅ Response (200 OK)**:
```json
{
  "week_start": "2024-01-15",
  "week_end": "2024-01-21",
  "total_study_time_minutes": 240,
  "total_sessions": 8,
  "total_cards_studied": 120,
  "average_accuracy": 0.85,
  "study_mode_breakdown": {
    "flashcards": 5,
    "learn": 2,
    "write": 1
  },
  "sets_studied": [1, 2, 3]
}
```

---

### 5. GET `/api/v1/analytics/stats/monthly` - Thống kê hàng tháng

**🎯 Mục đích**: Lấy thống kê học tập cho một tháng cụ thể

**🔑 Authentication**: Required

**🔍 Query Parameters**:
- `year` (optional): Năm (default: năm hiện tại)
- `month` (optional): Tháng 1-12 (default: tháng hiện tại)

**✅ Response (200 OK)**:
```json
{
  "year": 2024,
  "month": 1,
  "total_study_time_minutes": 1200,
  "total_sessions": 40,
  "total_cards_studied": 600,
  "average_accuracy": 0.82,
  "study_mode_breakdown": {
    "flashcards": 25,
    "learn": 10,
    "write": 3,
    "spell": 2
  },
  "sets_studied": [1, 2, 3, 4, 5]
}
```

---

### 6. GET `/api/v1/analytics/mastery` - Phân bố mastery levels

**🎯 Mục đích**: Lấy phân bố cards theo mastery levels

**🔑 Authentication**: Required

**✅ Response (200 OK)**:
```json
{
  "total_cards": 100,
  "mastery_distribution": {
    "not_learned": 20,
    "learning": 30,
    "well_learned": 25,
    "mastered": 25
  },
  "mastery_percentages": {
    "not_learned": 20.0,
    "learning": 30.0,
    "well_learned": 25.0,
    "mastered": 25.0
  },
  "progress_summary": {
    "cards_in_progress": 55,
    "cards_completed": 25,
    "completion_rate": 0.25
  }
}
```

---

### 7. GET `/api/v1/analytics/streaks` - Thông tin study streaks

**🎯 Mục đích**: Lấy thông tin về study streaks của user

**🔑 Authentication**: Required

**✅ Response (200 OK)**:
```json
{
  "current_streak_days": 7,
  "longest_streak_days": 15,
  "streak_start_date": "2024-01-09",
  "longest_streak_start_date": "2023-12-01",
  "longest_streak_end_date": "2023-12-15",
  "next_milestone_days": 3,
  "milestone_target": 10,
  "streak_history": [
    {
      "start_date": "2024-01-09",
      "end_date": "2024-01-15",
      "days": 7
    }
  ]
}
```

---

## 🔑 AUTHENTICATION & AUTHORIZATION

### **Authentication Levels**:
- **Required**: Tất cả endpoints đều cần JWT token
- **User Access**: User chỉ có thể xem analytics của mình

### **Authorization Rules**:
- **Personal Analytics**: User chỉ có thể xem thống kê của mình
- **Set Progress**: User chỉ có thể xem progress của sets mình sở hữu hoặc public sets

---

## 📊 RESPONSE MODELS

### UserProgressResponse
```json
{
  "user_id": 1,
  "total_cards": 100,
  "cards_studied": 80,
  "correct_answers": 720,
  "incorrect_answers": 180,
  "accuracy_rate": 0.8,
  "total_study_time_minutes": 1200,
  "total_sets": 5,
  "active_sets": 3,
  "study_sessions_count": 25,
  "current_streak_days": 7,
  "longest_streak_days": 15,
  "mastery_distribution": {
    "not_learned": 20,
    "learning": 30,
    "well_learned": 25,
    "mastered": 25
  },
  "average_session_duration_minutes": 48.0,
  "last_study_date": "2024-01-15T10:30:00Z"
}
```

### SetProgressResponse
```json
{
  "set_id": 1,
  "set_title": "Từ vựng tiếng Anh cơ bản",
  "total_cards": 50,
  "cards_studied": 45,
  "correct_answers": 180,
  "incorrect_answers": 45,
  "accuracy_rate": 0.8,
  "total_study_time_minutes": 300,
  "cards_in_set": 50,
  "mastery_distribution": {
    "not_learned": 5,
    "learning": 15,
    "well_learned": 20,
    "mastered": 10
  },
  "study_sessions_count": 8,
  "last_studied": "2024-01-15T10:30:00Z",
  "average_session_duration_minutes": 37.5,
  "study_mode_breakdown": {
    "flashcards": 5,
    "learn": 2,
    "write": 1
  }
}
```

### DailyStatsResponse
```json
{
  "date": "2024-01-15",
  "study_time_minutes": 45,
  "sessions_count": 2,
  "cards_studied": 25,
  "correct_answers": 22,
  "incorrect_answers": 3,
  "accuracy_rate": 0.88,
  "study_mode_breakdown": {
    "flashcards": 1,
    "learn": 1
  },
  "sets_studied": [1, 2]
}
```

### WeeklyStatsResponse
```json
{
  "week_start": "2024-01-15",
  "week_end": "2024-01-21",
  "total_study_time_minutes": 240,
  "total_sessions": 8,
  "total_cards_studied": 120,
  "average_accuracy": 0.85,
  "study_mode_breakdown": {
    "flashcards": 5,
    "learn": 2,
    "write": 1
  },
  "sets_studied": [1, 2, 3]
}
```

### MonthlyStatsResponse
```json
{
  "year": 2024,
  "month": 1,
  "total_study_time_minutes": 1200,
  "total_sessions": 40,
  "total_cards_studied": 600,
  "average_accuracy": 0.82,
  "study_mode_breakdown": {
    "flashcards": 25,
    "learn": 10,
    "write": 3,
    "spell": 2
  },
  "sets_studied": [1, 2, 3, 4, 5]
}
```

---

## 🎯 TÍNH NĂNG NỔI BẬT

- ✅ **Progress Tracking**: Theo dõi tiến độ tổng quan
- ✅ **Set Analytics**: Phân tích chi tiết từng flashcard set
- ✅ **Time-based Stats**: Thống kê theo ngày/tuần/tháng
- ✅ **Mastery Distribution**: Phân bố mastery levels
- ✅ **Study Streaks**: Theo dõi chuỗi học tập
- ✅ **Performance Metrics**: Các chỉ số hiệu suất
- ✅ **Study Mode Breakdown**: Phân tích theo chế độ học
- ✅ **Accuracy Tracking**: Theo dõi độ chính xác
- ✅ **Session Analytics**: Phân tích phiên học tập

---

## 🚀 EXAMPLES

### Lấy tiến độ tổng quan
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/progress" \
  -H "Authorization: Bearer <your_access_token>"
```

### Lấy tiến độ flashcard set
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/sets/1/progress" \
  -H "Authorization: Bearer <your_access_token>"
```

### Thống kê hàng ngày
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/stats/daily?date=2024-01-15" \
  -H "Authorization: Bearer <your_access_token>"
```

### Thống kê hàng tuần
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/stats/weekly?week_start=2024-01-15" \
  -H "Authorization: Bearer <your_access_token>"
```

### Thống kê hàng tháng
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/stats/monthly?year=2024&month=1" \
  -H "Authorization: Bearer <your_access_token>"
```

### Phân bố mastery levels
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/mastery" \
  -H "Authorization: Bearer <your_access_token>"
```

### Study streaks
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/streaks" \
  -H "Authorization: Bearer <your_access_token>"
```

---

## 🔧 ERROR HANDLING

### Common Error Responses

**400 Bad Request**:
```json
{
  "detail": "Invalid date format. Use YYYY-MM-DD"
}
```

**401 Unauthorized**:
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found**:
```json
{
  "detail": "Flashcard set not found"
}
```

**422 Validation Error**:
```json
{
  "detail": "Month must be between 1 and 12"
}
```

---

## 📈 ANALYTICS INSIGHTS

### Key Metrics:
- **Accuracy Rate**: Tỷ lệ trả lời đúng
- **Study Time**: Thời gian học tập
- **Cards Studied**: Số lượng cards đã học
- **Session Count**: Số phiên học tập
- **Streak Days**: Số ngày học liên tiếp

### Mastery Levels:
- **NOT_LEARNED**: Chưa học
- **LEARNING**: Đang học
- **WELL_LEARNED**: Học tốt
- **MASTERED**: Thành thạo

### Study Modes:
- **flashcards**: Chế độ flashcard
- **learn**: Chế độ học
- **write**: Chế độ viết
- **spell**: Chế độ đánh vần
- **test**: Chế độ kiểm tra

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Module**: Analytics API
