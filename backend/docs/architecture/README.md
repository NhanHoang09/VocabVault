# 🏗️ Architecture Documentation

## 📋 Tổng quan

Thư mục này chứa documentation về kiến trúc hệ thống và cấu trúc modules của dự án.

## 📁 Files

### 🏛️ **System Architecture**
- [`README-Architecture.md`](./README-Architecture.md) - Kiến trúc tổng thể hệ thống
- [`README-Module-Structure.md`](./README-Module-Structure.md) - Cấu trúc chi tiết các modules

## 🎯 Kiến trúc hệ thống

### 📊 **Architecture Overview**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔧 **Backend Architecture**
```
app/
├── core/           # Infrastructure
├── modules/        # Feature modules
│   ├── auth/       # Authentication
│   ├── flashcards/ # Flashcard management
│   ├── learning/   # Study sessions
│   └── analytics/  # Progress tracking
└── shared/         # Common utilities
```

### 📡 **API Structure**
- **Authentication**: `/api/v1/auth/*`
- **Flashcards**: `/api/v1/flashcards/*`
- **Learning**: `/api/v1/study/*`
- **Analytics**: `/api/v1/analytics/*`

## 🔗 Module Dependencies

### ✅ **Phase 1 Modules**
- **Auth** → Core (User management)
- **Flashcards** → Auth (User ownership)
- **Learning** → Auth, Flashcards (Study sessions)
- **Analytics** → Auth, Flashcards, Learning (Progress tracking)

### 🔮 **Future Modules**
- **AI** → Auth, Flashcards, Learning
- **Gamification** → Auth, Flashcards, Learning
- **Vocabulary** → Auth, Topics
- **Topics** → Auth

## 📊 Database Schema

### 🔐 **Core Tables**
- `users` - User accounts
- `flashcard_sets` - Flashcard collections
- `flashcards` - Individual cards
- `study_sessions` - Study sessions
- `study_attempts` - Individual attempts

### 📈 **Analytics Tables**
- `user_analytics` - User statistics
- `study_progress` - Progress tracking
- `learning_insights` - AI insights
- `performance_metrics` - Performance data

## 🚀 Performance & Scalability

### ✅ **Current Optimizations**
- Lazy loading relationships
- Proper indexing
- Connection pooling
- Caching strategies

### 🔮 **Future Optimizations**
- Redis caching
- Database sharding
- CDN for media files
- Microservices architecture

---

**Last Updated**: January 2024  
**Status**: Phase 1 Complete ✅
