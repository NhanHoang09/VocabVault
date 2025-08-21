from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import security_manager
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.modules.auth.services import AuthService
from app.core.dependencies import require_active_user
from typing import Any
from jose import JWTError

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
    
    # Create access token (30 phút)
    access_token = security_manager.create_access_token(data={"sub": str(user.id)})
    
    # Create refresh token (7 ngày)
    refresh_token = security_manager.create_refresh_token(data={"sub": str(user.id)})
    
    # Create response
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user).model_dump(mode='json')
    })
    
    # Set refresh token as HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,           # Không thể truy cập từ JavaScript
        secure=not settings.DEBUG,  # Chỉ gửi qua HTTPS trong production
        samesite="lax",          # Lax cho development, strict cho production
        max_age=7*24*60*60,      # 7 ngày
        path="/"                 # Gửi cho tất cả endpoints
    )
    
    return response


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
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Refresh access token using refresh token from cookie",
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"description": "Invalid refresh token"}
    }
)
def refresh_token(request: Request, db: Session = Depends(get_db)) -> Any:
    """
    Refresh access token using refresh token from HttpOnly cookie.
    
    The refresh token is automatically sent with the request via cookie.
    """
    # Lấy refresh token từ cookie
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    try:
        # Verify refresh token
        payload = security_manager.verify_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Get user
        user = AuthService.get_user_by_id(db, int(user_id))
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        new_access_token = security_manager.create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


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
    "/logout",
    summary="Logout user",
    description="Logout user and clear refresh token cookie",
    responses={
        200: {"description": "Logged out successfully"}
    }
)
def logout() -> Any:
    """
    Logout user and clear refresh token cookie.
    """
    response = JSONResponse(content={"message": "Logged out successfully"})
    
    # Clear refresh token cookie
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh"
    )
    
    return response
