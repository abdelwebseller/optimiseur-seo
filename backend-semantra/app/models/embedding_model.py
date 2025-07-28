from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer
from sqlalchemy.sql import func
from app.core.database import Base
import uuid

class EmbeddingModel(Base):
    __tablename__ = "embedding_models"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Informations du modèle
    name = Column(String, nullable=False, unique=True)
    provider = Column(String, nullable=False)  # openai, gemini, local
    
    # Configuration API
    api_key = Column(Text)  # Chiffré en production
    model_id = Column(String, nullable=False)  # text-embedding-3-large, etc.
    
    # Paramètres
    dimensions = Column(Integer)
    max_tokens = Column(Integer)
    
    # Statut
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Métadonnées
    metadata = Column(String, default="{}")  # JSON string
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<EmbeddingModel(id={self.id}, name={self.name}, provider={self.provider})>" 