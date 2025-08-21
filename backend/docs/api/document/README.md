# 📚 My Vocabulary Vault API Documentation

## 🎯 Tổng quan

My Vocabulary Vault là một ứng dụng học từ vựng kiểu Quizlet với các tính năng hiện đại và tích hợp AI. API này được xây dựng bằng FastAPI với kiến trúc module-based để dễ dàng mở rộng và bảo trì.

## 🏗️ Kiến trúc

API sử dụng kiến trúc module-based với các thành phần chính:

- **Core**: Các thành phần cơ sở (config, database, security, exceptions)
- **Modules**: Các module tính năng (auth, flashcards, learning, analytics, gamification, AI)
- **Shared**: Common utilities, constants, và helper functions

## 📋 Danh sách Modules

### 🔐 Authentication Module ✅
- **Path**: `/api/v1/auth`
- **Mô tả**: Quản lý đăng ký, đăng nhập, và xác thực người dùng
- **Endpoints**: 5 endpoints (Register, Login, Me, Refresh, Debug Token)
- **Tài liệu**: [Authentication API](./auth/README.md)

### 📚 Flashcards Module ✅
- **Path**: `/api/v1/flashcards`
- **Mô tả**: Quản lý bộ flashcard và các card riêng lẻ
- **Endpoints**: 12 endpoints (7 FlashcardSet + 5 Flashcard)
- **Tài liệu**: [Flashcards API](./flashcards/README.md)

### 🎮 Learning Module ✅
- **Path**: `/api/v1/study`
- **Mô tả**: Quản lý phiên học tập và theo dõi tiến độ
- **Endpoints**: 6 endpoints (4 Study Session + 3 Study Attempt)
- **Tài liệu**: [Learning API](./learning/README.md)

### 📊 Analytics Module ✅
- **Path**: `/api/v1/analytics`
- **Mô tả**: Phân tích tiến độ học tập và thống kê
- **Endpoints**: 7 endpoints (Progress, Stats, Mastery, Streaks)
- **Tài liệu**: [Analytics API](./analytics/README.md)

### 🤖 AI Module ⏳
- **Path**: `/api/v1/ai`
- **Mô tả**: AI tutor, content generation, smart recommendations
- **Endpoints**: Chưa implement
- **Tài liệu**: Chưa có

### 🏆 Gamification Module ⏳
- **Path**: `/api/v1/gamification`
- **Mô tả**: Points, badges, leaderboards, achievements
- **Endpoints**: Chưa implement
- **Tài liệu**: Chưa có

### 📝 Vocabulary Module ⏳
- **Path**: `/api/v1/vocabulary`
- **Mô tả**: Vocabulary management và word lists
- **Endpoints**: Chưa implement
- **Tài liệu**: Chưa có

### 🏷️ Topics Module ⏳
- **Path**: `/api/v1/topics`
- **Mô tả**: Topic management và categorization
- **Endpoints**: Chưa implement
- **Tài liệu**: Chưa có

## 🔑 Authentication

Hầu hết các endpoints yêu cầu xác thực. Sử dụng JWT token trong header:

```
Authorization: Bearer <your_access_token>
```

## 🚀 Getting Started

1. **Đăng ký**: Tạo tài khoản mới tại `/api/v1/auth/register`
2. **Đăng nhập**: Lấy access token tại `/api/v1/auth/login`
3. **Xác thực**: Thêm token vào Authorization header cho các endpoints được bảo vệ
4. **Bắt đầu học**: Tạo bộ flashcard và bắt đầu hành trình học tập!

## 📖 Swagger Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI JSON**: `/api/v1/openapi.json`

## 🔧 Development

### Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

### Chạy development server:
```bash
uvicorn app.main:app --reload
```

### Chạy tests:
```bash
pytest
```

## 📝 Response Format

Tất cả API responses tuân theo format chuẩn:

### Success Response:
```json
{
  "data": {...},
  "message": "Success",
  "status": "success"
}
```

### Error Response:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## 🔒 Security

- **JWT Authentication**: Sử dụng JWT tokens cho xác thực
- **CORS**: Cấu hình CORS cho frontend
- **Input Validation**: Validation tất cả input data
- **SQL Injection Protection**: Sử dụng SQLAlchemy ORM
- **Rate Limiting**: Giới hạn request rate (planned)

## 📈 Pagination

Các endpoints trả về danh sách đều hỗ trợ pagination:

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

## 🎯 Status Codes

- `200 OK`: Request thành công
- `201 Created`: Tạo resource thành công
- `204 No Content`: Xóa thành công
- `400 Bad Request`: Dữ liệu đầu vào không hợp lệ
- `401 Unauthorized`: Chưa xác thực
- `403 Forbidden`: Không có quyền truy cập
- `404 Not Found`: Resource không tồn tại
- `422 Validation Error`: Validation error
- `500 Internal Server Error`: Lỗi server

## 📊 API Summary

### Tổng số Endpoints: 30
- **Authentication**: 5 endpoints
- **Flashcards**: 12 endpoints
- **Learning**: 6 endpoints
- **Analytics**: 7 endpoints

### Authentication Levels:
- **Public**: 3 endpoints (Register, Login, Debug Token)
- **Protected**: 27 endpoints (cần JWT token)

### HTTP Methods:
- **GET**: 18 endpoints (lấy dữ liệu)
- **POST**: 8 endpoints (tạo mới)
- **PUT**: 3 endpoints (cập nhật)
- **DELETE**: 1 endpoint (xóa)

## 📞 Support

Nếu có vấn đề hoặc câu hỏi, vui lòng liên hệ:
- **Email**: support@vocabularyvault.com
- **Documentation**: [GitHub Wiki](https://github.com/vocabularyvault/docs)
- **Issues**: [GitHub Issues](https://github.com/vocabularyvault/issues)

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Maintained by**: My Vocabulary Vault Team
