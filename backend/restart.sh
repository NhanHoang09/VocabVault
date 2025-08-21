#!/bin/bash

# My Vocabulary Vault Backend - Restart Script
# This script restarts all services

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
    echo -e "${PURPLE} Restarting My Vocabulary Vault${NC}"
    echo -e "${PURPLE}================================${NC}"
}

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
}

# Main execution
main() {
    print_header
    
    # Step 1: Stop all services
    print_step "1. Stopping all services..."
    ./stop.sh >/dev/null 2>&1 || true
    
    # Step 2: Wait a moment
    print_status "Waiting 3 seconds..."
    sleep 3
    
    # Step 3: Start all services
    print_step "2. Starting all services..."
    ./run.sh
}

# Run main function
main "$@"
