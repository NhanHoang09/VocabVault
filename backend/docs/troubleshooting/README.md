# 🔍 Troubleshooting Documentation

## 📋 Tổng quan

Thư mục này chứa các hướng dẫn troubleshooting và giải quyết lỗi thường gặp trong dự án.

## 📁 Files

### 🔐 **Authentication Issues**
- [`AUTH_ISSUE_ANALYSIS.md`](./AUTH_ISSUE_ANALYSIS.md) - Phân tích và giải quyết lỗi authentication

### 📡 **Swagger/API Issues**
- [`SWAGGER_AUTH_GUIDE.md`](./SWAGGER_AUTH_GUIDE.md) - Hướng dẫn authentication trong Swagger
- [`SWAGGER_ISSUE_SOLVED.md`](./SWAGGER_ISSUE_SOLVED.md) - Giải quyết lỗi Swagger
- [`SWAGGER_TROUBLESHOOTING.md`](./SWAGGER_TROUBLESHOOTING.md) - Troubleshooting Swagger chi tiết

## 🚨 Common Issues

### 🔐 **Authentication Problems**
1. **JWT Token Issues**
   - Token expired
   - Invalid token format
   - Missing authorization header

2. **User Registration/Login**
   - Email already exists
   - Invalid credentials
   - Account not activated

### 📡 **API Issues**
1. **Swagger Documentation**
   - Authentication not working
   - Endpoints not showing
   - CORS errors

2. **Database Issues**
   - Connection errors
   - Migration problems
   - Foreign key constraints

## 🔧 Quick Fixes

### JWT Token Issues
```bash
# Check token format
curl -X POST "http://localhost:8000/api/v1/auth/debug-token" \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token_here"}'
```

### Database Migration Issues
```bash
# Reset database
alembic downgrade base
alembic upgrade head
```

### Swagger Issues
```bash
# Check if server is running
curl http://localhost:8000/docs
```

## 📞 Support

Nếu gặp vấn đề không có trong documentation:

1. **Check logs**: `tail -f backend/server.log`
2. **Database status**: `./backend/status.sh`
3. **Create issue**: GitHub repository
4. **Contact team**: Development team

---

**Last Updated**: January 2024  
**Status**: Active Maintenance 🔧
