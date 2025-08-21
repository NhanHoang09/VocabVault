# Error Handling & Toast Notifications Guide

## 🎯 **Overview**

Hệ thống error handling được thiết kế để tự động xử lý các lỗi API và hiển thị toast notifications cho user một cách nhất quán và user-friendly.

## 🏗️ **Architecture**

### **Error Handling Flow**

```
API Error → Error Middleware → Toast Middleware → User Notification
```

### **Components**

- **Toast Middleware**: Tự động show toast cho API errors
- **Toast Provider**: Quản lý toast notifications trong app
- **Toast Component**: UI component để hiển thị notifications
- **useToast Hook**: Hook để sử dụng toast programmatically

## 📝 **Cách sử dụng**

### 1. **Setup Toast Provider**

```tsx
// app/layout.tsx hoặc root component
import { ToastProvider } from '@/components/providers/ToastProvider';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ToastProvider>{children}</ToastProvider>
      </body>
    </html>
  );
}
```

### 2. **Automatic Error Handling**

```typescript
import { api } from '@/lib/api';

// API errors sẽ tự động show toast
try {
  await api.get('/users/profile');
} catch (error) {
  // Toast đã được show tự động bởi middleware
  console.log('Error handled automatically');
}
```

### 3. **Manual Toast Notifications**

```typescript
import { useToastNotification } from '@/hooks/useToastNotification';

function MyComponent() {
  const toast = useToastNotification();

  const handleSuccess = () => {
    toast.success('Operation completed successfully!');
  };

  const handleError = () => {
    toast.error('Something went wrong!');
  };

  const handleWarning = () => {
    toast.warning('Please check your input.');
  };

  const handleInfo = () => {
    toast.info('New updates available.');
  };
}
```

### 4. **Skip Automatic Toast**

```typescript
// Skip automatic toast for specific requests
try {
  await api.get('/api/data', { skipToast: true });
} catch (error) {
  // Handle error manually
  toast.error('Custom error message');
}
```

## 🛡️ **Error Types Handled**

### 1. **HTTP Status Errors**

- **400**: Validation errors
- **401**: Unauthorized (handled by auth middleware)
- **403**: Forbidden
- **404**: Not found
- **409**: Conflict
- **422**: Validation errors
- **429**: Rate limit
- **500**: Server errors
- **502/503/504**: Service unavailable

### 2. **Network Errors**

- Network connection issues
- Request timeouts
- DNS resolution failures

### 3. **API Response Errors**

```typescript
// FastAPI format
{
  detail: 'Error message';
}

// Custom format
{
  message: 'Error message';
}
{
  error: 'Error message';
}
```

## 🎨 **Toast Types**

### 1. **Success Toast**

```typescript
toast.success('Operation completed successfully!');
```

- **Color**: Green
- **Icon**: CheckCircle
- **Duration**: 3 seconds

### 2. **Error Toast**

```typescript
toast.error('Something went wrong!');
```

- **Color**: Red
- **Icon**: AlertCircle
- **Duration**: 5 seconds

### 3. **Warning Toast**

```typescript
toast.warning('Please check your input.');
```

- **Color**: Yellow
- **Icon**: AlertTriangle
- **Duration**: 4 seconds

### 4. **Info Toast**

```typescript
toast.info('New updates available.');
```

- **Color**: Blue
- **Icon**: Info
- **Duration**: 3 seconds

## 🔧 **Configuration**

### 1. **Custom Duration**

```typescript
toast.success('Message', 5000); // 5 seconds
toast.error('Message', 10000); // 10 seconds
```

### 2. **Skip Toast for Specific Requests**

```typescript
await api.get('/api/data', { skipToast: true });
await api.post('/api/data', data, { skipToast: true });
```

### 3. **Global Toast Function**

```typescript
import { showSuccessToast, showWarningToast } from '@/lib/api';

// Use anywhere in the app
showSuccessToast('Success message');
showWarningToast('Warning message');
```

## 📱 **Toast UI Features**

### 1. **Animation**

- Slide in from right
- Fade in/out effects
- Smooth transitions

### 2. **Multiple Toasts**

- Stack vertically
- Auto-remove after duration
- Manual close button

### 3. **Responsive Design**

- Mobile-friendly
- Max width for readability
- Proper spacing

## 🚀 **Advanced Usage**

### 1. **Custom Error Messages**

```typescript
try {
  await api.post('/users', userData);
} catch (error) {
  if (error.response?.status === 409) {
    toast.error('User already exists with this email.');
  } else {
    // Default error handling
    throw error;
  }
}
```

### 2. **Conditional Toast**

```typescript
const handleSubmit = async data => {
  try {
    await api.post('/api/submit', data);
    toast.success('Data submitted successfully!');
  } catch (error) {
    // Error toast shown automatically
    // Additional handling if needed
    if (error.response?.status === 422) {
      // Handle validation errors specifically
    }
  }
};
```

### 3. **Toast in Services**

```typescript
import { BaseService } from '@/lib/api';
import { showSuccessToast } from '@/lib/api';

export class UserService extends BaseService {
  async updateProfile(data) {
    try {
      const response = await this.put('/profile', data);
      showSuccessToast('Profile updated successfully!');
      return response.data;
    } catch (error) {
      // Error toast shown automatically
      throw error;
    }
  }
}
```

## 🧪 **Testing**

### 1. **Test Different Error Types**

```typescript
// Test 404 error
await api.get('/non-existent-endpoint');

// Test validation error
await api.post('/auth/login', { email: 'invalid' });

// Test network error
await api.get('http://invalid-url.com/api/test');
```

### 2. **Test Toast Skipping**

```typescript
try {
  await api.get('/api/data', { skipToast: true });
} catch (error) {
  // No automatic toast, handle manually
  toast.error('Custom error message');
}
```

## 📊 **Best Practices**

### 1. **Error Message Guidelines**

- **Be specific**: "Email is already registered" vs "Error occurred"
- **Be helpful**: Provide guidance on how to fix
- **Be consistent**: Use same tone and style
- **Be concise**: Keep messages short and clear

### 2. **Toast Usage Guidelines**

- **Success**: For completed actions
- **Error**: For failed operations
- **Warning**: For potential issues
- **Info**: For general information

### 3. **Performance Considerations**

- Toast middleware runs automatically
- No performance impact for successful requests
- Minimal overhead for error handling

### 4. **Accessibility**

- Toast notifications are keyboard accessible
- Screen reader friendly
- High contrast colors
- Clear close buttons

## 🔍 **Debugging**

### 1. **Check Toast Provider**

```typescript
// Ensure ToastProvider is wrapped around your app
<ToastProvider>
  <App />
</ToastProvider>
```

### 2. **Check Middleware Order**

```typescript
// Toast middleware should run after auth middleware
this.addErrorMiddleware(authErrorMiddleware);
this.addErrorMiddleware(toastErrorMiddleware);
```

### 3. **Console Logs**

```typescript
// Check browser console for error logs
// Toast middleware logs errors to console
```

## 🎯 **Examples**

### **Complete Example**

```typescript
import React, { useState } from 'react';
import { useToastNotification } from '@/hooks/useToastNotification';
import { api } from '@/lib/api';

export function UserForm() {
  const [loading, setLoading] = useState(false);
  const toast = useToastNotification();

  const handleSubmit = async (formData) => {
    setLoading(true);
    try {
      await api.post('/users', formData);
      toast.success('User created successfully!');
    } catch (error) {
      // Error toast shown automatically
      console.log('Error details:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

Hệ thống error handling này cung cấp một cách nhất quán và user-friendly để xử lý các lỗi API và hiển thị thông báo cho người dùng.
