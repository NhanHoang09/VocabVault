# 🚀 Getting Started - My Vocabulary Vault Backend

## 📋 **Prerequisites**

Trước khi bắt đầu, hãy đảm bảo bạn có:

- **Python 3.8+** installed
- **Docker & Docker Compose** installed
- **Git** installed
- **Terminal/Command Prompt** access

## 🛠️ **Step-by-Step Setup Guide**

### **Step 1: Clone và Setup Project**

```bash
# 1. Clone repository (nếu chưa có)
git clone <repository-url>
cd "My Vocabulary Vault/backend"

# 2. Kiểm tra cấu trúc thư mục
ls -la
```

**Expected output:**
```
README-Getting-Started.md
README-Module-Structure.md
README-Docker.md
requirements.txt
docker-compose.dev.yml
.env
app/
alembic/
scripts/
```

### **Step 2: Setup Environment Variables**

```bash
# 1. Copy environment template
cp env.example .env

# 2. Kiểm tra file .env đã có
cat .env
```

**Expected content:**
```env
# Database Configuration for Docker
DATABASE_URL=postgresql://vocabulary_user:vocabulary_password@localhost:5432/vocabulary_vault

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration for Docker
REDIS_URL=redis://localhost:6379

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your-openai-api-key-here

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]

# App Configuration
APP_NAME=My Vocabulary Vault
APP_VERSION=1.0.0
DEBUG=true
```

### **Step 3: Setup Python Virtual Environment**

```bash
# 1. Tạo virtual environment
python -m venv venv

# 2. Kích hoạt virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Kiểm tra installation
python -c "import fastapi, sqlalchemy, alembic; print('✅ Dependencies installed successfully')"
```

### **Step 4: Start Docker Services**

```bash
# 1. Kiểm tra Docker đang chạy
docker --version
docker-compose --version

# 2. Start Docker services
./scripts/docker-commands.sh start

# 3. Kiểm tra services đang chạy
./scripts/docker-commands.sh status
```

**Expected output:**
```
================================
 Docker Services Status
================================
NAME                           STATUS             PORTS
vocabulary_vault_db_dev        Up                0.0.0.0:5432->5432/tcp
vocabulary_vault_redis_dev     Up                0.0.0.0:6379->6379/tcp
vocabulary_vault_pgadmin_dev   Up                0.0.0.0:5050->80/tcp
```

### **Step 5: Test Database Connection**

```bash
# 1. Test kết nối database
python scripts/test-db-connection.py
```

**Expected output:**
```
🚀 My Vocabulary Vault - Database Connection Test
==================================================
🔍 Testing database connection...
✅ Database connection successful!
📊 PostgreSQL version: PostgreSQL 15.14
🗄️  Connected to database: vocabulary_vault
📋 Found 14 tables
🔍 Testing Redis connection...
✅ Redis connection successful!
==================================================
✅ Database connection test passed!
✅ Redis connection test passed!
```

### **Step 6: Run Database Migrations**

```bash
# 1. Chạy migrations
./scripts/docker-commands.sh migrate

# 2. Kiểm tra migration status
alembic current
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3e6164984888, initial migration
```

### **Step 7: Start Backend Server**

```bash
# 1. Đảm bảo virtual environment đang active
source venv/bin/activate

# 2. Start server
python run.py
```

**Expected output:**
```
INFO     Starting uvicorn server
INFO     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO     Starting reloader process
INFO     Started server process
INFO     Started reloader process
INFO     Application startup complete.
```

### **Step 8: Test API Endpoints**

```bash
# 1. Test health endpoint
curl http://localhost:8000/health

# 2. Test root endpoint
curl http://localhost:8000/

# 3. Mở Swagger UI trong browser
open http://localhost:8000/docs
```

**Expected responses:**
```json
// Health endpoint
{"status": "healthy"}

// Root endpoint
{
  "message": "Welcome to My Vocabulary Vault API",
  "version": "1.0.0",
  "architecture": "module-based",
  "docs": "/docs",
  "redoc": "/redoc",
  "health": "/health"
}
```

## 🎯 **Available Services**

| Service | URL | Description |
|---------|-----|-------------|
| **Backend API** | http://localhost:8000 | Main API server |
| **Swagger Docs** | http://localhost:8000/docs | **Interactive API documentation** |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |
| **Health Check** | http://localhost:8000/health | API health status |
| **PostgreSQL** | localhost:5432 | Database |
| **Redis** | localhost:6379 | Cache |
| **PgAdmin** | http://localhost:5050 | Database management |

## 🧪 **Testing the API**

### **1. Register a new user**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### **2. Login to get access token**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### **3. Use token for authenticated requests**
```bash
# Replace YOUR_TOKEN with the actual token from login response
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🛠️ **Development Commands**

### **Docker Management**
```bash
# Start services
./scripts/docker-commands.sh start

# Stop services
./scripts/docker-commands.sh stop

# Restart services
./scripts/docker-commands.sh restart

# View logs
./scripts/docker-commands.sh logs

# Check status
./scripts/docker-commands.sh status
```

### **Database Operations**
```bash
# Run migrations
./scripts/docker-commands.sh migrate

# Reset database
./scripts/docker-commands.sh reset

# Backup database
./scripts/docker-commands.sh backup

# Restore database
./scripts/docker-commands.sh restore
```

### **Application Development**
```bash
# Start server with auto-reload
python run.py

# Test database connection
python scripts/test-db-connection.py

# Run tests (when available)
pytest

# Format code
black app/

# Lint code
flake8 app/
```

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Port already in use**
```bash
# Check what's using the port
lsof -i :8000
# Kill the process
kill -9 <PID>
```

#### **2. Database connection failed**
```bash
# Check Docker services
./scripts/docker-commands.sh status

# Restart services
./scripts/docker-commands.sh restart

# Check database logs
./scripts/docker-commands.sh logs
```

#### **3. Migration errors**
```bash
# Reset database
./scripts/docker-commands.sh reset

# Run migrations again
./scripts/docker-commands.sh migrate
```

#### **4. Python dependencies issues**
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### **5. Permission denied for scripts**
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

## 📚 **Next Steps**

### **1. Explore the API**
- Open http://localhost:8000/docs
- Test different endpoints
- Understand the module structure

### **2. Understand the Architecture**
- Read `README-Module-Structure.md`
- Explore the code structure
- Understand module dependencies

### **3. Start Development**
- Add new features to existing modules
- Create new modules
- Write tests for your code

### **4. Connect Frontend**
- Configure frontend to use the API
- Implement authentication
- Test end-to-end functionality

## 🆘 **Getting Help**

### **Documentation**
- `README-Module-Structure.md` - Architecture overview
- `README-Docker.md` - Docker setup guide
- API documentation at http://localhost:8000/docs

### **Logs**
- Application logs: Check terminal output
- Docker logs: `./scripts/docker-commands.sh logs`
- Database logs: Check PgAdmin at http://localhost:5050

### **Common Commands Reference**
```bash
# Quick start (after initial setup)
./scripts/docker-commands.sh start
source venv/bin/activate
python run.py

# Quick stop
./scripts/docker-commands.sh stop

# Quick restart
./scripts/docker-commands.sh restart
```

## 🎉 **Congratulations!**

Bạn đã successfully setup và chạy My Vocabulary Vault Backend! 

Bây giờ bạn có thể:
- ✅ Access API tại http://localhost:8000
- ✅ View documentation tại http://localhost:8000/docs
- ✅ Manage database tại http://localhost:5050
- ✅ Start developing new features

Happy coding! 🚀
