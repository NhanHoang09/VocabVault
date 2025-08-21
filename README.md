# My Vocabulary Vault

A comprehensive vocabulary learning application with AI-powered features, gamification, and social learning capabilities.

## 🏗️ Project Structure

```
My Vocabulary Vault/
├── frontend/          # Next.js React frontend
├── backend/           # FastAPI Python backend
├── development/       # Development documentation
└── docs/             # API documentation
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker (optional, for containerized deployment)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend API will be available at: http://localhost:8000

### Docker Setup (Optional)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 🛠️ Development

### Frontend Commands

```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues
npm run test         # Run tests
npm run type-check   # TypeScript type checking
```

### Backend Commands

```bash
cd backend
# Activate virtual environment first
uvicorn app.main:app --reload    # Start development server
pytest                            # Run tests
alembic upgrade head             # Run database migrations
alembic revision --autogenerate  # Generate new migration
```

## 📚 Features

### Core Features
- **Vocabulary Management**: Create, edit, and organize vocabulary lists
- **Flashcard System**: Interactive flashcards with spaced repetition
- **Study Modes**: Multiple study modes including review, quiz, and practice
- **Progress Tracking**: Detailed analytics and learning progress

### AI-Powered Features
- **Adaptive Learning**: AI adjusts difficulty based on performance
- **Smart Recommendations**: Personalized vocabulary suggestions
- **Content Generation**: AI-generated study materials and examples

### Gamification
- **Achievement System**: Badges and rewards for learning milestones
- **Leaderboards**: Compete with other learners
- **Streak Tracking**: Daily learning streaks and motivation

### Social Features
- **Study Groups**: Create and join study groups
- **Sharing**: Share vocabulary lists and study materials
- **Community**: Connect with other learners

## 🗄️ Database

The application uses PostgreSQL with Alembic for database migrations.

### Database Setup

```bash
cd backend
# Create database (if using Docker)
docker-compose up -d postgres

# Run migrations
alembic upgrade head
```

## 🔧 Configuration

### Environment Variables

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=My Vocabulary Vault
```

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/vocabvault
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
```

## 📖 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Documentation**: See `docs/api/` directory

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app
```

## 📦 Deployment

### Production Build

#### Frontend
```bash
cd frontend
npm run build
npm start
```

#### Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```bash
docker-compose -f docker-compose.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `docs/` directory
- Review troubleshooting guides in `docs/troubleshooting/`
