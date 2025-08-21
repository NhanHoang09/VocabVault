from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str


class UserUpdate(BaseModel):
    """Schema for user updates"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    study_preferences: Optional[Dict[str, Any]] = None
    notification_settings: Optional[Dict[str, Any]] = None
    privacy_settings: Optional[Dict[str, Any]] = None


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    is_superuser: bool
    
    # Gamification fields
    total_points: int = 0
    level: int = 1
    experience_points: int = 0
    study_streak_days: int = 0
    longest_streak: int = 0
    last_study_date: Optional[datetime] = None
    
    # Analytics fields
    total_study_time_minutes: int = 0
    total_cards_studied: int = 0
    total_correct_answers: int = 0
    total_incorrect_answers: int = 0
    average_accuracy: float = 0.0
    
    # Preferences
    study_preferences: Dict[str, Any] = {}
    notification_settings: Dict[str, Any] = {}
    privacy_settings: Dict[str, Any] = {}
    
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str
    user: UserResponse
