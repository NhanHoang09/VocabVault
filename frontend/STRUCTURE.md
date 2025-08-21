# 🏗️ Cấu trúc thư mục VocabVault Frontend

## 📁 Tổng quan cấu trúc

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   ├── components/             # React Components
│   ├── hooks/                  # Custom React Hooks
│   ├── lib/                    # Utilities & Configurations
│   ├── types/                  # TypeScript Type Definitions
│   ├── constants/              # Application Constants
│   ├── services/               # API Services
│   ├── stores/                 # State Management
│   └── styles/                 # Global Styles
├── public/                     # Static Assets
├── docs/                       # Documentation
└── tests/                      # Test Files
```

## 🎯 Chi tiết từng thư mục

### 📱 **`src/app/`** - Next.js App Router

```
app/
├── layout.tsx                  # Root layout
├── page.tsx                    # Home page
├── globals.css                 # Global styles
├── favicon.ico                 # App icon
├── login/                      # Authentication pages
│   └── page.tsx
├── register/
│   └── page.tsx
├── demo/
│   └── page.tsx
├── dashboard/                  # Protected pages
│   └── page.tsx
├── study/
│   └── page.tsx
├── vocabulary/
│   └── page.tsx
├── progress/
│   └── page.tsx
├── profile/
│   └── page.tsx
└── settings/
    └── page.tsx
```

### 🧩 **`src/components/`** - React Components

```
components/
├── ui/                         # Reusable UI Components
│   ├── Button.tsx
│   ├── Modal.tsx
│   ├── Input.tsx
│   ├── Card.tsx
│   ├── Badge.tsx
│   └── index.ts
├── layout/                     # Layout Components
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── Sidebar.tsx
│   └── Navigation.tsx
├── study/                      # Study-specific Components
│   ├── Flashcard.tsx
│   ├── StudySession.tsx
│   ├── ProgressChart.tsx
│   └── VocabularyList.tsx
├── auth/                       # Authentication Components
│   ├── LoginForm.tsx
│   ├── RegisterForm.tsx
│   └── AuthGuard.tsx
└── common/                     # Common Components
    ├── Loading.tsx
    ├── ErrorBoundary.tsx
    └── Toast.tsx
```

### 🎣 **`src/hooks/`** - Custom React Hooks

```
hooks/
├── useAuth.ts                  # Authentication logic
├── useStudy.ts                 # Study session logic
├── useVocabulary.ts            # Vocabulary management
├── useProgress.ts              # Progress tracking
├── useLocalStorage.ts          # Local storage utilities
├── useDebounce.ts              # Debounce utility
└── useMediaQuery.ts            # Responsive utilities
```

### 🛠️ **`src/lib/`** - Utilities & Configurations

```
lib/
├── api.ts                      # API client configuration
├── utils.ts                    # Utility functions
├── store.ts                    # State management (Zustand)
├── validation.ts               # Form validation schemas
├── date.ts                     # Date utilities
└── storage.ts                  # Storage utilities
```

### 📝 **`src/types/`** - TypeScript Definitions

```
types/
├── index.ts                    # Main type definitions
├── api.ts                      # API response types
├── auth.ts                     # Authentication types
├── study.ts                    # Study-related types
├── vocabulary.ts               # Vocabulary types
└── ui.ts                       # UI component types
```

### 🔧 **`src/constants/`** - Application Constants

```
constants/
├── index.ts                    # Main constants
├── api.ts                      # API configuration
├── routes.ts                   # Route definitions
├── messages.ts                 # Error/Success messages
└── config.ts                   # App configuration
```

### 🌐 **`src/services/`** - API Services

```
services/
├── auth.service.ts             # Authentication API
├── vocabulary.service.ts       # Vocabulary API
├── study.service.ts            # Study session API
├── progress.service.ts         # Progress tracking API
└── user.service.ts             # User management API
```

### 📊 **`src/stores/`** - State Management

```
stores/
├── auth.store.ts               # Authentication state
├── study.store.ts              # Study session state
├── vocabulary.store.ts         # Vocabulary state
├── progress.store.ts           # Progress state
└── ui.store.ts                 # UI state
```

### 🎨 **`src/styles/`** - Global Styles

```
styles/
├── globals.css                 # Global CSS
├── components.css              # Component styles
├── utilities.css               # Utility classes
└── themes/                     # Theme definitions
    ├── light.css
    └── dark.css
```

## 🚀 **Nguyên tắc tổ chức**

### 1. **Separation of Concerns**

- Mỗi thư mục có trách nhiệm rõ ràng
- Tách biệt logic, UI, và data
- Dễ dàng tìm kiếm và bảo trì

### 2. **Scalability**

- Cấu trúc mở rộng được
- Dễ dàng thêm tính năng mới
- Không bị phụ thuộc lẫn nhau

### 3. **Reusability**

- Components tái sử dụng được
- Hooks có thể dùng chung
- Utilities phổ biến

### 4. **Maintainability**

- Code dễ đọc và hiểu
- Naming conventions rõ ràng
- Documentation đầy đủ

## 📋 **Naming Conventions**

### **Files & Folders**

- `camelCase` cho files
- `PascalCase` cho components
- `kebab-case` cho CSS classes
- `UPPER_SNAKE_CASE` cho constants

### **Components**

- `PascalCase` cho component names
- `camelCase` cho props
- `on` prefix cho event handlers
- `is` prefix cho boolean props

### **Hooks**

- `use` prefix cho custom hooks
- Descriptive names
- Return objects with clear properties

## 🔄 **Import/Export Patterns**

### **Barrel Exports**

```typescript
// components/ui/index.ts
export { default as Button } from './Button';
export { default as Modal } from './Modal';
export { default as Input } from './Input';
```

### **Absolute Imports**

```typescript
import { Button } from '@/components/ui';
import { useAuth } from '@/hooks/useAuth';
import { API_CONFIG } from '@/constants';
```

## 🧪 **Testing Structure**

```
tests/
├── components/                 # Component tests
├── hooks/                      # Hook tests
├── utils/                      # Utility tests
├── integration/                # Integration tests
└── e2e/                        # End-to-end tests
```

## 📚 **Documentation**

```
docs/
├── components/                 # Component documentation
├── api/                        # API documentation
├── deployment/                 # Deployment guides
└── contributing/               # Contributing guidelines
```

## 🎯 **Lợi ích của cấu trúc này**

1. **Dễ hiểu**: Cấu trúc rõ ràng, logic
2. **Dễ mở rộng**: Thêm tính năng mới dễ dàng
3. **Dễ bảo trì**: Code được tổ chức tốt
4. **Dễ test**: Tách biệt các concerns
5. **Dễ tái sử dụng**: Components và hooks modular
6. **Chuẩn quốc tế**: Theo best practices của React/Next.js
7. **Team-friendly**: Dễ dàng cho team collaboration
