# 🎯 Dashboard Test Guide

## ✅ Dashboard đã được tạo thành công!

### **Tính năng Dashboard:**

1. **Protected Route**: Chỉ user đã đăng nhập mới truy cập được
2. **User Info Display**: Hiển thị thông tin user
3. **Token Testing Tools**: Các button để test token storage
4. **Logout Functionality**: Test logout flow
5. **Security Verification**: Kiểm tra bảo mật token

## 🧪 Test Login → Dashboard Flow

### **Bước 1: Truy cập Login Page**

```
http://localhost:3000/login
```

### **Bước 2: Đăng nhập**

1. Nhập email: `test@example.com`
2. Nhập password: `password123`
3. Click "Đăng nhập"

### **Bước 3: Kiểm tra Redirect**

- ✅ Tự động chuyển đến `/dashboard`
- ✅ Hiển thị thông tin user
- ✅ Không bị redirect về login

## 🔍 Test Dashboard Features

### **1. User Information Display**

- ✅ Username hiển thị đúng
- ✅ Email hiển thị đúng
- ✅ User ID hiển thị đúng
- ✅ Trạng thái "Đã đăng nhập"

### **2. Token Security Tests**

#### **Test Access Token (RAM):**

```javascript
// Click button "🔍 Kiểm tra Token"
// Kết quả mong đợi: "✅ Access token có sẵn trong RAM"
```

#### **Test localStorage Security:**

```javascript
// Click button "🔒 Kiểm tra localStorage"
// Kết quả mong đợi: "✅ Token không có trong localStorage (an toàn)"
```

#### **Test Console Access:**

```javascript
// Mở DevTools Console
console.log(localStorage.getItem('access_token'));
// Kết quả mong đợi: null

// Kiểm tra cookies
document.cookie;
// Kết quả mong đợi: Không thấy refresh_token (HttpOnly)
```

### **3. Network Requests**

1. Mở DevTools → Network tab
2. Login → Xem request `/auth/login`
3. Kiểm tra:
   - ✅ Response có `access_token`
   - ✅ Response headers có `Set-Cookie: refresh_token`
   - ✅ Status 200 OK

### **4. Logout Test**

1. Click button "🚪 Đăng xuất"
2. Kiểm tra:
   - ✅ Redirect về home page
   - ✅ Access token bị clear khỏi RAM
   - ✅ Refresh token cookie bị clear
   - ✅ User state reset

## 🔒 Security Verification

### **XSS Protection:**

```javascript
// Thử access token từ console
localStorage.getItem('access_token');
// ❌ Nên trả về null

document.cookie;
// ❌ Không nên thấy refresh_token
```

### **CSRF Protection:**

- ✅ SameSite=Strict cookie
- ✅ Token rotation

### **Token Storage:**

- ✅ Access token chỉ trong RAM
- ✅ Refresh token trong HttpOnly cookie
- ✅ Không persistent storage

## 🚀 Test Auto Refresh

### **Bước 1: Login thành công**

### **Bước 2: Mở DevTools → Network tab**

### **Bước 3: Gọi API bất kỳ (nếu có)**

### **Bước 4: Kiểm tra:**

- ✅ Tự động gọi `/auth/refresh` khi 401
- ✅ Nhận access token mới
- ✅ Retry original request
- ✅ User không bị logout

## 📱 Test Cross-tab

### **Bước 1: Login ở tab 1**

### **Bước 2: Mở tab 2 → truy cập `/dashboard`**

### **Bước 3: Kiểm tra:**

- ✅ User vẫn authenticated
- ✅ Dashboard hiển thị bình thường
- ✅ Không bị redirect về login

## 🔄 Test Page Reload

### **Bước 1: Login thành công**

### **Bước 2: Reload page (F5)**

### **Bước 3: Kiểm tra:**

- ✅ Vẫn ở dashboard
- ✅ User info vẫn hiển thị
- ✅ Token được auto refresh

## 🐛 Troubleshooting

### **Lỗi "Cannot access dashboard"**

- Kiểm tra backend API có hoạt động không
- Kiểm tra CORS settings
- Kiểm tra network requests

### **Lỗi "Token not found"**

- Kiểm tra Zustand store
- Kiểm tra API response format
- Kiểm tra import paths

### **Lỗi "Redirect loop"**

- Kiểm tra ProtectedRoute component
- Kiểm tra auth state management
- Kiểm tra route configuration

## 📊 Expected Results

### **Login Success:**

- ✅ Form validation pass
- ✅ API call thành công
- ✅ Redirect to dashboard
- ✅ User info displayed
- ✅ Token stored correctly

### **Dashboard Access:**

- ✅ Protected route working
- ✅ User info displayed
- ✅ Token tests working
- ✅ Logout working

### **Security:**

- ✅ No token in localStorage
- ✅ HttpOnly cookies working
- ✅ XSS protection active
- ✅ CSRF protection active

## 🎯 Next Steps

1. **Test Register Flow** → Dashboard
2. **Test API Integration** với backend
3. **Test Error Handling**
4. **Performance Testing**
5. **Mobile Responsiveness**
6. **Accessibility Testing**

## 🔧 Development Commands

```bash
# Start frontend
cd frontend
npm run dev

# Start backend (if needed)
cd backend
uvicorn app.main:app --reload

# Test build
npm run build
```

## 📝 Notes

- Dashboard sử dụng **ProtectedRoute** component
- Token storage: **RAM + HttpOnly Cookies**
- Auto refresh: **Seamless experience**
- Security: **XSS + CSRF protection**
- UX: **Loading states + Error handling**
