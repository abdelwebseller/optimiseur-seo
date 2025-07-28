from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    sitemap_url = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    progress = Column(Integer, default=0)  # 0-100
    total_urls = Column(Integer, default=0)
    crawled_urls = Column(Integer, default=0)
    failed_urls = Column(Integer, default=0)
    
    # Configuration du crawl
    crawl_settings = Column(JSON, default={})
    
    # Configuration AI
    ai_settings = Column(JSON, default={})
    
    # Statistiques
    statistics = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relations
    user = relationship("User", back_populates="analyses")
    suggestions = relationship("Suggestion", back_populates="analysis")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, status={self.status}, progress={self.progress}%)>" 