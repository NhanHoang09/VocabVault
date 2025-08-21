# Frontend Structure - My Vocabulary Vault

## Overview

Cấu trúc frontend được tổ chức theo mô hình feature-based architecture với các shared components và utilities được tách biệt rõ ràng.

## Directory Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Auth route group
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/         # Dashboard pages
│   ├── study/            # Study pages
│   ├── flashcards/       # Flashcard pages
│   ├── gamification/     # Gamification pages
│   ├── ai-tutor/         # AI Tutor pages
│   ├── social/           # Social pages
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
│
├── components/            # Shared components
│   ├── ui/               # UI primitives (shadcn/ui style)
│   │   ├── form/         # Form components
│   │   │   ├── FormField.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Textarea.tsx
│   │   │   └── index.ts
│   │   ├── data-display/ # Data display components
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   └── index.ts
│   │   ├── feedback/     # Feedback components
│   │   │   ├── Toast.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── index.ts
│   │   ├── layout/       # Layout components
│   │   │   ├── Container.tsx
│   │   │   ├── Grid.tsx
│   │   │   └── index.ts
│   │   ├── navigation/   # Navigation components
│   │   │   ├── Tabs.tsx
│   │   │   └── index.ts
│   │   └── index.ts      # Main UI exports
│   ├── layout/           # Layout components
│   │   └── Header.tsx
│   └── ClientOnly.tsx
│
├── features/             # Feature-based modules
│   ├── auth/            # Authentication feature
│   │   ├── api/         # API layer
│   │   │   └── auth.api.ts
│   │   ├── components/  # Feature-specific components
│   │   ├── schemas/     # Validation schemas
│   │   │   └── auth.schema.ts
│   │   ├── types/       # TypeScript types
│   │   │   └── auth.ts
│   │   ├── store/       # State management
│   │   │   └── auth.store.ts
│   │   └── index.ts     # Feature exports
│   ├── flashcards/      # Flashcards feature
│   ├── study/           # Study feature
│   ├── gamification/    # Gamification feature
│   ├── ai/              # AI Tutor feature
│   └── social/          # Social feature
│
├── lib/                 # Shared utilities and configurations
│   ├── api-client.ts    # Axios wrapper
│   ├── query-client.ts  # TanStack Query configuration
│   ├── utils.ts         # Utility functions
│   ├── env.mjs          # Environment validation
│   └── logger.ts        # Logging utility
│
├── store/               # Global state management
│   └── app.store.ts     # Zustand stores
│
├── styles/              # Global styles
│   ├── globals.css      # Global CSS
│   └── tailwind.css     # Tailwind CSS with custom styles
│
├── assets/              # Static assets
│   ├── icons/           # Icon exports
│   │   └── index.ts
│   └── lottie/          # Lottie animations
│
├── hooks/               # Shared custom hooks
│   ├── useMediaQuery.ts
│   ├── useLocalStorage.ts
│   ├── useDebounce.ts
│   └── index.ts
│
├── config/              # Application configuration
│   ├── app.config.ts    # App configuration
│   ├── routes.ts        # Route constants
│   └── constants.ts     # General constants
│
├── types/               # Global TypeScript types
│   └── index.ts
│
└── tests/               # Test setup and utilities
    ├── setup-tests.ts
    └── e2e/
        └── auth.spec.ts
```

## Key Principles

### 1. Feature-Based Architecture

- Mỗi feature có cấu trúc riêng với API, components, schemas, types, và store
- Tách biệt logic theo domain
- Dễ dàng maintain và scale

### 2. Shared Components (UI Layer)

- **Form Components**: Input, Textarea, FormField với validation
- **Data Display**: Card, Badge, Table
- **Feedback**: Toast, LoadingSpinner, Alert
- **Layout**: Container, Grid, Flex
- **Navigation**: Tabs, Breadcrumb, Pagination

### 3. State Management

- **Zustand**: Lightweight state management
- **TanStack Query**: Server state management
- **Local Storage**: Persistent state

### 4. API Layer

- **Axios wrapper**: Centralized API client
- **Interceptors**: Automatic token handling
- **Error handling**: Consistent error responses

### 5. Type Safety

- **Zod schemas**: Runtime validation
- **TypeScript**: Compile-time type checking
- **Strict typing**: Full type coverage

## Usage Examples

### Using UI Components

```tsx
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from '@/components/ui/data-display';
import { Input, FormField } from '@/components/ui/form';
import { Button } from '@/components/ui/Button';

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>My Card</CardTitle>
      </CardHeader>
      <CardContent>
        <FormField name="email" label="Email">
          <Input name="email" type="email" placeholder="Enter email" />
        </FormField>
        <Button>Submit</Button>
      </CardContent>
    </Card>
  );
}
```

### Using Features

```tsx
import { useAuthStore } from '@/features/auth';
import { loginSchema, type LoginFormData } from '@/features/auth';

export function LoginForm() {
  const { login, isLoading } = useAuthStore();

  const onSubmit = async (data: LoginFormData) => {
    await login(data);
  };

  // Form implementation
}
```

### Using Hooks

```tsx
import { useMediaQuery, useLocalStorage, useDebounce } from '@/hooks';

export function MyComponent() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  const debouncedSearch = useDebounce(searchTerm, 300);

  // Component logic
}
```

## Benefits

1. **Scalability**: Easy to add new features
2. **Maintainability**: Clear separation of concerns
3. **Reusability**: Shared components and utilities
4. **Type Safety**: Full TypeScript coverage
5. **Performance**: Optimized with TanStack Query
6. **Developer Experience**: Consistent patterns and tools

## Migration Notes

- UI components hiện tại được giữ nguyên
- Cấu trúc mới bổ sung thêm organization
- Có thể migrate từng feature một
- Backward compatible với code hiện tại
