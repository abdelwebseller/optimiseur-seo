from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Configuration de base
    PROJECT_NAME: str = "Semantra API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Configuration de la base de données
    DATABASE_URL: str = "postgresql://user:password@localhost/semantra"
    
    # Configuration de sécurité
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuration CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Configuration Redis pour Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Configuration des APIs externes
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Configuration du crawl
    DEFAULT_USER_AGENT: str = "Semantra Bot 1.0"
    DEFAULT_CRAWL_DELAY: int = 1000  # ms
    DEFAULT_MAX_URLS: int = 1000000
    DEFAULT_RETRY_ATTEMPTS: int = 3
    
    # Configuration des modèles d'embedding
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-large"
    EMBEDDING_MODELS: List[str] = [
        "text-embedding-ada-002",
        "text-embedding-3-small", 
        "text-embedding-3-large"
    ]
    
    # Configuration Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_FILE: Optional[str] = None
    
    # Configuration des logs
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/semantra.log"
    
    # Configuration de l'environnement
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance globale des paramètres
settings = Settings() 