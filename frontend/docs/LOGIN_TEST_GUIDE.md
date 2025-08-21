# 🧪 Login Test Guide

## ✅ Login Form đã được kết nối với Auth System!

### **🔧 Test Credentials:**

**Test User 1:**

- Email: `john.doe@example.com`
- Password: `password123`

**Test User 2:**

- Email: `jane.smith@example.com`
- Password: `password123`

**Admin User:**

- Email: `admin@vocabularyvault.com`
- Password: `admin123`

### **🧪 Test Login Flow:**

#### **Bước 1: Truy cập Login Page**

```
http://localhost:3000/login
```

#### **Bước 2: Test Validation**

- **Email không hợp lệ**: Nhập email sai format
- **Password quá ngắn**: Nhập password < 8 ký tự
- **Field trống**: Để trống email hoặc password

#### **Bước 3: Test Login Success**

1. Nhập email hợp lệ: `john.doe@example.com`
2. Nhập password hợp lệ: `password123`
3. Click "Đăng nhập"
4. Kiểm tra:
   - ✅ Redirect đến `/dashboard`
   - ✅ Hiển thị thông tin user
   - ✅ Không bị redirect về login

#### **Bước 4: Test Login Error**

1. Nhập email/password sai
2. Click "Đăng nhập"
3. Kiểm tra:
   - ✅ Error message hiển thị
   - ✅ Form không reset
   - ✅ Loading state clear

### **🔍 Token Storage Verification:**

#### **Access Token (RAM):**

```javascript
// Mở DevTools Console
// Kiểm tra Zustand store
const { useAuthStore } = require('@/features/auth/store/auth.store');
const token = useAuthStore.getState().accessToken;
console.log('Access Token:', token ? '✅ Có token' : '❌ Không có token');
```

#### **Refresh Token (Cookie):**

```javascript
// Kiểm tra cookies
document.cookie;
// ❌ Không nên thấy refresh_token (HttpOnly)

// Kiểm tra localStorage
localStorage.getItem('access_token');
// ❌ Nên trả về null (an toàn)
```

#### **Network Requests:**

1. Mở DevTools → Network tab
2. Login → Xem request `/api/v1/auth/login`
3. Kiểm tra:
   - ✅ Response có `access_token`
   - ✅ Response headers có `Set-Cookie: refresh_token`
   - ✅ Status 200 OK

### **🔄 Auto Refresh Test:**

#### **Bước 1: Login thành công**

#### **Bước 2: Đợi access token hết hạn (30 phút)**

#### **Bước 3: Gọi API bất kỳ**

#### **Bước 4: Kiểm tra:**

- ✅ Tự động gọi `/api/v1/auth/refresh`
- ✅ Nhận access token mới
- ✅ Retry original request
- ✅ User không bị logout

### **🚪 Logout Test:**

#### **Bước 1: Login thành công**

#### **Bước 2: Click logout**

#### **Bước 3: Kiểm tra:**

- ✅ Redirect về home page
- ✅ Access token bị clear khỏi Zustand
- ✅ Refresh token cookie bị clear
- ✅ User state reset

### **📱 Cross-tab Test:**

#### **Bước 1: Login ở tab 1**

#### **Bước 2: Mở tab 2**

#### **Bước 3: Kiểm tra:**

- ✅ User vẫn authenticated
- ✅ Có thể sử dụng app
- ✅ Không bị redirect về login

### **🔄 Page Reload Test:**

#### **Bước 1: Login thành công**

#### **Bước 2: Reload page (F5)**

#### **Bước 3: Kiểm tra:**

- ✅ Vẫn ở dashboard
- ✅ User info vẫn hiển thị
- ✅ Token được auto refresh

### **🔒 Security Tests:**

#### **XSS Protection:**

```javascript
// Thử access token từ console
localStorage.getItem('access_token');
// ❌ Nên trả về null

document.cookie;
// ❌ Không nên thấy refresh_token
```

#### **CSRF Protection:**

- ✅ SameSite=Strict cookie
- ✅ Token rotation

### **📊 Expected Results:**

#### **Login Success:**

- ✅ Form validation pass
- ✅ API call thành công
- ✅ Redirect to dashboard
- ✅ User info displayed
- ✅ Token stored correctly

#### **Login Error:**

- ✅ Error message hiển thị
- ✅ Form không reset
- ✅ Loading state clear

#### **Auto Refresh:**

- ✅ Seamless experience
- ✅ No user interruption
- ✅ Token auto renewal

### **🐛 Troubleshooting:**

#### **Lỗi "Request failed with status code 404"**

- Kiểm tra API endpoint: `/api/v1/auth/login`
- Kiểm tra backend có chạy không: `http://localhost:8000/health`
- Kiểm tra CORS settings

#### **Lỗi "Request failed with status code 500"**

- Kiểm tra backend logs
- Kiểm tra database connection
- Kiểm tra test user có tồn tại không

#### **Lỗi "Token not found"**

- Kiểm tra Zustand store
- Kiểm tra API response format
- Kiểm tra import paths

### **🎯 Next Steps:**

1. **Test Register Flow** → Dashboard
2. **Test API Integration** với backend
3. **Test Error Handling**
4. **Performance Testing**
5. **Security Audit**

### **📚 Related Documentation:**

- **Token Strategy**: `frontend/docs/TOKEN_STORAGE_STRATEGY.md`
- **Dashboard Testing**: `frontend/docs/DASHBOARD_TEST_GUIDE.md`
- **API Documentation**: `http://localhost:8000/docs`

### **🔧 Development Commands:**

```bash
# Start frontend
cd frontend && npm run dev

# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Test build
cd frontend && npm run build
```

### **📝 Notes:**

- Login form sử dụng **Zod validation**
- Token storage: **RAM + HttpOnly Cookies**
- Auto refresh: **Seamless experience**
- Security: **XSS + CSRF protection**
- UX: **Loading states + Error handling**
