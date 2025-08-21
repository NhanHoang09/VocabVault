#!/bin/bash

# My Vocabulary Vault Backend - Auto Run Script
# This script automatically sets up and runs the backend server

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
    echo -e "${PURPLE} My Vocabulary Vault Backend${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to check if our server is running
is_our_server_running() {
    local port=$1
    if ! port_in_use $port; then
        return 1
    fi
    
    # Try to connect to our health endpoint
    if curl -s "http://localhost:$port/health" >/dev/null 2>&1; then
        return 0
    fi
    
    return 1
}

# Function to kill process on port
kill_port() {
    local port=$1
    local service_name=$2
    
    if port_in_use $port; then
        print_status "Port $port is in use. Checking if it's our server..."
        
        if is_our_server_running $port; then
            print_warning "$service_name is already running on port $port"
            return 0
        else
            print_status "Killing process on port $port..."
            lsof -ti :$port | xargs kill -9 2>/dev/null || true
            sleep 2
            print_success "Process on port $port killed"
        fi
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if nc -z $host $port 2>/dev/null; then
            print_success "$service_name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start after $max_attempts attempts"
    return 1
}

# Main execution
main() {
    print_header
    
    # Step 1: Check prerequisites
    print_step "1. Checking prerequisites..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.8+"
        exit 1
    fi
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose"
        exit 1
    fi
    
    print_success "All prerequisites are satisfied"
    
    # Step 2: Check if we're in the right directory
    print_step "2. Checking project structure..."
    
    if [ ! -f "requirements.txt" ] || [ ! -f "docker-compose.dev.yml" ]; then
        print_error "Please run this script from the backend directory"
        exit 1
    fi
    
    print_success "Project structure is correct"
    
    # Step 3: Check if .env file exists
    print_step "3. Checking environment configuration..."
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        if [ -f "env.example" ]; then
            cp env.example .env
            print_success "Created .env file from template"
        else
            print_error "No .env file or env.example template found"
            exit 1
        fi
    fi
    
    print_success "Environment configuration is ready"
    
    # Step 4: Setup Python virtual environment
    print_step "4. Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt >/dev/null 2>&1
    print_success "Dependencies installed"
    
    # Step 5: Start Docker services
    print_step "5. Starting Docker services..."
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first"
        exit 1
    fi
    
    # Start services
    print_status "Starting Docker services..."
    ./scripts/docker-commands.sh start >/dev/null 2>&1
    
    # Wait for services to be ready
    wait_for_service "localhost" "5432" "PostgreSQL"
    wait_for_service "localhost" "6379" "Redis"
    
    print_success "Docker services are running"
    
    # Step 6: Test database connection
    print_step "6. Testing database connection..."
    
    if python scripts/test-db-connection.py >/dev/null 2>&1; then
        print_success "Database connection successful"
    else
        print_warning "Database connection test failed, but continuing..."
    fi
    
    # Step 7: Run database migrations
    print_step "7. Running database migrations..."
    
    print_status "Running migrations..."
    if ./scripts/docker-commands.sh migrate >/dev/null 2>&1; then
        print_success "Database migrations completed"
    else
        print_warning "Migration failed, but continuing with existing database..."
    fi
    
    # Step 8: Check if server is already running
    print_step "8. Checking if server is already running..."
    
    if is_our_server_running 8000; then
        print_warning "Our server is already running on port 8000"
        print_status "You can access the API at: http://localhost:8000"
        print_status "API Documentation: http://localhost:8000/docs"
        print_status "Press Ctrl+C to stop the server"
        exit 0
    else
        # Kill any process on port 8000 that's not our server
        kill_port 8000 "Backend server"
    fi
    
    # Step 9: Start the server
    print_step "9. Starting the server..."
    
    print_success "🚀 Starting My Vocabulary Vault Backend..."
    print_status "API will be available at: http://localhost:8000"
    print_status "API Documentation: http://localhost:8000/docs"
    print_status "Health Check: http://localhost:8000/health"
    print_status "Press Ctrl+C to stop the server"
    echo ""
    
    # Start the server
    python run.py
}

# Function to cleanup on exit
cleanup() {
    print_status "Shutting down..."
    # Deactivate virtual environment
    deactivate 2>/dev/null || true
    print_success "Goodbye! 👋"
}

# Set up trap to call cleanup on script exit
trap cleanup EXIT

# Run main function
main "$@"
