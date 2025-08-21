# My Vocabulary Vault - Backend Architecture

## 🏗️ **Cấu trúc Module và Architecture**

### 📁 **Cấu trúc thư mục**

```
backend/
├── app/
│   ├── core/                    # Core components
│   │   ├── __init__.py
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # Database configuration
│   │   ├── security.py         # Authentication & authorization
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── dependencies.py     # Common dependencies
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   └── v1/                 # API version 1
│   │       ├── __init__.py
│   │       ├── deps.py         # API dependencies
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── vocabulary.py   # Vocabulary endpoints
│   │       ├── topics.py       # Topic endpoints
│   │       └── reviews.py      # Review endpoints
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── vocabulary.py
│   │   ├── topic.py
│   │   └── ...
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── vocabulary.py
│   │   └── ...
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   └── spaced_repetition.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Deprecated - use core.config
│   └── database.py             # Deprecated - use core.database
├── alembic/                    # Database migrations
├── scripts/                    # Management scripts
├── docker-compose.dev.yml      # Docker development setup
└── requirements.txt            # Python dependencies
```

## 🔧 **Core Components**

### **1. Configuration (`app/core/config.py`)**

- **Pydantic Settings**: Environment-based configuration
- **Type Safety**: Strong typing for all settings
- **Caching**: LRU cache for settings instance
- **Validation**: Automatic validation of environment variables

```python
from app.core.config import settings

# Access settings
database_url = settings.DATABASE_URL
secret_key = settings.SECRET_KEY
```

### **2. Database (`app/core/database.py`)**

- **Connection Pooling**: Optimized database connections
- **Session Management**: Automatic session cleanup
- **Error Handling**: Comprehensive error handling
- **Initialization**: Database table creation

```python
from app.core.database import get_db, init_db

# Dependency injection
def my_endpoint(db: Session = Depends(get_db)):
    # Use database session
    pass
```

### **3. Security (`app/core/security.py`)**

- **JWT Authentication**: Token-based authentication
- **Password Hashing**: Secure password storage
- **Authorization**: Role-based access control
- **Dependencies**: Authentication dependencies

```python
from app.core.security import get_current_active_user, require_superuser

# Protected endpoint
def protected_endpoint(user: User = Depends(get_current_active_user)):
    pass
```

### **4. Exceptions (`app/core/exceptions.py`)**

- **Custom Exceptions**: Application-specific exceptions
- **HTTP Status Codes**: Proper HTTP status codes
- **Error Messages**: Descriptive error messages
- **Consistent Handling**: Centralized exception handling

```python
from app.core.exceptions import NotFoundError, ConflictError

# Raise custom exceptions
if not user:
    raise NotFoundError("User", user_id)
```

### **5. Dependencies (`app/core/dependencies.py`)**

- **Pagination**: Standardized pagination parameters
- **Search**: Common search functionality
- **Optional Auth**: Endpoints with optional authentication
- **Superuser**: Superuser-only endpoints

```python
from app.core.dependencies import get_pagination_params, get_search_params

# Use common dependencies
def list_endpoint(
    pagination: PaginationParams = Depends(get_pagination_params),
    search: SearchParams = Depends(get_search_params)
):
    pass
```

## 🚀 **API Structure**

### **Versioning**

- **API v1**: Current stable version
- **Prefix**: `/api/v1`
- **Backward Compatibility**: Maintained across versions

### **Endpoint Organization**

- **Authentication**: `/api/v1/auth/*`
- **Vocabulary**: `/api/v1/vocabulary/*`
- **Topics**: `/api/v1/topics/*`
- **Reviews**: `/api/v1/reviews/*`

### **Swagger Documentation**

- **Interactive Docs**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Schema**: `/api/v1/openapi.json`

## 🔐 **Authentication & Authorization**

### **JWT Tokens**

```python
# Login to get token
POST /api/v1/auth/login
{
    "email": "user@example.com",
    "password": "password123"
}

# Use token in headers
Authorization: Bearer <access_token>
```

### **Protected Endpoints**

```python
# Require authentication
@router.get("/protected")
def protected_endpoint(user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {user.username}"}

# Require superuser
@router.delete("/admin")
def admin_endpoint(user: User = Depends(require_superuser)):
    return {"message": "Admin only"}
```

## 📊 **Database Models**

### **Relationships**

- **User → Vocabulary**: One-to-Many
- **User → Topics**: One-to-Many
- **Vocabulary ↔ Topics**: Many-to-Many
- **User → Learning Progress**: One-to-Many

### **Soft Deletes**

- **is_deleted**: Boolean flag for soft deletes
- **Data Preservation**: Keep data for analytics
- **Easy Recovery**: Simple undelete functionality

## 🛠️ **Development Tools**

### **Docker Management**

```bash
# Start services
./scripts/docker-commands.sh start

# View logs
./scripts/docker-commands.sh logs postgres

# Database operations
./scripts/docker-commands.sh migrate
./scripts/docker-commands.sh backup
./scripts/docker-commands.sh shell
```

### **Database Migrations**

```bash
# Create migration
alembic revision --autogenerate -m "Add new field"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### **Testing**

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_auth.py::test_login
```

## 🔄 **API Response Format**

### **Success Response**

```json
{
    "data": {...},
    "message": "Success message",
    "status": "success"
}
```

### **Error Response**

```json
{
  "detail": "Error message",
  "status_code": 400,
  "timestamp": "2023-12-01T12:00:00Z"
}
```

### **Paginated Response**

```json
{
    "data": [...],
    "pagination": {
        "page": 1,
        "size": 20,
        "total": 100,
        "pages": 5
    }
}
```

## 🚀 **Deployment**

### **Environment Variables**

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/vocabulary_vault

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI
OPENAI_API_KEY=your-openai-api-key
```

### **Production Setup**

```bash
# Build Docker image
docker build -t vocabulary-vault .

# Run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

## 📈 **Monitoring & Logging**

### **Logging Configuration**

```python
# Structured logging
logger.info("User logged in", extra={"user_id": user.id})

# Error logging
logger.error("Database connection failed", exc_info=True)
```

### **Health Checks**

```bash
# API health
curl http://localhost:8000/health

# Database health
./scripts/docker-commands.sh status
```

## 🔧 **Best Practices**

### **Code Organization**

- **Single Responsibility**: Each module has one purpose
- **Dependency Injection**: Use FastAPI dependencies
- **Type Hints**: Full type annotation
- **Documentation**: Comprehensive docstrings

### **Error Handling**

- **Custom Exceptions**: Application-specific errors
- **HTTP Status Codes**: Proper status codes
- **Error Messages**: User-friendly messages
- **Logging**: Comprehensive error logging

### **Security**

- **Input Validation**: Pydantic validation
- **SQL Injection**: SQLAlchemy ORM protection
- **XSS Protection**: Output sanitization
- **Rate Limiting**: Request rate limiting

### **Performance**

- **Connection Pooling**: Database connection optimization
- **Caching**: Redis caching for frequently accessed data
- **Pagination**: Efficient data pagination
- **Indexing**: Database query optimization

## 🎯 **Future Enhancements**

### **Planned Features**

- **API v2**: Enhanced API with new features
- **GraphQL**: Alternative to REST API
- **WebSocket**: Real-time communication
- **Microservices**: Service decomposition

### **Scalability**

- **Load Balancing**: Multiple server instances
- **Database Sharding**: Horizontal scaling
- **CDN**: Content delivery network
- **Caching**: Multi-level caching strategy
