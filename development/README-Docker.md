# 🐳 Docker Setup for My Vocabulary Vault Backend

Hướng dẫn sử dụng Docker để chạy database và các services cho backend.

## 📋 Prerequisites

- Docker Desktop (hoặc Docker Engine + Docker Compose)
- Python 3.8+ (cho development)

## 🚀 Quick Start

### 1. Setup Docker Environment

```bash
# Chạy script setup tự động
cd backend
./scripts/docker-setup.sh
```

### 2. Manual Setup

```bash
# Copy environment file
cp env.docker .env

# Start Docker services
docker-compose -f docker-compose.dev.yml up -d

# Run migrations
alembic upgrade head

# Start backend server
python run.py
```

## 📊 Services

Sau khi chạy Docker, các services sau sẽ được khởi động:

| Service         | Port | URL                     | Credentials                               |
| --------------- | ---- | ----------------------- | ----------------------------------------- |
| **PostgreSQL**  | 5432 | `localhost:5432`        | `vocabulary_user` / `vocabulary_password` |
| **Redis**       | 6379 | `localhost:6379`        | -                                         |
| **PgAdmin**     | 5050 | `http://localhost:5050` | `admin@vocabularyvault.com` / `admin123`  |
| **Backend API** | 8000 | `http://localhost:8000` | -                                         |

## 🛠️ Docker Commands

Sử dụng script `docker-commands.sh` để quản lý Docker services:

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

# Reset database (delete all data)
./scripts/docker-commands.sh reset

# Create backup
./scripts/docker-commands.sh backup

# Restore from backup
./scripts/docker-commands.sh restore backup_file.sql

# Open PostgreSQL shell
./scripts/docker-commands.sh shell

# Run migrations
./scripts/docker-commands.sh migrate

# Create new migration
./scripts/docker-commands.sh migrate-create "Add new table"
```

## 🔧 Manual Docker Commands

### Start Services

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Stop Services

```bash
docker-compose -f docker-compose.dev.yml down
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.dev.yml logs -f

# Specific service
docker-compose -f docker-compose.dev.yml logs -f postgres
docker-compose -f docker-compose.dev.yml logs -f redis
```

### Access PostgreSQL

```bash
# Connect to database
docker-compose -f docker-compose.dev.yml exec postgres psql -U vocabulary_user vocabulary_vault

# Run SQL file
docker-compose -f docker-compose.dev.yml exec -T postgres psql -U vocabulary_user vocabulary_vault < file.sql
```

### Backup & Restore

```bash
# Create backup
docker-compose -f docker-compose.dev.yml exec postgres pg_dump -U vocabulary_user vocabulary_vault > backup.sql

# Restore backup
docker-compose -f docker-compose.dev.yml exec -T postgres psql -U vocabulary_user vocabulary_vault < backup.sql
```

## 🗄️ Database Management

### Connection Details

- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `vocabulary_vault`
- **Username**: `vocabulary_user`
- **Password**: `vocabulary_password`

### Using PgAdmin

1. Mở browser và truy cập: `http://localhost:5050`
2. Login với:
   - Email: `admin@vocabularyvault.com`
   - Password: `admin123`
3. Thêm server mới:
   - Host: `postgres` (tên container)
   - Port: `5432`
   - Database: `vocabulary_vault`
   - Username: `vocabulary_user`
   - Password: `vocabulary_password`

## 🔄 Development Workflow

### 1. Start Development Environment

```bash
# Start Docker services
./scripts/docker-commands.sh start

# Run migrations
./scripts/docker-commands.sh migrate

# Start backend (in another terminal)
python run.py
```

### 2. Database Changes

```bash
# Create new migration
./scripts/docker-commands.sh migrate-create "Description of changes"

# Apply migrations
./scripts/docker-commands.sh migrate
```

### 3. Reset Development Data

```bash
# Reset database (delete all data)
./scripts/docker-commands.sh reset
```

## 🧹 Cleanup

### Remove All Data

```bash
# Stop services and remove volumes
docker-compose -f docker-compose.dev.yml down -v

# Clean up Docker system
docker system prune -f
```

### Remove Specific Volumes

```bash
# List volumes
docker volume ls

# Remove specific volume
docker volume rm vocabulary_vault_postgres_data_dev
```

## 🐛 Troubleshooting

### PostgreSQL Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose -f docker-compose.dev.yml ps

# Check PostgreSQL logs
docker-compose -f docker-compose.dev.yml logs postgres

# Test connection
docker-compose -f docker-compose.dev.yml exec postgres pg_isready -U vocabulary_user
```

### Port Conflicts

Nếu port 5432, 6379, hoặc 5050 đã được sử dụng:

1. Dừng service đang sử dụng port
2. Hoặc thay đổi port trong `docker-compose.dev.yml`:
   ```yaml
   ports:
     - "5433:5432" # Thay đổi từ 5432 thành 5433
   ```

### Permission Issues

```bash
# Fix script permissions
chmod +x scripts/*.sh

# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
```

## 📝 Environment Variables

File `env.docker` chứa cấu hình cho Docker:

```bash
# Database
DATABASE_URL=postgresql://vocabulary_user:vocabulary_password@localhost:5432/vocabulary_vault

# Redis
REDIS_URL=redis://localhost:6379

# Other settings...
```

## 🔒 Security Notes

⚠️ **Important**: Cấu hình này chỉ dành cho development. Trong production:

1. Thay đổi tất cả passwords
2. Sử dụng secrets management
3. Cấu hình SSL/TLS
4. Restrict network access
5. Regular security updates

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Redis Docker Image](https://hub.docker.com/_/redis)
