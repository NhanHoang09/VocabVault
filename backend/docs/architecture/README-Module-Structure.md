# My Vocabulary Vault - Module-Based Architecture

## 🏗️ **Cấu trúc Module-Based Architecture (Updated)**

### 📁 **Cấu trúc thư mục hiện tại (Sau cleanup)**

```
backend/
├── app/
│   ├── core/                    # Core infrastructure
│   │   ├── __init__.py
│   │   ├── config.py           # Application settings & environment
│   │   ├── database.py         # Database configuration & session
│   │   ├── security.py         # JWT authentication & authorization
│   │   ├── exceptions.py       # Custom exception classes
│   │   └── dependencies.py     # Common FastAPI dependencies
│   ├── modules/                # Feature-based modules
│   │   ├── __init__.py
│   │   ├── auth/               # Authentication module
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # User model
│   │   │   ├── schemas.py      # Pydantic schemas
│   │   │   ├── services.py     # Business logic
│   │   │   └── api.py          # API endpoints
│   │   ├── vocabulary/         # Vocabulary management
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # Vocabulary model
│   │   │   └── schemas.py      # Vocabulary schemas
│   │   ├── topics/             # Topic management
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # Topic models
│   │   │   └── schemas.py      # Topic schemas
│   │   └── learning/           # Learning & spaced repetition
│   │       ├── __init__.py
│   │       └── models.py       # Learning models
│   ├── shared/                 # Shared utilities
│   │   ├── __init__.py
│   │   ├── constants.py        # Application constants
│   │   └── utils.py            # Common utilities
│   ├── main.py                 # FastAPI application entry point
│   └── __init__.py
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
├── scripts/                    # Management scripts
│   ├── docker-commands.sh      # Docker management
│   └── test-db-connection.py   # Database connection test
├── tests/                      # Test suite (TODO)
├── docker-compose.dev.yml      # Docker development setup
├── docker-compose.yml          # Docker production setup
├── Dockerfile                  # Docker image configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── env.docker                  # Docker environment variables
├── env.example                 # Environment variables template
├── init.sql                    # Database initialization
├── run.py                      # Application runner
├── README-Module-Structure.md  # This file
├── README-Docker.md            # Docker setup guide
└── README-Getting-Started.md   # Step-by-step guide
```

## 🔧 **Module Structure Pattern**

### **Mỗi module có cấu trúc chuẩn:**

```
module_name/
├── __init__.py          # Module package
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── services.py          # Business logic
├── api.py              # FastAPI routes
└── tests/              # Module-specific tests (TODO)
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_api.py
```

### **1. Models (`models.py`)**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ExampleModel(Base):
    __tablename__ = "example_table"
    
    id = Column(Integer, primary_key=True, index=True)
    # ... other fields
    
    # Relationships
    user = relationship("User", back_populates="examples")
```

### **2. Schemas (`schemas.py`)**
```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExampleBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExampleCreate(ExampleBase):
    pass

class ExampleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ExampleResponse(ExampleBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### **3. Services (`services.py`)**
```python
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.modules.example.models import ExampleModel
from app.modules.example.schemas import ExampleCreate
from typing import List, Optional

class ExampleService:
    @staticmethod
    def create_example(db: Session, user_id: int, data: ExampleCreate) -> ExampleModel:
        # Business logic here
        pass
    
    @staticmethod
    def get_example(db: Session, example_id: int, user_id: int) -> Optional[ExampleModel]:
        # Business logic here
        pass
```

### **4. API (`api.py`)**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.example.models import ExampleModel
from app.modules.example.schemas import ExampleCreate, ExampleResponse
from app.modules.example.services import ExampleService
from app.core.dependencies import require_active_user
from typing import List

router = APIRouter(prefix="/examples", tags=["examples"])

@router.post("/", response_model=ExampleResponse)
def create_example(
    data: ExampleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_active_user)
):
    return ExampleService.create_example(db, current_user.id, data)
```

## 🚀 **Benefits của Module-Based Architecture**

### **1. Scalability**
- **Easy to add new features**: Chỉ cần tạo module mới
- **Independent development**: Teams có thể làm việc song song
- **Microservices ready**: Dễ dàng tách thành microservices

### **2. Maintainability**
- **Clear separation of concerns**: Mỗi module có trách nhiệm rõ ràng
- **Easy to test**: Test từng module độc lập
- **Easy to debug**: Lỗi được isolate trong module

### **3. Code Organization**
- **Feature-based structure**: Code được tổ chức theo tính năng
- **Reduced coupling**: Modules ít phụ thuộc lẫn nhau
- **Better readability**: Dễ hiểu và navigate code

### **4. Team Collaboration**
- **Parallel development**: Nhiều developers có thể làm việc song song
- **Clear ownership**: Mỗi module có owner rõ ràng
- **Reduced conflicts**: Ít conflict khi merge code

## 🔄 **Module Dependencies**

### **Core Dependencies**
```
modules/
├── auth/           # Base module - no dependencies
├── vocabulary/     # Depends on: auth, topics
├── topics/         # Depends on: auth
├── learning/       # Depends on: auth, vocabulary
├── quizzes/        # Depends on: auth, vocabulary
├── conversations/  # Depends on: auth, vocabulary
└── analytics/      # Depends on: all other modules
```

### **Dependency Management**
```python
# In vocabulary/models.py
from app.modules.auth.models import User
from app.modules.topics.models import Topic

class Vocabulary(Base):
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="vocabulary")
```

## 🧪 **Testing Strategy**

### **Module-Level Testing**
```python
# tests/test_vocabulary/test_services.py
import pytest
from app.modules.vocabulary.services import VocabularyService

def test_create_vocabulary(db_session, test_user):
    data = VocabularyCreate(word="test", meaning="test meaning")
    result = VocabularyService.create_vocabulary(db_session, test_user.id, data)
    assert result.word == "test"
```

### **Integration Testing**
```python
# tests/test_integration/test_auth_vocabulary.py
def test_user_can_create_vocabulary(client, test_user_token):
    response = client.post(
        "/api/v1/vocabulary/",
        json={"word": "test", "meaning": "test meaning"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 201
```

## 🚀 **Deployment Strategy**

### **Module-Based Deployment**
```yaml
# docker-compose.prod.yml
services:
  auth-service:
    build: .
    environment:
      MODULE: auth
  vocabulary-service:
    build: .
    environment:
      MODULE: vocabulary
  learning-service:
    build: .
    environment:
      MODULE: learning
```

### **Database Migrations**
```bash
# Create migration for specific module
alembic revision --autogenerate -m "Add vocabulary module tables"

# Run migrations
alembic upgrade head
```

## 📈 **Monitoring & Observability**

### **Module-Level Metrics**
```python
# In each module's services.py
from app.shared.metrics import module_metrics

class VocabularyService:
    @staticmethod
    def create_vocabulary(db: Session, user_id: int, data: VocabularyCreate):
        module_metrics.vocabulary_created.inc()
        # ... business logic
```

### **Health Checks**
```python
# In main.py
@app.get("/health/modules")
async def module_health_check():
    return {
        "auth": {"status": "healthy"},
        "vocabulary": {"status": "healthy"},
        "learning": {"status": "healthy"}
    }
```

## 🎯 **Best Practices**

### **1. Module Design**
- **Single Responsibility**: Mỗi module chỉ làm một việc
- **High Cohesion**: Các thành phần trong module liên quan chặt chẽ
- **Low Coupling**: Modules ít phụ thuộc lẫn nhau

### **2. API Design**
- **RESTful**: Tuân thủ REST principles
- **Versioning**: API versioning cho backward compatibility
- **Documentation**: Swagger documentation cho mỗi module

### **3. Database Design**
- **Normalization**: Database được normalize đúng cách
- **Indexing**: Proper indexing cho performance
- **Migrations**: Database migrations được quản lý tốt

### **4. Security**
- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Input Validation**: Pydantic validation cho tất cả inputs

## 🔮 **Future Enhancements**

### **Planned Modules**
- **Notifications**: Email/SMS notifications
- **Gamification**: Points, badges, leaderboards
- **Social**: User interactions, sharing
- **AI**: Advanced AI features
- **Mobile**: Mobile-specific APIs

### **Architecture Evolution**
- **Microservices**: Tách modules thành microservices
- **Event-Driven**: Event-driven architecture
- **CQRS**: Command Query Responsibility Segregation
- **GraphQL**: Alternative to REST API

## 📋 **Current Status**

### **✅ Completed Modules**
- **Auth Module**: Complete with models, schemas, services, and API
- **Core Infrastructure**: Complete with config, database, security, exceptions, dependencies
- **Shared Utilities**: Complete with constants and utils

### **🔄 In Progress Modules**
- **Vocabulary Module**: Models and schemas ready, need services and API
- **Topics Module**: Models and schemas ready, need services and API
- **Learning Module**: Models ready, need schemas, services, and API

### **📝 TODO Modules**
- **Quizzes Module**: Complete implementation needed
- **Conversations Module**: Complete implementation needed
- **Analytics Module**: Complete implementation needed
- **Testing**: Complete test suite needed
