#!/bin/bash

# My Vocabulary Vault - Docker Management Script
# Usage: ./scripts/docker-commands.sh [command]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.dev.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose > /dev/null 2>&1; then
        print_error "Docker Compose is not installed."
        exit 1
    fi
}

# Function to start services
start_services() {
    print_header "Starting Docker Services"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_warning "Creating .env file from env.docker..."
        cp env.docker .env
    fi
    
    print_status "Starting services with docker-compose..."
    docker-compose -f "$COMPOSE_FILE" up -d
    
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check service status
    docker-compose -f "$COMPOSE_FILE" ps
    
    print_status "Services started successfully!"
    print_status "PostgreSQL: localhost:5432"
    print_status "Redis: localhost:6379"
    print_status "PgAdmin: http://localhost:5050"
}

# Function to stop services
stop_services() {
    print_header "Stopping Docker Services"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    print_status "Stopping services..."
    docker-compose -f "$COMPOSE_FILE" down
    
    print_status "Services stopped successfully!"
}

# Function to restart services
restart_services() {
    print_header "Restarting Docker Services"
    stop_services
    sleep 2
    start_services
}

# Function to show service status
show_status() {
    print_header "Docker Services Status"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    print_status "Service status:"
    docker-compose -f "$COMPOSE_FILE" ps
    
    echo ""
    print_status "Service logs (last 10 lines):"
    docker-compose -f "$COMPOSE_FILE" logs --tail=10
}

# Function to show logs
show_logs() {
    print_header "Docker Services Logs"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    if [ -n "$2" ]; then
        print_status "Showing logs for service: $2"
        docker-compose -f "$COMPOSE_FILE" logs -f "$2"
    else
        print_status "Showing logs for all services:"
        docker-compose -f "$COMPOSE_FILE" logs -f
    fi
}

# Function to access PostgreSQL shell
postgres_shell() {
    print_header "PostgreSQL Shell"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    print_status "Connecting to PostgreSQL..."
    docker-compose -f "$COMPOSE_FILE" exec postgres psql -U vocabulary_user -d vocabulary_vault
}

# Function to run database migrations
run_migrations() {
    print_header "Running Database Migrations"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    print_status "Running Alembic migrations..."
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Run migrations
    alembic upgrade head
    
    print_status "Migrations completed successfully!"
}

# Function to reset database
reset_database() {
    print_header "Resetting Database"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    print_warning "This will delete all data in the database!"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Stopping services..."
        docker-compose -f "$COMPOSE_FILE" down
        
        print_status "Removing database volume..."
        docker volume rm vocabulary_vault_postgres_data_dev 2>/dev/null || true
        
        print_status "Starting services..."
        docker-compose -f "$COMPOSE_FILE" up -d
        
        print_status "Waiting for database to be ready..."
        sleep 15
        
        print_status "Running migrations..."
        run_migrations
        
        print_status "Database reset completed!"
    else
        print_status "Database reset cancelled."
    fi
}

# Function to backup database
backup_database() {
    print_header "Backing Up Database"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    BACKUP_DIR="backups"
    mkdir -p "$BACKUP_DIR"
    
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/vocabulary_vault_$TIMESTAMP.sql"
    
    print_status "Creating backup: $BACKUP_FILE"
    
    docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_dump -U vocabulary_user -d vocabulary_vault > "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        print_status "Backup created successfully: $BACKUP_FILE"
    else
        print_error "Backup failed!"
        exit 1
    fi
}

# Function to restore database
restore_database() {
    print_header "Restoring Database"
    check_docker
    check_docker_compose
    
    cd "$PROJECT_DIR"
    
    if [ -z "$2" ]; then
        print_error "Please specify backup file: ./scripts/docker-commands.sh restore <backup_file>"
        exit 1
    fi
    
    BACKUP_FILE="$2"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    print_warning "This will overwrite the current database!"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Restoring from backup: $BACKUP_FILE"
        
        docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -U vocabulary_user -d vocabulary_vault < "$BACKUP_FILE"
        
        if [ $? -eq 0 ]; then
            print_status "Database restored successfully!"
        else
            print_error "Database restore failed!"
            exit 1
        fi
    else
        print_status "Database restore cancelled."
    fi
}

# Function to show help
show_help() {
    print_header "Docker Management Commands"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start       - Start all Docker services"
    echo "  stop        - Stop all Docker services"
    echo "  restart     - Restart all Docker services"
    echo "  status      - Show service status"
    echo "  logs [service] - Show service logs (optional service name)"
    echo "  shell       - Access PostgreSQL shell"
    echo "  migrate     - Run database migrations"
    echo "  reset       - Reset database (delete all data)"
    echo "  backup      - Create database backup"
    echo "  restore <file> - Restore database from backup"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs postgres"
    echo "  $0 restore backups/vocabulary_vault_20231201_120000.sql"
}

# Main script logic
case "${1:-help}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "$@"
        ;;
    shell)
        postgres_shell
        ;;
    migrate)
        run_migrations
        ;;
    reset)
        reset_database
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
