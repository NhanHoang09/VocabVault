# API Management & Middleware Guide

## 🏗️ **Cấu trúc API Management**

### 1. **API Client Architecture**

```
src/lib/api/
├── client.ts              # Main API client với middleware system
├── types.ts               # TypeScript types cho API
├── middleware/            # Middleware modules
│   ├── auth.middleware.ts # Authentication middleware
│   ├── cache.middleware.ts # Caching middleware
│   ├── error.middleware.ts # Error handling middleware
│   ├── logging.middleware.ts # Logging middleware
│   └── index.ts           # Middleware exports
├── services/              # Service classes
│   ├── base.service.ts    # Base service class
│   ├── auth.service.ts    # Auth service
│   └── index.ts           # Service exports
└── index.ts               # Main exports
```

## 🔧 **Middleware System**

### **Request Middleware Flow**

```
Request → Logging → Auth → Cache → API
```

### **Response Middleware Flow**

```
API → Cache → Auth → Logging → Response
```

### **Error Middleware Flow**

```
Error → Logging → Auth → Retry → Global Error → Reject
```

## 📝 **Cách sử dụng**

### 1. **Basic API Calls**

```typescript
import { api } from '@/lib/api';

// Simple GET request
const response = await api.get('/users/profile');

// POST with data
const result = await api.post('/auth/login', {
  email: 'user@example.com',
  password: 'password',
});

// With custom config
const data = await api.get('/flashcards', {
  cache: true,
  cacheTime: 300000, // 5 minutes
  retry: true,
  skipErrorHandler: false,
});
```

### 2. **Using Services**

```typescript
import { authService } from '@/lib/api';

// Login
const authResponse = await authService.login({
  email: 'user@example.com',
  password: 'password',
});

// Register
const registerResponse = await authService.register({
  email: 'user@example.com',
  password: 'password',
  username: 'username',
});

// Upload file with progress
const avatarResponse = await authService.uploadAvatar(file, progress => {
  console.log(`Upload progress: ${progress}%`);
});
```

### 3. **Custom Middleware**

```typescript
import { RequestMiddleware } from '@/lib/api';

// Create custom middleware
const customMiddleware: RequestMiddleware = {
  name: 'custom-middleware',
  priority: 5,
  handler: async config => {
    // Add custom logic
    config.headers['X-Custom-Header'] = 'custom-value';
    return config;
  },
};

// Add to API client
import { apiClient } from '@/lib/api';
apiClient.addRequestMiddleware(customMiddleware);
```

## 🛡️ **Middleware Features**

### 1. **Authentication Middleware**

- **Auto token injection**: Tự động thêm Bearer token
- **Token refresh**: Tự động refresh khi token hết hạn
- **Auto logout**: Redirect to login khi unauthorized
- **Skip auth**: Có thể skip cho public endpoints

```typescript
// Skip auth for public endpoints
await api.get('/public/data', { skipAuth: true });
```

### 2. **Cache Middleware**

- **In-memory caching**: Cache responses trong memory
- **TTL support**: Configurable cache time
- **GET requests only**: Chỉ cache GET requests
- **Cache invalidation**: Utilities để clear cache

```typescript
// Enable caching
await api.get('/flashcards', {
  cache: true,
  cacheTime: 600000, // 10 minutes
});

// Clear cache
import { cacheUtils } from '@/lib/api';
cacheUtils.clear();
cacheUtils.clearByPattern('/flashcards');
```

### 3. **Error Handling Middleware**

- **Global error handling**: Consistent error responses
- **Retry mechanism**: Auto retry failed requests
- **Error logging**: Detailed error logs
- **Custom error messages**: User-friendly messages

```typescript
// Enable retry
await api.get('/api/data', {
  retry: true,
  retryCount: 3,
});

// Skip error handling
await api.get('/api/data', {
  skipErrorHandler: true,
});
```

### 4. **Logging Middleware**

- **Request logging**: Log tất cả requests
- **Response logging**: Log responses với timing
- **Error logging**: Detailed error logs
- **Performance tracking**: Response time tracking

## 🚀 **Advanced Features**

### 1. **File Upload with Progress**

```typescript
import { authService } from '@/lib/api';

const uploadResponse = await authService.uploadAvatar(file, progress => {
  // Update UI with progress
  setUploadProgress(progress);
});
```

### 2. **File Download**

```typescript
import { BaseService } from '@/lib/api';

class FileService extends BaseService {
  async downloadReport(reportId: string) {
    await this.download(
      `/reports/${reportId}/download`,
      `report-${reportId}.pdf`
    );
  }
}
```

### 3. **Custom Service Creation**

```typescript
import { BaseService } from '@/lib/api';

export class FlashcardService extends BaseService {
  constructor() {
    super('/flashcards');
  }

  async getLists() {
    return this.get('/lists', { cache: true });
  }

  async createList(data: CreateListRequest) {
    return this.post('/lists', data);
  }

  async updateList(id: string, data: UpdateListRequest) {
    return this.put(`/lists/${id}`, data);
  }

  async deleteList(id: string) {
    return this.delete(`/lists/${id}`);
  }
}
```

## ⚙️ **Configuration**

### 1. **Environment Variables**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=10000
```

### 2. **API Client Configuration**

```typescript
import { apiClient } from '@/lib/api';

// Set base URL
apiClient.setBaseURL('https://api.example.com');

// Set auth token
apiClient.setAuthToken('your-token');

// Remove auth token
apiClient.removeAuthToken();
```

## 🔍 **Debugging & Monitoring**

### 1. **Cache Statistics**

```typescript
import { cacheUtils } from '@/lib/api';

const stats = cacheUtils.getStats();
console.log('Cache size:', stats.size);
console.log('Cached keys:', stats.keys);
```

### 2. **Error Handling**

```typescript
try {
  const response = await api.get('/api/data');
} catch (error) {
  if (error.apiError) {
    console.log('API Error:', error.apiError.message);
    console.log('Error Code:', error.apiError.code);
    console.log('Status:', error.apiError.status);
  }
}
```

## 📊 **Performance Optimization**

### 1. **Caching Strategy**

- Cache static data (user profile, settings)
- Cache frequently accessed data (flashcard lists)
- Use appropriate TTL for different data types

### 2. **Request Optimization**

- Use pagination for large datasets
- Implement request deduplication
- Use appropriate retry strategies

### 3. **Error Recovery**

- Implement exponential backoff
- Handle network errors gracefully
- Provide fallback data when possible

## 🎯 **Best Practices**

1. **Always use services** for API calls instead of direct api calls
2. **Enable caching** for read-only data
3. **Handle errors properly** with try-catch blocks
4. **Use TypeScript** for type safety
5. **Monitor performance** with logging middleware
6. **Test error scenarios** including network failures
7. **Implement proper loading states** for better UX
