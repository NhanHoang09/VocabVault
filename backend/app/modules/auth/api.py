from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import security_manager
from app.core.exceptions import AuthenticationError
from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.modules.auth.services import AuthService
from app.core.dependencies import require_active_user
from typing import Any

router = APIRouter(
    prefix="/auth", 
    tags=["authentication"],
    responses={
        404: {"description": "Resource not found"},
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient permissions"},
        422: {"description": "Validation error"}
    }
)


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Register new user",
    description="Create a new user account with email, username, and password",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "User already exists"},
        422: {"description": "Validation error"}
    }
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user.
    
    - **email**: User's email address (must be unique)
    - **username**: User's username (must be unique)
    - **full_name**: User's full name (optional)
    - **password**: User's password (minimum 6 characters)
    """
    return AuthService.create_user(db, user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login",
    description="Authenticate user and return access token",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
        400: {"description": "Inactive user"}
    }
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    """
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    
    if not user:
        raise AuthenticationError("Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = security_manager.create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get information about the currently authenticated user",
    responses={
        200: {"description": "User information retrieved successfully"},
        401: {"description": "Not authenticated"}
    }
)
def get_current_user_info(
    current_user: User = Depends(require_active_user)
) -> Any:
    """
    Get current user information.
    
    Returns the profile information of the currently authenticated user.
    """
    return UserResponse.model_validate(current_user)


@router.post(
    "/debug-token",
    summary="Debug JWT token",
    description="Debug JWT token without authentication (for troubleshooting)",
    responses={
        200: {"description": "Token analysis completed"},
        400: {"description": "Invalid token format"}
    }
)
def debug_token(
    token_data: dict
) -> dict:
    """
    Debug JWT token to identify issues.
    
    - **token**: JWT token to analyze
    """
    from app.core.security import security_manager
    from jose import JWTError, jwt
    from datetime import datetime
    import logging
    
    logger = logging.getLogger(__name__)
    
    token = token_data.get("token", "")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is required"
        )
    
    # Check token format
    parts = token.split('.')
    if len(parts) != 3:
        return {
            "error": "Invalid token format",
            "detail": "Token must have 3 parts (header.payload.signature)",
            "parts_count": len(parts)
        }
    
    try:
        # Decode without verification
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        # Check expiration
        exp_info = {}
        if 'exp' in decoded:
            exp_timestamp = decoded['exp']
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            current_datetime = datetime.now()
            exp_info = {
                "expiration": exp_datetime.isoformat(),
                "current_time": current_datetime.isoformat(),
                "is_expired": exp_datetime < current_datetime
            }
        
        # Try to verify with secret key
        verification_result = "unknown"
        try:
            verified = security_manager.verify_token(token)
            verification_result = "success" if verified else "failed"
        except Exception as e:
            verification_result = f"error: {str(e)}"
        
        return {
            "token_format": "valid",
            "payload": decoded,
            "expiration_info": exp_info,
            "verification_result": verification_result,
            "token_length": len(token)
        }
        
    except JWTError as e:
        return {
            "error": "JWT decode error",
            "detail": str(e),
            "token_format": "invalid"
        }


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Get a new access token using current user session",
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"description": "Not authenticated"}
    }
)
def refresh_token(
    current_user: User = Depends(require_active_user)
) -> Any:
    """
    Refresh access token.
    
    Generate a new access token for the currently authenticated user.
    """
    # Create new access token
    access_token = security_manager.create_access_token(data={"sub": str(current_user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(current_user)
    }
