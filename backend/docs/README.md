# 📚 My Vocabulary Vault Documentation

## 🎯 Tổng quan

Đây là thư mục chứa tất cả documentation của dự án My Vocabulary Vault - một ứng dụng học từ vựng kiểu Quizlet với các tính năng hiện đại.

## 📁 Cấu trúc Documentation

### 📖 **Root Documentation**
- [`README.md`](./README.md) - Tổng quan dự án
- [`CORE_FEATURES.md`](./CORE_FEATURES.md) - Mô tả các tính năng chính

### 🏗️ **Architecture** (`/architecture/`)
- [`README-Architecture.md`](./architecture/README-Architecture.md) - Kiến trúc hệ thống
- [`README-Module-Structure.md`](./architecture/README-Module-Structure.md) - Cấu trúc modules

### 🔧 **Development** (`/development/`)
- [`README-Getting-Started.md`](./development/README-Getting-Started.md) - Hướng dẫn bắt đầu
- [`README-Docker.md`](./development/README-Docker.md) - Docker setup
- [`DETAILED-ROADMAP.md`](./development/DETAILED-ROADMAP.md) - Roadmap chi tiết
- [`ROADMAP-Quizlet-Features.md`](./development/ROADMAP-Quizlet-Features.md) - Roadmap tính năng Quizlet
- [`DATABASE_RELATIONSHIP_SOLUTIONS.md`](./development/DATABASE_RELATIONSHIP_SOLUTIONS.md) - Giải pháp database
- [`OPTIMIZATION_REVIEW.md`](./development/OPTIMIZATION_REVIEW.md) - Review tối ưu hóa
- [`PHASE1_CLEANUP_REPORT.md`](./development/PHASE1_CLEANUP_REPORT.md) - Báo cáo cleanup Phase 1

### 🔍 **Troubleshooting** (`/troubleshooting/`)
- [`AUTH_ISSUE_ANALYSIS.md`](./troubleshooting/AUTH_ISSUE_ANALYSIS.md) - Phân tích lỗi authentication
- [`SWAGGER_AUTH_GUIDE.md`](./troubleshooting/SWAGGER_AUTH_GUIDE.md) - Hướng dẫn Swagger auth
- [`SWAGGER_ISSUE_SOLVED.md`](./troubleshooting/SWAGGER_ISSUE_SOLVED.md) - Giải quyết lỗi Swagger
- [`SWAGGER_TROUBLESHOOTING.md`](./troubleshooting/SWAGGER_TROUBLESHOOTING.md) - Troubleshooting Swagger

### 📡 **API Documentation** (`/api/`)
- [`document/`](./api/document/) - API documentation chi tiết
  - [`auth/`](./api/document/auth/) - Authentication API
  - [`flashcards/`](./api/document/flashcards/) - Flashcards API
  - [`learning/`](./api/document/learning/) - Learning API
  - [`analytics/`](./api/document/analytics/) - Analytics API

## 🚀 Quick Start

1. **Bắt đầu**: Đọc [`development/README-Getting-Started.md`](./development/README-Getting-Started.md)
2. **Kiến trúc**: Xem [`architecture/README-Architecture.md`](./architecture/README-Architecture.md)
3. **API**: Tham khảo [`api/document/`](./api/document/)
4. **Roadmap**: Xem [`development/DETAILED-ROADMAP.md`](./development/DETAILED-ROADMAP.md)

## 📊 Project Status

### ✅ **Phase 1: Core API (COMPLETED)**
- Authentication Module (5 endpoints)
- Flashcards Module (12 endpoints)
- Learning Module (6 endpoints)
- Analytics Module (7 endpoints)
- **Total**: 30 endpoints

### 🔮 **Future Phases**
- Phase 2: AI Integration
- Phase 3: Gamification
- Phase 4: Advanced Features

## 🔗 Links

- **Backend Repository**: `./backend/`
- **Frontend Repository**: `./frontend/`
- **API Documentation**: [`./api/document/`](./api/document/)
- **Swagger UI**: `http://localhost:8000/docs`

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Status**: Phase 1 Complete ✅
