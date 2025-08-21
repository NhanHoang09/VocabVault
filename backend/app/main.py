from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.core.exceptions import VocabularyVaultException
# Import all models to ensure they are registered with proper order
import app.models_registry
from app.modules.auth.api import router as auth_router
from app.modules.flashcards.api import router as flashcards_router
from app.modules.learning.api import router as learning_router
from app.modules.analytics.api import router as analytics_router
from app.modules.gamification.api import router as gamification_router
from app.modules.ai.api import router as ai_router
from app.modules.social.api import router as social_router
import logging
import time

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    # My Vocabulary Vault API
    
    A comprehensive Quizlet-like vocabulary learning application with modern features and AI integration.
    
    ## 🎯 Core Features
    
    * **🔐 Authentication**: JWT-based user authentication and authorization
    * **📚 Flashcard Management**: Create, organize, and manage flashcard sets
    * **🎮 Study Modes**: Multiple study modes (Flashcards, Learn, Write, Spell, Test)
    * **📊 Analytics**: Progress tracking, performance metrics, and learning insights
    
    ## 🏗️ Architecture
    
    This API uses a modern module-based architecture for better scalability and maintainability:
    
    - **Core**: Infrastructure components (config, database, security, exceptions)
    - **Modules**: Feature-based modules (auth, flashcards, learning, analytics)
    - **Shared**: Common utilities, constants, and helper functions
    
    ## 🚀 Getting Started
    
    1. **Register**: Create a new account using `/auth/register`
    2. **Login**: Get your access token using `/auth/login`
    3. **Authenticate**: Include the token in the Authorization header for protected endpoints
    4. **Start Learning**: Create flashcard sets and begin your learning journey!
    
    ## 🔐 Authentication
    
    Most endpoints require authentication. Include your JWT token in the Authorization header:
    
    ```
    Authorization: Bearer <your_access_token>
    ```
    
    ## 📚 Flashcard System
    
    The flashcard system supports:
    - **Multiple card types**: Text, image, audio, video
    - **Rich metadata**: Difficulty levels, custom tags, progress tracking
    - **Study modes**: Traditional flashcards, structured learning, typing practice
    - **Progress tracking**: Mastery levels, review statistics, spaced repetition
    
    ## 📊 Analytics & Insights
    
    Track your progress with:
    - **Study statistics**: Time spent, cards studied, accuracy rates
    - **Performance trends**: Learning progress over time
    - **Learning insights**: Tips and recommendations
    - **Goal tracking**: Set and monitor study goals
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "operationsSorter": "method",
        "tagsSorter": "alpha",
    }
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handler for custom exceptions
@app.exception_handler(VocabularyVaultException)
async def vocabulary_vault_exception_handler(
    request: Request, 
    exc: VocabularyVaultException
):
    logger.error(f"VocabularyVaultException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )


# Health check endpoint
@app.get(
    "/health",
    summary="Health check",
    description="Check if the API is running",
    response_description="API health status",
    tags=["health"]
)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API.
    """
    return {"status": "healthy"}


# Root endpoint
@app.get(
    "/",
    summary="API root",
    description="Get API information and available endpoints",
    response_description="API information",
    tags=["root"]
)
async def read_root():
    """
    API root endpoint.
    
    Returns basic information about the API and links to documentation.
    """
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "architecture": "module-based",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=app.description,
        routes=app.routes,
    )
    
    # Custom security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    # Add security to all protected endpoints
    protected_paths = [
        "/api/v1/auth/me",
        "/api/v1/flashcards",
        "/api/v1/flashcards/",
        "/api/v1/flashcards/{set_id}",
        "/api/v1/flashcards/{set_id}/",
        "/api/v1/flashcards/{set_id}/cards",
        "/api/v1/flashcards/{set_id}/cards/",
        "/api/v1/flashcards/{set_id}/cards/{card_id}",
        "/api/v1/flashcards/{set_id}/cards/{card_id}/",
        "/api/v1/flashcards/{set_id}/study",
        "/api/v1/flashcards/{set_id}/study/",
        "/api/v1/flashcards/{set_id}/share",
        "/api/v1/flashcards/{set_id}/share/",
        "/api/v1/study",
        "/api/v1/study/",
        "/api/v1/study/sessions",
        "/api/v1/study/sessions/",
        "/api/v1/study/sessions/{session_id}",
        "/api/v1/study/sessions/{session_id}/",
        "/api/v1/study/attempts",
        "/api/v1/study/attempts/",
        "/api/v1/study/attempts/{attempt_id}",
        "/api/v1/study/attempts/{attempt_id}/",
        "/api/v1/analytics",
        "/api/v1/analytics/",
        "/api/v1/analytics/progress",
        "/api/v1/analytics/progress/",
        "/api/v1/analytics/sets/{set_id}/progress",
        "/api/v1/analytics/sets/{set_id}/progress/",
        "/api/v1/analytics/stats/daily",
        "/api/v1/analytics/stats/daily/",
        "/api/v1/analytics/stats/weekly",
        "/api/v1/analytics/stats/weekly/",
        "/api/v1/analytics/stats/monthly",
        "/api/v1/analytics/stats/monthly/",
        "/api/v1/analytics/mastery",
        "/api/v1/analytics/mastery/",
        "/api/v1/analytics/streaks",
        "/api/v1/analytics/streaks/",
        "/api/v1/gamification",
        "/api/v1/gamification/",
        "/api/v1/gamification/badges",
        "/api/v1/gamification/badges/",
        "/api/v1/gamification/badges/{badge_id}",
        "/api/v1/gamification/badges/{badge_id}/",
        "/api/v1/gamification/badges/{badge_id}/award",
        "/api/v1/gamification/badges/{badge_id}/award/",
        "/api/v1/gamification/users/{user_id}/badges",
        "/api/v1/gamification/users/{user_id}/badges/",
        "/api/v1/gamification/points",
        "/api/v1/gamification/points/",
        "/api/v1/gamification/points/transactions",
        "/api/v1/gamification/points/transactions/",
        "/api/v1/gamification/leaderboard",
        "/api/v1/gamification/leaderboard/",
        "/api/v1/gamification/games",
        "/api/v1/gamification/games/",
        "/api/v1/gamification/games/sessions",
        "/api/v1/gamification/games/sessions/",
        "/api/v1/gamification/games/sessions/{session_id}",
        "/api/v1/gamification/games/sessions/{session_id}/",
        "/api/v1/gamification/games/match/{session_id}",
        "/api/v1/gamification/games/match/{session_id}/",
        "/api/v1/gamification/games/match/{session_id}/move",
        "/api/v1/gamification/games/gravity/{session_id}",
        "/api/v1/gamification/games/gravity/{session_id}/",
        "/api/v1/gamification/games/gravity/{session_id}/answer",
    ]
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            # Add security to protected paths
            if any(protected_path in path for protected_path in protected_paths):
                openapi_schema["paths"][path][method]["security"] = [
                    {"BearerAuth": []}
                ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Include module routers
app.include_router(
    auth_router,
    prefix=settings.API_V1_STR,
    tags=["authentication"]
)

app.include_router(
    flashcards_router,
    prefix=settings.API_V1_STR,
    tags=["flashcards"]
)

app.include_router(
    learning_router,
    prefix=settings.API_V1_STR,
    tags=["study"]
)

app.include_router(
    analytics_router,
    prefix=settings.API_V1_STR,
    tags=["analytics"]
)

app.include_router(
    gamification_router,
    prefix=settings.API_V1_STR,
    tags=["gamification"]
)

app.include_router(
    ai_router,
    prefix=settings.API_V1_STR,
    tags=["ai"]
)

app.include_router(
    social_router,
    prefix=settings.API_V1_STR,
    tags=["social"]
)

# Phase 1 & 2 complete - Core modules and Gamification
# Future phases will add:
# - AI Module (Phase 3)
# - Social Features (Phase 4)
# - Advanced Analytics (Phase 5)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Architecture: Module-based")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    
    # Register all models
    from app.models_registry import register_models, validate_foreign_keys
    registered_models = register_models()
    logger.info(f"Successfully registered {len(registered_models)} models")
    
    # Validate foreign keys
    if validate_foreign_keys():
        logger.info("All foreign keys validated successfully")
    else:
        logger.warning("Foreign key validation completed with warnings")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
