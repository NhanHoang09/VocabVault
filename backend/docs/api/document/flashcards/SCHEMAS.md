# 📊 Flashcards API - Schema Documentation

## 🎯 Tổng quan

Tài liệu này mô tả chi tiết tất cả các schema (request/response models) được sử dụng trong Flashcards API.

---

## 📝 REQUEST SCHEMAS

### FlashcardSetCreate
Schema để tạo bộ flashcard mới.

```json
{
  "title": "string (1-200 chars, required)",
  "description": "string (optional)",
  "category": "string (optional)",
  "tags": ["string"] (optional),
  "is_public": "boolean (required)",
  "is_featured": "boolean (optional, default: false)"
}
```

**Field Descriptions:**
- `title`: Tiêu đề bộ flashcard (bắt buộc, 1-200 ký tự)
- `description`: Mô tả chi tiết (tùy chọn)
- `category`: Danh mục để tổ chức (tùy chọn)
- `tags`: Danh sách tags để tìm kiếm dễ dàng (tùy chọn)
- `is_public`: Có công khai hay không (bắt buộc)
- `is_featured`: Đánh dấu là featured (tùy chọn, mặc định: false)

**Validation Rules:**
- `title`: Required, min length 1, max length 200
- `description`: Optional, max length 1000
- `category`: Optional, max length 100
- `tags`: Optional, max 10 tags, each tag max 50 chars
- `is_public`: Required, boolean
- `is_featured`: Optional, boolean, default false

---

### FlashcardSetUpdate
Schema để cập nhật bộ flashcard (partial update).

```json
{
  "title": "string (1-200 chars, optional)",
  "description": "string (optional)",
  "category": "string (optional)",
  "tags": ["string"] (optional),
  "is_public": "boolean (optional)",
  "is_featured": "boolean (optional)"
}
```

**Field Descriptions:** Giống FlashcardSetCreate nhưng tất cả fields đều optional.

**Validation Rules:** Giống FlashcardSetCreate.

---

### FlashcardCreate
Schema để tạo flashcard mới.

```json
{
  "front_content": "string (1+ chars, required)",
  "back_content": "string (1+ chars, required)",
  "card_type": "string (optional, enum)",
  "difficulty": "string (optional, enum)",
  "media_url": "string (optional, URL)",
  "card_metadata": "object (optional, JSON)"
}
```

**Field Descriptions:**
- `front_content`: Nội dung mặt trước (câu hỏi/prompt) - bắt buộc
- `back_content`: Nội dung mặt sau (câu trả lời/giải thích) - bắt buộc
- `card_type`: Loại card - tùy chọn
- `difficulty`: Độ khó - tùy chọn
- `media_url`: URL đến media content - tùy chọn
- `card_metadata`: Metadata bổ sung dạng JSON - tùy chọn

**Enums:**
- `card_type`: `["text", "image", "audio", "video"]`
- `difficulty`: `["easy", "medium", "hard"]`

**Validation Rules:**
- `front_content`: Required, min length 1, max length 1000
- `back_content`: Required, min length 1, max length 1000
- `card_type`: Optional, must be one of enum values
- `difficulty`: Optional, must be one of enum values
- `media_url`: Optional, valid URL format
- `card_metadata`: Optional, valid JSON object

---

### FlashcardUpdate
Schema để cập nhật flashcard (partial update).

```json
{
  "front_content": "string (1+ chars, optional)",
  "back_content": "string (1+ chars, optional)",
  "card_type": "string (optional, enum)",
  "difficulty": "string (optional, enum)",
  "media_url": "string (optional, URL)",
  "card_metadata": "object (optional, JSON)"
}
```

**Field Descriptions:** Giống FlashcardCreate nhưng tất cả fields đều optional.

**Validation Rules:** Giống FlashcardCreate.

---

## 📊 RESPONSE SCHEMAS

### FlashcardSetResponse
Schema response cho bộ flashcard.

```json
{
  "id": "integer (required)",
  "title": "string (required)",
  "description": "string (optional)",
  "category": "string (optional)",
  "tags": ["string"] (optional),
  "is_public": "boolean (required)",
  "is_featured": "boolean (required)",
  "user_id": "integer (required)",
  "cards_count": "integer (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)"
}
```

**Field Descriptions:**
- `id`: ID duy nhất của bộ flashcard
- `title`: Tiêu đề bộ flashcard
- `description`: Mô tả chi tiết
- `category`: Danh mục
- `tags`: Danh sách tags
- `is_public`: Có công khai hay không
- `is_featured`: Có được đánh dấu featured hay không
- `user_id`: ID của user sở hữu
- `cards_count`: Số lượng cards trong set
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

---

### FlashcardSetListResponse
Schema response cho danh sách bộ flashcard (có pagination).

```json
{
  "items": ["FlashcardSetResponse"] (required),
  "total": "integer (required)",
  "page": "integer (required)",
  "size": "integer (required)",
  "pages": "integer (required)"
}
```

**Field Descriptions:**
- `items`: Danh sách các bộ flashcard
- `total`: Tổng số bộ flashcard
- `page`: Trang hiện tại
- `size`: Kích thước trang
- `pages`: Tổng số trang

---

### FlashcardSetWithCards
Schema response cho bộ flashcard kèm tất cả cards.

```json
{
  "id": "integer (required)",
  "title": "string (required)",
  "description": "string (optional)",
  "category": "string (optional)",
  "tags": ["string"] (optional),
  "is_public": "boolean (required)",
  "is_featured": "boolean (required)",
  "user_id": "integer (required)",
  "cards_count": "integer (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)",
  "cards": ["FlashcardResponse"] (required)
}
```

**Field Descriptions:** Giống FlashcardSetResponse + thêm field `cards` chứa danh sách tất cả cards.

---

### FlashcardResponse
Schema response cho flashcard.

```json
{
  "id": "integer (required)",
  "set_id": "integer (required)",
  "front_content": "string (required)",
  "back_content": "string (required)",
  "card_type": "string (required)",
  "media_url": "string (optional)",
  "difficulty": "string (required)",
  "card_metadata": "object (required)",
  "mastery_level": "string (required, enum)",
  "mastery_score": "float (required)",
  "review_count": "integer (required)",
  "correct_count": "integer (required)",
  "incorrect_count": "integer (required)",
  "created_at": "datetime (required)",
  "updated_at": "datetime (required)"
}
```

**Field Descriptions:**
- `id`: ID duy nhất của flashcard
- `set_id`: ID của bộ flashcard chứa card này
- `front_content`: Nội dung mặt trước
- `back_content`: Nội dung mặt sau
- `card_type`: Loại card
- `media_url`: URL đến media content
- `difficulty`: Độ khó
- `card_metadata`: Metadata bổ sung
- `mastery_level`: Mức độ thành thạo
- `mastery_score`: Điểm thành thạo (0.0 - 1.0)
- `review_count`: Số lần review
- `correct_count`: Số lần trả lời đúng
- `incorrect_count`: Số lần trả lời sai
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật cuối

**Enums:**
- `mastery_level`: `["NOT_LEARNED", "LEARNING", "WELL_LEARNED", "MASTERED"]`

---

## 🔍 QUERY PARAMETERS

### Pagination Parameters
```json
{
  "skip": "integer (optional, default: 0, min: 0)",
  "limit": "integer (optional, default: 100, min: 1, max: 1000)"
}
```

### Search & Filter Parameters
```json
{
  "search": "string (optional, search in title and description)",
  "category": "string (optional, filter by category)"
}
```

---

## 🎯 PATH PARAMETERS

### Set ID
```json
{
  "set_id": "integer (required, min: 1)"
}
```

### Card ID
```json
{
  "card_id": "integer (required, min: 1)"
}
```

---

## 🔧 VALIDATION RULES

### String Lengths
- `title`: 1-200 characters
- `description`: 0-1000 characters
- `category`: 0-100 characters
- `tags`: Max 10 tags, each 0-50 characters
- `front_content`: 1-1000 characters
- `back_content`: 1-1000 characters
- `search`: 0-100 characters

### Numeric Ranges
- `skip`: 0 to infinity
- `limit`: 1 to 1000
- `set_id`: 1 to infinity
- `card_id`: 1 to infinity
- `mastery_score`: 0.0 to 1.0

### Boolean Fields
- `is_public`: true/false
- `is_featured`: true/false

### Enum Values
- `card_type`: `["text", "image", "audio", "video"]`
- `difficulty`: `["easy", "medium", "hard"]`
- `mastery_level`: `["NOT_LEARNED", "LEARNING", "WELL_LEARNED", "MASTERED"]`

---

## 📝 EXAMPLE SCHEMAS

### Complete FlashcardSetCreate Example
```json
{
  "title": "Advanced English Vocabulary",
  "description": "A comprehensive collection of advanced English words for TOEFL preparation",
  "category": "English",
  "tags": ["advanced", "toefl", "vocabulary", "academic"],
  "is_public": true,
  "is_featured": false
}
```

### Complete FlashcardCreate Example
```json
{
  "front_content": "Ubiquitous",
  "back_content": "Present, appearing, or found everywhere",
  "card_type": "text",
  "difficulty": "hard",
  "media_url": null,
  "card_metadata": {
    "example_sentence": "Smartphones have become ubiquitous in modern society.",
    "pronunciation": "juːˈbɪkwɪtəs",
    "synonyms": ["omnipresent", "pervasive", "widespread"],
    "antonyms": ["rare", "scarce", "uncommon"]
  }
}
```

### Complete FlashcardResponse Example
```json
{
  "id": 1,
  "set_id": 1,
  "front_content": "Ubiquitous",
  "back_content": "Present, appearing, or found everywhere",
  "card_type": "text",
  "media_url": null,
  "difficulty": "hard",
  "card_metadata": {
    "example_sentence": "Smartphones have become ubiquitous in modern society.",
    "pronunciation": "juːˈbɪkwɪtəs",
    "synonyms": ["omnipresent", "pervasive", "widespread"],
    "antonyms": ["rare", "scarce", "uncommon"]
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

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Module**: Flashcards API Schemas
