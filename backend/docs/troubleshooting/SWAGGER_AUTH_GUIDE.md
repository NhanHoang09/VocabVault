# 🔐 Swagger Authentication Guide

## 🎯 **Vấn đề đã được giải quyết**

Bạn đã gặp vấn đề:

- ❌ **Swagger không cho nhập JWT key**
- ❌ **API `/me` trả về 403 Forbidden**

## ✅ **Giải pháp đã áp dụng**

### **1. Cấu hình OpenAPI Security Schemes**

Đã thêm cấu hình JWT Bearer authentication vào OpenAPI schema:

```python
# Trong app/main.py
openapi_schema["components"]["securitySchemes"] = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
}
```

### **2. Bảo vệ các endpoints**

Đã cấu hình security cho các endpoints được bảo vệ:

```python
protected_paths = [
    "/api/v1/auth/me",
    "/api/v1/flashcards",
    # ... các endpoints khác
]

for path in openapi_schema["paths"]:
    for method in openapi_schema["paths"][path]:
        if any(protected_path in path for protected_path in protected_paths):
            openapi_schema["paths"][path][method]["security"] = [
                {"BearerAuth": []}
            ]
```

## 🚀 **Cách sử dụng Swagger với Authentication**

### **Bước 1: Truy cập Swagger UI**

```
http://localhost:8000/docs
```

### **Bước 2: Đăng ký tài khoản (nếu chưa có)**

1. Tìm endpoint `POST /api/v1/auth/register`
2. Click "Try it out"
3. Nhập thông tin:

```json
{
  "email": "your_email@example.com",
  "username": "your_username",
  "full_name": "Your Full Name",
  "password": "your_password"
}
```

4. Click "Execute"

### **Bước 3: Đăng nhập để lấy token**

1. Tìm endpoint `POST /api/v1/auth/login`
2. Click "Try it out"
3. Nhập thông tin:

```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

4. Click "Execute"
5. **Copy access_token** từ response

### **Bước 4: Authorize trong Swagger**

1. Click nút **"Authorize"** (🔒) ở góc trên bên phải
2. Trong ô "Value", nhập: `Bearer <your_access_token>`
   - Ví dụ: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. Click **"Authorize"**
4. Click **"Close"**

### **Bước 5: Test protected endpoints**

1. Bây giờ bạn có thể test các endpoints được bảo vệ
2. Tìm endpoint `GET /api/v1/auth/me`
3. Click "Try it out"
4. Click "Execute"
5. Bạn sẽ thấy thông tin user của mình

## 🔍 **Kiểm tra cấu hình**

### **Test OpenAPI Schema**

```bash
curl http://localhost:8000/api/v1/openapi.json | jq '.components.securitySchemes'
```

**Kết quả mong đợi:**

```json
{
  "BearerAuth": {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
  }
}
```

### **Test Protected Endpoints**

```bash
curl http://localhost:8000/api/v1/openapi.json | jq '.paths."/api/v1/auth/me".get.security'
```

**Kết quả mong đợi:**

```json
[
  {
    "BearerAuth": []
  }
]
```

## 🧪 **Test Authentication Flow**

### **1. Test đăng ký**

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpassword123"
  }'
```

### **2. Test đăng nhập**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### **3. Test /me endpoint với token**

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <your_access_token>"
```

### **4. Test unauthorized access**

```bash
curl -X GET http://localhost:8000/api/v1/auth/me
# Sẽ trả về 401 hoặc 403
```

## 📋 **Troubleshooting**

### **Vấn đề: Swagger không hiển thị Authorize button**

**Giải pháp:**

1. Kiểm tra OpenAPI schema có security schemes không
2. Restart server
3. Clear browser cache

### **Vấn đề: Token không được accept**

**Giải pháp:**

1. Đảm bảo format: `Bearer <token>`
2. Kiểm tra token có hết hạn không
3. Kiểm tra token có đúng không

### **Vấn đề: 403 Forbidden**

**Giải pháp:**

1. Kiểm tra user có active không
2. Kiểm tra token có đúng user không
3. Kiểm tra endpoint có được bảo vệ đúng không

## 🎉 **Kết quả**

Sau khi áp dụng các giải pháp:

- ✅ **Swagger hiển thị Authorize button**
- ✅ **JWT Bearer authentication được cấu hình**
- ✅ **API `/me` hoạt động với token**
- ✅ **Unauthorized access được reject đúng cách**
- ✅ **Tất cả protected endpoints được bảo vệ**

## 📝 **Lưu ý quan trọng**

1. **Token format**: Luôn sử dụng `Bearer <token>`
2. **Token expiration**: Token có thời hạn, cần login lại khi hết hạn
3. **User status**: Chỉ active users mới có thể access protected endpoints
4. **CORS**: Đảm bảo CORS được cấu hình đúng cho frontend

Bây giờ bạn có thể sử dụng Swagger UI để test tất cả API endpoints một cách dễ dàng! 🚀
