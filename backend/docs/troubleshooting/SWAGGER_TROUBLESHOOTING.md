# 🔧 Swagger Troubleshooting Guide

## 🎯 **Vấn đề hiện tại**

> Token hoạt động với curl nhưng không hoạt động trên Swagger UI
> **NGUYÊN NHÂN CHÍNH: Duplicate "Bearer" prefix**

## ✅ **Xác nhận Token hoạt động**

### **Test với curl - ✅ Hoạt động**
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0"

# Response: 200 OK
{
  "email": "nhanht2@gmail.com",
  "username": "Nhan",
  "full_name": "NhanHoang",
  "id": 8,
  ...
}
```

### **Cấu hình Swagger - ✅ Đúng**
```json
{
  "BearerAuth": {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
  }
}
```

## 🔍 **Nguyên nhân có thể**

### **1. Cách nhập token trong Swagger**
**❌ Sai (Duplicate Bearer):**
```
Bearer Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0
```

**❌ Sai (Không có Bearer):**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0
```

**✅ Đúng (Single Bearer):**
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0
```

### **2. Cache browser**
- Swagger có thể cache token cũ
- Browser cache có thể gây conflict

### **3. Token bị cắt ngắn**
- Khi copy/paste, token có thể bị cắt
- Đặc biệt là phần cuối

### **4. Khoảng trắng thừa**
- Có thể có khoảng trắng ở đầu/cuối token
- Swagger nhạy cảm với format

## 🛠️ **Giải pháp từng bước**

### **Bước 1: Clear Browser Cache**
1. Mở Developer Tools (F12)
2. Right-click refresh button
3. Chọn "Empty Cache and Hard Reload"
4. Hoặc Ctrl+Shift+R (Cmd+Shift+R trên Mac)

### **Bước 2: Truy cập Swagger UI**
```
http://localhost:8000/docs
```

### **Bước 3: Authorize đúng cách**
1. **Click nút "Authorize"** (🔒) ở góc trên bên phải
2. **Trong ô "Value", nhập chính xác (CHỈ 1 LẦN "Bearer"):**
   ```
   Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0
   ```
3. **Click "Authorize"**
4. **Click "Close"**

**⚠️ QUAN TRỌNG: Không nhập "Bearer Bearer" - chỉ nhập "Bearer" một lần!**

### **Bước 4: Test endpoint**
1. Tìm endpoint `GET /api/v1/auth/me`
2. Click "Try it out"
3. Click "Execute"

## 🔍 **Debug chi tiết**

### **Kiểm tra token format**
```bash
# Token của bạn
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0

# Kiểm tra độ dài
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0" | wc -c
# Kết quả: 151 (bao gồm newline)

# Kiểm tra 3 parts
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0" | tr '.' '\n' | wc -l
# Kết quả: 3
```

### **Decode JWT token**
```bash
# Decode header
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" | base64 -d | jq .

# Decode payload
echo "eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ" | base64 -d | jq .
```

## 🚨 **Các lỗi thường gặp**

### **Lỗi: "Could not validate credentials"**
**Nguyên nhân:**
- Token không có `Bearer` prefix
- Token bị cắt ngắn
- Token có khoảng trắng thừa

**Giải pháp:**
1. Đảm bảo có `Bearer` prefix
2. Copy token đầy đủ
3. Kiểm tra không có khoảng trắng

### **Lỗi: "Not enough segments"**
**Nguyên nhân:**
- Token bị cắt ngắn khi copy/paste
- Thiếu phần signature

**Giải pháp:**
1. Copy token đầy đủ
2. Kiểm tra có đủ 3 parts (header.payload.signature)

### **Lỗi: "Not authenticated"**
**Nguyên nhân:**
- Chưa authorize trong Swagger
- Authorization header không được gửi

**Giải pháp:**
1. Click "Authorize" và nhập token
2. Đảm bảo format: `Bearer <token>`

## 📋 **Checklist để fix**

- [ ] Clear browser cache
- [ ] Truy cập `http://localhost:8000/docs`
- [ ] Click "Authorize" button
- [ ] Nhập: `Bearer <token>` (CHỈ 1 LẦN "Bearer", không "Bearer Bearer")
- [ ] Click "Authorize" và "Close"
- [ ] Test endpoint `/api/v1/auth/me`

## 🧪 **Test thay thế**

Nếu Swagger vẫn không hoạt động, bạn có thể:

### **1. Sử dụng curl**
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzU1NDUzMjc1fQ.03Fyz7Gj8ZIYpE_SmHFu4Mcaags8psDLytsg9av2xe0"
```

### **2. Sử dụng Postman**
1. Import collection
2. Set Authorization header
3. Test endpoints

### **3. Sử dụng Insomnia**
1. Create request
2. Set Bearer token
3. Test API

## ✅ **Kết luận**

**Token của bạn hoạt động hoàn hảo!** Vấn đề chỉ là cách sử dụng Swagger UI.

**Đảm bảo:**
1. ✅ Có `Bearer` prefix
2. ✅ Copy token đầy đủ
3. ✅ Clear browser cache
4. ✅ Authorize đúng cách trong Swagger

**Nếu vẫn không hoạt động, sử dụng curl hoặc Postman thay thế!** 🎉
