# 📚 Flashcards API Documentation

## 🎯 Tổng quan

Flashcards module cung cấp **12 endpoints** để quản lý bộ flashcard và các card riêng lẻ. Module này được chia thành 2 nhóm chính: **FlashcardSet Endpoints** và **Flashcard Endpoints**.

**Base URL**: `/api/v1/flashcards`

---

## 📋 Danh sách Endpoints

### 🔐 FlashcardSet Endpoints (7 endpoints)
| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| POST | `/sets` | Tạo bộ flashcard mới | Required |
| GET | `/sets` | Lấy danh sách bộ flashcard của user | Required |
| GET | `/sets/public` | Lấy danh sách bộ flashcard công khai | Optional |
| GET | `/sets/{set_id}` | Lấy chi tiết bộ flashcard | Optional |
| GET | `/sets/{set_id}/with-cards` | Lấy bộ flashcard kèm tất cả cards | Optional |
| PUT | `/sets/{set_id}` | Cập nhật bộ flashcard | Required |
| DELETE | `/sets/{set_id}` | Xóa bộ flashcard | Required |

### 🃏 Flashcard Endpoints (5 endpoints)
| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| POST | `/sets/{set_id}/cards` | Tạo flashcard mới | Required |
| GET | `/sets/{set_id}/cards` | Lấy tất cả cards trong set | Optional |
| GET | `/cards/{card_id}` | Lấy chi tiết flashcard | Optional |
| PUT | `/cards/{card_id}` | Cập nhật flashcard | Required |
| DELETE | `/cards/{card_id}` | Xóa flashcard | Required |

---

## 🔐 FLASHCARD SET ENDPOINTS

### 1. POST `/api/v1/flashcards/sets` - Tạo bộ flashcard mới

**🎯 Mục đích**: Tạo một bộ flashcard mới cho user

**🔑 Authentication**: Required

**📝 Request Body**:
```json
{
  "title": "Từ vựng tiếng Anh cơ bản",
  "description": "Bộ từ vựng cho người mới bắt đầu",
  "category": "English",
  "tags": ["basic", "vocabulary", "beginner"],
  "is_public": true,
  "is_featured": false
}
```

**📋 Field Descriptions**:
- `title` (required): Tiêu đề bộ flashcard (1-200 ký tự)
- `description` (optional): Mô tả chi tiết
- `category` (optional): Danh mục để tổ chức
- `tags` (optional): Danh sách tags để tìm kiếm dễ dàng
- `is_public` (required): Có công khai hay không
- `is_featured` (optional): Đánh dấu là featured

**✅ Response (201 Created)**:
```json
{
  "id": 1,
  "title": "Từ vựng tiếng Anh cơ bản",
  "description": "Bộ từ vựng cho người mới bắt đầu",
  "category": "English",
  "tags": ["basic", "vocabulary", "beginner"],
  "is_public": true,
  "is_featured": false,
  "user_id": 1,
  "cards_count": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### 2. GET `/api/v1/flashcards/sets` - Lấy danh sách bộ flashcard của user

**🎯 Mục đích**: Lấy tất cả bộ flashcard thuộc sở hữu của user hiện tại

**🔑 Authentication**: Required

**🔍 Query Parameters**:
- `skip` (optional): Số record bỏ qua cho pagination (default: 0)
- `limit` (optional): Số record tối đa trả về (default: 100, max: 1000)
- `search` (optional): Từ khóa tìm kiếm trong title hoặc description
- `category` (optional): Lọc theo category cụ thể

**📝 Example Request**:
```
GET /api/v1/flashcards/sets?skip=0&limit=20&search=english&category=English
```

**✅ Response (200 OK)**:
```json
{
  "items": [
    {
      "id": 1,
      "title": "Từ vựng tiếng Anh cơ bản",
      "description": "Bộ từ vựng cho người mới bắt đầu",
      "category": "English",
      "tags": ["basic", "vocabulary"],
      "is_public": true,
      "is_featured": false,
      "user_id": 1,
      "cards_count": 10,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

---

### 3. GET `/api/v1/flashcards/sets/public` - Lấy danh sách bộ flashcard công khai

**🎯 Mục đích**: Lấy tất cả bộ flashcard công khai từ cộng đồng

**🔑 Authentication**: Optional (có thể xem mà không cần đăng nhập)

**🔍 Query Parameters**: Giống endpoint `/sets`

**✅ Response (200 OK)**: Giống endpoint `/sets`

---

### 4. GET `/api/v1/flashcards/sets/{set_id}` - Lấy chi tiết bộ flashcard

**🎯 Mục đích**: Lấy thông tin chi tiết của một bộ flashcard cụ thể

**🔑 Authentication**: Optional

**📋 Access Control**:
- User có thể xem set của mình
- Mọi người có thể xem public sets
- Private sets chỉ owner mới xem được

**📝 Path Parameters**:
- `set_id` (required): ID của bộ flashcard (integer > 0)

**✅ Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Từ vựng tiếng Anh cơ bản",
  "description": "Bộ từ vựng cho người mới bắt đầu",
  "category": "English",
  "tags": ["basic", "vocabulary"],
  "is_public": true,
  "is_featured": false,
  "user_id": 1,
  "cards_count": 10,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### 5. GET `/api/v1/flashcards/sets/{set_id}/with-cards` - Lấy bộ flashcard kèm tất cả cards

**🎯 Mục đích**: Lấy bộ flashcard cùng với tất cả cards trong một request

**🔑 Authentication**: Optional

**📋 Access Control**: Giống endpoint `/sets/{set_id}`

**✅ Response (200 OK)**:
```json
{
  "id": 1,
  "title": "Từ vựng tiếng Anh cơ bản",
  "description": "Bộ từ vựng cho người mới bắt đầu",
  "category": "English",
  "tags": ["basic", "vocabulary"],
  "is_public": true,
  "is_featured": false,
  "user_id": 1,
  "cards_count": 2,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "cards": [
    {
      "id": 1,
      "set_id": 1,
      "front_content": "Hello",
      "back_content": "Xin chào",
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
  ]
}
```

---

### 6. PUT `/api/v1/flashcards/sets/{set_id}` - Cập nhật bộ flashcard

**🎯 Mục đích**: Cập nhật thông tin bộ flashcard

**🔑 Authentication**: Required

**📋 Access Control**: Chỉ owner mới có thể update

**📝 Request Body** (partial update):
```json
{
  "title": "Từ vựng tiếng Anh nâng cao",
  "description": "Bộ từ vựng cho người học nâng cao",
  "is_public": false
}
```

**✅ Response (200 OK)**: Giống POST response

---

### 7. DELETE `/api/v1/flashcards/sets/{set_id}` - Xóa bộ flashcard

**🎯 Mục đích**: Xóa vĩnh viễn bộ flashcard

**🔑 Authentication**: Required

**📋 Access Control**: Chỉ owner mới có thể delete

**⚠️ Warning**: 
- Hành động này không thể hoàn tác
- Tất cả cards trong set sẽ bị xóa
- Progress học tập sẽ bị mất

**✅ Response (204 No Content)**:
```json
{
  "message": "Flashcard set deleted successfully"
}
```

---

## 🃏 FLASHCARD ENDPOINTS

### 1. POST `/api/v1/flashcards/sets/{set_id}/cards` - Tạo flashcard mới

**🎯 Mục đích**: Thêm flashcard mới vào bộ flashcard

**🔑 Authentication**: Required

**📋 Access Control**: Chỉ owner của set mới có thể thêm card

**📝 Path Parameters**:
- `set_id` (required): ID của bộ flashcard (integer > 0)

**📝 Request Body**:
```json
{
  "front_content": "Hello",
  "back_content": "Xin chào",
  "card_type": "text",
  "difficulty": "easy",
  "media_url": null,
  "card_metadata": {
    "example_sentence": "Hello, how are you?",
    "pronunciation": "həˈloʊ"
  }
}
```

**📋 Field Descriptions**:
- `front_content` (required): Nội dung mặt trước (câu hỏi/prompt)
- `back_content` (required): Nội dung mặt sau (câu trả lời/giải thích)
- `card_type` (optional): Loại card (text, image, audio, video)
- `difficulty` (optional): Độ khó (easy, medium, hard)
- `media_url` (optional): URL đến media content
- `card_metadata` (optional): Metadata bổ sung dạng JSON

**✅ Response (201 Created)**:
```json
{
  "id": 1,
  "set_id": 1,
  "front_content": "Hello",
  "back_content": "Xin chào",
  "card_type": "text",
  "media_url": null,
  "difficulty": "easy",
  "card_metadata": {
    "example_sentence": "Hello, how are you?",
    "pronunciation": "həˈloʊ"
  },
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

### 2. GET `/api/v1/flashcards/sets/{set_id}/cards` - Lấy tất cả cards trong set

**🎯 Mục đích**: Lấy danh sách tất cả flashcards trong một set

**🔑 Authentication**: Optional

**📋 Access Control**: Giống set endpoints

**🔍 Query Parameters**:
- `skip` (optional): Số record bỏ qua (default: 0)
- `limit` (optional): Số record tối đa (default: 100, max: 1000)

**✅ Response (200 OK)**:
```json
[
  {
    "id": 1,
    "set_id": 1,
    "front_content": "Hello",
    "back_content": "Xin chào",
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
]
```

---

### 3. GET `/api/v1/flashcards/cards/{card_id}` - Lấy chi tiết flashcard

**🎯 Mục đích**: Lấy thông tin chi tiết của một flashcard

**🔑 Authentication**: Optional

**📋 Access Control**: Giống set endpoints

**📝 Path Parameters**:
- `card_id` (required): ID của flashcard (integer > 0)

**✅ Response (200 OK)**: Giống POST response

---

### 4. PUT `/api/v1/flashcards/cards/{card_id}` - Cập nhật flashcard

**🎯 Mục đích**: Cập nhật thông tin flashcard

**🔑 Authentication**: Required

**📋 Access Control**: Chỉ owner của set mới có thể update card

**📝 Request Body** (partial update):
```json
{
  "front_content": "Hello there",
  "back_content": "Xin chào bạn",
  "difficulty": "medium"
}
```

**✅ Response (200 OK)**: Giống POST response

---

### 5. DELETE `/api/v1/flashcards/cards/{card_id}` - Xóa flashcard

**🎯 Mục đích**: Xóa vĩnh viễn flashcard

**🔑 Authentication**: Required

**📋 Access Control**: Chỉ owner của set mới có thể delete card

**⚠️ Warning**: 
- Hành động này không thể hoàn tác
- Progress học tập cho card này sẽ bị mất
- Số lượng card trong set sẽ được cập nhật tự động

**✅ Response (204 No Content)**:
```json
{
  "message": "Flashcard deleted successfully"
}
```

---

## 🔑 AUTHENTICATION & AUTHORIZATION

### **Authentication Levels**:
- **Required**: Cần JWT token trong header `Authorization: Bearer <token>`
- **Optional**: Có thể xem mà không cần đăng nhập (public sets)

### **Authorization Rules**:
- **Owner Access**: Chỉ owner mới có thể create/update/delete
- **Public Access**: Mọi người có thể xem public sets
- **Private Access**: Private sets chỉ owner mới xem được

---

## 📊 RESPONSE MODELS

### **FlashcardSetResponse**:
```json
{
  "id": 1,
  "title": "Từ vựng tiếng Anh",
  "description": "Bộ từ vựng cơ bản",
  "category": "English",
  "tags": ["basic", "vocabulary"],
  "is_public": true,
  "is_featured": false,
  "user_id": 1,
  "cards_count": 10,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### **FlashcardResponse**:
```json
{
  "id": 1,
  "set_id": 1,
  "front_content": "Hello",
  "back_content": "Xin chào",
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

### **FlashcardSetListResponse**:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

### **FlashcardSetWithCards**:
```json
{
  "id": 1,
  "title": "Từ vựng tiếng Anh",
  "description": "Bộ từ vựng cơ bản",
  "category": "English",
  "tags": ["basic", "vocabulary"],
  "is_public": true,
  "is_featured": false,
  "user_id": 1,
  "cards_count": 2,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "cards": [...]
}
```

---

## 🎯 TÍNH NĂNG NỔI BẬT

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

## 🚀 EXAMPLES

### **Tạo bộ flashcard mới**:
```bash
curl -X POST "http://localhost:8000/api/v1/flashcards/sets" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Từ vựng tiếng Anh",
    "description": "Bộ từ vựng cơ bản",
    "category": "English",
    "tags": ["basic", "vocabulary"],
    "is_public": true
  }'
```

### **Thêm flashcard vào set**:
```bash
curl -X POST "http://localhost:8000/api/v1/flashcards/sets/1/cards" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "front_content": "Hello",
    "back_content": "Xin chào",
    "card_type": "text",
    "difficulty": "easy"
  }'
```

### **Lấy danh sách sets với pagination**:
```bash
curl -X GET "http://localhost:8000/api/v1/flashcards/sets?skip=0&limit=10&search=english" \
  -H "Authorization: Bearer <your_token>"
```

---

## 🔧 ERROR HANDLING

### **Common Error Responses**:

**400 Bad Request**:
```json
{
  "detail": "Invalid input data"
}
```

**401 Unauthorized**:
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden**:
```json
{
  "detail": "Insufficient permissions"
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
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Module**: Flashcards API
