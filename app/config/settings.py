"""
Application Configuration Management

Centralizes all configuration settings and provides validation.
"""

from pydantic import BaseSettings, validator
from typing import Dict, List, Optional
import os
from loguru import logger

class Settings(BaseSettings):
    # API Keys and Secrets
    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    TWITTER_ACCESS_TOKEN: str
    TWITTER_ACCESS_TOKEN_SECRET: str
    
    # Application Settings
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    REDIS_URL: Optional[str] = None
    MAX_REQUESTS_PER_MINUTE: int = 100
    
    # Security Settings
    ALLOWED_HOSTS: List[str] = ["*"]
    API_KEY_HEADER: str = "X-API-Key"
    SECRET_KEY: str
    
    # Cache Settings
    CACHE_TTL: int = 300  # 5 minutes
    
    @validator('ENVIRONMENT')
    def validate_environment(cls, v):
        allowed = ['development', 'testing', 'production']
        if v not in allowed:
            raise ValueError(f'Environment must be one of {allowed}')
        return v
    
    @validator('SECRET_KEY')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long')
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 