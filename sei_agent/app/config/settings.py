from typing import List
from pydantic import BaseSettings, validator, SecretStr

class Settings(BaseSettings):
    # Twitter API Credentials
    TWITTER_API_KEY: SecretStr
    TWITTER_API_SECRET: SecretStr
    TWITTER_ACCESS_TOKEN: SecretStr
    TWITTER_ACCESS_TOKEN_SECRET: SecretStr
    
    # SEI Network Configuration
    SEI_RPC_URL: str = "https://rest.sei-apis.com"
    SEI_CHAIN_ID: str = "sei-chain"
    
    # Application Settings
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    POST_INTERVAL: int = 3600  # 1 hour in seconds
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    @validator('ENVIRONMENT')
    def validate_environment(cls, v: str) -> str:
        allowed = ['development', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False 