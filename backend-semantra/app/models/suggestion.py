from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Suggestion(Base):
    __tablename__ = "suggestions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, ForeignKey("analyses.id"), nullable=False)
    
    # URLs source et cible
    source_page = Column(Text, nullable=False)
    target_page = Column(Text, nullable=False)
    
    # Ancre et score
    anchor_text = Column(Text, nullable=False)
    score = Column(Float, nullable=False)  # 0.0 - 1.0
    
    # Statut de la suggestion
    status = Column(String, default="pending")  # pending, approved, rejected
    
    # Raisonnement IA
    reasoning = Column(Text)
    
    # Métadonnées
    metadata = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    analysis = relationship("Analysis", back_populates="suggestions")
    optimizations = relationship("AnchorOptimization", back_populates="suggestion")
    
    def __repr__(self):
        return f"<Suggestion(id={self.id}, score={self.score}, status={self.status})>" 