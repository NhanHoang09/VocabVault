# 📡 API Documentation

## 📋 Tổng quan

Thư mục này chứa documentation chi tiết cho tất cả API endpoints của My Vocabulary Vault.

## 📁 Structure

```
api/
└── document/
    ├── README.md           # API overview
    ├── STRUCTURE.md        # Documentation structure
    ├── auth/              # Authentication API
    ├── flashcards/        # Flashcards API
    ├── learning/          # Learning API
    └── analytics/         # Analytics API
```

## 🔐 **Authentication API** (`/auth/`)

- **Base URL**: `/api/v1/auth`
- **Endpoints**: 5 endpoints
- **Documentation**: [`auth/README.md`](./document/auth/README.md)

### Endpoints:

- `POST /register` - Đăng ký tài khoản
- `POST /login` - Đăng nhập
- `GET /me` - Lấy thông tin user
- `POST /refresh` - Làm mới token
- `POST /debug-token` - Debug JWT token

## 📚 **Flashcards API** (`/flashcards/`)

- **Base URL**: `/api/v1/flashcards`
- **Endpoints**: 12 endpoints
- **Documentation**: [`flashcards/README.md`](./document/flashcards/README.md)

### FlashcardSet Endpoints:

- `GET /sets` - Lấy danh sách sets
- `POST /sets` - Tạo set mới
- `GET /sets/{id}` - Lấy chi tiết set
- `PUT /sets/{id}` - Cập nhật set
- `DELETE /sets/{id}` - Xóa set
- `GET /sets/{id}/cards` - Lấy cards trong set
- `POST /sets/{id}/cards` - Thêm card vào set

### Flashcard Endpoints:

- `GET /cards/{id}` - Lấy chi tiết card
- `PUT /cards/{id}` - Cập nhật card
- `DELETE /cards/{id}` - Xóa card
- `GET /cards/{id}/mastery` - Lấy mastery level
- `PUT /cards/{id}/mastery` - Cập nhật mastery level

## 🎮 **Learning API** (`/learning/`)

- **Base URL**: `/api/v1/study`
- **Endpoints**: 6 endpoints
- **Documentation**: [`learning/README.md`](./document/learning/README.md)

### Study Session Endpoints:

- `POST /sessions` - Tạo session mới
- `GET /sessions` - Lấy danh sách sessions
- `GET /sessions/{id}` - Lấy chi tiết session
- `PUT /sessions/{id}` - Cập nhật session

### Study Attempt Endpoints:

- `POST /attempts` - Ghi lại attempt
- `GET /sessions/{id}/attempts` - Lấy attempts của session
- `GET /attempts/{id}` - Lấy chi tiết attempt

## 📊 **Analytics API** (`/analytics/`)

- **Base URL**: `/api/v1/analytics`
- **Endpoints**: 7 endpoints
- **Documentation**: [`analytics/README.md`](./document/analytics/README.md)

### Endpoints:

- `GET /progress` - Tiến độ tổng quan
- `GET /sets/{id}/progress` - Tiến độ flashcard set
- `GET /stats/daily` - Thống kê hàng ngày
- `GET /stats/weekly` - Thống kê hàng tuần
- `GET /stats/monthly` - Thống kê hàng tháng
- `GET /mastery` - Phân bố mastery levels
- `GET /streaks` - Study streaks

## 🔑 **Authentication**

Hầu hết endpoints yêu cầu JWT token:

```bash
Authorization: Bearer <your_access_token>
```

## 📖 **Quick Reference**

### Public Endpoints (Không cần auth):

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/debug-token`

### Protected Endpoints (Cần auth):

- Tất cả endpoints khác

## 🚀 **Getting Started**

1. **Register**: `POST /api/v1/auth/register`
2. **Login**: `POST /api/v1/auth/login`
3. **Use token**: Thêm vào Authorization header
4. **Start using**: Gọi các endpoints khác

## 📡 **Swagger UI**

- **Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/api/v1/openapi.json`

---

**Total Endpoints**: 30  
**Version**: 1.0.0  
**Status**: Phase 1 Complete ✅
