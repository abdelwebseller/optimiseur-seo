from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer l'engine SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)

# Créer la session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer la base pour les modèles
Base = declarative_base()

def get_db():
    """Dependency pour obtenir la session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 