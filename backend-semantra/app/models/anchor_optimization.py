from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class AnchorOptimization(Base):
    __tablename__ = "anchor_optimizations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    suggestion_id = Column(String, ForeignKey("suggestions.id"), nullable=False)
    
    # Ancres originales et optimisées
    original_anchor = Column(Text, nullable=False)
    optimized_anchor = Column(Text, nullable=False)
    
    # Configuration de l'optimisation
    provider = Column(String, nullable=False)  # openai, gemini
    model = Column(String, nullable=False)  # gpt-4, gpt-3.5-turbo, etc.
    
    # Score de confiance
    confidence_score = Column(Float, nullable=False)  # 0.0 - 1.0
    
    # Alternatives proposées
    alternatives = Column(JSON, default=[])
    
    # Paramètres utilisés
    parameters = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    suggestion = relationship("Suggestion", back_populates="optimizations")
    
    def __repr__(self):
        return f"<AnchorOptimization(id={self.id}, confidence={self.confidence_score})>" 