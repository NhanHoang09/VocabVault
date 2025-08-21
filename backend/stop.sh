#!/bin/bash

# My Vocabulary Vault Backend - Stop Script
# This script stops all services and cleans up

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
    echo -e "${PURPLE} Stopping My Vocabulary Vault${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to kill process on port
kill_port() {
    local port=$1
    local service_name=$2
    
    if port_in_use $port; then
        print_status "Stopping $service_name on port $port..."
        lsof -ti :$port | xargs kill -9 2>/dev/null || true
        print_success "$service_name stopped"
    else
        print_status "$service_name is not running"
    fi
}

# Main execution
main() {
    print_header
    
    # Step 1: Stop the backend server
    print_step "1. Stopping backend server..."
    kill_port 8000 "Backend server"
    
    # Step 2: Stop Docker services
    print_step "2. Stopping Docker services..."
    
    if command -v docker >/dev/null 2>&1; then
        print_status "Stopping Docker services..."
        ./scripts/docker-commands.sh stop >/dev/null 2>&1 || true
        print_success "Docker services stopped"
    else
        print_warning "Docker not found, skipping Docker services"
    fi
    
    # Step 3: Deactivate virtual environment
    print_step "3. Cleaning up Python environment..."
    
    if [ -n "$VIRTUAL_ENV" ]; then
        print_status "Deactivating virtual environment..."
        deactivate 2>/dev/null || true
        print_success "Virtual environment deactivated"
    fi
    
    print_success "🎉 All services stopped successfully!"
    print_status "You can start them again with: ./run.sh"
}

# Run main function
main "$@"
