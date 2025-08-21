# Cấu trúc Frontend Tối ưu

## 🎯 **Tổng quan**

Đã tối ưu lại cấu trúc thư mục frontend theo nguyên tắc **Feature-Based Architecture** với các cải tiến sau:

### **Thay đổi chính:**

- ✅ **Tách components theo features**: Mỗi feature có components riêng
- ✅ **Đổi tên demo → preview**: Tên gọi phù hợp hơn
- ✅ **Tích hợp ToastProvider & QueryClient**: Trong layout chính
- ✅ **Tối ưu imports**: Sử dụng barrel exports
- ✅ **Tách biệt concerns**: UI logic tách khỏi business logic

## 📁 **Cấu trúc thư mục mới**

```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout với providers
│   ├── page.tsx           # Home page
│   ├── login/             # Login page
│   ├── register/          # Register page
│   ├── demo/              # Demo page (legacy)
│   └── preview/           # Preview page (new)
├── features/              # Feature-based modules
│   ├── home/              # Home feature
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── HeroSection.tsx
│   │   │   ├── FeaturesGrid.tsx
│   │   │   └── Footer.tsx
│   │   └── index.ts
│   ├── auth/              # Authentication feature
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── schemas/
│   │   ├── store/
│   │   ├── types/
│   │   └── index.ts
│   └── demo/              # Demo/Preview feature
│       ├── components/
│       │   ├── DemoHeader.tsx
│       │   ├── DemoFeatures.tsx
│       │   └── DemoCTA.tsx
│       └── index.ts
├── components/            # Shared UI components
│   ├── ui/               # UI primitives
│   ├── providers/        # Context providers
│   └── examples/         # Example components
├── lib/                  # Utilities & configurations
│   ├── api/              # API management
│   ├── hooks/            # Shared hooks
│   └── utils/            # Utility functions
└── config/               # App configuration
```

## 🔄 **Migration Changes**

### **1. Layout Updates**

```tsx
// app/layout.tsx
import { ToastProvider } from '@/components/providers/ToastProvider';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <QueryClientProvider client={queryClient}>
          <ToastProvider>{children}</ToastProvider>
          <ReactQueryDevtools />
        </QueryClientProvider>
      </body>
    </html>
  );
}
```

### **2. Feature Components**

```tsx
// features/home/components/HeroSection.tsx
export const HeroSection: React.FC = () => {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      {/* Hero content */}
    </main>
  );
};

// features/home/index.ts
export { HeroSection } from './components/HeroSection';
export { FeaturesGrid } from './components/FeaturesGrid';
export { Header } from './components/Header';
export { Footer } from './components/Footer';
```

### **3. Page Updates**

```tsx
// app/page.tsx
import { Header, HeroSection, FeaturesGrid, Footer } from '@/features/home';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header />
      <HeroSection />
      <FeaturesGrid />
      <Footer />
    </div>
  );
}
```

## 🎨 **Component Architecture**

### **1. Feature-Based Components**

- **Home Feature**: Landing page components
- **Auth Feature**: Authentication forms & logic
- **Demo Feature**: Preview/demo components

### **2. Shared Components**

- **UI Primitives**: Form, data-display, feedback, layout, navigation
- **Providers**: Toast, Query Client, Auth context
- **Examples**: Error handling, demo components

### **3. Component Structure**

```tsx
// Standard component structure
export const ComponentName: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // Hooks
  const [state, setState] = useState();

  // Event handlers
  const handleClick = () => {};

  // Render
  return <div className="component-classes">{/* Component content */}</div>;
};
```

## 🚀 **Benefits**

### **1. Maintainability**

- ✅ **Separation of concerns**: UI logic tách khỏi business logic
- ✅ **Reusability**: Components có thể tái sử dụng
- ✅ **Testability**: Dễ dàng test từng component riêng biệt

### **2. Scalability**

- ✅ **Feature-based**: Dễ dàng thêm features mới
- ✅ **Modular**: Mỗi feature độc lập
- ✅ **Extensible**: Có thể mở rộng dễ dàng

### **3. Developer Experience**

- ✅ **Clear structure**: Cấu trúc rõ ràng, dễ hiểu
- ✅ **Barrel exports**: Import/export đơn giản
- ✅ **Type safety**: TypeScript support đầy đủ

## 📋 **Best Practices**

### **1. Component Organization**

```tsx
// ✅ Good: Feature-based organization
features / auth / components / LoginForm.tsx;
features / home / components / HeroSection.tsx;

// ❌ Bad: Mixed components
components / LoginForm.tsx;
components / HeroSection.tsx;
```

### **2. Import/Export**

```tsx
// ✅ Good: Barrel exports
export { LoginForm } from './components/LoginForm';
export { RegisterForm } from './components/RegisterForm';

// ✅ Good: Clean imports
import { LoginForm } from '@/features/auth';

// ❌ Bad: Direct imports
import LoginForm from '@/features/auth/components/LoginForm';
```

### **3. Component Props**

```tsx
// ✅ Good: Typed props
interface ComponentProps {
  title: string;
  onAction?: () => void;
}

export const Component: React.FC<ComponentProps> = ({ title, onAction }) => {
  // Component logic
};

// ❌ Bad: Untyped props
export const Component = props => {
  // Component logic
};
```

## 🔧 **Configuration**

### **1. TypeScript Paths**

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/features/*": ["./src/features/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/config/*": ["./src/config/*"]
    }
  }
}
```

### **2. ESLint Configuration**

```js
// .eslintrc.js
module.exports = {
  extends: ['next/core-web-vitals', '@typescript-eslint/recommended'],
  rules: {
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index',
        ],
        'newlines-between': 'always',
      },
    ],
  },
};
```

## 📊 **Performance Optimizations**

### **1. Code Splitting**

- ✅ **Feature-based**: Mỗi feature có thể lazy load
- ✅ **Component-based**: Components có thể lazy load
- ✅ **Route-based**: Pages có thể lazy load

### **2. Bundle Optimization**

- ✅ **Tree shaking**: Loại bỏ unused code
- ✅ **Minification**: Giảm kích thước bundle
- ✅ **Compression**: Gzip compression

### **3. Caching Strategy**

- ✅ **Static assets**: Cache lâu dài
- ✅ **API responses**: Cache với React Query
- ✅ **Component memoization**: React.memo cho performance

## 🧪 **Testing Strategy**

### **1. Unit Tests**

```tsx
// __tests__/features/auth/components/LoginForm.test.tsx
import { render, screen } from '@testing-library/react';
import { LoginForm } from '@/features/auth';

describe('LoginForm', () => {
  it('renders login form', () => {
    render(<LoginForm />);
    expect(screen.getByText('Đăng nhập')).toBeInTheDocument();
  });
});
```

### **2. Integration Tests**

```tsx
// __tests__/features/auth/LoginFlow.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from '@/features/auth';

describe('Login Flow', () => {
  it('submits form with valid data', async () => {
    render(<LoginForm />);
    // Test form submission
  });
});
```

## 🚀 **Next Steps**

### **1. Immediate Actions**

- [ ] Add more features (flashcards, study, analytics)
- [ ] Implement error boundaries
- [ ] Add loading states
- [ ] Optimize images and assets

### **2. Future Enhancements**

- [ ] Add PWA support
- [ ] Implement offline functionality
- [ ] Add internationalization (i18n)
- [ ] Implement advanced caching

### **3. Monitoring & Analytics**

- [ ] Add performance monitoring
- [ ] Implement error tracking
- [ ] Add user analytics
- [ ] Monitor bundle size

Cấu trúc mới này cung cấp nền tảng vững chắc cho việc phát triển và mở rộng ứng dụng trong tương lai.
