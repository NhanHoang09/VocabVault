# 📁 Documentation Structure

## 🎯 Tổng quan

Tài liệu API được tổ chức theo cấu trúc module-based, tương ứng với kiến trúc của ứng dụng.

---

## 📂 Cấu trúc thư mục

```
document/
├── README.md                 # Tài liệu chính - Tổng quan API
├── STRUCTURE.md             # File này - Cấu trúc tài liệu
├── auth/                    # Authentication Module
│   ├── README.md           # Tài liệu chi tiết
│   ├── QUICK_REFERENCE.md  # Tham khảo nhanh
│   ├── SCHEMAS.md          # Schema documentation
│   └── INDEX.md            # Index và navigation
├── flashcards/              # Flashcards Module ✅
│   ├── README.md           # Tài liệu chi tiết ✅
│   ├── QUICK_REFERENCE.md  # Tham khảo nhanh ✅
│   ├── SCHEMAS.md          # Schema documentation ✅
│   └── INDEX.md            # Index và navigation ✅
├── learning/                # Learning Module
│   ├── README.md           # Tài liệu chi tiết
│   ├── QUICK_REFERENCE.md  # Tham khảo nhanh
│   ├── SCHEMAS.md          # Schema documentation
│   └── INDEX.md            # Index và navigation
└── analytics/               # Analytics Module
    ├── README.md           # Tài liệu chi tiết
    ├── QUICK_REFERENCE.md  # Tham khảo nhanh
    ├── SCHEMAS.md          # Schema documentation
    └── INDEX.md            # Index và navigation
```

---

## 📋 Mô tả từng module

### 🔐 Authentication Module (`/auth`)
- **Path**: `/api/v1/auth`
- **Mô tả**: Quản lý đăng ký, đăng nhập, và xác thực người dùng
- **Endpoints**: Register, Login, Refresh Token, etc.
- **Status**: ⏳ Chưa tạo tài liệu

### 📚 Flashcards Module (`/flashcards`) ✅
- **Path**: `/api/v1/flashcards`
- **Mô tả**: Quản lý bộ flashcard và các card riêng lẻ
- **Endpoints**: 12 endpoints (7 FlashcardSet + 5 Flashcard)
- **Status**: ✅ Hoàn thành tài liệu

### 🎮 Learning Module (`/learning`)
- **Path**: `/api/v1/study`
- **Mô tả**: Quản lý phiên học tập và theo dõi tiến độ
- **Endpoints**: Study sessions, Study attempts, Progress tracking
- **Status**: ⏳ Chưa tạo tài liệu

### 📊 Analytics Module (`/analytics`)
- **Path**: `/api/v1/analytics`
- **Mô tả**: Phân tích tiến độ học tập và thống kê
- **Endpoints**: Progress analytics, Statistics, Mastery tracking
- **Status**: ⏳ Chưa tạo tài liệu

---

## 📖 Cấu trúc tài liệu cho mỗi module

Mỗi module đều có 4 file tài liệu:

### 1. **README.md** - Tài liệu chi tiết
- Mô tả đầy đủ tất cả endpoints
- Request/Response examples chi tiết
- Authentication & Authorization rules
- Error handling và status codes
- Tính năng nổi bật và examples

### 2. **QUICK_REFERENCE.md** - Tham khảo nhanh
- Bảng tóm tắt tất cả endpoints
- Authentication levels (Required/Optional)
- Common request bodies và response models
- Quick examples với curl commands
- Important notes và validation rules

### 3. **SCHEMAS.md** - Schema Documentation
- Request schemas chi tiết (Create/Update)
- Response schemas đầy đủ
- Validation rules và field descriptions
- Enum values và data types
- Example schemas hoàn chỉnh

### 4. **INDEX.md** - Index và Navigation
- Tổng quan module
- Cấu trúc tài liệu
- Quick start examples
- Endpoints summary
- Navigation links

---

## 🎯 Tiêu chuẩn tài liệu

### Format chuẩn
- **Markdown** format
- **Emoji icons** để dễ nhận biết
- **Code blocks** với syntax highlighting
- **Tables** cho endpoints summary
- **Consistent structure** across modules

### Nội dung bắt buộc
- ✅ **Base URL** và authentication info
- ✅ **Endpoints list** với method, path, auth level
- ✅ **Request/Response examples** với JSON
- ✅ **Error handling** và status codes
- ✅ **Validation rules** và field descriptions
- ✅ **Quick examples** với curl commands

### Navigation
- ✅ **Cross-references** giữa các file
- ✅ **Back to main** documentation links
- ✅ **Module-specific** navigation
- ✅ **Version info** và last updated

---

## 🚀 Cách sử dụng

### Cho Developers
1. **Bắt đầu**: Đọc `document/README.md` để hiểu tổng quan
2. **Chọn module**: Vào thư mục module cụ thể
3. **Quick start**: Đọc `QUICK_REFERENCE.md` để bắt đầu nhanh
4. **Chi tiết**: Đọc `README.md` để hiểu đầy đủ
5. **Schemas**: Tham khảo `SCHEMAS.md` cho validation rules

### Cho API Users
1. **Authentication**: Đọc auth module để setup
2. **Core features**: Sử dụng flashcards module
3. **Study tracking**: Sử dụng learning module
4. **Analytics**: Sử dụng analytics module

---

## 📝 Template cho module mới

Khi tạo tài liệu cho module mới, sử dụng template:

```markdown
# 📚 [Module Name] API Documentation

## 🎯 Tổng quan
[Module description]

**Base URL**: `/api/v1/[module-path]`

## 📋 Danh sách Endpoints
[Endpoints table]

## 🔐 Authentication
[Auth requirements]

## 📝 Examples
[Quick examples]

## 📊 Response Models
[Common response formats]

## 🎯 Tính năng chính
[Key features list]

---
**Version**: 1.0.0  
**Last Updated**: [Date]  
**Module**: [Module Name] API
```

---

## 🔄 Maintenance

### Cập nhật tài liệu
- ✅ **Version tracking** trong mỗi file
- ✅ **Last updated** timestamps
- ✅ **Changelog** cho major changes
- ✅ **Cross-reference** updates

### Quality checks
- ✅ **Link validation** giữa các file
- ✅ **Example testing** với actual API
- ✅ **Schema validation** với code
- ✅ **Consistency check** across modules

---

**Documentation Version**: 1.0.0  
**Last Updated**: January 2024  
**Maintained by**: My Vocabulary Vault Team
