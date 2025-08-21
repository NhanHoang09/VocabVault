#!/bin/bash

echo "🚀 Starting Login Flow Test Environment"
echo "========================================"

# Check if backend is running
echo "🔍 Checking backend status..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is already running on http://localhost:8000"
else
    echo "⚠️  Backend is not running"
    echo "📋 To start backend, run:"
    echo "   cd backend"
    echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
fi

# Check if frontend is running
echo "🔍 Checking frontend status..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is already running on http://localhost:3000"
else
    echo "⚠️  Frontend is not running"
    echo "📋 To start frontend, run:"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
fi

echo ""
echo "🎯 Test Instructions:"
echo "===================="
echo "1. Start backend (if not running):"
echo "   cd backend && uvicorn app.main:app --reload"
echo ""
echo "2. Start frontend (if not running):"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Test Login Flow:"
echo "   - Open: http://localhost:3000/login"
echo "   - Login with test credentials"
echo "   - Should redirect to: http://localhost:3000/dashboard"
echo ""
echo "4. Test Dashboard Features:"
echo "   - Check user info display"
echo "   - Test token security buttons"
echo "   - Test logout functionality"
echo ""
echo "📚 Documentation:"
echo "================="
echo "- Login Test Guide: frontend/docs/LOGIN_TEST_GUIDE.md"
echo "- Dashboard Test Guide: frontend/docs/DASHBOARD_TEST_GUIDE.md"
echo "- Token Strategy: frontend/docs/TOKEN_STORAGE_STRATEGY.md"
echo ""
echo "🔧 Quick Commands:"
echo "=================="
echo "Backend:  cd backend && uvicorn app.main:app --reload"
echo "Frontend: cd frontend && npm run dev"
echo "Build:    cd frontend && npm run build"
echo ""
echo "🎉 Happy Testing!"
