# 🔐 Token Storage Strategy - Optimal & Secure Implementation

## 📋 Tổng quan

Phương án lưu trữ token tối ưu và an toàn cho My Vocabulary Vault, kết hợp giữa RAM storage và HttpOnly cookies.

## 🎯 Phương án được chọn

### **1. Access Token: Lưu trong RAM (Zustand State)**

- ✅ **Chỉ sống trong memory** - Không persistent
- ✅ **Tự động mất khi reload** - Bảo mật cao
- ✅ **Fast access** - Performance tốt
- ✅ **Không thể bị XSS** - An toàn

### **2. Refresh Token: HttpOnly Cookie (Backend)**

- ✅ **HttpOnly cookie** - Không thể truy cập từ JavaScript
- ✅ **Secure flag** - Chỉ gửi qua HTTPS
- ✅ **SameSite=Strict** - Chống CSRF
- ✅ **Auto gửi với requests** - Tiện lợi

## 🔄 Flow hoạt động

### **Login Flow:**

```
1. User login → Backend xác thực
2. Backend trả về:
   - access_token (JSON response)
   - refresh_token (HttpOnly cookie)
3. Frontend lưu access_token vào Zustand (RAM)
4. User được chuyển đến dashboard
```

### **API Request Flow:**

```
1. Frontend gọi API với access_token từ Zustand
2. Axios interceptor tự động attach token
3. Backend xác thực và trả response
```

### **Token Refresh Flow:**

```
1. API trả về 401 Unauthorized
2. Axios interceptor catch error
3. Gọi /auth/refresh (cookie tự động gửi)
4. Nhận access_token mới
5. Update Zustand state
6. Retry original request
```

### **Logout Flow:**

```
1. Frontend gọi /auth/logout
2. Backend clear refresh_token cookie
3. Frontend clear access_token khỏi Zustand
4. Redirect to login page
```

## 🏗️ Kiến trúc Implementation

### **Backend Components:**

- `SecurityManager` - Tạo và verify tokens
- `AuthService` - Xử lý authentication logic
- `AuthAPI` - Endpoints với cookie handling

### **Frontend Components:**

- `Zustand Store` - Quản lý access token trong RAM
- `API Client` - Axios với auto refresh
- `Auth Hooks` - React hooks cho auth state

## 🔧 Technical Details

### **Token Configuration:**

- **Access Token**: 30 phút expiration
- **Refresh Token**: 7 ngày expiration
- **Cookie Path**: `/auth/refresh` (chỉ cho refresh endpoint)

### **Security Headers:**

- `HttpOnly: true` - Không thể access từ JavaScript
- `Secure: true` - Chỉ gửi qua HTTPS
- `SameSite: Strict` - Chống CSRF attacks

### **Error Handling:**

- 401 Unauthorized → Auto refresh
- Refresh failed → Logout user
- Network errors → Retry logic

## 📊 So sánh với các phương án khác

| Tiêu chí            | LocalStorage | HttpOnly Cookies | RAM + Cookies | SessionStorage |
| ------------------- | ------------ | ---------------- | ------------- | -------------- |
| **Bảo mật**         | ❌ Thấp      | ✅ Cao           | ✅ Cao nhất   | ✅ Cao         |
| **UX**              | ✅ Tốt       | ✅ Tốt           | ✅ Tốt        | ❌ Kém         |
| **Cross-tab**       | ✅ Có        | ✅ Có            | ✅ Có         | ❌ Không       |
| **Persistent**      | ✅ Có        | ✅ Có            | ❌ Không      | ❌ Không       |
| **XSS Protection**  | ❌ Không     | ✅ Có            | ✅ Có         | ✅ Có          |
| **CSRF Protection** | ❌ Không     | ✅ Có            | ✅ Có         | ❌ Không       |

## 🚀 Implementation Steps

### **Phase 1: Backend Setup**

1. Update SecurityManager với refresh token methods
2. Modify login endpoint để set HttpOnly cookie
3. Create refresh endpoint
4. Update logout endpoint để clear cookie
5. Test endpoints với Postman

### **Phase 2: Frontend Setup**

1. Update Zustand store với access token
2. Modify API client với auto refresh
3. Update auth hooks
4. Test login/logout flow
5. Test token refresh

### **Phase 3: Integration & Testing**

1. End-to-end testing
2. Security testing
3. Performance testing
4. Cross-browser testing
5. Production deployment

## 🔍 Testing Checklist

### **Security Tests:**

- [ ] XSS protection (không thể access token từ console)
- [ ] CSRF protection (SameSite cookie)
- [ ] Token expiration handling
- [ ] Refresh token rotation
- [ ] Secure cookie flags

### **Functionality Tests:**

- [ ] Login flow
- [ ] Logout flow
- [ ] Auto refresh on 401
- [ ] Cross-tab session sharing
- [ ] Network error handling

### **Performance Tests:**

- [ ] Token access speed
- [ ] Refresh latency
- [ ] Memory usage
- [ ] Network requests optimization

## 📝 Code Examples

### **Backend Login Endpoint:**

```python
@router.post("/login")
def login(user_data: UserLogin):
    # ... authentication logic

    response = JSONResponse(content={
        "access_token": access_token,
        "user": user_data
    })

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7*24*60*60,
        path="/auth/refresh"
    )

    return response
```

### **Frontend Zustand Store:**

```typescript
export const useAuthStore = create<AuthStore>(set => ({
  accessToken: null, // Chỉ trong RAM
  user: null,
  isAuthenticated: false,

  login: async credentials => {
    const response = await authApi.login(credentials);
    set({
      accessToken: response.access_token,
      user: response.user,
      isAuthenticated: true,
    });
  },

  logout: async () => {
    await authApi.logout();
    set({
      accessToken: null,
      user: null,
      isAuthenticated: false,
    });
  },
}));
```

### **Axios Interceptor:**

```typescript
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      try {
        const response = await axios.post(
          '/auth/refresh',
          {},
          {
            withCredentials: true,
          }
        );

        useAuthStore.getState().setAccessToken(response.data.access_token);
        return apiClient(error.config);
      } catch {
        useAuthStore.getState().logout();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

## 🎯 Kết luận

Phương án **RAM + HttpOnly Cookies** cung cấp:

- **Bảo mật cao nhất** với XSS và CSRF protection
- **UX tốt** với seamless auto refresh
- **Performance tối ưu** với RAM storage
- **Maintainability** với clean architecture

Đây là phương án được khuyến nghị cho production environments.
