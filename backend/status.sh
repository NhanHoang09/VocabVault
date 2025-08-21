#!/bin/bash

# My Vocabulary Vault Backend - Status Script
# This script checks the status of all services

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE} My Vocabulary Vault Status${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to check service status
check_service() {
    local port=$1
    local service_name=$2
    local url=$3
    
    if port_in_use $port; then
        print_success "$service_name: Running on port $port"
        if [ -n "$url" ]; then
            echo "   URL: $url"
        fi
        return 0
    else
        print_error "$service_name: Not running"
        return 1
    fi
}

# Function to test API endpoint
test_api() {
    local url=$1
    local endpoint=$2
    
    if curl -s "$url" >/dev/null 2>&1; then
        print_success "API $endpoint: Responding"
        return 0
    else
        print_error "API $endpoint: Not responding"
        return 1
    fi
}

# Main execution
main() {
    print_header
    echo ""
    
    # Check Docker services
    print_step "1. Docker Services Status"
    if command -v docker >/dev/null 2>&1; then
        ./scripts/docker-commands.sh status
    else
        print_error "Docker not installed"
    fi
    echo ""
    
    # Check backend server
    print_step "2. Backend Server Status"
    if check_service 8000 "Backend Server" "http://localhost:8000"; then
        echo "   API Documentation: http://localhost:8000/docs"
        echo "   Health Check: http://localhost:8000/health"
        echo ""
        
        # Test API endpoints
        print_step "3. API Endpoints Test"
        test_api "http://localhost:8000/health" "Health Check"
        test_api "http://localhost:8000/" "Root Endpoint"
    fi
    echo ""
    
    # Check database connection
    print_step "4. Database Connection Test"
    if command -v python3 >/dev/null 2>&1 && [ -d "venv" ]; then
        source venv/bin/activate 2>/dev/null || true
        if python scripts/test-db-connection.py >/dev/null 2>&1; then
            print_success "Database connection: OK"
        else
            print_error "Database connection: Failed"
        fi
    else
        print_warning "Python environment not ready"
    fi
    echo ""
    
    # Summary
    print_step "5. Summary"
    echo "Services:"
    check_service 5432 "PostgreSQL" "localhost:5432" >/dev/null 2>&1 || echo "   ❌ PostgreSQL: Not running"
    check_service 6379 "Redis" "localhost:6379" >/dev/null 2>&1 || echo "   ❌ Redis: Not running"
    check_service 5050 "PgAdmin" "http://localhost:5050" >/dev/null 2>&1 || echo "   ❌ PgAdmin: Not running"
    check_service 8000 "Backend API" "http://localhost:8000" >/dev/null 2>&1 || echo "   ❌ Backend API: Not running"
    
    echo ""
    print_status "To start all services: ./run.sh"
    print_status "To stop all services: ./stop.sh"
    print_status "To restart all services: ./restart.sh"
}

# Run main function
main "$@"
