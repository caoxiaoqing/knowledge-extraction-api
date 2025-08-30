"""
Application Configuration Settings
Centralized configuration management
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    API_TITLE: str = "LangChain PDF Knowledge Extraction API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Extract and structure knowledge points from course PDFs using LangChain"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "https://api.deepseek.com")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "deepseek-chat")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "4000"))
    
    # Processing Configuration
    MAX_FILE_SIZE_PDF: int = 50 * 1024 * 1024  # 50MB
    MAX_FILE_SIZE_JSON: int = 10 * 1024 * 1024  # 10MB
    MAX_CONCURRENT_CHAPTERS: int = int(os.getenv("MAX_CONCURRENT_CHAPTERS", "3"))
    
    # Text Processing Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "4000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate_settings(cls) -> None:
        """Validate required settings"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

# Global settings instance
settings = Settings()