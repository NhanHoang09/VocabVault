# 📚 Flashcards API Documentation - Index

## 🎯 Tổng quan

Flashcards module cung cấp **12 endpoints** để quản lý bộ flashcard và các card riêng lẻ. Tài liệu này được tổ chức thành các phần để dễ dàng tham khảo.

---

## 📋 Cấu trúc tài liệu

### 📖 [README.md](./README.md) - Tài liệu chi tiết
- **Mô tả đầy đủ** tất cả 12 endpoints
- **Request/Response examples** chi tiết
- **Authentication & Authorization** rules
- **Error handling** và status codes
- **Tính năng nổi bật** và examples

### ⚡ [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Tham khảo nhanh
- **Bảng tóm tắt** tất cả endpoints
- **Authentication levels** (Required/Optional)
- **Common request bodies** và response models
- **Quick examples** với curl commands
- **Important notes** và validation rules

### 📊 [SCHEMAS.md](./SCHEMAS.md) - Schema Documentation
- **Request schemas** chi tiết (Create/Update)
- **Response schemas** đầy đủ
- **Validation rules** và field descriptions
- **Enum values** và data types
- **Example schemas** hoàn chỉnh

---

## 🚀 Quick Start

### 1. **Tạo bộ flashcard mới**
```bash
POST /api/v1/flashcards/sets
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My Flashcard Set",
  "description": "Description here",
  "is_public": true
}
```

### 2. **Thêm flashcard vào set**
```bash
POST /api/v1/flashcards/sets/{set_id}/cards
Authorization: Bearer <token>
Content-Type: application/json

{
  "front_content": "Question",
  "back_content": "Answer"
}
```

### 3. **Lấy danh sách sets**
```bash
GET /api/v1/flashcards/sets?limit=10
Authorization: Bearer <token>
```

---

## 📋 Endpoints Summary

### 🔐 FlashcardSet Endpoints (7)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/sets` | ✅ | Create new flashcard set |
| `GET` | `/sets` | ✅ | Get user's flashcard sets |
| `GET` | `/sets/public` | ❌ | Get public flashcard sets |
| `GET` | `/sets/{id}` | ❌ | Get specific flashcard set |
| `GET` | `/sets/{id}/with-cards` | ❌ | Get set with all cards |
| `PUT` | `/sets/{id}` | ✅ | Update flashcard set |
| `DELETE` | `/sets/{id}` | ✅ | Delete flashcard set |

### 🃏 Flashcard Endpoints (5)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/sets/{id}/cards` | ✅ | Create new flashcard |
| `GET` | `/sets/{id}/cards` | ❌ | Get all cards in set |
| `GET` | `/cards/{id}` | ❌ | Get specific flashcard |
| `PUT` | `/cards/{id}` | ✅ | Update flashcard |
| `DELETE` | `/cards/{id}` | ✅ | Delete flashcard |

---

## 🔑 Authentication Levels

- **✅ Required**: Cần JWT token trong header `Authorization: Bearer <token>`
- **❌ Optional**: Có thể xem mà không cần đăng nhập (public sets)

---

## 📊 Response Models

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

---

## 🎯 Tính năng chính

- ✅ **CRUD Operations**: Đầy đủ Create, Read, Update, Delete
- ✅ **Pagination**: Hỗ trợ phân trang cho large datasets
- ✅ **Search & Filter**: Tìm kiếm và lọc theo nhiều tiêu chí
- ✅ **Access Control**: Phân quyền chi tiết
- ✅ **Progress Tracking**: Tự động track học tập
- ✅ **Media Support**: Hỗ trợ text, image, audio, video
- ✅ **Metadata**: Custom metadata cho cards
- ✅ **Public/Private**: Quản lý visibility
- ✅ **Validation**: Kiểm tra dữ liệu đầu vào
- ✅ **Error Handling**: Xử lý lỗi chi tiết

---

## 📖 Navigation

- **[📖 README.md](./README.md)** - Tài liệu chi tiết đầy đủ
- **[⚡ QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Tham khảo nhanh
- **[📊 SCHEMAS.md](./SCHEMAS.md)** - Schema documentation
- **[🔙 Back to Main Documentation](../README.md)** - Quay lại tài liệu chính

---

**Base URL**: `/api/v1/flashcards`  
**Version**: 1.0.0  
**Last Updated**: January 2024  
**Module**: Flashcards API
