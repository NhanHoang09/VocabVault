# 🔐 Authentication API Documentation

## 🎯 Tổng quan

Authentication module cung cấp **4 endpoints** để quản lý đăng ký, đăng nhập, và xác thực người dùng. Module này sử dụng JWT (JSON Web Tokens) cho xác thực và bảo mật.

**Base URL**: `/api/v1/auth`

---

## 📋 Danh sách Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register` | ❌ | Đăng ký tài khoản mới |
| `POST` | `/login` | ❌ | Đăng nhập và lấy access token |
| `GET` | `/me` | ✅ | Lấy thông tin user hiện tại |
| `POST` | `/refresh` | ✅ | Làm mới access token |
| `POST` | `/debug-token` | ❌ | Debug JWT token (troubleshooting) |

---

## 🔐 AUTHENTICATION ENDPOINTS

### 1. POST `/api/v1/auth/register` - Đăng ký tài khoản mới

**🎯 Mục đích**: Tạo tài khoản người dùng mới

**🔑 Authentication**: Không cần (public endpoint)

**📝 Request Body**:
```json
{
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "password": "password123"
}
```

**📋 Field Descriptions**:
- `email` (required): Email của user (phải unique)
- `username` (required): Username (phải unique)
- `full_name` (optional): Tên đầy đủ
- `password` (required): Mật khẩu (tối thiểu 6 ký tự)

**✅ Response (201 Created)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**❌ Error Responses**:
- `400 Bad Request`: User đã tồn tại
- `422 Validation Error`: Dữ liệu không hợp lệ

---

### 2. POST `/api/v1/auth/login` - Đăng nhập

**🎯 Mục đích**: Xác thực user và trả về access token

**🔑 Authentication**: Không cần (public endpoint)

**📝 Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**📋 Field Descriptions**:
- `email` (required): Email của user
- `password` (required): Mật khẩu

**✅ Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**❌ Error Responses**:
- `401 Unauthorized`: Email hoặc password sai
- `400 Bad Request`: User không active
- `422 Validation Error`: Dữ liệu không hợp lệ

---

### 3. GET `/api/v1/auth/me` - Lấy thông tin user hiện tại

**🎯 Mục đích**: Lấy thông tin chi tiết của user đang đăng nhập

**🔑 Authentication**: Required (JWT token)

**📝 Headers**:
```
Authorization: Bearer <your_access_token>
```

**✅ Response (200 OK)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**❌ Error Responses**:
- `401 Unauthorized`: Token không hợp lệ hoặc hết hạn

---

### 4. POST `/api/v1/auth/refresh` - Làm mới access token

**🎯 Mục đích**: Tạo access token mới cho user hiện tại

**🔑 Authentication**: Required (JWT token)

**📝 Headers**:
```
Authorization: Bearer <your_access_token>
```

**✅ Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**❌ Error Responses**:
- `401 Unauthorized`: Token không hợp lệ hoặc hết hạn

---

### 5. POST `/api/v1/auth/debug-token` - Debug JWT token

**🎯 Mục đích**: Phân tích và debug JWT token (cho troubleshooting)

**🔑 Authentication**: Không cần (public endpoint)

**📝 Request Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**📋 Field Descriptions**:
- `token` (required): JWT token cần debug

**✅ Response (200 OK)**:
```json
{
  "token_format": "valid",
  "payload": {
    "sub": "1",
    "exp": 1705312200,
    "iat": 1705308600
  },
  "expiration_info": {
    "expiration": "2024-01-15T11:30:00",
    "current_time": "2024-01-15T10:30:00",
    "is_expired": false
  },
  "verification_result": "success",
  "token_length": 200
}
```

**❌ Error Responses**:
- `400 Bad Request`: Token không được cung cấp
- `200 OK` với error info: Token format không hợp lệ

---

## 🔑 AUTHENTICATION & AUTHORIZATION

### **JWT Token Format**:
```
Authorization: Bearer <your_access_token>
```

### **Token Structure**:
- **Header**: Algorithm và token type
- **Payload**: User ID, expiration time, issued time
- **Signature**: Được ký bằng secret key

### **Token Expiration**:
- **Access Token**: 30 phút (có thể cấu hình)
- **Refresh**: Sử dụng endpoint `/refresh` để lấy token mới

### **Security Features**:
- ✅ **JWT-based authentication**
- ✅ **Token expiration**
- ✅ **Password hashing** (bcrypt)
- ✅ **Input validation**
- ✅ **Rate limiting** (planned)
- ✅ **CORS protection**

---

## 📊 RESPONSE MODELS

### UserResponse
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### TokenResponse
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## 🎯 TÍNH NĂNG NỔI BẬT

- ✅ **JWT Authentication**: Xác thực an toàn với JWT tokens
- ✅ **User Registration**: Đăng ký tài khoản với validation
- ✅ **Secure Login**: Đăng nhập với password hashing
- ✅ **Token Refresh**: Làm mới token tự động
- ✅ **User Profile**: Quản lý thông tin user
- ✅ **Debug Tools**: Debug token cho troubleshooting
- ✅ **Input Validation**: Kiểm tra dữ liệu đầu vào
- ✅ **Error Handling**: Xử lý lỗi chi tiết
- ✅ **Security**: Bảo mật cao với bcrypt và JWT

---

## 🚀 EXAMPLES

### Đăng ký tài khoản mới
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "full_name": "Full Name",
    "password": "password123"
  }'
```

### Đăng nhập
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Lấy thông tin user
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <your_access_token>"
```

### Làm mới token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Authorization: Bearer <your_access_token>"
```

### Debug token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/debug-token" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

## 🔧 ERROR HANDLING

### Common Error Responses

**400 Bad Request**:
```json
{
  "detail": "User already exists"
}
```

**401 Unauthorized**:
```json
{
  "detail": "Incorrect email or password"
}
```

**422 Validation Error**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🔒 SECURITY CONSIDERATIONS

### Password Requirements
- Tối thiểu 6 ký tự
- Được hash bằng bcrypt
- Không lưu plain text

### Token Security
- JWT tokens có expiration time
- Secret key được bảo vệ
- Tokens được verify signature

### Best Practices
- Luôn sử dụng HTTPS trong production
- Không lưu tokens trong localStorage
- Implement token refresh logic
- Validate tất cả input data

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Module**: Authentication API
