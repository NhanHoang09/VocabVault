#!/bin/bash

# Initialize Git repository for My Vocabulary Vault
echo "🚀 Initializing Git repository for My Vocabulary Vault..."

# Check if git is already initialized
if [ -d ".git" ]; then
    echo "⚠️  Git repository already exists!"
    read -p "Do you want to continue? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "🎉 Initial commit: My Vocabulary Vault

- Frontend: Next.js React application with TypeScript
- Backend: FastAPI Python application with PostgreSQL
- Docker configuration for development and production
- Comprehensive documentation and project structure
- ESLint and Prettier configuration
- Testing setup for both frontend and backend

Features:
- Vocabulary management and flashcard system
- AI-powered learning features
- Gamification and social learning
- Modern UI with Tailwind CSS
- RESTful API with comprehensive documentation"

echo "✅ Git repository setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add remote repository: git remote add origin <your-repo-url>"
echo "2. Push to remote: git push -u origin main"
echo "3. Start development:"
echo "   - Frontend: cd frontend && npm run dev"
echo "   - Backend: cd backend && uvicorn app.main:app --reload"
echo "4. Or use Docker: docker-compose -f docker-compose.dev.yml up"
echo ""
echo "🎯 Happy coding!"
